import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os

PORT = int(os.environ.get('PORT', 5000))

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

TOKEN = os.getenv("TOKEN")

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.headless = True
options.add_experimental_option('excludeSwitches', ['enable-logging'])

driver = webdriver.Chrome('./chromedriver.exe', options=options)

driver.get('https://bancosantanderinversiones.finmarketslive.cl/www/mercados.html')
#driver.get('https://mercadosenlinea.inversionessecurity.cl/www/resumen.html')

wait = WebDriverWait(driver, 10)
wait.until(presence_of_element_located((By.ID, "Wrapper")))
#wait.until(presence_of_element_located((By.XPATH, "/html/body/div[4]/div")))

def start(update, context):
    update.message.reply_text('Se ha iniciado el reporte de indicadores cada 5 segundos.')
    while True:
        mensaje = []
        mensaje1 = ""
        mensaje2 = ""
        mensaje3 = ""
        mensaje4 = ""
        mensaje5 = ""
        mensaje6 = ""
        mensajef = []
        
        ipsa = driver.find_elements_by_xpath("//tr[@id='Edom:2,i:3969,q:1,c:numerito_instrument_2']/td")
        for indicador in ipsa:
            mensaje1 = mensaje1 + ": " + indicador.text
        mensaje.append(mensaje1)
        cobre = driver.find_elements_by_xpath("//tr[@id='Edom:9,i:393,q:2,c:numerito_instrument_2']/td")
        for indicador in cobre:
            mensaje2 = mensaje2 + ": " + indicador.text
        mensaje.append(mensaje2)
        dolar = driver.find_elements_by_xpath("//tr[@id='Edom:14,i:2,q:2,c:numerito_instrument_4']/td")
        for indicador in dolar:
            mensaje3 = mensaje3 + ": " + indicador.text
        mensaje.append(mensaje3)
        wti = driver.find_elements_by_xpath("//tr[@id='Edom:10,i:982,q:2,c:numerito_instrument_2']/td")
        for indicador in wti:
            mensaje4 = mensaje4 + ": " + indicador.text
        mensaje.append(mensaje4)
        oro = driver.find_elements_by_xpath("//tr[@id='Edom:11,i:980,q:2,c:numerito_instrument_2']/td")
        for indicador in oro:
            mensaje5 = mensaje5 + ": " + indicador.text
        mensaje.append(mensaje5)
        uf = driver.find_elements_by_xpath("//*[@id='Wrapper']/div[1]/div/div[2]/div/div/div[1]/ul/li[4]/div")
        for indicador in uf:
            mensaje6 = mensaje6 + ": " + indicador.text
        mensaje.append(mensaje6)
        '''
        ipsa = driver.find_elements_by_xpath("//*[@id='Edom:237224065932,i:3969,q:1,c:pushNormalFilterIndices']")
        for indicador in ipsa:
            mensaje1 = mensaje1 + ": " + indicador.text
        mensaje.append(mensaje1)
        cobre = driver.find_elements_by_xpath("//*[@id='Edom:12953293362,i:393,q:1,c:pushFilterCommodities']")
        for indicador in cobre:
            mensaje2 = mensaje2 + ": " + indicador.text
        mensaje.append(mensaje2)
        dolar = driver.find_elements_by_xpath("//*[@id='Edom:195794128,i:2,q:2,c:pushFilterCurrencies']")
        for indicador in dolar:
            mensaje3 = mensaje3 + ": " + indicador.text
        mensaje.append(mensaje3)
        uf = driver.find_elements_by_xpath("/html/body/div[4]/div/div[2]/div[2]/div[6]/div[2]/div[1]")
        for indicador in uf:
            mensaje4 = mensaje4 + ": " + indicador.text
        mensaje.append(mensaje4)
        '''
        for i in mensaje:
            mensajef.append(i.replace(": ", "", 1) + "\n")
        print(mensajef)
        update.message.reply_text("".join(mensajef))
        update.message.reply_text("-------------")
        time.sleep(5)

def prueba(update, context):
    update.message.reply_text('Hola mundo')

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("prueba", prueba))
    dp.add_handler(CommandHandler("start", start))

    dp.add_error_handler(error)
    updater.start_polling()
    '''
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook('https://indicadoreschile.herokuapp.com/' + TOKEN)
    '''
    updater.idle()

if __name__ == '__main__':
    print("ejecutandose")
    main()