import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import time
import datetime
import threading

PORT = int(os.environ.get('PORT', 5000))

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

TOKEN = os.getenv("TOKEN")

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)

driver.get('https://bancobci.finmarketslive.cl/www/index.html')

wait = WebDriverWait(driver, 10)
wait.until(presence_of_element_located((By.XPATH, "/html/body/section/div/div[2]")))

iniciador = False

def scrapping(update, context):
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
    x = 0
    for i in mensaje:
        mensaje[i] = valores[x] + " " + variaciones[x]
        x += 1

    for i in mensaje:
        mensaje_lista.append(i + " " + mensaje[i] + "\n")
    ahora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    mensaje_lista.insert(0, "Registro a las: " + ahora + "\n")
    update.message.reply_text("".join(mensaje_lista))
    time.sleep(5)

def loopeador(update, context):
    global iniciador
    update.message.reply_text("Se ha iniciado el reporte de indicadores a las 10:00. Para detenerlo, escribe '/stop'. Para solicitar un reporte al instante, escribir /muestra.")
    reloj = time.gmtime(time.time())
    while iniciador:
        if (reloj.tm_sec == 0) and (reloj.tm_min == 0) and (reloj.tm_hour == 10 - 4): #Cada día a las 10am
            scrapping(update, context)

def start(update, context):
    global iniciador
    iniciador = True
    t = threading.Thread(target=loopeador, args=(update, context))
    t.start()

def prueba(update, context):
    update.message.reply_text('Hola mundo')

def stop(update, context):
    global iniciador
    iniciador = False
    update.message.reply_text("Se ha desactivado el reporte. Para volverlo a iniciar, escriba '/start'")

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("prueba", prueba))
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("stop", stop))
    dp.add_handler(CommandHandler("muestra", scrapping))

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