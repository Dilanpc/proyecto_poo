from bs4 import BeautifulSoup
import requests

class ValueNotFoundByClass(Exception):
    pass

# Clase que recibe un link y lo convierte en un objeto BeautifulSoup para facilitar la extracción de datos
class Page(BeautifulSoup):
    def __init__(self, link) -> None:
        self.html = requests.get(link).text
        super().__init__(self.html, 'lxml')



# Recibe un tag que continene la información de un producto para crear un objeto con los datos del procuto y facilitar su acceso
class ProductCard():
    def __init__(self, tag: BeautifulSoup, class_name:list=None, class_price:list=None, class_link:list=None, exc_class_name:list=None, exc_class_price:list=None, exc_class_link:list=None) -> None:
        self.tag = tag
        self._class_name = class_name
        self._class_price = class_price
        self._class_link = class_link
        self._exc_class_name = exc_class_name
        self._exc_class_price = exc_class_price
        self._exc_class_link = exc_class_link
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
        if self._class_name == None:
            self.name = "Sin nombre"
            return self.name
        
        try:
            #Se busca el tag de siguiendo el orden de las clases especificadas
            section:list[BeautifulSoup] = [self.tag]
            for i in range(len(self._class_name)):
                section = self._search_class_in_list(section, self._class_name[i], self._exc_class_name)

            if len(section) > 1:
                raise ValueNotFoundByClass("Se encontraron varios nombres")
            
            self.name = section[0].text
            return self.name
        except Exception as e:
            print(e, "No se pudo obtener el nombre")
            return ""
    
    def _compute_price(self):
        if self._class_price == None:
            self.price = "Sin precio"
            return self.price

        try:
            #Se busca el tag de siguiendo el orden de las clases especificadas
            section:list[BeautifulSoup] = [self.tag]
            for i in range(len(self._class_price)):
                section = self._search_class_in_list(section, self._class_price[i], self._exc_class_price)

            if len(section) > 1:
                raise ValueNotFoundByClass("Se encontraron varios precios")
            
            self.price_txt = section[0].text
            self.__decode_price()
            return self.price
        except Exception as e:
            print(e, "No se pudo obtener el precio")
            return -1

    def _compute_link(self):
        if self._class_link == None:
            self.link = "Sin link"
            return self.link
        
        try:
            #Se busca el tag de siguiendo el orden de las clases especificadas
            section:list[BeautifulSoup] = [self.tag]
            for i in range(len(self._class_link)):
                section = self._search_class_in_list(section, self._class_link[i], self._exc_class_link)

            if len(section) > 1:
                print(section)
                raise ValueNotFoundByClass("Se encontraron varios links")
            
            self.link = section[0].get('href')
            return self.name
        except Exception as e:
            print(e, "No se pudo obtener el link")
            return ""
        

    def _search_class_in_list(self, sections:list, class_, excluded:list=None):
        if excluded == None:
            excluded = []
        # Obtener todos los tags con la clase especificada en cada section
        result = []
        for i in range(len(sections)):
            result = result + sections[i].find_all(class_=class_)
            
        # Filtrar los tags que no contienen las clases excluidas
        filtered = []
        for tag in result:
            if any(exc in tag['class'] for exc in excluded):
                continue
            filtered.append(tag)
        return filtered
    
    def __decode_price(self):
        self.price = int(self.price_txt.replace(".", ""))
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
    def __init__(self) -> None:
        self.page_name = ""
        self.link = ""
        self.products = []
        self.names = []
        self.prices = []
        self.links = []
    
    def _enter_webpage(self, link):
        self.link = link
        super().__init__(link)

    def search_products(self, link: str):
        self._enter_webpage(link)
        self._compute_products()
        self._compute_info()

    def get_product_by_link(self, link: str):
        self._enter_webpage(link)
        return self._compute_one_product(link)

    def _compute_info(self):
        for product in self.products:
            self.prices.append(product.price)
            self.names.append(product.name)
            self.links.append(product.link)

    def _compute_products(self, *args): # Cada página tiene una estructura diferente, por lo que se debe sobreescribir
        pass
    def _compute_one_product(self, *args): # Cada página tiene una estructura diferente, por lo que se debe sobreescribir
        pass
    
    def print_products(self):
        if not self.products:
            print("No se encontraron productos")
            return None
        
        #Buscar cadena más larga para ajustar el tamaño de la columna
        largest = len(self.products[0].name)
        for product in self.products:
            if len(product.name) > largest:
                largest = len(product.name)

        #Imprimir productos con precio
        for product in self.products:
            print(product.name + "."*(largest - len(product.name)), "->", product.price)

    
    def average_price(self):
        return sum([int(product.price) for product in self.products]) / len(self.products)
    


class MercadoLibre(Products):
    def __init__(self) -> None:
        super().__init__()
        self.page_name = "MercadoLibre"
        self.__CARD_DATA = [["ui-search-item__title"], ["ui-search-price ui-search-price--size-medium", "andes-money-amount", "andes-money-amount__fraction"], ["ui-search-item__group__element ui-search-link__title-card ui-search-link"], [], ["ui-search-price__original-value"], []]


    def search_products(self, product: str):
        super().search_products(f"https://listado.mercadolibre.com.co/{product}")

    def get_product_by_link(self, link: str):
        return super().get_product_by_link(link)
    
    def _compute_one_product(self, link):
        section = self.find(class_="ui-pdp-container__col col-2 mr-32")
        CLASS_NAME = ["ui-pdp-title"]
        CLASS_PRICE = ["ui-pdp-price__main-container", "andes-money-amount--cents-superscript", "andes-money-amount__fraction"]
        EXCLUDED_CLASS_PRICE = ["ui-pdp-price__original-value"]
        product = ProductCard(section, CLASS_NAME, CLASS_PRICE, exc_class_price=EXCLUDED_CLASS_PRICE)
        product.link = link
        return product



    def _compute_products(self):
        try:
            product_section: BeautifulSoup = self.find(class_="ui-search-layout")
            card_list = product_section.find_all(class_="ui-search-layout__item")

            for card in card_list: #Convierte todos los tags en objetos ProductCard
                self.products.append(ProductCard(card, *self.__CARD_DATA))

            return self.products

        except Exception as e:
            print(e, "No se encontraron productos")
            return None















if __name__ == "__main__":
    page = MercadoLibre()
    
    page.search_products("Computador")
    page.print_products()

    product = page.get_product_by_link("https://www.mercadolibre.com.co/all-in-one-hp-24-cb0003la-amd-ryzen-3-8-gb-256-gb-238/p/MCO32669085")
    print(product.name)
    print(product.price)
    print(product.link)

    

    