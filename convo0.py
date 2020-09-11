#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import os
import sys
import time
from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

# Enable logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)

reply_keyboard = [['Rants', 'Shout-outs'],
                  ['Confessions', 'Something else...'],
                  ['Done'],['/start']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

uname = ['@sco_beta', '@artemio_official', '@chilling21', '@onlinelambingan']


def restart_prog():
  python = sys.executable
  os.execl(python, python, *sys.argv)
  curdir = os.getcwd()

def facts_to_str(user_data):
    facts = list()

    for key, value in user_data.items():
        facts.append('{} - {}'.format(key, value))

    return "\n".join(facts).join(['\n', '\n'])


def start(update, context):
    update.message.reply_text(
        "Hi! My name is Traviz, isang cute na bot na cute ang owner.\n"
        "Kamusta {}, dahil sa pag gamit kay Traviz ikaw ay Cute na rin.\n"
        "Mayroon kabang Rants? Confessions? or Shout-outs? Hmmmmm... something else?\n"
        "\n"
        "Ahahaha! Nasa tamang lugar ka nice!\n"
        "\n"
        "HOW TO USE?\n"
        "1. Press /start\n"
        "2. Choose what button you'll gonna use.\n"
        "3. Send and press Done.\n"
        "4. OPTIONAL: You can use all the buttons at the same time.\n"
        "3. IMPORTANT!!! Press /start button to Reboot Traviz and use Traviz again.\n"
        "\n"
        "\n"
        "\n"
        "JOIN US NOW!\n"
        "Discord:\n"
        "Telegram Channel:\n"
        ">>>SCO beta @sco_beta\n"
        ">>>Love Alarm @scolovealarm\n"
        "Telegram Groupchats:\n"
        ">>>SCO online lambingan @onlinelambingan\n"
        "\n"
        "\n"
        "\n"
        "Watch the video tutorial if you still cannot understand the written tutorial\n"
        "https:t.me/travizph/2".format(update.message.from_user.first_name),
        reply_markup=markup)

    return CHOOSING


def regular_choice(update, context):
    text = update.message.text
    context.user_data['choice'] = text
    update.message.reply_text(
        'Your {}? Yes, I would love to hear about that!'.format(text.lower()))

    return TYPING_REPLY


def custom_choice(update, context):
    update.message.reply_text('Alright, please send me the category first, '
                              'for example "Most impressive skill"')

    return TYPING_CHOICE


def received_information(update, context):
    user_data = context.user_data
    text = update.message.text
    category = user_data['choice']
    user_data[category] = text
    del user_data['choice']

    update.message.reply_text("Neat! Just so you know, this is what you already told me:"
                              "{} You can tell me more, or change your thoughts"
                              " on something.".format(facts_to_str(user_data)),
                              reply_markup=markup)

    return CHOOSING


def done(update, context):
    user_data = context.user_data
    if 'choice' in user_data:
        del user_data['choice']

    update.message.reply_text("I will broadcast your message now:"
                              "{}"
                              "Until next time!".format(facts_to_str(user_data)))
    for unames in uname:
      context.bot.send_message(chat_id=unames,text=((
                              "{}"
                              .format(facts_to_str(user_data)))))

    user_data.clear()
    return ConversationHandler.END


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1213507926:AAEvwOV2dlV1_bnL96lFVPQweBchFblWV9E", use_context=True)



    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            CHOOSING: [MessageHandler(Filters.regex('^(Rants|Shout-outs|Confessions)$'),
                                      regular_choice),
                       MessageHandler(Filters.regex('^Something else...$'),
                                      custom_choice)
                       ],

            TYPING_CHOICE: [
                MessageHandler(Filters.text & ~(Filters.command | Filters.regex('^Done$')),
                               regular_choice)],

            TYPING_REPLY: [
                MessageHandler(Filters.text & ~(Filters.command | Filters.regex('^Done$')),
                               received_information)],
        },

        fallbacks=[MessageHandler(Filters.regex('^Done$'), done)]

    )

    dp.add_handler(conv_handler)

    # Start the Bot
    #updater.start_polling()
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook('https://travizpy.herokuapp.com/' + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
