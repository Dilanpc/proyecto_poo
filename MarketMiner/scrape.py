from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import datetime
import pandas as pd
import threading
import MarketMiner.csv_utils as csv


class ValueNotFoundByAttr(Exception):
    pass


# Clase que recibe un link y lo convierte en un objeto BeautifulSoup para facilitar la extracción de datos
class Page(BeautifulSoup):
    def __init__(self, link, use_selenium=False) -> None:
        self._driver = None
        if use_selenium:
            options = webdriver.chrome.options.Options()
            options.add_argument("--headless") # No abrir ventana de chrome
            options.add_argument('log-level=2') # No mostrar mensajes de log

            service = webdriver.chrome.service.Service(executable_path="./drivers/chromedriver.exe")
            self._driver = webdriver.Chrome(service=service, options=options)
            self._driver.get(link)
            self.html = self._driver.page_source
            threading.Thread(target=self._driver.quit).start()

        else:
            self.html = requests.get(link).text

        super().__init__(self.html, 'lxml')

    def find(self, *args, **kwargs):
        if 'attrs' in kwargs and 'etiqueta' in kwargs['attrs']: # Si se especifica una etiqueta, se busca por ella
            etiqueta = kwargs['attrs']['etiqueta']
            del kwargs['attrs']['etiqueta']
            return super().find(etiqueta, *args, **kwargs)
                
        return super().find(*args, **kwargs)
    
    def find_all(self, *args, **kwargs):
        if 'attrs' in kwargs and 'etiqueta' in kwargs['attrs']:
            etiqueta = kwargs['attrs']['etiqueta']
            del kwargs['attrs']['etiqueta']
            return super().find_all(etiqueta, *args, **kwargs)
        
        return super().find_all(*args, **kwargs)



