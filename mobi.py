# -*- coding: utf-8 -*-
# encoding=utf8
import sys
import datetime
from botanio import botan
import jsonpickle
import requests
# reload(sys)
# sys.setdefaultencoding('utf8')
# continuous-integration
import telebot
from tinydb import TinyDB, Query
from tinydb_smartcache import SmartCacheTable
from pprint import pprint

TinyDB.table_class = SmartCacheTable

wl = TinyDB('whitelist.json')
bl = TinyDB('bl.json')

users = Query()

#wl.purge()
#wl.all()




if not (wl.contains(users.name == '@Kylmakalle')):
    wl.insert({"name": "@Kylmakalle", "ID": "94026383"})
if not (wl.contains(users.name == '@Aggroberlin')):
    wl.insert({"name": "@Aggroberlin", "ID": "163656504"})
if not (wl.contains(users.name == '@ru2chmobi')):
    wl.insert({"name": "@ru2chmobi", "ID": "-1001098866708"})
if not (wl.contains(users.name == '@ru2chhw')):
    wl.insert({"name": "@ru2chhw", "ID": "-1001086103845"})
if not (wl.contains(users.name == '@mobitester')):
    wl.insert({"name": "@mobitester", "ID": "345258980"})

technoconf = -1001070076534
me = 94026383
TA = -1001109363260
token = '357359911:AAGhxPUJxVhUl8tNjz76MByQPYBPtwnfvR4'
bot = telebot.TeleBot(token)

