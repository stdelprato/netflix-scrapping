# El script trabaja con ChromeDriver v85 para el navegador Google Chrome v85

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select

# Indicar ruta de donde se encuentra el chromedriver.exe
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

# Ingreso directamente a la url de la información de Breaking Bad, aunque también debería funcionar 
# con la URL de cualquier otra serie que tenga mas de una temporada (no funciona con peliculas)
driver.get("https://www.netflix.com/ar/title/70143836")

try:
    # Container de la sección de información
    tv_show_info = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "title-info"))
    )

    # Container de la sección de episodios
    seccion_capitulos = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "section-seasons-and-episodes"))
    )

    # Asignación del elemento <select> para cambiar de temporada en el Dropdown menu de netflix
    select_element = WebDriverWait(seccion_capitulos, 10).until(
        EC.presence_of_element_located((By.ID, "undefined-select"))
    )
    select_temporada = Select(select_element)

    # Línea para asignar a una variable la cantidad de opciones que tiene
    # el elemento <select> para determinar la cantidad de temporadas que tiene la serie
    cantidad_temporadas = len(select_temporada.options)

    # Esta parte del diccionario esta escrita manualmente por cada TV show para agarrar
    # lo mas relevante de la sección info de la pagina de la serie en netflix.
    #
    #
    # Luego, automaticamente se agregan al diccionario las sinopsis 
    # de cada uno de los capitulos, separado por temporada.
    datos_serie = {
        "titulo": tv_show_info.find_element_by_class_name("title-title").text,
        "sinopsis": tv_show_info.find_element_by_class_name("title-info-synopsis").text,
        "anio_de_salida": tv_show_info.find_element_by_class_name("item-year").text,
        "genero": tv_show_info.find_element_by_class_name("item-genre").text,
        "clasificación_por_edad": tv_show_info.find_element_by_class_name("maturity-number").text,
        "premios": driver.find_element_by_class_name("hook-text").text
    }

    # Agrego llaves y valores de cada temporada y episodios al dict datos_serie
    for i in range(cantidad_temporadas):
        select_temporada.select_by_index(i)
        temporada_seleccionada = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "season-active"))
        )
        episodios = temporada_seleccionada.find_elements_by_class_name("episode")
        anio_de_salida = temporada_seleccionada.find_element_by_class_name("season-release-year").text[-4:]

        datos_serie[f"temporada_{i+1}_anio_de_salida"] = anio_de_salida
        for episodio in episodios:
            episodio_titulo = episodio.find_element_by_class_name("episode-title").text
            episodio_sinopsis = episodio.find_element_by_class_name("epsiode-synopsis").text

            if episodio_titulo[1] == ".":
                datos_serie[f"T{i+1}_episodio_{episodios.index(episodio)+1}"] = episodio_titulo[3:]
            else:
                datos_serie[f"T{i+1}_episodio_{episodios.index(episodio)+1}"] = episodio_titulo[4:]

            datos_serie[f"T{i+1}_episodio_{episodios.index(episodio)+1}_sinopsis"] = episodio_sinopsis
    
    # Imprimo cada valor del diccionario datos_serie
    for key, value in datos_serie.items():
        print(key, ':', value)
finally:
    driver.quit()