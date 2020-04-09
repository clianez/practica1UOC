# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException
from itertools import chain
import re
import time
import urllib.robotparser


def filter_price(price_string):
    # Usado para limpiar el precio y quedarnos solo con el valor numerico
    price_text = price_string.find_element_by_xpath('./div[2]').text
    price_text = price_text.replace('Desde EUR ', '').replace(
        ' PVP Recomendado ', '')[:-1]
    return price_text


def get_acelerations(driver, acelerations):
    # Buscamos las aceleraciones en caso de encontrarlas las agregamos al vector de aceleraciones
    # sino las encontramos agregamos un NA
    try:
        # Buscamos el primer hijo del hermano anterior al nodo que contiene la palabra Aceleración
        acel_node = driver.find_element_by_xpath(
            '//*[contains(text(),"Aceleración")]/preceding-sibling::*[1]')
        # Eliminamos las unidades
        acel = acel_node.get_attribute('innerHTML').replace(' s', '')
        acelerations.insert(len(acelerations), acel)
        return acelerations
    except NoSuchElementException:
        acelerations.insert(len(acelerations), 'NA')
        return acelerations
        pass


def get_max_speeds(driver, max_speeds):
    try:
        # Obtenemos la velocidad máxima buscando el elemento Velocidad máxima
        # que tenga como nodo tio algo que ponga km/h
        spd_node = driver.find_element_by_xpath(
            '//*[contains(text(),"Velocidad máxima")]/../*[contains(text(),"km/h")]')
        # Limpiamos las unidades
        spd = spd_node.get_attribute('innerHTML').replace(' km/h', '')
        max_speeds.insert(len(max_speeds), spd)
        return max_speeds
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
            return max_speeds
        except NoSuchElementException:
            max_speeds.insert(len(max_speeds), 'NA')
            return max_speeds
            pass


def get_powers(driver, powers):
    pwr = ''

    try:
        # Buscamos la potencia del motor buscando un texto que contenga Potencia máxima y CV
        # Y que a su vez tenga un nodo tio que contenga kW
        # Esto lo hacemos así por que hay modelos que tienen como una carácteristica destacada la potencia
        # en dos unidades
        pwr_node = driver.find_element_by_xpath(
            '//*[contains(text(),"Potencia máxima") and contains(text(),"CV")]/../*[contains(text(),"kW")]')
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
        except NoSuchElementException:
            pwr = 'NA'
            pass

    # y limpiamos las unidades
    if pwr == '':
        # Aplicamos una expresión regular para limpiar y obtener el valor
        pwr_filter = re.search(
            '(\d*) CV', pwr_node.get_attribute('innerHTML'), re.IGNORECASE)
        # Si la expresión recgular no es capaz de encontrar el valor agregamos un NA sino agregamos el valor
        pwr = 'NA' if pwr_filter is None else pwr_filter.group(1)
    powers.insert(len(powers), pwr)
    return powers


def get_dimensions(driver, text, dimArray, url):
    # Iniciailzamos el valor a vacio
    value = ''

    try:
        # Las dimensiones hay varias formas de obtenerlas.
        # Buscando el texto directamente que debe de incluir el valor en el mismo nodo
        node = driver.find_element_by_xpath(
            '//*[contains(text(),"' + text + '") and contains(text(),"mm")]')
    except NoSuchElementException:
        try:
            # Teniendo el valor separado del nodo del texto
            node = driver.find_element_by_xpath(
                '//*[contains(text(),"' + text + '")]/../*[contains(text(),"mm")]')
        except NoSuchElementException:
            try:
                # Teniendo el valor separado del nodo del texto pero estando en una tabla
                node = driver.find_element_by_xpath(
                    '//*[contains(text(),"' + text + '")]/../../td/span[contains(text(),"mm")]')
            except NoSuchElementException:
                try:
                    # O desplegando descubrir aspectos destacados
                    driver.find_element_by_xpath(
                        '//*[contains(text(),"Descubrir aspectos destacados") or contains(text(),"Todas las especificaciones")]').click()
                    # Esperamos po la animación en JS
                    time.sleep(1)
                    # Desplegamos carrocería
                    try:
                        driver.find_element_by_xpath(
                            '//*[contains(text(),"Carrocería")]').click()
                    except ElementClickInterceptedException:
                        # Hay páginas en las que el elemento picable es el padre
                        driver.find_element_by_xpath(
                            '//*[contains(text(),"Carrocería")]/..').click()
                        pass
                    # Volvemos a esperar por el JS
                    time.sleep(1)
                    # Y ahora buscamos el valor separada del nodo que contiene el texto
                    node = driver.find_element_by_xpath(
                        '//*[contains(text(),"' + text + '")]/../../td/span[contains(text(),"mm")]')
                except NoSuchElementException:
                    value = 'NA'
                    pass
                pass
            pass
        pass

    # y limpiamos las unidades
    if value == '':
        value = node.get_attribute(
            'innerHTML').replace(text + ': ', '').replace('.', '').replace(' mm', '')
    dimArray.insert(len(dimArray), value)
    return dimArray


