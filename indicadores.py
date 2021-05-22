import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os

PORT = int(os.environ.get('PORT', 5000))

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
TOKEN = '1827921985:AAFyMZYqk4bSQYlzfHbGFcaaYKz_N8kR0Bg'

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.headless = True

driver = webdriver.Chrome('chromedriver.exe', chrome_options=options)

driver.get('https://bancosantanderinversiones.finmarketslive.cl/www/mercados.html')

wait = WebDriverWait(driver, 10)
wait.until(presence_of_element_located((By.ID, "Wrapper")))

def start(update, context):
    update.message.reply_text('Se ha iniciado el reporte de indicadores cada 5 segundos.')
    while True:
        ipsa = driver.find_elements_by_xpath("//tr[@id='Edom:2,i:3969,q:1,c:numerito_instrument_2']/td[position()<=2]")
        for indicador in ipsa:
            update.message.reply_text(indicador.text)
        print()
        cobre = driver.find_elements_by_xpath("//tr[@id='Edom:9,i:393,q:2,c:numerito_instrument_2']/td[position()<=2]")
        for indicador in cobre:
            update.message.reply_text(indicador.text)
        print()
        dolar = driver.find_elements_by_xpath("//tr[@id='Edom:14,i:2,q:2,c:numerito_instrument_4']/td[position()<=2]")
        for indicador in dolar:
            update.message.reply_text(indicador.text)
        print()
        wti = driver.find_elements_by_xpath("//tr[@id='Edom:10,i:982,q:2,c:numerito_instrument_2']/td[position()<=2]")
        for indicador in wti:
            update.message.reply_text(indicador.text)
        print()
        oro = driver.find_elements_by_xpath("//tr[@id='Edom:11,i:980,q:2,c:numerito_instrument_2']/td[position()<=2]")
        for indicador in oro:
            update.message.reply_text(indicador.text)
        update.message.reply_text("-------------")
        time.sleep(5)

'''
def help(update, context):
    update.message.reply_text('Help!')


def echo(update, context):
    """Reemplaza las vocales por la i, ya sea minúscula, mayuscola, con o sin tilde"""

    texto1 = update.message.text

    texto2 = texto1.replace("a", "i").replace("e", "i").replace("o", "i").replace("u", "i")

    texto3 = texto2.replace("A", "I").replace("E", "I").replace("O", "I").replace("U", "I")

    texto4 = texto3.replace("á", "í").replace("é", "í").replace("ó", "í").replace("ú", "í")

    texto5 = texto4.replace("Á", "Í").replace("É", "Í").replace("Ó", "Í").replace("Ú", "Í")
    
    update.message.reply_text(texto5, quote=False)
'''

def prueba(update, context):
    update.message.reply_text('Hola mundo')


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    
    dp.add_handler(CommandHandler("prueba", prueba))
    dp.add_handler(CommandHandler("start", start))
    #dp.add_handler(CommandHandler("help", help))
    '''
    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))
    '''
    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook('https://indicadoreschile.herokuapp.com/' + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()