# Recibe un tag que continene la información de un producto para crear un objeto con los datos del procuto y facilitar su acceso
class ProductCard():
    def __init__(self, tag: BeautifulSoup, attrs_name:list[dict]=None, attrs_price:list[dict]=None, attrs_link:list[dict]=None, exc_attrs_name:dict=None, exc_attrs_price:dict=None, exc_attrs_link:dict=None) -> None:
        self.tag = tag
        self._attrs_name = attrs_name
        self._attrs_price = attrs_price
        self._attrs_link = attrs_link
        self._exc_attrs_name = exc_attrs_name
        self._exc_attrs_price = exc_attrs_price
        self._exc_attrs_link = exc_attrs_link
        self.name = ""
        self.price_txt = ""
        self.price = -1
        self.link = ""
        self.define_product()
    
    def define_product(self):
        self._compute_name()
        self._compute_price()
        self._compute_link()

    def _compute_name(self):
        if self._attrs_name == None:
            self.name = "Sin nombre"
            return self.name
        
        try:
            #Se busca el tag de siguiendo el orden de los atributos especificadas
            section:list[BeautifulSoup] = [self.tag]
            for attr in self._attrs_name:
                section = self._search_attrs_in_list(section, attr, self._exc_attrs_name)

            if len(section) > 1:
                raise ValueNotFoundByAttr("Se encontraron varios nombres")
            
            self.name = section[0].text
            return self.name
        except ValueNotFoundByAttr:
            raise ValueNotFoundByAttr("No se encontró el nombre")
        except Exception as e:
            print(e, "No se pudo obtener el nombre")
            raise e
    
    def _compute_price(self):
        if self._attrs_price == None:
            self.price = "Sin precio"
            return self.price

        try:
            #Se busca el tag de siguiendo el orden de las clases especificadas
            section:list[BeautifulSoup] = [self.tag]
            for attr in self._attrs_price:
                section = self._search_attrs_in_list(section, attr, self._exc_attrs_price)

            if len(section) > 1:
                # raise ValueNotFoundByAttr("Se encontraron varios precios en", self.name)
                print("Se encontraron varios precios en ", self.name)
            
            self.price_txt = section[0].text
            self.__decode_price()
            return self.price
        except ValueNotFoundByAttr:
            raise ValueNotFoundByAttr("No se encontró el precio en", self.name)
        except Exception as e:
            print(e, "No se pudo obtener el precio en", self.name)
            raise e
    def _compute_link(self):
        if self._attrs_link == None:
            self.link = "Sin link"
            return self.link
        
        try:
            #Se busca el tag de siguiendo el orden de las clases especificadas
            section:list[BeautifulSoup] = [self.tag]
            for attr in self._attrs_link:
                section = self._search_attrs_in_list(section, attr, self._exc_attrs_link)

            if len(section) > 1:
                print(section)
                raise ValueNotFoundByAttr("Se encontraron varios links en", self.name)
            
            self.link = section[0].get('href')
            return self.link
        except ValueNotFoundByAttr:
            raise ValueNotFoundByAttr("No se encontró el link en", self.name)
        except Exception as e:
            print(e, "No se pudo obtener el link en", self.name)
            raise e

        

    def _search_attrs_in_list(self, sections:list, attrs:dict, excluded:dict=None):
        
        # Obtener todos los tags con los atributos especificados en cada section
        result = []
        for i in range(len(sections)):
            if 'etiqueta' in attrs: # Añadir opción de buscar por etiqueta
                etiqueta = attrs['etiqueta']
                del attrs['etiqueta']
                result += sections[i].find_all(etiqueta, attrs=attrs)
            else:
                result += sections[i].find_all(attrs=attrs)
            
        # Filtrar los tags que no contienen las clases excluidas
        filtered = []
        if excluded == None or excluded == {}:
            excluded = {}
            filtered = result
        for tag in result:
            # iterar en cada atributo excluido
            for exc in excluded:
                if exc not in tag.attrs or excluded[exc] not in tag[exc]:
                    filtered.append(tag)  # Si no se encuentra el atributo excluido, se agrega a la lista de tags filtrados

        if len(filtered) == 0:
            raise ValueNotFoundByAttr(f"No se encontró ningún tag con los atributos {attrs} y sin {excluded}")

        return filtered

    
    def __decode_price(self):
        self.price = ""
        for c in self.price_txt:
            if c.isdigit():
                self.price += c
        self.price = int(self.price)

        # Añadir puntos para separar miles en price_txt
        desfase = len(str(self.price)) % 3
        if desfase == 0: desfase = 3
        self.price_txt = ""
        for c in str(self.price):
            self.price_txt += c
            desfase -= 1
            if desfase == 0:
                self.price_txt += "."
                desfase = 3
        self.price_txt = self.price_txt[:-1] # Eliminar el último punto
            
        return self.price
    
    #Getters
    def get_name(self):
        return self.name
    def get_price(self):
        return self.price
    def get_link(self):
        return self.link
    
    def __str__(self) -> str:
        return f"{self.name} -> {self.price}"
        


