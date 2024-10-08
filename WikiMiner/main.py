from wikiminer.wikipedia import Wikipedia
from wikiminer.wikiquote_science import WikiQuoteScience
from wikiminer.wikimovie import WikiMovie

if __name__ == "__main__":
    # WIKIQUOTE
    print("----------------------  WIKIQUOTE  ---------------------------")
    wiki_quote_page = WikiQuoteScience('https://es.wikiquote.org/wiki/Ciencia')  # Crear una instancia de WikiQuoteScience

    keywords = ["ciencia", "científico"]  # Definir las palabras clave a buscar

    print(wiki_quote_page.get_title())  # Imprimir el título de la página
    
    # Obtener las citas y autores
    quotes, authors = wiki_quote_page.find_quotes_and_authors(keywords)
    
    # Imprimir cada cita con su respectivo autor
    for quote, author in zip(quotes, authors):
        print(f"{quote} - {author}")  # Imprimir cita y autor
        print("-------------------------------------------------")
        
    # Contar citas y autores
    print(f"Total de citas encontradas: {len(quotes)}")  # Imprimir la cantidad total de citas encontradas
    print(f"Total de autores encontrados: {len(authors)}")  # Imprimir la cantidad total de autores encontrados

# WIKIPEDIA
    print("----------------------  WIKIPEDIA  ---------------------------")
    wikipedia_page = Wikipedia('https://es.wikipedia.org/wiki/Real_Madrid_Club_de_Fútbol')
    
 # Definir la lista de palabras clave a buscar
    keywords = []
    while True:
        keywords.append(input("Ingrese una palabra clave: "))
        if keywords[-1] == "salir":
            keywords.pop()
            break
    
    print(wikipedia_page.get_title())  

    # Llamar al método para encontrar párrafos que contengan las palabras clave
    wikipedia_page.find_keyword(keywords)
    
# WIKIMOVIE
    print("----------------------  WIKIMOVIE  ---------------------------")
    link = input("Ingrese el enlace de la película en Wikipedia, vacio se usa oppenheimer: ")
    if link == "":
        movie = WikiMovie('https://es.wikipedia.org/wiki/Oppenheimer_(pel%C3%ADcula)')
    else:
        movie = WikiMovie(link)

    details = movie.get_movie_details()
    print("Título:", details['title'])
    print("Director:", details['director'])
    print("Actores:")
    for actor in details['actors']:
        print("-", actor)
    print("Argumento:", details['argument'])