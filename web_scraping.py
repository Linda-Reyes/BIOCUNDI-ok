# Importación de las librerías necesarias
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

# Buscar la ubicación del driver de Google Chrome y conectarlo para manipularlo
def conectarDriverChrome(page):
    # Configurar el driver de Chrome
    chrome_options = Options()
    service = Service(executable_path='C:/Drivers/chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(page)
    driver.implicitly_wait(0.5)  # Aumentar el tiempo de espera implícito
    return driver

# Extración de datos de las diversas especies de los departamentos de Cundinamarca y Boyacá
def procesarEspecie(driver, i, department, classs, typee, class_container, class_name, class_scientific_name, class_img, class_icon):
    species = driver.find_elements(By.CSS_SELECTOR, class_container)
    for spe in species:
        # Inicializar valores por defecto
        name_text = 'No disponible'
        sci_name_text = 'No disponible'
        src_img = 'No disponible'
        src_ico = 'No disponible'

        try:
            # Obtener el nombre común
            name_elements = spe.find_elements(By.CSS_SELECTOR, class_name)
            if name_elements and name_elements[0].text.strip():
                name_text = name_elements[0].text

            # Obtener el nombre científico
            sci_name_elements = spe.find_elements(By.CSS_SELECTOR, class_scientific_name)
            if sci_name_elements and sci_name_elements[0].text.strip():
                sci_name_text = sci_name_elements[0].text

            # Obtener la imagen
            img_elements = spe.find_elements(By.XPATH, class_img)
            if img_elements:
                src_img = img_elements[0].get_attribute('src')

            # Obtener el icono
            ico_elements = spe.find_elements(By.CLASS_NAME, class_icon)
            if ico_elements:
                src_ico = ico_elements[0].get_attribute('src')

            # Guardar los datos de la especie en la lista
            spe_dict = {'DEPARTAMENTO': department, 
                        'CLASE': classs,
                        'TIPO': typee, 
                        'NOMBRE': name_text, 
                        'NOMBRE CIENTÍFICO': sci_name_text, 
                        'IMAGEN': src_img,
                        'ICONO': src_ico}
            species_list.append(spe_dict)

            # Imprimir los resultados
            print(f'{i}. Departamento: {department}, Clase: {classs}, Tipo: {typee}\n   Nombre: {name_text}\n   Nombre científico: {sci_name_text}\n   Imagen: {src_img}\n   Icono: {src_ico}')
            i += 1

        except Exception as e:
            print(f"Error en la especie {i}: {e}")

    return i  # Devolver el contador actualizado

# Validar que no hayan mas páginas de las especies buscadas
def navegarPagina(driver, class_container, class_name, class_scientific_name, class_img, class_icon, class_next, department, classs, typee):
    i = 1
    while True:
        i = procesarEspecie(driver, i, department, classs, typee, class_container, class_name, class_scientific_name, class_img, class_icon)

        # Intentar encontrar y hacer clic en el botón "Siguiente"
        try:
            next_button = WebDriverWait(driver, 4).until(
                EC.element_to_be_clickable((By.XPATH, class_next))
            )
            driver.execute_script("arguments[0].scrollIntoView();", next_button)  # Asegurar que el botón esté visible
            next_button.click()
            
            WebDriverWait(driver, 10).until(
                lambda d: d.execute_script('return document.readyState') == 'complete'
            )
            time.sleep(5)

        except Exception as e:
            print('No se encontró más páginas.')
            break

# Crear el archivo CSV con los datos extraidos de las especies
def crearCSV():
    with open(file_name, mode='a', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=None, delimiter=';')
    
        if species_list:
            fieldnames = species_list[0].keys()
            writer.fieldnames = fieldnames
            writer.writeheader()
            for row in species_list:
                writer.writerow(row)
        else:
            for row in species_list:
                writer.writerow(row.values())

    print(f'Se ha modificado el archivo {file_name}')
    species_list.clear()

def ejecutarProceso(pagina, department, classs, typee):
    driver = conectarDriverChrome(pagina)
    navegarPagina(driver, class_container, class_name, class_scientific_name, class_img, class_icon, class_next, department, classs, typee)
    driver.quit()
    crearCSV()

# Parámetros de las páginas a ser scraping con su clasificación de especies
species = [

    # Datos de las especies del departamento de Boyacá
    {'page': 'https://colombia.inaturalist.org/places/boyaca-co#taxon=1', 'department':'Boyacá', 'class':'Animales', 'type': 'Todos'},
    {'page': 'https://colombia.inaturalist.org/places/boyaca-co#establishment_means=native&taxon=1', 'department':'Boyacá', 'class':'Animales', 'type': 'Nativa'},
    {'page': 'https://colombia.inaturalist.org/places/boyaca-co#establishment_means=endemic&taxon=1', 'department':'Boyacá', 'class':'Animales', 'type': 'Endémica'},
    {'page': 'https://colombia.inaturalist.org/places/boyaca-co#establishment_means=introduced&taxon=1', 'department':'Boyacá', 'class':'Animales', 'type': 'Introducida'},
    {'page': 'https://colombia.inaturalist.org/places/boyaca-co#taxon=47686', 'department':'Boyacá', 'class': 'Protozoarios', 'type': 'Todos'},
    {'page': 'https://colombia.inaturalist.org/places/boyaca-co#taxon=47126', 'department':'Boyacá', 'class': 'Plantas', 'type': 'Todos'},
    {'page': 'https://colombia.inaturalist.org/places/boyaca-co#establishment_means=native&taxon=47126', 'department':'Boyacá', 'class': 'Plantas', 'type': 'Nativa'},
    {'page': 'https://colombia.inaturalist.org/places/boyaca-co#establishment_means=endemic&taxon=47126', 'department':'Boyacá', 'class': 'Plantas', 'type': 'Endémica'},
    {'page': 'https://colombia.inaturalist.org/places/boyaca-co#establishment_means=introduced&taxon=47126', 'department':'Boyacá', 'class': 'Plantas', 'type': 'Introducida'},
    {'page': 'https://colombia.inaturalist.org/places/boyaca-co?taxon=47170', 'department':'Boyacá', 'class': 'Hongos', 'type': 'Todos'},
    # Datos de las especies del departamento de Cundinamarca
    {'page': 'https://colombia.inaturalist.org/places/cundinamarca-co#taxon=1', 'department':'Cundinamarca', 'class':'Animales', 'type': 'Todos'},
    {'page': 'https://colombia.inaturalist.org/places/cundinamarca-co#establishment_means=native&taxon=1', 'department':'Cundinamarca', 'class':'Animales', 'type': 'Nativa'},
    {'page': 'https://colombia.inaturalist.org/places/cundinamarca-co#establishment_means=endemic&taxon=1', 'department':'Cundinamarca', 'class':'Animales', 'type': 'Endémica'},
    {'page': 'https://colombia.inaturalist.org/places/cundinamarca-co#establishment_means=introduced&page=1&taxon=1', 'department':'Cundinamarca', 'class':'Animales', 'type': 'Introducida'},
    {'page': 'https://colombia.inaturalist.org/places/cundinamarca-co#establishment_means=&taxon=47686', 'department':'Cundinamarca', 'class': 'Protozoarios', 'type': 'Todos'},
    {'page': 'https://colombia.inaturalist.org/places/cundinamarca-co#taxon=47126', 'department':'Cundinamarca', 'class': 'Plantas', 'type': 'Todos'},
    {'page': 'https://colombia.inaturalist.org/places/cundinamarca-co#establishment_means=native&taxon=47126', 'department':'Cundinamarca', 'class': 'Plantas', 'type': 'Nativa'},
    {'page': 'https://colombia.inaturalist.org/places/cundinamarca-co#establishment_means=endemic&taxon=47126', 'department':'Cundinamarca', 'class': 'Plantas', 'type': 'Endémica'},
    {'page': 'https://colombia.inaturalist.org/places/cundinamarca-co#establishment_means=introduced&taxon=47126', 'department':'Cundinamarca', 'class': 'Plantas', 'type': 'Introducida'},
    {'page': 'https://colombia.inaturalist.org/places/cundinamarca-co#taxon=47170', 'department':'Cundinamarca', 'class': 'Hongos', 'type': 'Todos'},
    {'page': 'https://colombia.inaturalist.org/places/cundinamarca-co#taxon=48222', 'department':'Cundinamarca', 'class': 'Algas pardas y parientes', 'type': 'Todos'},
]

# Lista para almacenar la información de las especies
species_list = []
# Clases y Xpaths para obtener los datos solicitados
class_container = 'div.taxon'
class_name = 'span.comname'
class_scientific_name = 'span.sciname'
class_img = './/preceding-sibling::div//img[contains(@class, "photo")]'
class_icon = 'iconic'
class_next = '//a[contains(@class, "next_page")]'  
# Nombre del fichero CSV a crear y modificar
file_name = 'Biodiversidad en Boyacá y Cundinamarca.csv'

# Ejecución del script
for specie in species:
    ejecutarProceso(specie['page'], specie['department'], specie['class'], specie['type'])
