# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from itertools import chain

#accedo a la página 
urlBase = "https://www.lamborghini.com/es-en/"
driver = webdriver.Chrome()
driver.get(urlBase)
driver.find_element_by_xpath("/html/body/div/header/nav/ul[1]/li[1]/a/span").click()

#otengo modelos
modelos = list(map(lambda x: x.get_attribute('innerHTML'), driver.find_elements_by_xpath("//*[@data-item='left-0']/*[@class='lev-3']/li/a/span")))

#urls para acceder a la página con las características de cada modelo
urls = list(map(lambda x: x.get_attribute('href'), driver.find_elements_by_xpath("//*[@data-item='left-0']/*[@class='lev-3']/li/a")))

cilindradas = list()
potencias = list()
velocidadesMax = list()
aceleracionS = list()
alturas = list()
anchurasB = list()
andhurasT = list()
longitudes = list()
pesos = list()
consumos = list()

	
for i in urls:
    driver.get(i)
   	#obtengo cilindrada
    try:
        cilindrada = driver.find_element_by_xpath('//*[@id="tech-specification"]/div[1]/div/div[1]/ul/li[1]/span[2]').get_attribute('innerHTML')
        cilindradas.insert(len(cilindradas), cilindrada)
    except NoSuchElementException:
        cilindradas.insert(len(cilindradas), "NA")
        pass
    #obtengo potencia
    try:
        potencia = driver.find_element_by_xpath('//*[@id="tech-specification"]/div[1]/div/div[1]/ul/li[2]/span[2]').get_attribute('innerHTML')
        potencias.insert(len(potencias), potencia)
    except NoSuchElementException:
        potencias.insert(len(potencias), 'NA')
        pass
    #obtengo velocidad máxima
    try:
        velMax = driver.find_element_by_xpath('//*[@id="tech-specification"]/div[1]/div/div[1]/ul/li[3]/span[2]').get_attribute('innerHTML')
        velocidadesMax.insert(len(velocidadesMax), velMax)
    except NoSuchElementException:
        velocidadesMax.insert(len(velocidadesMax), 'NA')
        pass
    #obtengo aceleración
    try:
        acel = driver.find_element_by_xpath('//*[@id="tech-specification"]/div[1]/div/div[1]/ul/li[4]/span[2]').get_attribute('innerHTML')
        aceleracionS.insert(len(aceleracionS), acel)
    except NoSuchElementException:
        aceleracionS.insert(len(aceleracionS), 'NA')
        pass 
 

