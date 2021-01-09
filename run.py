from flask import Flask, render_template, request, session, redirect
import search_gourmet
import insert_event

app = Flask(__name__)
app.secret_key = b'random string...'

name_list = {}
rail_data =[]
shres = ()
shres2 = {}
wead = {}

select = int()
num = int()
select_lat = int()
select_lng = int()
check = int()
select_shop = str()
select_add = str()
open_time = str()
start_t = str()
end_t = str()

@app.route('/', methods=['GET'])
def index():
    global name_list
    global rail_data
    global select
    global num

    title ="ようこそアプリケーションページへ"
    msg1 = """
    <strong>概要</strong><br>
    ・急に旅行行きたい<br>
    ・ご飯もその辺りの美味しいものが食べたい<br>
    ・でも天気はどうなんだろう<br>
    ・これいっぺんに確認してカレンダーに登録したい<br>
    上記の要望を一度に全部叶えてくれるのがこのアプリケーションページです．
    """
    msg2 = """
    <strong>使い方</strong><br>
    1.旅行の目的地付近の駅名と都道府県名，その駅からの距離を1~5の番号(1:300m,2:500m,3:1000m,4:2000m,5:3000m)で入力してください．何件表示するかも1~100で指定してください<br>
    2.1に該当するレストラン，料亭を表示します．どれか一つを選択してください．<br>
    3.選択した料亭・レストランの今日から５日間の3時間ごとの天気情報を表示します．表示の時間帯のうちどれか一つを選択してください．<br>
    4.選択した時間帯を自動でGoogleカレンダーに登録します．
    """
    print(select)
    print("?")
    return render_template('step1.html', \
                title=title, \
                message=msg1,\
                message2=msg2,\
                name = name_list,\
                #user_id = user_id,\
                #flag = flag,\
                select = select,\
                num = num,\
                data = rail_data) 

@app.route('/st1', methods=['POST'])
def step1():
    global select
    global num
    global shres
    global shres2
    st_name = request.form.get('st_name')
    pref_name = request.form.get('pref_name')
    num = int(request.form.get('number'))
    select = int(request.form.get('selected'))
    title ="ようこそアプリケーションページへ"

    
    rail_data.append((st_name,pref_name))
    try:
        shres=search_gourmet.RailAPI(st_name, pref_name)
    except (KeyError,IndexError) as e:
        return render_template('/exept.html',\
                title = title,\
                select = select,\
                num = num,\
                data = rail_data)
    shres2=search_gourmet.HotpepperAPI(shres,select,num)

    return redirect('/step2')

"""
    print(num)
    print(type(num))
    print("!!")
    print(select)
 #ここでif-elseの分岐によって該当の店が存在しなかった場合のreturn先を分岐してもいいかも
"""

@app.route('/step2', methods=['GET'])
def index2():
    global name_list

    title ="ようこそアプリケーションページへ"
    msg1 = """
    <strong>概要</strong><br>
    ・急に旅行行きたい<br>
    ・ご飯もその辺りの美味しいものが食べたい<br>
    ・でも天気はどうなんだろう<br>
    ・これいっぺんに確認してカレンダーに登録したい<br>
    上記の要望を一度に全部叶えてくれるのがこのアプリケーションページです．
    """
    msg2 = """
    <strong>使い方</strong><br>
    1.旅行の目的地付近の駅名と都道府県名，その駅からの距離を1~5の番号(1:300m,2:500m,3:1000m,4:2000m,5:3000m)で入力してください．何件表示するかも1~100で指定してください<br>
    2.1に該当するレストラン，料亭を表示します．どれか一つを選択してください．<br>
    3.選択した料亭・レストランの今日から５日間の3時間ごとの天気情報を表示します．表示の時間帯のうちどれか一つを選択してください．<br>
    4.選択した時間帯を自動でGoogleカレンダーに登録します．
    """
    print(shres2)
    print("≥≥/")
    return render_template('step2.html', \
                title=title, \
                message=msg1,\
                message2=msg2,\
                select =select,\
                num = num,\
                name = name_list,\
                data = rail_data,\
                shop = shres2)

