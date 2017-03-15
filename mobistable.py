# -*- coding: utf-8 -*-
# encoding=utf8
import sys
from botanio import botan
import jsonpickle

#reload(sys)
#sys.setdefaultencoding('utf8')
# continuous-integration
import telebot
from tinydb import TinyDB, Query
from tinydb_smartcache import SmartCacheTable
from pprint import pprint
TinyDB.table_class = SmartCacheTable

wl = TinyDB('wl.json')
bl = TinyDB('bl.json')

users=Query()

#wl.purge()
#wl.all()

if not (wl.contains(users.name == '@Kylmakalle')):
    wl.insert({"name": "@Kylmakalle", "ID": "94026383"})
if not(wl.contains(users.name == '@Aggeoberlin')):
    wl.insert({"name": "@Aggeoberlin", "ID": "63656504"})
if not(wl.contains(users.name == '@ru2chmobi')):
    wl.insert({"name": "@ru2chmobi", "ID": "-1001098866708"})      
if not(wl.contains(users.name == '@ru2chhw')):
    wl.insert({"name": "@ru2chhw", "ID": "-1001086103845"})  





technoconf = -1001070076534
me = 94026383
TA= -1001109363260
token='357359911:AAGhxPUJxVhUl8tNjz76MByQPYBPtwnfvR4'
bot = telebot.TeleBot(token)



dvachch={
    '@Kylmakalle':94026383,
    'test':-1001100823817

}

def clearoutput(string):
    for x in ['[', ']', ',', '}', "'", ' ']:
        string = string.replace(x, '')
    for x in ["{"]:
        string = string.replace(x, '\n')
    for x in [":"]:
        string = string.replace(x, ': ')
    for x in ["ID:"]:
        string = string.replace(x, '  ID:')
    return(string)

def legit(message):
    users = Query()
    if wl.search(users.ID.matches(str(message.chat.id))) or wl.search(users.ID.matches(str(message.from_user.id))):
        return 1
    else:
        bot.send_message(message.chat.id, 'Contact @Kylmakalle first!')
        if not (message.chat.type == 'private'):
            bot.leave_chat(message.chat.id)
        return 0

"""def legit_check(message):
    l = 0
    for n in range(len(wl)):
        #print(wl.all()[n]['ID'])
        if (wl.all()[n]['ID'] == str(message.chat.id)) or (wl.all()[n]['ID'] == str(message.from_user.id)):
            l = 0
            break
        else:
            l = 1
    if (l == 1):
        bot.send_message(message.chat.id, 'Contact @Kylmakalle first!')
        if not(message.chat.type == 'private'):
            bot.leave_chat(message.chat.id)
        return 0
    else:
        return 1"""

def bl_check(message):
     #print(message)
     if (message.forward_from_chat):
        forwared = str(message.forward_from_chat.id)
        #print(bl.all()[k]['ID'])
        #print(forwared)
        users=Query()
        #print(bl.search(users.ID.matches(forwared)))
        if bl.search(users.ID.matches(forwared)):
            uid = message.from_user
            #pprint(message)
            m = (jsonpickle.encode(message))
            message_dict = m
            event_name = 'Ban'
            botan.track(botan_token, uid, message_dict, event_name)
            bot.kick_chat_member(message.chat.id, message.from_user.id)
            bot.send_message(message.chat.id,message.from_user.first_name + ' (@' + message.from_user.username + ') ' + '*BANNED!*',parse_mode='Markdown')
            bot.forward_message(me, message.chat.id, message.message_id)
            bot.send_message(me,message.from_user.first_name + ' (@' + message.from_user.username + ') ' + 'id: #' + str(message.from_user.id) + ' *BANNED!*',parse_mode='Markdown')

def cancel(message):
    if str(message.text) == '0':
        bot.reply_to(message, 'ОТМЕНА')
        return 0
    else:
        return 1

login=token[0:9]

botan_token = 'ImTjEtyVoiwO9eIgq6ytaxwBl:hg0QJ6' # Token got from @botaniobot

