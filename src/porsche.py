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


def get_acelerations():
    try:
        acel_node = driver.find_element_by_xpath(
            '//*[contains(text(),"Aceleración")]/preceding-sibling::*[1]')
        acel = acel_node.get_attribute('innerHTML').replace(' s', '')
        acelerations.insert(len(acelerations), acel)
    except NoSuchElementException:
        acelerations.insert(len(acelerations), 'NA')
        pass


def get_max_speeds():
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
            max_speeds.insert(len(max_speeds), 'NA')
            pass


def get_powers():
    try:
        pwr_node = driver.find_element_by_xpath(
            '//*[contains(text(),"Potencia máxima") and contains(text(),"CV")]/../*[contains(text(),"kW")]')
        pwr_filter = re.search(
            '(\d*) CV', pwr_node.get_attribute('innerHTML'), re.IGNORECASE)
        pwr = 'NA' if pwr_filter is None else pwr_filter.group(1)
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
            pwr = 'NA' if pwr_filter is None else pwr_filter.group(1)
            powers.insert(len(powers), pwr)
        except NoSuchElementException:
            powers.insert(len(powers), 'NA')
            pass


def get_heights():
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
                    heights.insert(len(heights), 'NA')
                    pass
                pass
            pass
        pass


def get_lengths():
    try:
        lngth_node = driver.find_element_by_xpath(
            '//*[contains(text(),"Longitud") and contains(text(),"mm")]')
        lngth = lngth_node.get_attribute('innerHTML').replace(
            'Longitud: ', '').replace('.', '').replace(' mm', '')
        lengths.insert(len(lengths), lngth)
    except NoSuchElementException:
        try:
            lngth_node = driver.find_element_by_xpath(
                '//*[contains(text(),"Longitud")]/../*[contains(text(),"mm")]')
            lngth = lngth_node.get_attribute(
                'innerHTML').replace('.', '').replace(' mm', '')
            lengths.insert(len(lengths), lngth)
        except NoSuchElementException:
            try:
                lngth_node = driver.find_element_by_xpath(
                    '//*[contains(text(),"Longitud")]/../../td/span[contains(text(),"mm")]')
                lngth = lngth_node.get_attribute(
                    'innerHTML').replace('.', '').replace(' mm', '')
                lengths.insert(len(heights), lngth)
            except NoSuchElementException:
                try:
                    driver.find_element_by_xpath(
                        '//*[contains(text(),"Descubrir aspectos destacados")]').click()
                    time.sleep(1)
                    driver.find_element_by_xpath(
                        '//*[contains(text(),"Carrocería")]').click()
                    time.sleep(1)
                    lngth_node = driver.find_element_by_xpath(
                        '//*[contains(text(),"Longitud")]/../../td/span[contains(text(),"mm")]')
                    lngth = lngth_node.get_attribute(
                        'innerHTML').replace('.', '').replace(' mm', '')
                    lengths.insert(len(lengths), lngth)
                except NoSuchElementException:
                    lengths.insert(len(lengths), 'NA')
                    pass
                pass
            pass
        pass


def get_consumption():
    try:
        cnsmp_nodes = driver.find_element_by_xpath(
            '//*[contains(@class,"b-eco__value")]')
        cnsmp = cnsmp_nodes.get_attribute('innerHTML').split(' ')[0]
        consumptions.insert(len(consumptions), cnsmp)
    except NoSuchElementException:
        consumptions.insert(len(consumptions), 'NA')
        pass


def get_models_nodes_flatten():
    branch_nodes = driver.find_elements_by_xpath('//h3/a')
    root_nodes = list(
        map(lambda x: x.find_element_by_xpath('./../..'), branch_nodes))
    models_nodes = list(
        map(lambda x: x.find_elements_by_xpath('./div/div[1]/div[2]'), root_nodes))
    return list(chain(*models_nodes))


def get_models(models_nodes_flatten):
    return list(map(lambda x: x.find_element_by_xpath(
        './div[1]').text, models_nodes_flatten))


def get_prices(models_nodes_flatten):
    return list(map(lambda x: filter_price(x), models_nodes_flatten))


def get_urls(models_nodes_flatten):
    return list(map(lambda x: x.find_element_by_xpath(
        './..').get_attribute('href'), models_nodes_flatten))


base_url = 'https://www.porsche.com'

driver = webdriver.Chrome()
driver.get(base_url + '/spain')
menu_models = driver.find_element_by_id('m-01-models-menu-button')
menu_models.click()
models_nodes_flatten = get_models_nodes_flatten()
manufacturer = ['porsche']*len(models_nodes_flatten)
models = get_models(models_nodes_flatten)
prices = get_prices(models_nodes_flatten)
urls = get_urls(models_nodes_flatten)

acelerations = list()
max_speeds = list()
powers = list()
heights = list()
lengths = list()
consumptions = list()

for x in urls:
    driver.get(base_url + x)
    get_acelerations()
    get_max_speeds()
    get_powers()
    get_heights()
    get_lengths()
    get_consumption()

driver.close()