class Products(Page):
    def __init__(self, use_selenium=False) -> None:
        self.page_name = ""
        self.link = ""
        self.products: list[ProductCard] = []
        self.names = []
        self.prices = []
        self.links = []
        self.SELENIUM = use_selenium
    
    def _enter_webpage(self, link):
        self.link = link
        super().__init__(link, use_selenium=self.SELENIUM)

    def search_products(self, link: str):
        try:
            self._enter_webpage(link)
            self._compute_products()
            self._compute_info()
        except Exception as e:
            print("Error en ", self.page_name, ": ")
            print(e)


    def get_product_by_link(self, link: str):
        self._enter_webpage(link)
        return self._compute_one_product(link)

    def _compute_info(self):
        self.prices, self.names, self.links = [], [], []
        for product in self.products:
            self.prices.append(product.price)
            self.names.append(product.name)
            self.links.append(product.link)

    def _compute_products(self, product_section_attrs: dict = None, product_card_attrs: dict = None, card_data: list = None): 
        product_section: BeautifulSoup = self.find(attrs = product_section_attrs)
        if product_section == None: raise ValueNotFoundByAttr("No se encontró la sección de productos")
        card_list = product_section.find_all(attrs = product_card_attrs)
        if len(card_list) == 0: raise ValueNotFoundByAttr("No se encontraron tarjetas de productos")

        for card in card_list:  #Convierte todos los tags en objetos ProductCard
            self.products.append(ProductCard(card, *card_data))
        
        return self.products


    
    def _compute_one_product(self, *args): # Cada página tiene una estructura diferente, por lo que se debe sobreescribir
        pass
    
    def make_report(self, file_name:str, link_file_name:str=None):
        # Crea un archivo csv con los productos encontrados
        file = csv.Csv(file_name)
        fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d")

        if link_file_name != None:
            link_file = csv.Csv(link_file_name)

        if len(file) == 0:
            # Si el archivo está vacío, se crean los productos a rastrear
            matriz = [["Nombres", f"Precio {fecha_actual}"]] + [[name, price] for name, price in zip(self.names, self.prices)] # [[Nombres, fecha], [name1, precio1], [name2, precio2], ...]
            file.write(matriz)

            if link_file_name != None:
                link_file.write([["Nombres", f"Link {fecha_actual}"]] + [[name, link] for name, link in zip(self.names, self.links)])

        else:
            #Se agrega una nueva columna con los precios actuales
            column_names = file.get_column(0)
            column_to_add = [f"Precio {fecha_actual}"] + ["N/A"] * len(column_names)
            column_links = [f"link {fecha_actual}"] + ["N/A"] * len(column_names)
            #Se busca si los nombres de los productos que ya están en el archivo
            for i in range(1, len(column_names)): # Se inicia desde el segundo porque el primero es el nombre de la columna
                if column_names[i] in self.names:
                    index = self.names.index(column_names[i]) # Obtiene el índice del nombre en la lista de nombres
                    # Se ubica el precio y link en la misma posición que el nombre
                    column_to_add[i] = self.prices[index]
                    column_links[i] = self.links[index]
            
            # Escribir datos en el archivo
            file.add_column(column_to_add)
            if link_file_name != None:
                link_file.add_column(column_links)


    def print_products(self):
        if not self.products:
            print("No hay productos")
            return None
        
        #Buscar cadena más larga para ajustar el tamaño de la columna
        largest = len(self.products[0].name)
        for product in self.products:
            if len(product.name) > largest:
                largest = len(product.name)

        #Imprimir productos con precio
        for product in self.products:
            print(product.name + "."*(largest - len(product.name)), "->", product.price)
    
    def clean_up(self):
        self.products = []
        self.names = []
        self.prices = []
        self.links = []
        self.link = ""

    def sort_by_price(self, reverse=False):
        self.products.sort(key=lambda product: product.price, reverse=reverse)
        self.names, self.prices, self.links = [], [], []
        self.names = [product.name for product in self.products]
        self.prices = [product.price for product in self.products]
        self.links = [product.link for product in self.products]
    
    def average_price(self):
        return sum([int(product.price) for product in self.products]) / len(self.products)
    
    def get_dataframe(self):
        data = pd.DataFrame({"Nombres": self.names, "Precios": self.prices, "Links": self.links})
        return data
    
    def get_dataframe_report(self, file_name:str):
        file = csv.Csv(file_name)
        return file.get_dataframe()


