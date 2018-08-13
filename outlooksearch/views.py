from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from outlooksearch.authhelper import get_signin_url
from outlooksearch.outlookservice import get_me
from outlooksearch.authhelper import get_signin_url, get_token_from_code, get_access_token
from outlooksearch.outlookservice import get_me, get_my_messages
import time
import re
import json
from collections import OrderedDict
import pprint
from outlooksearch import markovLearn
# Create your views here.

def home(request):
  redirect_uri = request.build_absolute_uri(reverse('outlooksearch:gettoken'))
  sign_in_url = get_signin_url(redirect_uri)
  return HttpResponse('<a href="' + sign_in_url +'">Click here to sign in and view your mail</a>')

def gettoken(request):
  auth_code = request.GET['code']
  redirect_uri = request.build_absolute_uri(reverse('outlooksearch:gettoken'))
  token = get_token_from_code(auth_code, redirect_uri)
  access_token = token['access_token']
  user = get_me(access_token)
  refresh_token = token['refresh_token']
  expires_in = token['expires_in']

  # expires_in is in seconds
  # Get current timestamp (seconds since Unix Epoch) and
  # add expires_in to get expiration time
  # Subtract 5 minutes to allow for clock differences
  expiration = int(time.time()) + expires_in - 300

  # Save the token in the session
  request.session['access_token'] = access_token
  request.session['refresh_token'] = refresh_token
  request.session['token_expires'] = expiration
  return HttpResponseRedirect(reverse('outlooksearch:mail'))

def mail(request):
  access_token = get_access_token(request, request.build_absolute_uri(reverse('outlooksearch:gettoken')))
  # If there is no token in the session, redirect to home
  if not access_token:
    return HttpResponseRedirect(reverse('outlooksearch:home'))
  else:
    messages = get_my_messages(access_token)
    # for message in messages:
    #     pprint.pprint(messages)
    values=messages["value"]
    list = []
    for value in values:
        nippoBody = value["body"]["content"]
        if "所感" in nippoBody and "明日も" in nippoBody:
            start = nippoBody.index("所感")
            end = nippoBody.index("明日も")
            slice = nippoBody[start+3:end]
            pureText = cleanhtml(slice)
            textList = pureText.split("。")
            for text in textList:
                if text:
                    list.append(text + "。")
    f = open('test.text', 'w') # ファイルを開く(該当ファイルがなければ新規作成)
    for text in list:
         f.write(text)
    f.close()

    nippoAuto = "本日は"+ markovLearn.markov()
    # path_w = 'texts/test_w.txt'
    # with open(path_w, mode="w") as f:
    #     for text in list:
    #         f.write(text)
    params = {"str": nippoAuto}
    return render(request, "mail.html", params)

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  clean = re.compile('\r.*?\n')
  cleantext = re.sub(cleanr, '', raw_html)
  cleantextAfter = re.sub(clean, '', cleantext)
  return cleantextAfter