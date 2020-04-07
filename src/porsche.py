from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException
from itertools import chain
import re
import time


def filter_price(price_string):
    # Usado para limpiar el precio y quedarnos solo con el valor numerico
    price_text = price_string.find_element_by_xpath('./div[2]').text
    price_text = price_text.replace('Desde EUR ', '').replace(
        ' PVP Recomendado ', '')[:-1]
    return price_text


def get_acelerations():
    # Buscamos las aceleraciones en caso de encontrarlas las agregamos al vector de aceleraciones
    # sino las encontramos agregamos un NA
    try:
        # Buscamos el primer hijo del hermano anterior al nodo que contiene la palabra Aceleración
        acel_node = driver.find_element_by_xpath(
            '//*[contains(text(),"Aceleración")]/preceding-sibling::*[1]')
        # Eliminamos las unidades
        acel = acel_node.get_attribute('innerHTML').replace(' s', '')
        acelerations.insert(len(acelerations), acel)
    except NoSuchElementException:
        acelerations.insert(len(acelerations), 'NA')
        pass


def get_max_speeds():
    try:
        # Obtenemos la velocidad máxima buscando el elemento Velocidad máxima
        # que tenga como nodo tio algo que ponga km/h
        spd_node = driver.find_element_by_xpath(
            '//*[contains(text(),"Velocidad máxima")]/../*[contains(text(),"km/h")]')
        # Limpiamos las unidades
        spd = spd_node.get_attribute('innerHTML').replace(' km/h', '')
        max_speeds.insert(len(max_speeds), spd)
    except NoSuchElementException:
        try:
            # Sin no lo encuentra, lo intenamos de otra manera.
            # Desplegamos la opción "Descubrir aspectos destacados"
            driver.find_element_by_xpath(
                '//*[contains(text(),"Descubrir aspectos destacados")]').click()
            # Esperamos ya que dispara una animación JS y sino el contenido no estará disponible
            time.sleep(1)
            # Buscamos el elemento de la clase m-095-title dentro de prestaciones y picamos en él.
            # La clase m-095-title identifica al titulo picable de cada una de las opciones.
            driver.find_element_by_xpath(
                '//*[contains(text(),"Prestaciones") and contains(@class,"m-095-title")]').click()
            # Esperamos de nuevo por la animación JS
            time.sleep(1)
            # Capturamos la velocidad máxima de la tabla en la que está
            spd_node = driver.find_element_by_xpath(
                '//*[contains(text(),"Velocidad máxima")]/../../td/span[contains(text(),"km/h")]')
            # Limpiamos las unidades
            spd = spd_node.get_attribute('innerHTML').replace(' km/h', '')
            max_speeds.insert(len(max_speeds), spd)
        except NoSuchElementException:
            max_speeds.insert(len(max_speeds), 'NA')
            pass


def get_powers():
    try:
        # Buscamos la potencia del motor buscando un texto que contenga Potencia máxima y CV
        # Y que a su vez tenga un nodo tio que contenga kW
        # Esto lo hacemos así por que hay modelos que tienen como una carácteristica destacada la potencia
        # en dos unidades
        pwr_node = driver.find_element_by_xpath(
            '//*[contains(text(),"Potencia máxima") and contains(text(),"CV")]/../*[contains(text(),"kW")]')
        # Usamos una expresión regular para ignorar las otras unidades y limpiar la potencia en CV
        pwr_filter = re.search(
            '(\d*) CV', pwr_node.get_attribute('innerHTML'), re.IGNORECASE)
        # Si la expresión recgular no es capaz de encontrar el valor agregamos un NA sino agregamos el valor
        pwr = 'NA' if pwr_filter is None else pwr_filter.group(1)
        powers.insert(len(powers), pwr)
    except NoSuchElementException:
        try:
            # En caso de no encontrarlo de la manera anterior probamos de otra manera.
            # Desplegamos la opción de unidad de potencia.
            driver.find_element_by_xpath(
                '//*[contains(text(),"Unidad de Potencia") and contains(@class,"m-095-title")]').click()
            # Esperamos por la animación JS
            time.sleep(1)
            # Buscamos la entrada de potencia en CV ya que dentro de este menu las opciones están separadas.
            pwr_node = driver.find_element_by_xpath(
                '//*[contains(text(),"Potencia máxima") and contains(text(),"CV")]/../following-sibling::td/span[contains(text(),"CV")]')
            # Aplicamos una expresión regular para limpiar y obtener el valor
            pwr_filter = re.search(
                '(\d*) CV', pwr_node.get_attribute('innerHTML'), re.IGNORECASE)
            # Si la expresión recgular no es capaz de encontrar el valor agregamos un NA sino agregamos el valor
            pwr = 'NA' if pwr_filter is None else pwr_filter.group(1)
            powers.insert(len(powers), pwr)
        except NoSuchElementException:
            powers.insert(len(powers), 'NA')
            pass