class MercadoLibre(Products):
    def __init__(self) -> None:
        super().__init__(use_selenium=False)
        self.page_name = "MercadoLibre"
        self.__CARD_DATA = [
            [{"class":"ui-search-item__title"}], # Atributos para nombre
            [{"class":"ui-search-price ui-search-price--size-medium"},{"class":"andes-money-amount"}], # Atributos para precio
            [{"class":"ui-search-item__group__element ui-search-link__title-card ui-search-link"}], # Atribitos para link
            {}, # Atributos excluidos para nombre
            {"class":"ui-search-price__original-value"}, # Atributos excluidos para precio
            {} # Atributos excluidos para link
        ]
        self.__CARD_DATA2 = [
            [{"class":"poly-box"}],
            [{"class":"andes-money-amount andes-money-amount--cents-superscript"}, {"class":"andes-money-amount__fraction"}],
            [{"class":"poly-box"}, {"etiqueta":"a"}],
            {"class":"poly-coupon"},
            {"class":"poly-component__buy-box"}, # No funciona
            {}
        ]


    def search_products(self, product: str):
        super().search_products(f"https://listado.mercadolibre.com.co/{product}")

    def get_product_by_link(self, link: str):
        return super().get_product_by_link(link)
    
    def _compute_one_product(self, link):
        section = self.find(class_="ui-pdp-container__col col-2 mr-32")
        ATTR_NAME = [{"class":"ui-pdp-title"}]
        ATTR_PRICE = [{"class":"ui-pdp-price__main-container"}, {"class":"andes-money-amount--cents-superscript"}, {"class":"andes-money-amount__fraction"}]
        EXCLUDED_ATTR_PRICE = {"class":"ui-pdp-price__original-value"}
        product = ProductCard(section, ATTR_NAME, ATTR_PRICE, exc_attrs_price=EXCLUDED_ATTR_PRICE)
        product.link = link
        self.products.append(product)
        self._compute_info()
        return product

    def _compute_products(self, product_section_attrs: dict = {"class": "ui-search-layout"}, product_card_attrs: dict = {"class": "ui-search-layout__item"}, card_data: list = None):
        try:
            return super()._compute_products(product_section_attrs, product_card_attrs, self.__CARD_DATA)

        except ValueNotFoundByAttr:
            print("Usando segunda estructura")
            return super()._compute_products(product_section_attrs, product_card_attrs, self.__CARD_DATA2)


class Exito(Products):
    def __init__(self):
        super().__init__(use_selenium=True)
        self.page_name = "Exito"
        self.__CARD_DATA = [
            [{"data-fs-product-card-title":"true"}], # Atributos para nombre
            [{"class":"ProductPrice_container__price__XmMWA"}], # Atributos para precio
            [{"data-fs-product-card-title":"true"}, {"data-testid":"product-link"}], # Atributos para link
            {}, # Atributos excluidos para nombre
            {}, # Atributos excluidos para precio
            {}  # Atributos excluidos para link
        ]
        self.__CARD_DATA2 = [
            [{"class":"styles_name__qQJiK"}], # Atributos para nombre
            [{"class":"ProductPrice_container__price__XmMWA"}], # Atributos para precio
            [{"class":"productCard_productLinkInfo__It3J2"}], # Atributos para link
            {}, # Atributos excluidos para nombre
            {}, # Atributos excluidos para precio
            {}  # Atributos excluidos para link
        ]

    def search_products(self, product: str):
        super().search_products(f"https://www.exito.com/s?q={product}")

    def _compute_products(self, product_section_attrs: dict = {"class": "product-grid_fs-product-grid___qKN2"}, product_card_attrs: dict = {"class": "productCard_contentInfo__CBBA7"}, card_data: list = None):
        try:
            super()._compute_products(product_section_attrs, product_card_attrs, self.__CARD_DATA2)
            for product in self.products:
                product.link = "https://www.exito.com" + product.link

            return self.products


        except Exception as e:
            print(e)
            return None
    


class Linio(Products):
    def __init__(self):
        super().__init__(use_selenium=True)

        self.page_name = "Linio"
        self.__CARD_DATA = [
            [{"class":"pod-subTitle"}], # Atributos para nombre
            [{"class":"prices-0"}, {"class": "primary"}], # Atributos para precio
            [{"class":"pod-link"}], # Atributos para link
            {}, # Atributos excluidos para nombre
            {"class":"discount-badge-item"}, # Atributos excluidos para precio
            {}  # Atributos excluidos para link
        ]

    def search_products(self, product: str):
        super().search_products(f"https://linio.falabella.com.co/linio-co/search?Ntt={product}")

    def _compute_products(self, product_section_attrs: dict = {"id": "testId-searchResults-products"}, product_card_attrs: dict = {"class": "grid-pod"}, card_data: list = None):
        try:                                                                                                                                 
            return super()._compute_products(product_section_attrs, product_card_attrs, self.__CARD_DATA)


        except Exception as e:
            print(e)
            return None
        
