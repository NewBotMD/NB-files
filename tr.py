from utlis.rank import setrank,isrank,remrank,remsudos,setsudo, GPranks,IDrank
from utlis.send import send_msg, BYusers, GetLink,Name,Glang
from utlis.locks import st,getOR
from utlis.tg import Bot
from config import *

from pyrogram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
import threading, requests, time, random, re, json
import importlib

from pyrogram.api.types import InputPeerChat
def updateMsgs(client, message,redis):
  type = message.chat.type
  userID = message.from_user.id
  chatID = message.chat.id
  rank = isrank(redis,userID,chatID)
  text = message.text
  title = message.chat.title
  userFN = message.from_user.first_name
  type = message.chat.type

  if text and text == "نقل البيانات" and rank == "sudo":
    if redis.smembers(BOT_ID+"Tshake:Chek:Groups"):
      Ngp = redis.scard(BOT_ID+"Tshake:Chek:Groups")
      Bot("sendMessage",{"chat_id":chatID,"text":"تم ايجاد ({}) مجموعات خاصه بسورس تشاكي سيتم نقلها الى (<a href=\"http://t.me/nbbot\">NewBot</a>)\nقد يستغرق بعض الوقت".format(Ngp),"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True})
    else:
      Bot("sendMessage",{"chat_id":chatID,"text":"عذراً لا توجد بيانات خاصه بسورس تشاكي","reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True})
      return False

    groups = redis.smembers(BOT_ID+"Tshake:Chek:Groups")
    for gp in groups:
      redis.sadd("{}Nbot:groups".format(BOT_ID),gp)
      ads =redis.smembers(BOT_ID+'Tshake:Mod:User'+gp)
      ows =redis.smembers(BOT_ID+'Tshake:Manager'+gp)
      vps =redis.smembers(BOT_ID+'Tshake:Special:User'+gp)
      cr = Bot("getChatAdministrators",{"chat_id":gp})
      for c in cr['result']:
        userId = c["user"]["id"]
        if c['status'] == "creator":
          setrank(redis,"creator",userId,gp,"one")
          break
      for ad in ads:
        if ad != BOT_ID:
          redis.sadd("{}Nbot:{}:{}".format(BOT_ID,gp,"admin"),ad)

      for ow in ows:
        if ow != BOT_ID:
          redis.sadd("{}Nbot:{}:{}".format(BOT_ID,gp,"owner"),ow)

      for vp in vps:
        if vp != BOT_ID:
          redis.sadd("{}Nbot:{}:{}".format(BOT_ID,gp,"vip"),vp)

      if redis.get(BOT_ID+"Tshake:Lock:tagservr"+gp):
        redis.sadd("{}Nbot:Ltag".format(BOT_ID),gp)
      if redis.get(BOT_ID+"Tshake:Lock:edit"+gp):
        redis.sadd("{}Nbot:Ledits".format(BOT_ID),gp)
      if redis.hget(BOT_ID+"Tshake:flooding:settings:"+gp,"flood"):
        redis.sadd("{}Nbot:Lflood".format(BOT_ID),gp)
      if redis.get(BOT_ID+"Tshake:Lock:Animation"+gp):
        redis.sadd("{}Nbot:Lgifs".format(BOT_ID),gp)
      if redis.get(BOT_ID+"Tshake:Lock:Document"+gp):
        redis.sadd("{}Nbot:Lfiles".format(BOT_ID),gp)
      if redis.get(BOT_ID+"Tshake:Lock:Markdaun"+gp):
        redis.sadd("{}Nbot:Lmarkdown".format(BOT_ID),gp)
      if redis.get(BOT_ID+"Tshake:Lock:Photo"+gp):
        redis.sadd("{}Nbot:Lphoto".format(BOT_ID),gp)
      if redis.get(BOT_ID+"Tshake:Lock:Sticker"+gp):
        redis.sadd("{}Nbot:Lsticker".format(BOT_ID),gp)
      if redis.get(BOT_ID+"Tshake:Lock:Video"+gp):
        redis.sadd("{}Nbot:Lvideo".format(BOT_ID),gp)
      if redis.get(BOT_ID+"Tshake:Lock:Audio"+gp):
        redis.sadd("{}Nbot:Lmusic".format(BOT_ID),gp)
      if redis.get(BOT_ID+"Tshake:Lock:vico"+gp):
        redis.sadd("{}Nbot:Lvoice".format(BOT_ID),gp)
      if redis.get(BOT_ID+"Tshake:Lock:Contact"+gp):
        redis.sadd("{}Nbot:Lcontact".format(BOT_ID),gp)
      if redis.get(BOT_ID+"Tshake:Lock:forward"+gp):
        redis.sadd("{}Nbot:Lfwd".format(BOT_ID),gp)
      if redis.get(BOT_ID+"Tshake:Lock:Link"+gp):
        redis.sadd("{}Nbot:Llink".format(BOT_ID),gp)
      if redis.get(BOT_ID+"Tshake:Lock:User:Name"+gp):
        redis.sadd("{}Nbot:Lusername".format(BOT_ID),gp)

    Bot("sendMessage",{"chat_id":chatID,"text":"تم نقل البيانات من سورس تشاكي الى (<a href=\"http://t.me/nbbot\">NewBot</a>)","reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True})