def get_heights():
    try:
        # La altura hay varias formas de obtenerla.
        # Buscando Altura directamente que debe de incluir la altura en el mismo nodo
        hght_node = driver.find_element_by_xpath(
            '//*[contains(text(),"Altura") and contains(text(),"mm")]')
        # Y limpiando las unidades
        hght = hght_node.get_attribute('innerHTML').replace(
            'Altura: ', '').replace('.', '').replace(' mm', '')
        heights.insert(len(heights), hght)
    except NoSuchElementException:
        try:
            # Teniendo la altura separada del nodo del texto "Altura"
            hght_node = driver.find_element_by_xpath(
                '//*[contains(text(),"Altura")]/../*[contains(text(),"mm")]')
            # y limpiamos las unidades
            hght = hght_node.get_attribute(
                'innerHTML').replace('.', '').replace(' mm', '')
            heights.insert(len(heights), hght)
        except NoSuchElementException:
            try:
                # Teniendo la altura separada del nodo del texto "Altura" pero estando en una tabla
                hght_node = driver.find_element_by_xpath(
                    '//*[contains(text(),"Altura")]/../../td/span[contains(text(),"mm")]')
                # Y limpiamos las unidades
                hght = hght_node.get_attribute(
                    'innerHTML').replace('.', '').replace(' mm', '')
                heights.insert(len(heights), hght)
            except NoSuchElementException:
                try:
                    # O desplegando descubrir aspectos destacados
                    driver.find_element_by_xpath(
                        '//*[contains(text(),"Descubrir aspectos destacados")]').click()
                    # Esperamos po la animación en JS
                    time.sleep(1)
                    # Desplegamos carrocería
                    driver.find_element_by_xpath(
                        '//*[contains(text(),"Carrocería")]').click()
                    # Volvemos a esperar por el JS
                    time.sleep(1)
                    # Y ahora buscamos la altura separada del nodo que contiene la etiqueta
                    hght_node = driver.find_element_by_xpath(
                        '//*[contains(text(),"Altura")]/../../td/span[contains(text(),"mm")]')
                    # Y limpiamos las unidades
                    hght = hght_node.get_attribute(
                        'innerHTML').replace('.', '').replace(' mm', '')
                    heights.insert(len(heights), hght)
                except NoSuchElementException:
                    heights.insert(len(heights), 'NA')
                    pass
                pass
            pass
        pass