dvachch = {
    '@Kylmakalle': 94026383,
    'test': -1001100823817

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
    return (string)



def legit(message):
    users = Query()
    if wl.search(users.ID.matches(str(message.chat.id))) or wl.search(users.ID.matches(str(message.from_user.id))):
        return 1
    else:
        #bot.send_message(message.chat.id, 'Contact @Kylmakalle first!')
        #if not (message.chat.type == 'private'):
            #bot.leave_chat(message.chat.id)
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
        # print(bl.all()[k]['ID'])
        # print(forwared)
        users = Query()
        # print(bl.search(users.ID.matches(forwared)))
        if bl.search(users.ID.matches(forwared)):
            uid = message.from_user
            # pprint(message)
            m = (jsonpickle.encode(message))
            message_dict = m
            event_name = 'Ban'
            botan.track(botan_token, uid, message_dict, event_name)
            bot.kick_chat_member(message.chat.id, message.from_user.id)
            try:    
                bot.send_message(message.chat.id,
                             '`' + message.from_user.first_name +'`' + ' (@' + message.from_user.username + ') ' + '*BANNED!*',
                             parse_mode='Markdown')
                bot.forward_message(me, message.chat.id, message.message_id)
                bot.send_message(me,
                             '`' + message.from_user.first_name +'`' + ' (@' + message.from_user.username + ') ' + 'id: #' + str(
                                 message.from_user.id) + ' *BANNED!*', parse_mode='Markdown')
            except:
              try:    
                bot.send_message(message.chat.id,
                             '`' + message.from_user.first_name +'`'  + ' *BANNED!*',
                             parse_mode='Markdown')
                bot.forward_message(me, message.chat.id, message.message_id)
                bot.send_message(me,
                             '`' + message.from_user.first_name +'`' + ' id: #' + str(
                                 message.from_user.id) + ' *BANNED!*', parse_mode='Markdown')
              except:
                return 0  

def cancel(message):
    if str(message.text) == '0':
        bot.reply_to(message, 'ОТМЕНА')
        return 0
    else:
        return 1


login = token[0:9]

botan_token = 'ImTjEtyVoiwO9eIgq6ytaxwBl:hg0QJ6'  # Token got from @botaniobot


@bot.message_handler(content_types=['text'])
def handle_text(message):
    #uid = message.from_user
    #print(message)
    #m = (jsonpickle.encode(message))
    #message_dict = m
    #event_name = 'msg'
    #botan.track(botan_token, uid, message_dict, event_name)
    #print('['+datetime.datetime.fromtimestamp(message.date).strftime('%Y-%m-%d %H:%M:%S') +'] ' +message.from_user.first_name +' ('+ str(message.from_user.id) + ') ' + ': ' + message.text)
    if legit(message):
        bl_check(message)
        if "Ассистент, тест" in message.text:
            th = 'https://2ch.hk/mobi/threads.json'
            board = requests.get(th).json()
            title = (board['threads'][1]['subject'])
            text = (board['threads'][1]['comment'])
            print(text)
            bot.send_message(me,str(title) + '\n'+ str(text) ,parse_mode='HTML')
        if message.chat.type == 'private':
            print('['+datetime.datetime.fromtimestamp(message.date).strftime('%Y-%m-%d %H:%M:%S') +'] ' +message.from_user.first_name +' ('+ str(message.from_user.id) + ') ' + ': ' + message.text)
            if message.text == '/help':
                bot.send_message(message.chat.id,
                                 'Доступные команды: \n /help - Вызов этого окна \n /addwl - Добавление чатов в *WHITELIST* \n /addbl - Добавление каналов в *BLACKLIST* \n /wl - Вывод *WHITELIST* \n /bl - Вывод *BLACKLIST*\n /announce @username _Твой текст_ - От имени бота пишет в чат @username сообщение \n \n Напиши `0` для отмены операции \n По проблемам и вопросам: @Kylmakalle',
                                 parse_mode='Markdown')
            if message.text == '/addwl':
                msg = bot.reply_to(message, 'Добавление в WHITELIST, введи @username')
                bot.register_next_step_handler(msg, WL_ADD)
            if message.text == '/addbl':
                msg = bot.reply_to(message, 'Добавление в BLACKLIST, форвардни сообщение из чата')
                bot.register_next_step_handler(msg, BL_INSERT)
            if message.text == '/wl':
                # print(clearoutput(str(wl.all())))
                bot.send_message(message.chat.id, clearoutput(str(wl.all())))
            if message.text == '/bl':
                bot.send_message(message.chat.id, clearoutput(str(bl.all())))
            if '/announce' in message.text:
               try:
                Uname = bot.get_chat(message.text.split(' ')[1]).id
                bot.send_message(Uname, message.text.split(' ', maxsplit=2)[2], parse_mode='Markdown')
                bot.reply_to(message, 'Отправлено!')
               except:
                bot.reply_to(message, 'Что-то неправильно, скорее всего чата не существует или я в него не добавлен, попробуй еще раз по аналогу:\n\n/announce @username _Твой текст_',parse_mode='Markdown')

def BL_INSERT(message):
    if cancel(message):
        if not (message.forward_from_chat == None):
            users = Query()
            if bl.search(users.ID.matches(str(message.forward_from_chat.id))):
                msg = bot.reply_to(message, "Такой есть уже, ещё разок!")
                bot.register_next_step_handler(msg, WL_ADD)
            else:
                key = '@' + message.forward_from_chat.username
                ident = str(message.forward_from_chat.id)
                bl.insert({'name': key, 'ID': ident})
                bl_reply = str(bl.search(users.name == key))
                bl_reply = clearoutput(bl_reply)
                bot.reply_to(message, 'Добавлено! ' + bl_reply)
                bot.send_message(me,
                                 '`' + message.from_user.first_name +'`' + ' (@' + message.from_user.username + ') ' + 'id: #' + str(
                                     message.from_user.id) + ' Добавил в BLACKLIST ' + bl_reply, parse_mode='Markdown')
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
                bot.send_message(me,
                                 '`' + message.from_user.first_name +'`' + ' (@' + message.from_user.username + ') ' + 'id: #' + str(
                                     message.from_user.id) + ' Добавил в WHITELIST ' + wl_reply, parse_mode='Markdown')
        except:
            msg = bot.reply_to(message, "Чата не существует, ещё разок!")
            bot.register_next_step_handler(msg, WL_ADD)


@bot.message_handler(content_types=['photo'])
def handle_photos(message):
    # print(message)
    if not (message.forward_from_chat == None):
        if not (message.chat.type == 'private'):
            bl_check(message)


bot.polling(none_stop=True, interval=0)