def get_weights(driver, url, weights):
    wghts = ''

    # Cargamos la página principal del subtipo
    driver.get(url)

    # Obtenemos el peso del coche, dependiendo del modelo está en un sitio u otro.
    try:
        # Si tiene accesible un enlace con Todas las especificaciones o Descubrir aspectos destacados lo desplegamos
        driver.find_element_by_xpath(
            '//*[contains(text(),"Descubrir aspectos destacados") or contains(text(),"Todas las especificaciones")]').click()
        # Obtenemos la Tara según DIN
        wghts_nodes = driver.find_element_by_xpath(
            '//*[contains(text(),"Tara según DIN")]/../../td[2]/span')
    except NoSuchElementException:
        try:
            # Lo buscamos picando en el abuelo de más información
            driver.find_element_by_xpath(
                '//*[contains(text(),"Más información")]/../..').click()
            # Obtenemos el valor
            wghts_nodes = driver.find_element_by_xpath(
                '//*[contains(text(),"Tara según DIN")]/../p[2]')
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
            except (NoSuchElementException, ElementNotInteractableException) as e:
                try:
                    # En caso de que no se encuentre (NoSunchElementException)
                    # o el elemento no sea picable (ElementNotInteractableException)
                    # Buscamos directamente el peso
                    wghts_nodes = driver.find_element_by_xpath(
                        '//*[contains(text(),"Tara según DIN")]/../p[2]')
                except NoSuchElementException:
                    # En este punto, trás intentarlo de cuatro maneras diferentes,
                    # entendemos que no se puede obtener y ponemos un NA
                    wghts = 'NA'
                    pass

    # Limpiamos los valores, quitamos los puntos y las unidades para quedarnos con el valor númerico
    if wghts == '':
        wghts = wghts_nodes.get_attribute(
            'innerHTML').replace('.', '').replace(' kg', '')
    weights.insert(len(weights), wghts)
    return weights


def get_consumptions(driver, url, consumptions):
    cnsmp = ''

    # Cargamos la página principal del subtipo
    driver.get(url)

    # Obtenemos el consumo que está en un elemento que tiene la clase b-eco__value
    try:
        cnsmp_nodes = driver.find_element_by_xpath(
            '//*[contains(@class,"b-eco__value")]')
    except NoSuchElementException:
        cnsmp = 'NA'
        pass

    if cnsmp == '':
        # Cogemos el primer elemento para eliminar las unidades
        cnsmp = cnsmp_nodes.get_attribute('innerHTML').split(' ')[0]
    consumptions.insert(len(consumptions), cnsmp)
    return consumptions