def get_lengths():
    try:
        # La longitud también tenemos 4 maneras de obtenerla
        # O en el titular donde se incluyen la longitud y el valor juntos
        lngth_node = driver.find_element_by_xpath(
            '//*[contains(text(),"Longitud") and contains(text(),"mm")]')
        # Y limpiamos las unidades
        lngth = lngth_node.get_attribute('innerHTML').replace(
            'Longitud: ', '').replace('.', '').replace(' mm', '')
        lengths.insert(len(lengths), lngth)
    except NoSuchElementException:
        try:
            # Teniendo la longitud separada del nodo del texto "Longitud"
            lngth_node = driver.find_element_by_xpath(
                '//*[contains(text(),"Longitud")]/../*[contains(text(),"mm")]')
            # Y limpiamos las unidades
            lngth = lngth_node.get_attribute(
                'innerHTML').replace('.', '').replace(' mm', '')
            lengths.insert(len(lengths), lngth)
        except NoSuchElementException:
            try:
                # Teniendo la longitud separada del nodo del texto "Lonngitud" pero estando en una tabla
                lngth_node = driver.find_element_by_xpath(
                    '//*[contains(text(),"Longitud")]/../../td/span[contains(text(),"mm")]')
                # Y limpiamos las unidades
                lngth = lngth_node.get_attribute(
                    'innerHTML').replace('.', '').replace(' mm', '')
                lengths.insert(len(heights), lngth)
            except NoSuchElementException:
                try:
                    # Picamos en Descubrir aspectos destacados
                    driver.find_element_by_xpath(
                        '//*[contains(text(),"Descubrir aspectos destacados")]').click()
                    # Esperamos por la animación JS
                    time.sleep(1)
                    # Picamos en carrocería
                    driver.find_element_by_xpath(
                        '//*[contains(text(),"Carrocería")]').click()
                    # Esperamos por la animación JS
                    time.sleep(1)
                    # Obtenemos la longitud separada del nodo que contiene la etiqueta
                    lngth_node = driver.find_element_by_xpath(
                        '//*[contains(text(),"Longitud")]/../../td/span[contains(text(),"mm")]')
                    # Y limpiamos las unidades
                    lngth = lngth_node.get_attribute(
                        'innerHTML').replace('.', '').replace(' mm', '')
                    lengths.insert(len(lengths), lngth)
                except NoSuchElementException:
                    lengths.insert(len(lengths), 'NA')
                    pass
                pass
            pass
        pass


def get_weights():
    # Obtenemos el peso del coche, dependiendo del modelo está en un sitio u otro.
    try:
        # Si tiene accesible un enlace con Todas las especificaciones lo desplegamos
        driver.find_element_by_xpath(
            '//*[contains(text(),"Todas las especificaciones")]').click()
        # Obtenemos la Tara según DIN
        wghts_nodes = driver.find_element_by_xpath(
            '//*[contains(text(),"Tara según DIN")]/../../td[2]/span')
        # Limpiamos los valores, quitamos los puntos y las unidades para quedarnos con el valor númerico
        wghts = wghts_nodes.get_attribute(
            'innerHTML').replace('.', '').replace(' kg', '')
        weights.insert(len(weights), wghts)
    except NoSuchElementException:
        try:
            # Lo buscamos picando en el abuelo de más información
            driver.find_element_by_xpath(
                '//*[contains(text(),"Más información")]/../..').click()
            # Obtenemos el valor
            wghts_nodes = driver.find_element_by_xpath(
                '//*[contains(text(),"Tara según DIN")]/../p[2]')
            # Lo limpiamos
            wghts = wghts_nodes.get_attribute(
                'innerHTML').replace('.', '').replace(' kg', '')
            weights.insert(len(weights), wghts)
        except (ElementNotInteractableException, NoSuchElementException, ElementClickInterceptedException) as e:
            try:
                # En caso de que no se encuentre (NoSunchElementException)
                # o el evento del click no esté en ese elemento (ElementClickInterceptedException)
                # o el elemento no sea picable (ElementNotInteractableException)
                # Buscamos el enlace de "Más información" en el padre del nodo
                driver.find_element_by_xpath(
                    '//*[contains(text(),"Más información")]/..').click()
                # Obtenemos el valor
                wghts_nodes = driver.find_element_by_xpath(
                    '//*[contains(text(),"Tara según DIN")]/../p[2]')
                # Lo limpiamos
                wghts = wghts_nodes.get_attribute(
                    'innerHTML').replace('.', '').replace(' kg', '')
                weights.insert(len(weights), wghts)
                pass
            except (NoSuchElementException, ElementNotInteractableException) as e:
                try:
                    # En caso de que no se encuentre (NoSunchElementException)
                    # o el elemento no sea picable (ElementNotInteractableException)
                    # Buscamos el enlace de "Más información" en el padre del nodo
                    # Buscamos directamente el peso
                    wghts_nodes = driver.find_element_by_xpath(
                        '//*[contains(text(),"Tara según DIN")]/../p[2]')
                    # Y lo limpiamos
                    wghts = wghts_nodes.get_attribute(
                        'innerHTML').replace('.', '').replace(' kg', '')
                    weights.insert(len(weights), wghts)
                    pass
                except NoSuchElementException:
                    # En este punto, trás intentarlo de cuatro maneras diferentes,
                    # entendemos que no se puede obtener y ponemos un NA
                    weights.insert(len(weights), 'NA')
                    pass


