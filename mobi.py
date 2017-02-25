# -*- coding: utf-8 -*-
# continuous-integration
import telebot
import os
import redis

redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
redis = redis.from_url(redis_url)
from pprint import pprint
technoconf = -1001070076534
me = 94026383
TA= -1001109363260
token='357359911:AAHxnKF-bXuVQKUVxsaV_FTqXSJg8AkbFDE'
bot = telebot.TeleBot(token)
twoch={
    '@Kylmakalle':94026383,
    'test':-1001100823817
}
blacklist={
    'TA':-1001109363260
}
wl = redis.from_url(os.environ.get("REDIS_URL"))

bl = redis.from_url(os.environ.get("HEROKU_REDIS_MAROON_URL"))
print(wl.get('@Kylmakalle'))

login=token[0:9]


@bot.message_handler(content_types=['text'])
def handle_text(message):
    print(message.text)
    for n in wl.llen():
        if (message.chat.id == wl.lindex(n)) or (message.from_user.id == wl.lindex(n)):
            print(wl.lindex(n))
            break
        else:
            bot.send_message(message.chat.id, 'Contact @Kylmakalle first!')
            bot.leave_chat(message.chat.id)
    if message.chat.type == 'private':
        print(login)
        if "/get_wl " + str(login) in message.text:
            bot.reply_to(message, 'WHITELIST '+ str(wl.hgetall()))
        if "/add_wl " + str(login) in message.text:
            bot.reply_to(message, 'Добавление в WHITELIST, введите имя')
            def handle_text(message):
                name = message.text
                bot.reply_to(message, 'Добавление в WHITELIST, введите id')
                def handle_text(message):
                    ident=message.text
                    wl.hset(str(name),ident)

    if "Ассистент, тест" in message.text:
            bot.send_message(me,'TESTED!')


@bot.message_handler(content_types=['photo'])
def handle_photos(message):
    print(message)
    if not(message.forward_from_chat == None):
        forwared = message.forward_from_chat.id
        if not (message.chat.type == 'private'):
            #Admins = bot.get_chat_administrators(message.chat.id)
            #for i in range(len(list(Admins))):
             #   pprint(Admins)
               # if 'id' in Admins[i]['user'] != message.from_user.id:
                for k in blacklist:
                    print(blacklist[k])
                    if (forwared == blacklist[k]):
                        bot.kick_chat_member(message.chat.id,message.from_user.id)
                        bot.send_message(message.chat.id, message.from_user.first_name+'(@' + message.from_user.username + ') '+'BANNED!')
                        bot.forward_message(me,message.chat.id,message.message_id)
                        bot.send_message(me, message.from_user.first_name + ' (@' + message.from_user.username + ') ' +'id: #'+ str(message.from_user.id) +' BANNED!')
bot.polling(none_stop=True, interval=0)
