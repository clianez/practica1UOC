from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from itertools import chain
import re
import time


def filter_price(price_string):
    price_text = price_string.find_element_by_xpath('./div[2]').text
    price_text = price_text.replace('Desde EUR ', '').replace(
        ' PVP Recomendado ', '')[:-1]
    return price_text


base_url = 'https://www.porsche.com'
driver = webdriver.Chrome()
driver.get(base_url + '/spain')
menu_models = driver.find_element_by_id('m-01-models-menu-button')
menu_models.click()
branch_nodes = driver.find_elements_by_xpath('//h3/a')
root_nodes = list(
    map(lambda x: x.find_element_by_xpath('./../..'), branch_nodes))
models_nodes = list(
    map(lambda x: x.find_elements_by_xpath('./div/div[1]/div[2]'), root_nodes))
models_nodes_flatten = list(chain(*models_nodes))
manufacturer = ['porsche']*len(models_nodes_flatten)
models = list(map(lambda x: x.find_element_by_xpath(
    './div[1]').text, models_nodes_flatten))
prices = list(map(lambda x: filter_price(x), models_nodes_flatten))
urls = list(map(lambda x: x.find_element_by_xpath(
    './..').get_attribute('href'), models_nodes_flatten))
acelerations = list()
max_speeds = list()
powers = list()
heights = list()

for x in urls:
    driver.get(base_url + x)
    # get acel
    try:
        acel_node = driver.find_element_by_xpath(
            '//*[contains(text(),"Aceleración")]/preceding-sibling::*[1]')
        acel = acel_node.get_attribute('innerHTML').replace(' s', '')
        acelerations.insert(len(acelerations), acel)
    except NoSuchElementException:
        acelerations.insert(len(acelerations), '-1')
        pass
    # get speed
    try:
        spd_node = driver.find_element_by_xpath(
            '//*[contains(text(),"Velocidad máxima")]/../*[contains(text(),"km/h")]')
        spd = spd_node.get_attribute('innerHTML').replace(' km/h', '')
        max_speeds.insert(len(max_speeds), spd)
    except NoSuchElementException:
        try:
            driver.find_element_by_xpath(
                '//*[contains(text(),"Descubrir aspectos destacados")]').click()
            time.sleep(1)
            driver.find_element_by_xpath(
                '//*[contains(text(),"Prestaciones") and contains(@class,"m-095-title")]').click()
            time.sleep(1)
            spd_node = driver.find_element_by_xpath(
                '//*[contains(text(),"Velocidad máxima")]/../../td/span[contains(text(),"km/h")]')
            spd = spd_node.get_attribute('innerHTML').replace(' km/h', '')
            max_speeds.insert(len(max_speeds), spd)
        except NoSuchElementException:
            print(base_url+x)
            max_speeds.insert(len(max_speeds), '-1')
            pass
    # get power
    try:
        pwr_node = driver.find_element_by_xpath(
            '//*[contains(text(),"Potencia máxima") and contains(text(),"CV")]/../*[contains(text(),"kW")]')
        pwr_filter = re.search(
            '(\d*) CV', pwr_node.get_attribute('innerHTML'), re.IGNORECASE)
        pwr = '-1' if pwr_filter is None else pwr_filter.group(1)
        powers.insert(len(powers), pwr)
    except NoSuchElementException:
        try:
            driver.find_element_by_xpath(
                '//*[contains(text(),"Unidad de Potencia") and contains(@class,"m-095-title")]').click()
            time.sleep(1)
            pwr_node = driver.find_element_by_xpath(
                '//*[contains(text(),"Potencia máxima") and contains(text(),"CV")]/../following-sibling::td/span[contains(text(),"CV")]')
            pwr_filter = re.search(
                '(\d*) CV', pwr_node.get_attribute('innerHTML'), re.IGNORECASE)
            pwr = '-1' if pwr_filter is None else pwr_filter.group(1)
            powers.insert(len(powers), pwr)
        except NoSuchElementException:
            print(base_url+x)
            powers.insert(len(powers), '-1')
            pass
    # get height
    try:
        hght_node = driver.find_element_by_xpath(
            '//*[contains(text(),"Altura") and contains(text(),"mm")]')
        hght = hght_node.get_attribute('innerHTML').replace(
            'Altura: ', '').replace('.', '').replace(' mm', '')
        heights.insert(len(heights), hght)
    except NoSuchElementException:
        try:
            hght_node = driver.find_element_by_xpath(
                '//*[contains(text(),"Altura")]/../*[contains(text(),"mm")]')
            hght = hght_node.get_attribute(
                'innerHTML').replace('.', '').replace(' mm', '')
            heights.insert(len(heights), hght)
        except NoSuchElementException:
            try:
                hght_node = driver.find_element_by_xpath(
                    '//*[contains(text(),"Altura")]/../../td/span[contains(text(),"mm")]')
                hght = hght_node.get_attribute(
                    'innerHTML').replace('.', '').replace(' mm', '')
                heights.insert(len(heights), hght)
            except NoSuchElementException:
                try:
                    driver.find_element_by_xpath(
                        '//*[contains(text(),"Descubrir aspectos destacados")]').click()
                    time.sleep(1)
                    driver.find_element_by_xpath(
                        '//*[contains(text(),"Carrocería")]').click()
                    time.sleep(1)
                    hght_node = driver.find_element_by_xpath(
                        '//*[contains(text(),"Altura")]/../../td/span[contains(text(),"mm")]')
                    hght = hght_node.get_attribute(
                        'innerHTML').replace('.', '').replace(' mm', '')
                    heights.insert(len(heights), hght)
                except NoSuchElementException:
                    print(base_url+x)
                    heights.insert(len(heights), '-1')
                    pass
                pass
            pass
        pass