def get_consumptions():
    # Obtenemos el consumo que está en un elemento que tiene la clase b-eco__value
    try:
        cnsmp_nodes = driver.find_element_by_xpath(
            '//*[contains(@class,"b-eco__value")]')
        # Cogemos el primer elemento para eliminar las unidades
        cnsmp = cnsmp_nodes.get_attribute('innerHTML').split(' ')[0]
    except NoSuchElementException:
        cnsmp = 'NA'
        pass
    finally:
        consumptions.insert(len(consumptions), cnsmp)


def get_models_nodes_flatten():
    # Obtenemos los nodos de cada uno de los subtipos de coches
    # Buscamos primero el nodo del tipo de coche
    branch_nodes = driver.find_elements_by_xpath('//h3/a')
    # Como todos los submodelos están metidos en un div junto con el nombre del tipo
    # buscamos el nodo raíz
    root_nodes = list(
        map(lambda x: x.find_element_by_xpath('./../..'), branch_nodes))
    # Capturamos los subtipos a partir de los nodos raíz
    models_nodes = list(
        map(lambda x: x.find_elements_by_xpath('./div/div[1]/div[2]'), root_nodes))
    return list(chain(*models_nodes))


def get_models(models_nodes_flatten):
    # Obtenemos los modelos disponibles
    return list(map(lambda x: x.find_element_by_xpath(
        './div[1]').text, models_nodes_flatten))


def get_prices(models_nodes_flatten):
    # Obtenemos los precios base de los modelos
    return list(map(lambda x: filter_price(x), models_nodes_flatten))


def get_urls(models_nodes_flatten):
    # Obtenemos las urls de cada uno de los modelos
    return list(map(lambda x: x.find_element_by_xpath(
        './..').get_attribute('href'), models_nodes_flatten))


base_url = 'https://www.porsche.com'

driver = webdriver.Chrome()
# Cargamos la página en español
driver.get(base_url + '/spain')
# Obtenemos el enlace de los modelos
menu_models = driver.find_element_by_id('m-01-models-menu-button')
# Picamos en él
menu_models.click()
# Obtenemos todos los modelos. Flatten es porque hay tipos de coches y subtipos.
# Por ejemplo el 911 tiene 911 carrera y 911 turbo, así que obtenemos los nodos de
# los subtipos
models_nodes_flatten = get_models_nodes_flatten()
# Rellenamos un vector con el nombre del fabricante
manufacturer = ['porsche']*len(models_nodes_flatten)
# Obtenemos los modelos a partir de los nodos de los modelos
models = get_models(models_nodes_flatten)
# Obtenemos los precios a partir de los nodos de los modelos
prices = get_prices(models_nodes_flatten)
# Obtenemos las urls de cada submodelo
urls = get_urls(models_nodes_flatten)

acelerations = list()
max_speeds = list()
powers = list()
heights = list()
lengths = list()
weights = list()
consumptions = list()

# Iteramos por todas las urls
for x in urls:
    driver.get(base_url + x)
    print(base_url + x)
    # Añadimos la aceleración del modelo actual
    get_acelerations()
    # La velocidad máxima
    get_max_speeds()
    # La potencia
    get_powers()
    # La altura
    get_heights()
    # La longitud
    get_lengths()
    # El peso
    get_weights()
    # El consumo
    get_consumptions()
    #tbd: get_widths()
    #tbd: get_cylinder()


driver.close()
