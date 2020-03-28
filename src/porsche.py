from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from itertools import chain

def filter_price(price_string):
    price_text = price_string.find_element_by_xpath('./div[2]').text
    price_text = price_text.replace('Desde EUR ','').replace(' PVP Recomendado ','')[:-1]
    return price_text


base_url = 'https://www.porsche.com'
driver = webdriver.Chrome()
driver.get(base_url + '/spain')
menu_models = driver.find_element_by_id('m-01-models-menu-button')
menu_models.click()
branch_nodes = driver.find_elements_by_xpath('//h3/a')
root_nodes = list(map(lambda x: x.find_element_by_xpath('./../..'), branch_nodes))
models_nodes = list(map(lambda x: x.find_elements_by_xpath('./div/div[1]/div[2]'), root_nodes))
models_nodes_flatten = list(chain(*models_nodes))
manufacturer = ['porsche']*len(models_nodes_flatten)
models = list(map(lambda x: x.find_element_by_xpath('./div[1]').text, models_nodes_flatten))
prices = list(map(lambda x: filter_price(x), models_nodes_flatten))
urls = list(map(lambda x: x.find_element_by_xpath('./..').get_attribute('href'), models_nodes_flatten))
aceleration = list()
max_speed = list()
power = list()

for x in urls:
    driver.get(base_url + x)
    #get acel
    try:
        acel_node = driver.find_element_by_xpath('//*[contains(text(),"Aceleración")]/preceding-sibling::*[1]')
        acel = acel_node.get_attribute('innerHTML').replace(' s','')
        aceleration.insert(len(aceleration), acel)
    except NoSuchElementException:
        aceleration.insert(len(aceleration), '-1')
        pass
    #get speed
    try:
        spd_node = driver.find_element_by_xpath('//*[contains(text(),"Velocidad máxima")]/../*[contains(text(),"km/h")]')
        spd = spd_node.get_attribute('innerHTML').replace(' km/h','')
        max_speed.insert(len(max_speed), spd)
    except NoSuchElementException:
        max_speed.insert(len(max_speed), '-1')
        pass
    #get power
    try:
        pwr_node = driver.find_element_by_xpath('//*[contains(text(),"Potencia máxima") and contains(text(),"CV")]/../*[contains(text(),"kW")]')
        pwr_filter = re.search('(\d*) CV',pwr_node.get_attribute('innerHTML'),re.IGNORECASE)
        pwr = '-1' if pwr_filter is None else pwr_filter.group(1)
        power.insert(len(power), pwr)
    except NoSuchElementException:
        power.insert(len(power), '-1')
        pass
    

