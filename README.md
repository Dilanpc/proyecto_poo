# Sistema de WebScrapping-Proyecto Programación Orientada a Objetos

## Alternativa Seleccionada:
 * **_Sistema de WebScrapping para páginas de retail y páginas tipo wiki_**

## Definición del Problema

### Páginas de Retail:
 * ### Realizar la extracción de datos asociados a productos de diferentes páginas de retail, como Mercado Libre, Linio y Éxito, con el fin de comparar precios, disponibilidad y otras características de los productos. 
 
 * El enfoque principal de la parte del programa dedicada a las páginas de retail, será a productos de tecnología y electrodomésticos. Los datos recolectados de productos como televisores, celulares, tablets, audífonos, entre otros, serán tomados durante un cierto periodo de tiempo para tener un registro histórico de las variaciones de los precios y disponibilidades, que será almacenado en una base de datos. Con el objetivo de enseñar los datos de una manera más intuitiva y un poco más práctica, inicialmente se pensó en la realización de una pequeña interfaz que sea capaz de mostrar los datos recolectados dependiendo del producto que el usuario desee buscar, y tenga la posibilidad de acceder directamente al link del producto en específico que le llame la atención. 
 * De esta manera y en sentido de orientar los datos recolectados por el sistema mencionado, paralelo y aparte a este proyecto, se puede buscar en un futuro es la creación de una interfaz mayor que sea capaz de permitir al usuario realizar la comparativa simultáneamente entre productos de diferentes páginas de retail, y así es permitirle evitar la acción de realizar la comparación del producto de interés ingresando a cada una de las páginas individualmente. 

### Páginas Wiki:
 * ### Realizar la extracción de texto de páginas como Wikipedia o Wiki Quotes, buscando automatizar la extracción de títulos, párrafos y citas. 
 
 * La extracción de texto vendría sujeta al interés del usuario del programa. En ese sentido se planteó específicamente para el caso de la extracción de Wiki Quotes, el registro de las citas asociadas a ciencia. Principalmente se busca que el programa entregue una cita con su respectivo autor asociado. Para el caso de Wikipedia, se tiene como primera alternativa la extracción de texto de un tema en concreto, y como segunda la extracción de una página asociada a una película en específico, capaz de brindar información particular de la misma, como su título, su director, su trama y sus premios. 

## Páginas Web:

### Sitios de Retail:

