# -*- coding: utf-8 -*-

import webapp2
import os
import yaml
import time
import jinja2
import datetime

from apiclient.discovery import build
from oauth2client.appengine import OAuth2Decorator
from dateutil import parser
from itertools import *

# jinja2
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

# api.yamlから読み取り
api_key = yaml.safe_load(open('api.yaml').read().decode('utf-8'))

decorator = OAuth2Decorator(
        client_id=api_key['client_id'],
        client_secret=api_key['client_secret'],
        scope='https://www.googleapis.com/auth/calendar',
        )

# オブジェクトを生成。build() は JSON のサービス定義ファイルからメソッドを構築するためのもの。
service = build('calendar', 'v3')

# add start
DEFAULT_GUESTBOOK_NAME = 'default_guestbook'


class CalendarCalHandler(webapp2.RequestHandler):

    @decorator.oauth_required
    def get(self):

        # Ajaxリクエストの処理
        if self.request.get('fmt') == 'json':

            timeMax = '2014-03-31T23:59:59+09:00'
            timeMin = '2013-04-01T00:00:00+09:00'

            allgokei = 0

            count = 0
            data = "{"

            # calendarへのrequest情報作成
            page_token = None
            while True:
                request = service.events().list(
                    calendarId = 'primary',
                    timeMax = timeMax,
                    timeMin = timeMin,
                    singleEvents = True,
                    orderBy = 'startTime',
                    pageToken=page_token)
                http = decorator.http()
                events = request.execute(http=http)

                tobe = 0
                gokei = 0

                # calendarのeventから値取得
                for event in events['items']:

                    # 開始日抽出
                    try:
                        dts = parser.parse(event['start']['dateTime'])
                    except:
                        dts = datetime.datetime(9999, 12, 31, 13)

                    # 終了日抽出
                    # AsIsに、ToBeに代入
                    asis = tobe
                    try:
                        dte = parser.parse(event['end']['dateTime'])
                        enddate = str(dte.strftime('%Y-%m-%d'))
                    except:
                        dte = datetime.datetime(9999, 12, 31, 13)
                        enddate = '9999-12-31'
                    # 取得した日付をToBeに代入
                    tobe = enddate

                    # 作業時間（終了時刻-開始時刻）を算出。start
                    dtes = dte - dts
                    # 文字列に変換。コロンを削除するため。
                    strdtes = str(dtes)
                    strlstripdtes = strdtes.replace(":","")

                    try:
                        workinghours = int(strlstripdtes) / 10000
                    except:
                        workinghours = 0

                    # unixtime取得
                    # 日付→文字列取得
                    year = dte.strftime('%Y')
                    month = dte.strftime('%m')
                    day = dte.strftime('%d')

                    # 文字列→数値型変換。mktime methodでint型が必要のため。
                    intyear = int(year)
                    intmonth = int(month)
                    intday = int(day)

                    # unixtimeに変換
                    unixtime = time.mktime([intyear, intmonth, intday, 0, 0, 0, 0, 0, 0])

                    allgokei = allgokei + workinghours

                    if asis == tobe:
                        gokei = gokei + workinghours
                    else:
                        gokei = 0
                        gokei = gokei + workinghours

                    # jsonデータ作成
                    count = count + 1
                    if count == 1:
                        data = data + '"' + str(unixtime) + '"' + ":" + str(gokei)
                    else:
                        data = data + ',"' + str(unixtime) + '"' + ":" + str(gokei)

                page_token = events.get('nextPageToken')
                if not page_token:
                    data = data + "}"
                    break

            # responseのデータ形式をjson形式にする
            self.response.out.headers['Content-Type'] = 'text/json'

            self.response.out.write(data)

            return


        # Ajaxリクエストの処理
        elif self.request.get('fmt') == 'jsonsum':

            timeMax = '2014-03-31T23:59:59+09:00'
            timeMin = '2013-04-01T00:00:00+09:00'

            allgokei = 0

            count = 0
            data = "{"

            # calendarへのrequest情報作成
            page_token = None
            while True:
                request = service.events().list(
                    calendarId = 'primary',
                    timeMax = timeMax,
                    timeMin = timeMin,
                    singleEvents = True,
                    orderBy = 'startTime',
                    pageToken=page_token)
                http = decorator.http()
                events = request.execute(http=http)

                tobe = 0
                gokei = 0

                # calendarのeventから値取得
                for event in events['items']:

                    # 開始日抽出
                    try:
                        dts = parser.parse(event['start']['dateTime'])
                    except:
                        dts = datetime.datetime(9999, 12, 31, 13)

                    # 終了日抽出
                    # AsIsに、ToBeに代入
                    asis = tobe
                    try:
                        dte = parser.parse(event['end']['dateTime'])
                        enddate = str(dte.strftime('%Y-%m-%d'))
                    except:
                        dte = datetime.datetime(9999, 12, 31, 13)
                        enddate = '9999-12-31'
                    # 取得した日付をToBeに代入
                    tobe = enddate

                    # 作業時間（終了時刻-開始時刻）を算出。start
                    dtes = dte - dts
                    # 文字列に変換。コロンを削除するため。
                    strdtes = str(dtes)
                    strlstripdtes = strdtes.replace(":","")

                    try:
                        workinghours = int(strlstripdtes) / 10000
                    except:
                        workinghours = 0

                    # unixtime取得
                    # 日付→文字列取得
                    year = dte.strftime('%Y')
                    month = dte.strftime('%m')
                    day = dte.strftime('%d')

                    # 文字列→数値型変換。mktime methodでint型が必要のため。
                    intyear = int(year)
                    intmonth = int(month)
                    intday = int(day)

                    # unixtimeに変換
                    unixtime = time.mktime([intyear, intmonth, intday, 0, 0, 0, 0, 0, 0])

                    allgokei = allgokei + workinghours

                    if asis == tobe:
                        gokei = gokei + workinghours
                    else:
                        gokei = 0
                        gokei = gokei + workinghours

                data02 = "{" + '"' + 'allgokei' + '"' + ":" + str(allgokei) + "}" 

                page_token = events.get('nextPageToken')
                if not page_token:
                    break

            # responseのデータ形式をjson形式にする
            self.response.out.headers['Content-Type'] = 'text/json'

            # 上記で作成したjson形式でそのままresponse
            self.response.out.write(data02)

            return
        
        else:
            # Calendar操作権限付与
            page_token = None
            request = service.events().list(
                calendarId = 'primary',
                timeMax = '2014-04-01T23:59:59+09:00',
                timeMin = '2014-04-01T23:59:58+09:00',
                maxResults = 1,
                pageToken=page_token)
            http = decorator.http()
            events = request.execute(http=http)

            # Rendering
            template_values = {
            }
            template = JINJA_ENVIRONMENT.get_template('cal.html')
            self.response.write(template.render(template_values))

debug = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')

app = webapp2.WSGIApplication([
                               ('/cal', CalendarCalHandler),
                               (decorator.callback_path, decorator.callback_handler()),
                              ],
                              debug=debug)
