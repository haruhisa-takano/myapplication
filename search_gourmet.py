"""
仕事検索サンプルプログラム
# python search_job_json.py 飛行機 研究 ・・・
"""

import sys  # 入出力
import urllib.request # URLアクセス
import requests
import urllib.parse # URL生成
import json    # JSON（APIの受け取り形式）
import os
import datetime
import insert_event
import pprint

from pytz import timezone

import pandas as pd

def RailAPI(station, pref):
    station_url =urllib.parse.quote(station)
    pref_url =urllib.parse.quote(pref)
    api='http://express.heartrails.com/api/json?method=getStations&name={station_name}&prefecture={pref_name}'
    url=api.format(station_name=station_url, pref_name=pref_url)
    response=requests.get(url)
    result_list = json.loads(response.text)['response']['station']
    lng=result_list[0]['x']
    lat=result_list[0]['y']
    return lat, lng

def HotpepperAPI(key2,range=3,count=20):
    # APIを通して、Webサービスを実行
    print(range)
    url = "http://webservice.recruit.co.jp/hotpepper/gourmet/v1/?{}".format(
        urllib.parse.urlencode(
            {"key"     : "1a84bdf9535ab439",                         # APIキー(このキーはダミー。自分で取得したものを記入。db*3+9)
             #"keyword" : keyword,   # 入力からクエリを生成
             "format"  : "json",                                    # レスポンス型式をJSONに指定
             "range"   : range, #これもWeb上で設定できるようになるといいな
             "lat"     : key2[0],
             "lng"     : key2[1],
             "count"   : count
            #  "parking" : parking
            #  "genre"   : genre
            #  "budget"  : budget
            }))

    f_url = urllib.request.urlopen(url).read()
    json_result = json.loads(f_url.decode("utf-8"))   # JSON形式の実行結果を格納
    jres = json_result['results']['shop']
    #pprint.pprint(jres)
    shop_datas=[]
    for shop_data in jres:
        shop_datas.append([shop_data["name"],shop_data["address"],shop_data["urls"]['pc'], shop_data['open'],shop_data['parking'], shop_data['photo']['pc']['l'], shop_data["lat"], shop_data['lng'], ])#'Hotpepper'])
    print(key2)
    #print(shop_datas)
    return shop_datas

    """
    api_key=""　#自身で取得したAPI keyを入力
    api = "http://webservice.recruit.co.jp/hotpepper/gourmet/v1/?" \
            "key={key}&lat={lat}&lng={lng}&free_drink=1&private_room=1&course=1range=2&count=100&order=1&format=json"
    url=api.format(key=api_key,lat=lat_st, lng=lng_st)
    response = requests.get(url)
    result_list = json.loads(response.text)['results']['shop']
    shop_datas=[]
    for shop_data in result_list:
        shop_datas.append([shop_data["name"],shop_data["address"],shop_data["urls"]['pc'], shop_data["budget"]['average'], 'Hotpepper'])
    return shop_datas
    """

