import urllib.request
import telegram
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, InlineQueryHandler
from telegram.ext import BaseFilter, MessageHandler, Filters
import logging
import argparse
import os, random


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)


def parse_input():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument('token', metavar='TOKEN', type=str)
    args = parser.parse_args()
    return args


def findOccurrences(s, ch):
    return [i for i, letter in enumerate(s) if letter == ch]


def movies(bot, update):
  poster = random.choice(os.listdir("oncime/"))
  bot.send_photo(update.message.chat_id, open('oncime/'+poster,'rb'))

  fp = urllib.request.urlopen("https://www.lanacion.com.ar/cartelera-de-cine")
  mybytes = fp.read()
  htmlStr = mybytes.decode("utf8")
  fp.close()

  splittedHtmlStr = htmlStr.split('\n')
  for htmlLine in splittedHtmlStr:
    if 'poster' in htmlLine:
      indices=findOccurrences(htmlLine, '"')[0:2]
      bot.send_message(chat_id=update.message.chat_id, text=htmlLine[indices[0]+1:indices[1]])



def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='pedime peliculas con /movies')


def help(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='pedime peliculas con /movies')


def main():
    botArgs = parse_input()
    updater = Updater(botArgs.token)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_handler(CommandHandler('movies', movies))

    
    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process_reply_msg receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == "__main__":
    main()