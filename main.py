import solicitud
from datetime import datetime
import asyncio

import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os

PORT = int(os.environ.get('PORT', 5000))

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

#TOKEN = os.getenv("TOKEN")
TOKEN = "1827921985:AAFyMZYqk4bSQYlzfHbGFcaaYKz_N8kR0Bg"


def prueba(update, context):
    update.message.reply_text('Hola mundo. Para mostrar los indicadores, escribe /muestra.')

def scrapping(update, context):
    
    lista_str = solicitud.solicitud()
    ahora = datetime.now().strftime("%H:%M:%S %d/%m/%Y")
    mensaje = ahora + ":\n"
    for i in lista_str:
        mensaje += i + "\n"
    update.message.reply_text(mensaje)

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


async def vuelta(update, context):
    print("async_foo started")
    while True:
        update.message.reply_text(":)")
        await asyncio.sleep(5)

def go(update, context):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(vuelta())


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("prueba", prueba))
    dp.add_handler(CommandHandler("start", prueba))
    dp.add_handler(CommandHandler("muestra", scrapping))
    dp.add_handler(CommandHandler("vuelta", go))

    dp.add_error_handler(error)
    
    #updater.start_webhook(listen="0.0.0.0", port=int(PORT), url_path=TOKEN)
    #updater.bot.setWebhook('https://indicadoreschile.herokuapp.com/' + TOKEN)
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    print("ejecutandose")
    main()
    