@app.route('/step1', methods=['POST'])
def step2():
    #global select
    #global num
    global shres
    global shres2
    global select_lat
    global select_lng
    global select_shop
    global open_time
    global wead
    global check

    check = int(request.form.get('check'))
    
    select_shop = shres2[check][0]
    open_time = shres2[check][3]
    select_lat = shres2[check][6]
    select_lng = shres2[check][7]

    wead = search_gourmet.WeatherAPI([select_lat,select_lng])

    print(check)
    print(type(check))
    print("!!!")
    print(select_lat,select_lng)

    return redirect('/step3')

#3段階目表示
@app.route('/step3', methods=['GET'])
def index3():
    global name_list

    title ="ようこそアプリケーションページへ"
    msg1 = """
    <strong>概要</strong><br>
    ・急に旅行行きたい<br>
    ・ご飯もその辺りの美味しいものが食べたい<br>
    ・でも天気はどうなんだろう<br>
    ・これいっぺんに確認してカレンダーに登録したい<br>
    上記の要望を一度に全部叶えてくれるのがこのアプリケーションページです．
    """
    msg2 = """
    <strong>使い方</strong><br>
    1.旅行の目的地付近の駅名と都道府県名，その駅からの距離を1~5の番号(1:300m,2:500m,3:1000m,4:2000m,5:3000m)で入力してください．何件表示するかも1~100で指定してください<br>
    2.1に該当するレストラン，料亭を表示します．どれか一つを選択してください．<br>
    3.選択した料亭・レストランの今日から５日間の3時間ごとの天気情報を表示します．表示の時間帯のうちどれか一つを選択してください．<br>
    4.選択した時間帯を自動でGoogleカレンダーに登録します．
    """
    print(shres2)
    print("≥/")
    return render_template('step3.html', \
                title=title, \
                message=msg1,\
                message2=msg2,\
                select =select,\
                num = num,\
                name = name_list,\
                data = rail_data,\
                wead = wead,\
                select_shop = select_shop,\
                open_time = open_time,\
                select_lat = select_lat,\
                select_lng = select_lng,\
                shop = shres2)

@app.route('/finish', methods=['POST'])
def step3():
    #global select
    #global num
    #global shres
    #global shres2
    global select_lat
    global select_lng
    #global select_shop
    global open_time
    global wead
    global select_add
    global start_t
    global end_t

    select_time = int(request.form.get('time_num'))
    print(select_time)
    select_add = shres2[check][1]
    start_t = wead[select_time]['予定開始時刻']
    end_t = wead[select_time]['予定終了時刻']

    insert_event.main(select_shop, select_add, start_t, end_t)
    
    print(check)
    print(type(check))
    print("!!!")
    print(select_lat,select_lng)

    return redirect('/step4')

#最終段階表示
@app.route('/step4', methods=['GET'])
def index4():
    global name_list

    title ="ようこそアプリケーションページへ"
    
    print(shres2)
    print("≥/")
    return render_template('step4.html', \
                title=title, \
                select =select,\
                num = num,\
                name = name_list,\
                data = rail_data,\
                wead = wead,\
                select_shop = select_shop,\
                open_time = open_time,\
                select_lat = select_lat,\
                select_lng = select_lng,\
                start_t = start_t,\
                end_t = end_t, \
                shop = shres2)

@app.route('/',methods=['POST'])
def backtop():
    global rail_data 
    global shres 
    global shres2 
    global wead 

    global select 
    global num 
    global select_lat  
    global select_lng 
    global check 
    global select_shop 
    global select_add 
    global open_time 
    global start_t 
    global end_t 

    rail_data =[]
    shres = ()
    shres2 = {}
    wead = {}

    select = int()
    num = int()
    select_lat = int()
    select_lng = int()
    check = int()
    select_shop = str()
    select_add = str()
    open_time = str()
    start_t = str()
    end_t = str()

    return redirect('/')

@app.route('/',methods=['GET'])
def exept():
    global rail_data 
    global shres 
    global select 
    global num 

    rail_data =[]
    shres = ()
    select = int()
    num = int()

    return redirect('/')

if __name__ == '__main__':
   app.run(debug=True)
   # app.run()