* [Mercado Libre](https://www.mercadolibre.com.co)
* [Linio](https://linio.falabella.com.co/linio-co)
* [Éxito](https://www.exito.com/?srsltid=AfmBOor0YAfmwqltX-hxWduWqMq0UKwCbFNT9Od6TJyyvHtGHMWu7Rpw)

###### NOTA: Sujeto a adición de más páginas

### Sitios Wiki:
  * [Wikiquote](https://es.wikiquote.org/wiki/Portada)
  * [Wikipedia](https://es.wikipedia.org/wiki/Wikipedia:Portada)
  
    


## Diagramas de Clases:

### Diagrama de Clases Scrapping a Páginas de Retail:

A continuación se presenta el diagrama de clases del programa principal encargado de realizar el scrapeo a las páginas de Retail. Se puede observar que se parte del trabajo con librerías como Selenium y BeautifulSoup que facilitan la automatización del navegador y la extracción de datos estructurados de las páginas web.

```mermaid
classDiagram
    BeautifulSoup <|-- Page
    Page <|-- Products
    Products *-- ProductCard
    Products <|-- MercadoLibre
    Products <|-- Exito
    Products <|-- Linio


    class BeautifulSoup{
        + find()
        + find_all()
    }

    class Page{
        - _driver
        + html

        + find()
        + find_all()
    }

    class Products{
        + page_name
        + link
        + products
        + names
        + prices
        + links
        + SELENIUM

        - _enter_webpage(link: str)
        + search_products(link: str)
        + get_product_by_link(link: str)
        - _compute_info()
        - _compude_product(link:str)
        - _compute_one_product()

    }

    class ProductCard{
        + tag
        + _attrs_name
        + _attrs_price
        + _attrs_link
        + _exc_attrs_name
        + _exc_attrs_price
        + _exc_attrs_link
        + name
        + price_txt
        + price
        + link

        + define_product()
        - _compute_name()
        - _compute_price()
        - _compute_link()
        - _search_attrs_in_list(sections: list, attrs: dict, excluded: dict)
        - __decode_price()
    }


    class MercadoLibre{
        + CARD_DATA
        + CARD_DATA2

        + search_products(product)
        - compute_one_product()
        - _compute_products()
    }

    class Exito{
        + CARD_DATA
        + CARD_DATA2

        + search_products(product)
        - compute_one_product()
        - _compute_products()
    }

    class Linio {
        + __CARD_DATA
        + page_name: str
        + search_products(product)
        + _compute_products()
    }

```

Las clases presentes en el diagrama se explican a continuación:  

* BeautifulSoup: Será la clase encargada de encapsular las funcionalidades de la librería BeautifulSoup, permitiendo el uso de métodos como find() y find_all(), que facilitan la búsqueda de elementos en el HTML de las páginas web.

* Page: Será la clase que representa a una página web. Contiene un controlador de navegador _driver y el contenido HTML de la página. Esta clase también proporciona métodos para buscar elementos en la página utilizando las capacidades de la librería BeautifulSoup.

* Products: Será la clase responsable de gestionar la búsqueda y extracción de productos de las páginas de retail. Esta clase incluye atributos como page_name, link, products, names, prices, y links. Los métodos proporcionan el ingreso a una página web, permitiendo buscar productos, y obtener información específica de productos mediante enlaces.

* ProductCard: Será la clase que represente una tarjeta de producto individual, que contiene atributos como name, price, y link. Sus métodos permiten definir los productos y estimar sus atributos.

 ###### NOTA: Se decidió utilizar el término tarjeta para describir a la sección de la página web que encapsula a cada uno de los productos y los enseña en la página principal tras la búsqueda. Muestra la imagen del producto, su nombre, precio, descuento, valoración, entre otras características. Para este caso solo se utilizan los datos de precio, nombre y link. 

* Mercado Libre, Exito y Linio: Serán las clases destinadas a manejar la búsqueda de productos en sus respectivas plataformas. Todas las clases tienen atributos para almacenar datos de tarjetas de productos (CARD_DATA, CARD_DATA2) y métodos para realizar búsquedas y calcular información sobre los productos.


### Diagrama de Clases Scrapping a Páginas Wiki:

A continuación se presenta el diagrama de clases del programa encargado de extraer el texto de páginas de Wiki, como Wikipedia y Wikiquote.

```mermaid

classDiagram
   WikiPage <|-- Wikipedia
   WikiPage <|-- WikiQuoteScience
   Wikipedia<|-- WikiMovie
    
   

   class WikiPage{
        + url: str
        + page
        + soup: BeautifulSoup
+ get_tittle()
+ get_paragraph()
    }

    class Wikipedia{
        + find_keywords(keywords: list)
    }

    class WikiQuoteScience{
        + find_quotes(keywords: list)
+find_author(keywords: list)

    }

   class WikiMovie{


        + get_title()
+get_actors()
+get_director()
+get_argument()
+get_movie_details()

    }
    

```


El diagrama incluye las siguientes clases:

* WikiPage: Esta clase representará a una página Wiki genérica. Por esto contará con atributos como url, page, y soup. Este último utiliza la librería BeautifulSoup y facilita el análisis del contenido HTML. Los métodos get_title() y get_paragraph(), permitirán extraer el título y los párrafos de la página, proporcionando una base común para las clases hijas. 

* Wikipedia: Esta será una subclase de WikiPage y añadirá funcionalidades específicas para la búsqueda de palabras clave en Wikipedia. Para esto se utilizará el método find_keywords(keywords: list), que recibirá unas palabras clave de interés y serán buscadas en la página.

* WikiQuoteScience: También será una subclase de Wikipage y se enfocará en la búsqueda de citas científicas en la página WikiQuote. Los métodos find_quotes() y y find_author() permitirán extraer citas junto a los autores de las mismas.

* WikiMovie: Esta clase será una clase hija de Wikipedia, y estará dedicada a la información sobre películas encontrada en dicha página. La idea es que permita, mediante los métodos definidos, encontrar, el título de la película, los actores, director/es y argumento de la película de interés que se busquen en la página principal de Wikipedia.
   
### Diagrama de Clases Posible Interfaz:

```mermaid

classDiagram
    Interface "1" *--  FrameHome
   FrameHome *-- FrameMenuShops
   FrameHome *-- FrameInfoShop
   FrameInfoShop *-- FrameResult
   Tk <|-- Interface
   Frame <|-- FrameHome
   Frame <|-- FrameMenuShops
   Frame <|-- FrameInfoShop
   Frame <|-- FrameResult
   
   

 class Tk{
    }

 class Frame{
    }

    class Interface{
        + title
        + geometry
        + frame: FrameHome
    }

    class FrameHome{
        + master
        + frame_menu: FrameMenuShops
        + frame_info

        + show_info(page_name, color)
    }

    class FrameMenuShops{
        + master: FrameHome
+ labels
+ buttons: list
+ info

+ _show_buttons()

    }

class FrameInfoShop{
        + master
        + result
        + __BG
        + page
        + search_input
        + load_label
        + button_search

        + __search_web(class_name)
+ search()
+ __ search_thread()
+ __loading()
    }

class FrameResult{
        + master
+ data
+ label
+ canvas
+ scrollbar
+ inner_frame
+ buttons
+ canvas_frame
      
+ __on_frame_configure(event)
+ __on_canvas_configure(event)
+ _calculate_buttons()
+ _show_buttons()
+ _go_to_link(link)
    }

 
   

```


## Abordaje de Solución:

Para el sistema dedicado a las páginas de retail se buscó plantear un programa que fuese capaz de...


### Clase WikiPage:
Para el sistema dedicado a las páginas wiki, se definieron las clases que se plantearon en el diagrama de clases, con sus respectivos métodos y atributos. En primer lugar, dentro del módulo wiki_page.py se construyó la clase WikiPage, que será la clase padre que busca abstraer a una página Wiki en general. La clase recibe como atributo un link que dirige a la página wiki que se va a instanciar, y define un método que entrega el título de la página. Utilizando las librerías Requests y BeautifulSoup, se registra como txto el HTML de la página para poder parsearla (analizar una cadena de texto para identificar y extraer la información de interés). Esta clase será la encargada de heredar el atributo de URL y el método get_title a las demás clases hijas (WikiQuoteScience y Wikipedia)

``` python
"""
Módulo que contiene la clase WikiPage e importa las bibliotecas necesarias.

"""

import requests  # Importa la biblioteca requests para realizar peticiones HTTP
from bs4 import BeautifulSoup  # Importa BeautifulSoup para el análisis de HTML

# Clase Padre que representa una página tipo Wiki y define atributos y métodos comunes
class WikiPage:
    def __init__(self, url):  # Constructor que inicializa la URL y realiza la petición a la página
        self.url = url  # Asignar la URL proporcionada a la instancia
        self.page = requests.get(url)  # Hacer la solicitud HTTP para obtener el contenido de la página
        # Parsear el contenido HTML de la página utilizando BeautifulSoup
        self.soup = BeautifulSoup(self.page.text, 'html.parser') 
    
    # Método que obtiene el título de la página web    
    def get_title(self):
        return self.soup.title.text  # Retorna el texto del título de la página

```

### Clase Wikipedia:

En segundo lugar, dentro del módulo wikipedia.py se construyó la clase Wikipedia, que es una clase hija de WikiPage y hereda el atributo que define al link de la página. Como el objetivo del sistema que scrapea las páginas de Wikipedia es permitir al usuario la búsqueda de la información de interés con la ayuda del filtrado por palabras clave, se definió un método find_keywords. Este método se encargará de recibir las palabras clave que ingrese el usuario y recorrer los diferentes párrafos de la página para buscar dentro de ellos, los que contengan a las palabras digitadas por el usuario


``` python
"""
Módulo que contiene la clase Wikipedia que hereda de WikiPage.
"""

from .wiki_page import WikiPage  # Importa la clase WikiPage del módulo wiki_page

class Wikipedia(WikiPage):
    def __init__(self, url):
        super().__init__(url)  
 
    def find_keyword(self, keywords):
        for paragraph in self.soup.select('p'):  # Selecciona todos los párrafos en la página
            # Comprobar si alguna de las palabras clave está en el texto del párrafo
            for keyword in keywords:
                if keyword.lower() in paragraph.text.lower():  # Si se encuentra palabra clave está en el párrafo se imprime el párrafo
                    print(paragraph.text)  
                    print("-------------------------------------------------") 
                    break  # Salir del bucle de palabras clave si se encontró una coincidencia
```
### Ejecución

### Clase WikiQuoteScience

### Ejecución

### Clase WikiMovie

### Ejecución


## Instalación e Uso:

## Librerías usadas

- beautifulsoup4
- requests
- lxml
- pandas
- openpyxl
- matplotlib
- selenium
- PySide6

## Reportes
[Reporte de datos](https://unaledu-my.sharepoint.com/:f:/g/personal/diporrasc_unal_edu_co/EgGtalNhip1EqE6p7OGyqIIB4OAbREHbszYB5mtlMhiqcA?e=m3yN1G)


## Uso de selenium

Algunas páginas cargan su contenido después de acceder a ellas, haciendo que la librería requests no sea útil en estas páginas. Con selenium se evita este problema aunque toma más tiempo su ejecución.

El uso de selenium está disponible en este programa para Google Chrome. **Es necesario instalar el driver del navegador.** Puede descargarlo a través de este [link](https://googlechromelabs.github.io/chrome-for-testing/) y guardarlo en la carpeta `./drivers/`
