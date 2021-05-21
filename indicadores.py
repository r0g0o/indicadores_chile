from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.ui import WebDriverWait
import time

driver = webdriver.Chrome(r"C:\Users\PC1337\Desktop\Codigo Curso Python\chromedriver.exe")

driver.get('https://bancosantanderinversiones.finmarketslive.cl/www/mercados.html')

wait = WebDriverWait(driver, 10)
wait.until(presence_of_element_located((By.ID, "Wrapper")))

while True:        
    ipsa = driver.find_elements_by_xpath("//tr[@id='Edom:2,i:3969,q:1,c:numerito_instrument_2']/td[position()<=2]")
    for indicador in ipsa:
        print(indicador.text)
    print()
    cobre = driver.find_elements_by_xpath("//tr[@id='Edom:9,i:393,q:2,c:numerito_instrument_2']/td[position()<=2]")
    for indicador in cobre:
        print(indicador.text)
    print()
    dolar = driver.find_elements_by_xpath("//tr[@id='Edom:14,i:2,q:2,c:numerito_instrument_4']/td[position()<=2]")
    for indicador in dolar:
        print(indicador.text)
    print()
    wti = driver.find_elements_by_xpath("//tr[@id='Edom:10,i:982,q:2,c:numerito_instrument_2']/td[position()<=2]")
    for indicador in wti:
        print(indicador.text)
    print()
    oro = driver.find_elements_by_xpath("//tr[@id='Edom:11,i:980,q:2,c:numerito_instrument_2']/td[position()<=2]")
    for indicador in oro:
        print(indicador.text)
    print("----------")
    time.sleep(5)

