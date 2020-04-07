# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from itertools import chain
from selenium.webdriver.common.action_chains import ActionChains


def scrapingLambo():
    #accedo a la página 
    urlBase = "https://www.lamborghini.com/es-en/"
    driver = webdriver.Chrome()
    driver.get(urlBase)
    driver.find_element_by_xpath("/html/body/div/header/nav/ul[1]/li[1]/a/span").click()

    #otengo modelos
    modelos = list(map(lambda x: x.get_attribute('innerHTML'), driver.find_elements_by_xpath("//*[@data-item='left-0']/*[@class='lev-3']/li/a/span")))

    #urls para acceder a la página con las características de cada modelo
    urls = list(map(lambda x: x.get_attribute('href'), driver.find_elements_by_xpath("//*[@data-item='left-0']/*[@class='lev-3']/li/a")))

    #el modelo URUS como no tiene submodelos lo cojo de otro sitio y lo añado al final de las listas de modelos y urls
    modeloU = list(map(lambda x: x.get_attribute('innerHTML'), driver.find_elements_by_xpath("//*[@data-item='left-0']/*[@class='lev-2']/li/a/span")))
    modelos.insert(len(modelos), modeloU[2])
    urlU = list(map(lambda x: x.get_attribute('href'), driver.find_elements_by_xpath("//*[@data-item='left-0']/*[@class='lev-2']/li/a")))
    urls.insert(len(urls), urlU[2])


    cilindradas = list()
    potencias = list()
    velocidadesMax = list()
    aceleracionS = list()
    longitudes = list()
    alturas = list()
    anchurasB = list()
    anchurasT = list()
    pesos = list()
    consumos = list()
    precio = list ()
    marca = list ()


    for i in urls:
        driver.get(i)
   	    #obtengo cilindrada
        try:
            if i == urls[7] or i == urls[8] or i == urls[9]: #modelos de serie limitada
                cilindrada = driver.find_element_by_xpath('//*[@id="block6"]/div/div/div[2]/div/ul[1]/li[2]/span').get_attribute('innerHTML')
            elif i == urls[11]: #submodelo Concept Asterion
                cilindrada = driver.find_element_by_xpath('//*[@id="block6"]/div/div/div[2]/div/ul[4]/li[2]/span').get_attribute('innerHTML')
            else:
                cilindrada = driver.find_element_by_xpath('//*[@id="tech-specification"]/div[1]/div/div[1]/ul/li[1]/span[2]').get_attribute('innerHTML')
            cilindradas.insert(len(cilindradas), cilindrada)
        except NoSuchElementException:
            cilindradas.insert(len(cilindradas), "NA")
            pass
        #obtengo potencia
        try:
            if i == urls[7] or i == urls[8] or i == urls[9]:
                potencia = driver.find_element_by_xpath('//*[@id="block6"]/div/div/div[2]/div/ul[1]/li[5]/span').get_attribute('innerHTML')
            elif i == urls[11]:
                potencia = driver.find_element_by_xpath('//*[@id="block6"]/div/div/div[2]/div/ul[4]/li[8]/span').get_attribute('innerHTML')
            else:
                potencia = driver.find_element_by_xpath('//*[@id="tech-specification"]/div[1]/div/div[1]/ul/li[2]/span[2]').get_attribute('innerHTML')
            potencias.insert(len(potencias), potencia)
        except NoSuchElementException:
            potencias.insert(len(potencias), 'NA')
            pass
        #obtengo velocidad máxima
        try:
            if i == urls[7] or i == urls[8] or i == urls[9]:
                velMax = driver.find_element_by_xpath('//*[@id="block6"]/div/div/div[2]/div/ul[3]/li[1]/span').get_attribute('innerHTML')
            else:
                velMax = driver.find_element_by_xpath('//*[@id="tech-specification"]/div[1]/div/div[1]/ul/li[3]/span[2]').get_attribute('innerHTML')
            velocidadesMax.insert(len(velocidadesMax), velMax)
        except NoSuchElementException:
            velocidadesMax.insert(len(velocidadesMax), 'NA')
            pass
        #obtengo aceleración
        try:
            if i == urls[7] or i == urls[8] or i == urls[9]:
                acel = driver.find_element_by_xpath('//*[@id="block6"]/div/div/div[2]/div/ul[3]/li[2]/span').get_attribute('innerHTML')
            else:
                acel = driver.find_element_by_xpath('//*[@id="tech-specification"]/div[1]/div/div[1]/ul/li[4]/span[2]').get_attribute('innerHTML')
            aceleracionS.insert(len(aceleracionS), acel)
        except NoSuchElementException:
            aceleracionS.insert(len(aceleracionS), 'NA')
            pass
        #obtengo longitud
        try:
            longitud = driver.find_element_by_xpath('//*[@id="techSpecificationDetail"]/div/div[2]/div[9]/ul/li[1]/span[2]').get_attribute('innerHTML')
            longitudes.insert(len(longitudes), longitud)
        except NoSuchElementException:
            longitudes.insert(len(longitudes), 'NA')
            pass
        #obtengo alturas
        try:
            altura = driver.find_element_by_xpath('//*[@id="techSpecificationDetail"]/div/div[2]/div[9]/ul/li[4]/span[2]').get_attribute('innerHTML')
            alturas.insert(len(alturas), altura)
        except NoSuchElementException:
            alturas.insert(len(alturas), 'NA')
            pass
        #obtengo anchurasB, excluidos los espejos retrovisores
        try:
            anchB = driver.find_element_by_xpath('//*[@id="techSpecificationDetail"]/div/div[2]/div[9]/ul/li[2]/span[2]').get_attribute('innerHTML')
            anchurasB.insert(len(anchurasB), anchB)
        except NoSuchElementException:
            anchurasB.insert(len(anchurasB), 'NA')
            pass
        #obtengo anchurasT, incluidos los espejos retrovisores
        try:
            anchT = driver.find_element_by_xpath('//*[@id="techSpecificationDetail"]/div/div[2]/div[9]/ul/li[3]/span[2]').get_attribute('innerHTML')
            anchurasT.insert(len(anchurasT), anchT)
        except NoSuchElementException:
            anchurasT.insert(len(anchurasT), 'NA')
            pass
        #obtengo pesos en seco o al vacío
        try: 
            peso = driver.find_element_by_xpath('//*[@id="techSpecificationDetail"]/div/div[2]/div[9]/ul/li[6]/span[2]').get_attribute('innerHTML')
            pesos.insert(len(pesos), peso)
        except NoSuchElementException:
            pesos.insert(len(pesos), 'NA')
            pass
        #obtengo consumo combinado
        try:
            if i == urls[11]:
                consumo = driver.find_element_by_xpath('//*[@id="block6"]/div/div/div[2]/div/ul[5]/li[1]/span').get_attribute('innerHTML')
            else:
                consumo = driver.find_element_by_xpath('//*[@id="techSpecificationDetail"]/div/div[2]/div[10]/ul/li[1]/span[2]').get_attribute('innerHTML')
            consumos.insert(len(consumos), consumo)
        except NoSuchElementException:
            consumos.insert(len(consumos), 'NA')
            pass 
        #relleno las listas del precio y de la marca con igual número de elementos que el resto de listas
        precio.insert(len(precio), "NA")
        marca.insert(len(marca), "Lamborghini")   

    driver.close()

    matrizDatos = [
        marca,
        modelos,
        alturas,
        anchurasB,
        anchurasT,
        longitudes,
        pesos,
        cilindradas,
        consumos,
        potencia,
        aceleracionS,
        velocidadesMax,
        precio
    ]
    #trasponer filas y columnas en la matriz
    matrizDatosT = [list(i) for i in zip(*matrizDatos)]
    print(matrizDatosT)
    return matrizDatosT