def get_cylinder(driver, url, cylinders):
    clndr = ''

    # Cargamos la página principal del subtipo
    driver.get(url)

    # Obtenemos el peso del coche, dependiendo del modelo está en un sitio u otro.
    try:
        # Si tiene accesible un enlace con Todas las especificaciones o Descubrir aspectos destacados lo desplegamos
        driver.find_element_by_xpath(
            '//*[contains(text(),"Descubrir aspectos destacados") or contains(text(),"Todas las especificaciones")]').click()
        # Buscamos el elemento que contenga Cilindrada y a partir de ese buscamos el elemento con el valor
        clndr_nodes = driver.find_element_by_xpath(
            '//*[contains(text(),"Cilindrada")]/../../td[2]/span')
    except NoSuchElementException:
        try:
            # Picamos en más información
            driver.find_element_by_xpath(
                '//*/a/span[contains(text(),"Más información")]').click()
            # Buscamos el elemento que contenga cm³
            clndr_nodes = driver.find_element_by_xpath(
                '//*[contains(text(),"cm³")]')
        except NoSuchElementException:
            try:
                # Buscamos directamente un elemento que incluya cm³
                clndr_nodes = driver.find_element_by_xpath(
                    '//*[contains(text(),"cm³")]')
            except NoSuchElementException:
                # En este punto, trás intentarlo de tres maneras diferentes,
                # entendemos que no se puede obtener y ponemos un NA
                clndr = 'NA'
                pass
            pass
        pass

    # Limpiamos los valores, quitamos los puntos y las unidades para quedarnos con el valor númerico
    if clndr == '':
        clndr = clndr_nodes.get_attribute(
            'innerHTML').replace('.', '').replace(' cm³', '')
    cylinders.insert(len(cylinders), clndr)
    return cylinders


def get_models_nodes_flatten(driver):
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


def scrapingPorsche():
    base_url = 'https://www.porsche.com'

    # Leemos el robots.txt para verificar que se puede acceder a las urls
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(base_url + '/robots.txt')
    rp.read()

    driver = webdriver.Chrome()
    # Cargamos la página en español en caso de que esté permitida por el robots

    if rp.can_fetch("*", base_url + '/spain'):
        driver.get(base_url + '/spain')
    else:
        exit()

    # Obtenemos el enlace de los modelos
    menu_models = driver.find_element_by_id('m-01-models-menu-button')
    # Picamos en él
    menu_models.click()
    # Obtenemos todos los modelos. Flatten es porque hay tipos de coches y subtipos.
    # Por ejemplo el 911 tiene 911 carrera y 911 turbo, así que obtenemos los nodos de
    # los subtipos
    models_nodes_flatten = get_models_nodes_flatten(driver)
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
    widthsB = list()
    widthsT = list()
    weights = list()
    consumptions = list()
    cylinders = list()

    # Iteramos por todas las urls
    for x in urls:

        if rp.can_fetch("*", base_url + x):
            driver.get(base_url + x)
            print(base_url + x)
            # Añadimos la aceleración del modelo actual
            acelerations = get_acelerations(driver, acelerations)
            # La velocidad máxima
            max_speeds = get_max_speeds(driver, max_speeds)
            # La potencia
            powers = get_powers(driver, powers)
            # La altura
            heights = get_dimensions(driver, 'Altura', heights, base_url + x)
            # La longitud
            lengths = get_dimensions(driver, 'Longitud', lengths, base_url + x)
            # La anchura
            widthsB = get_dimensions(driver, 'Anchura (con retrovisores abatidos)',
                                     widthsB, base_url + x)
            widthsT = get_dimensions(driver, 'Anchura (con retrovisores extendidos)',
                                     widthsT, base_url + x)
            # El peso
            weigths = get_weights(driver, base_url + x, weights)
            # El consumo
            consumptions = get_consumptions(driver, base_url + x, consumptions)
            # La cilindrada
            cylinders = get_cylinder(driver, base_url + x, cylinders)

    driver.close()

    matrix = [
        manufacturer,
        models,
        heights,
        widthsB,
        widthsT,
        lengths,
        weights,
        cylinders,
        consumptions,
        powers,
        acelerations,
        max_speeds,
        prices
    ]
    # Trasponemos las filas en columnas

    matrixT = [list(i) for i in zip(*matrix)]
    print(matrixT)
    return matrix