@bot.message_handler(content_types=['text'])
def handle_text(message):
    #uid = message.from_user
    #pprint(message)
    #m = (jsonpickle.encode(message))
    #message_dict = m
    #event_name = 'msg'
    #botan.track(botan_token, uid, message_dict, event_name)
    print(message.from_user.first_name +' ('+ str(message.from_user.id) + ') ' + ': ' + message.text)
    if legit(message):
        bl_check(message)
        if "Ассистент, тест" in message.text:
            bot.send_message(me,'TESTED!')
        if message.chat.type == 'private':
            if message.text == '/help':
                bot.send_message(message.chat.id, 'Доступные команды: \n /help - Вызов этого окна \n /addwl - Добавление чатов в *WHITELIST* \n /addbl - Добавление каналов в *BLACKLIST* \n /wl - Вывод *WHITELIST* \n /bl - Вывод *BLACKLIST* \n \n Напиши `0` для отмены операции \n По проблемам и вопросам: @Kylmakalle',parse_mode='Markdown')
            if message.text == '/addwl':
                msg = bot.reply_to(message, 'Добавление в WHITELIST, введите @username')
                bot.register_next_step_handler(msg, WL_ADD)
            if message.text == '/addbl':
                msg = bot.reply_to(message, 'Добавление в BLACKLIST, форвардни сообщение из чата')
                bot.register_next_step_handler(msg, BL_INSERT)
            if message.text == '/wl':
                #print(clearoutput(str(wl.all())))
                bot.send_message(message.chat.id, clearoutput(str(wl.all())))
            if message.text == '/bl':
                bot.send_message(message.chat.id, clearoutput(str(bl.all())))

def BL_INSERT(message):
      if cancel(message):
        if not(message.forward_from_chat==None):
            users = Query()
            if bl.search(users.ID.matches(str(message.forward_from_chat.id))):
                msg = bot.reply_to(message, "Такой есть уже, ещё разок!")
                bot.register_next_step_handler(msg, WL_ADD)
            else:
                key = '@' + message.forward_from_chat.username
                ident = str(message.forward_from_chat.id)
                bl.insert({'name': key, 'ID' : ident})
                bl_reply = str(bl.search(users.name == key))
                bl_reply = clearoutput(bl_reply)
                bot.reply_to(message, 'Добавлено! ' + bl_reply)
                bot.send_message(me,message.from_user.first_name + ' (@' + message.from_user.username + ') ' + 'id: #' + str(message.from_user.id) + ' Добавил в BLACKLIST ' + bl_reply)
        else:
            msg = bot.reply_to(message, 'Форвардни сообщение из чата!')
            bot.register_next_step_handler(msg, BL_INSERT)


def WL_ADD(message):
  if cancel(message):
    uname = str(message.text)
    try:
        bot.get_chat(uname)
        users = Query()
        if wl.search(users.ID.matches(str(bot.get_chat(uname).id))):
            msg = bot.reply_to(message, "Такой есть уже, ещё разок!")
            bot.register_next_step_handler(msg, WL_ADD)
        else:
            info = bot.get_chat(uname)
            wl.insert({'name': uname, 'ID': str(info.id)})
            wl_reply = str(wl.search(users.name == uname))
            wl_reply = clearoutput(wl_reply)
            bot.reply_to(message, 'Добавлено! ' + wl_reply)
            bot.send_message(me, message.from_user.first_name + ' (@' + message.from_user.username + ') ' + 'id: #' + str(
                message.from_user.id) + ' Добавил в WHITELIST ' + wl_reply)
    except:
        msg = bot.reply_to(message, "Чата не существует, ещё разок!")
        bot.register_next_step_handler(msg, WL_ADD)




@bot.message_handler(content_types=['photo'])
def handle_photos(message):
    #print(message)
    if not(message.forward_from_chat == None):
        if not (message.chat.type == 'private'):
            bl_check(message)


bot.polling(none_stop=True, interval=0)