def WeatherAPI(key3): #７日間指定にして時間帯を決定するようにしても良い
    print(key3[0],key3[1]) #DailyForecastは使えない説がある
    url = "http://api.openweathermap.org/data/2.5/forecast?{}".format(
        urllib.parse.urlencode(
            {"lat"     : key3[0],
             "lon"     : key3[1],
             "appid"     : "b480b4b4f37f3659e156652fdbe0ca95",                         # APIキー(このキーはダミー。自分で取得したものを記入。db*3+9)
             "units" : "metric",
             #"keyword" : keyword,   # 入力からクエリを生成
             "mode"  : "json",                                    # レスポンス型式をJSONに指定
             "lang"   : "ja", #これもWeb上で設定できるようになるといいな
            # "cnt"    : "16",
            #  "genre"   : genre
            #  "budget"  : budget
            }))
    print(url)
    f_url = urllib.request.urlopen(url).read()
    json_result = json.loads(f_url.decode("utf-8"))   # JSON形式の実行結果を格納
    jres = json_result['list']
    weather_datas=[]
    for i,item in enumerate(jres):
        # forecastDatetime = timezone( #https://qiita.com/marksard/items/472000594ca83b64f00c ここに5日間３時間ごとの天気予報のやり方も乗ってる
        #     'Asia/Tokyo').localize(datetime.datetime.fromtimestamp(item['dt']))
        forecastDatetime = datetime.datetime.fromtimestamp(item['dt'])
        forecastDatetime2 = forecastDatetime+datetime.timedelta(hours=3)
        forecastDatetime2 = forecastDatetime2.isoformat()
        forecastDatetime = forecastDatetime.isoformat()
        weatherDescription = item['weather'][0]['description']
        temperature = item['main']['temp']
        pop = float(item['pop'])*100
        humidity = item['main']['humidity']
        icon = item['weather'][0]['icon']
        rainfall = 0
        #if 'rain' in item: #and '3h' in item['rain']:
            #rainfall = item['rain']#['3h']
        tmp={'No.':i+1,
            '予定開始時刻':forecastDatetime, 
            '予定終了時刻':forecastDatetime2,
            '天気':weatherDescription, 
            '気温(℃)':temperature, 
            '降水確率(%)':pop, 
            '湿度(%)':humidity,
            '天気アイコン':icon
            }
        print(tmp)
        weather_datas.append(tmp)
        # print('日時:{0} 天気:{1} 気温(℃):{2} 降水確率(%):{3} 湿度(%):{4}'.format(
        #     forecastDatetime, weatherDescription, temperature, pop, humidity))
    """
    weather_datas=[]
    for weather_data in jres:
        weather_datas.append([weather_data["name"],weather_data["address"],weather_data["urls"]['pc'], weather_data["lat"], weather_data['lng'], ])#'Hotpepper'])
    print(key2)
    """
    #print(shop_datas)
    return weather_datas

def create_result_info(json_result):
#Webサービスからの出力を解析
    return "{}件のお仕事が見つかりました。最初の{}件を表示します。".format(
            json_result["results"]["results_available"], # ~件のお仕事が・・・
            json_result["results"]["results_returned"]   # 最初の~件を・・・
            )


def main():
    #駅情報取得API
    print("駅名，県名の順で入力してください")
    rail={}
    cin=input()
    rail['name']=cin.split()[0]
    rail['prefecture']=cin.split()[1]
    shres=RailAPI(rail['name'], rail['prefecture'])
    print(type(shres[0]))
    print(type(shres))
    
    #HotpepperAPI
    gourmet={}
    key2=[shres[0],shres[1]]
    print(key2)
    gourmet['place']=" ".join(map(str,key2))
    print("距離を指定してください") #この部分をweb上でどう実装できるか
    cin2=input()
    gourmet['range']=cin2[0] #標準入力は適宜受け付ける感じか(グルメサーチAPIの仕様から1~5で指定)
    #gourmet['budget']=cin[1] #余裕あれば
    #print(key2)
    #shres2=HotpepperAPI(key2,range=1)
    shres2=HotpepperAPI(key2,gourmet['range'])
    print(len(shres2))#初期値10で固定
    # 出力
    columns = ['name','address', 'url', '開店時間', '駐車場', '画像', '緯度', '経度']
    #print(shres2)
    HP_data =pd.DataFrame(shres2, columns=columns)
    """
    print(create_result_info(json_result))
    for index, work in enumerate(json_result["results"]["work"]): #enumerate → 何ループ目かがindexに格納される
        print(create_work_info(index+1,work))
    """
    print(HP_data.head(10)) #上から10個だっけな

    #weatherAPI
    print(shres2)
    print("!!")
    print("好みのレストラン・料亭の番号を一つ指定してください")
    num = int(input())
    key3=[shres2[num][6], shres2[num][7]]
    rest_name, rest_add = shres2[num][0], shres2[num][1]
    wead = WeatherAPI(key3)
    print(wead)
    print("希望の日程の番号を一つ指定してください")
    weanum = int(input())-1
    #sort_wead=sorted(wead, key=lambda x: x['降水確率(%)']) #https://note.nkmk.me/python-dict-list-sort/ 降水確率が最も低い時間帯
    #print(sort_wead)
    pick=wead[weanum]['予定開始時刻']
    pick2=wead[weanum]['予定終了時刻']
    print(pick)
    #HP_data.head() #?

    #CalendarAPI
    insert_event.main(rest_name,rest_add,pick,pick2)

    return 

if __name__ == "__main__":
    main()
