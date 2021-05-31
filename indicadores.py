import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os

PORT = int(os.environ.get('PORT', 5000))

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

TOKEN = os.getenv("TOKEN")

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import time
import datetime

options = Options()
options.headless = True
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no_sandbox")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
driver = webdriver.Chrome(executable_path="chromedriver.exe", options=options)

driver.get('https://bancobci.finmarketslive.cl/www/index.html')

wait = WebDriverWait(driver, 10)
wait.until(presence_of_element_located((By.XPATH, "/html/body/section/div/div[2]")))

def start(update, context):
    update.message.reply_text('Se ha iniciado el reporte de indicadores cada 5 segundos.')
    while True:
        mensaje = {"IPSA": "", "Dolar": "", "Cobre": "", "UF": ""}
        mensaje_lista = []
        valores = []
        variaciones = []
        xpath = ["/html/body/section/div/div[2]/div[2]/table/tbody/tr[1]", 
        "/html/body/section/div/div[2]/div[1]/div/div[1]/div[2]/div[2]/table/tbody/tr[1]", 
        "/html/body/section/div/div[2]/div[1]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[1]", 
        "/html/body/section/div/div[2]/div[1]/div/div[1]/div[2]/div[2]/table/tbody/tr[4]"]  #IPSA, Dolar, Cobre y UF, respectivamente

        for i in xpath: #agregar valor
            valores.append(driver.find_element_by_xpath(i + "/td[2]/span").text)
        for i in xpath: # agregar variación
            variaciones.append(driver.find_element_by_xpath(i + "/td[3]/span[1]").text)
        
        for i in mensaje:
            x = 0
            y = valores[x] + " " + variaciones[x]
            mensaje[i] = y
            x += 1

        for i in mensaje:
            mensaje_lista.append(i + " " + mensaje[i] + "\n")
        ahora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        mensaje_lista.insert(0, "Registro a las: " + ahora + "\n")
        update.message.reply_text("".join(mensaje_lista))
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

    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook('https://indicadoreschile.herokuapp.com/' + TOKEN)

    #updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    print("ejecutandose")
    main()