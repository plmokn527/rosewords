import hashlib
from flask import Flask, render_template, redirect, url_for, request, jsonify
import sqlite3
import os
import pandas as pd
app = Flask(__name__)
def 新建数据库():
    if os.path.exists('data.db'):
        return False
    # 若无该数据库，则创建Sqlite数据库并打开
    # 若有，则直接打开数据库
    conn = sqlite3.connect('data.db')
    # 获取该数据库的游标
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE User (PageCode TEXT,Name TEXT, Words TEXT)')
    print("数据库新建成功！")
    # 执行一条SQL语句，创建user表:
    # 关闭Cursor:
    cursor.close()
    # 提交事务:
    conn.commit()
    # 关闭Connection:
    conn.close()
    return True
def 更新数据(页码,名字,话语):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("UPDATE User SET Name = ?, Words = ? WHERE PageCode = ?", (名字, 话语, 页码))
    conn.commit()
    conn.close()
def 读取数据(页码):
    # 打开数据库
    conn = sqlite3.connect('data.db')
    # 获取该数据库的游标
    cursor = conn.cursor()
    # 一次读取一条结果，循环获取所有记录
    cursor.execute("SELECT * FROM User")
    #print("一次读取一条结果，循环获取所有记录：")
    while True:
        singleData = cursor.fetchone()
        if singleData is None:
            break
        if 页码 == singleData[0]:
            if(singleData[1]!='null' and singleData[2]!='null'):
                # 关闭Cursor:
                cursor.close()
                # 提交事务:
                conn.commit()
                # 关闭Connection:
                conn.close()
                return (singleData[0],singleData[1],singleData[2])
            # 关闭Cursor:
            cursor.close()
            # 提交事务:
            conn.commit()
            # 关闭Connection:
            conn.close()
            return 'null_name'
    # 关闭Cursor:
    cursor.close()
    # 提交事务:
    conn.commit()
    # 关闭Connection:
    conn.close()
    return 'null_page'

def 删除数据():
    pass
def 插入单条数据(页码,名字,想说的话):
    if(读取数据(页码)=='null_name'):
        return "页面已经存在！"
    # 打开数据库
    conn = sqlite3.connect('data.db')

    # 获取该数据库的游标
    cursor = conn.cursor()

    # 执行单条数据插入，并返回操作行数

    sql = "INSERT INTO User (PageCode,Name, Words) VALUES (?, ?, ?)"
    batchInsert = cursor.executemany(sql, [(页码, 名字, 想说的话)])
    # 关闭Cursor:
    cursor.close()

    # 提交事务:
    conn.commit()

    # 关闭Connection:
    conn.close()
    return  "插入数据成功！"
@app.route("/rose_words/<pageCode>")
def index1(pageCode):
    if(pageCode == "gonglve"):
        return render_template('gonglve.html')
    get = 读取数据(pageCode)
    编号 = pageCode[-5:]
    if(get=="null_page"):
        return '抱歉，不存在该数据！'
    elif(get=="null_name"):
        return render_template('send.html', myPageCode=pageCode,id=编号)
    #return f'hello,{get[1]},我想对你说:{get[2]}'
    return render_template('login.html',name = get[1],pagecode = pageCode,words=get[2],id=编号)

def 获取图片链接数据(地名):
    ###获取数据
    数据 = pd.read_excel(f'{地名}.xlsx')
    图片的链接 = []
    图片的描述 = []
    dat = []
    for myUrl in 数据['图片的链接']:
        图片的链接.append(myUrl)
    for myDescribe in 数据['图片的描述']:
        图片的描述.append(myDescribe)
    dat.append(图片的链接)
    dat.append(图片的描述)
    return dat

@app.route("/places/<placename>")
def jiangtangongyuan(placename):
    获取图片链接数据(placename)
    if os.path.exists(f'{placename}.xlsx') == False:
        return "抱歉，数据库未建立！"
    dat = 获取图片链接数据(placename)
    return render_template("placesPics.html",picDat = dat , placeName = placename)
@app.route('/rose_words/success',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      name = request.form['recipient']
      pageCode = request.form['pagecode']
      words = request.form['message']
      words = words.replace('\r\n', '@@@')
      read_res = 读取数据(pageCode)
      if(read_res=='null_name'):
          更新数据(pageCode, name, words)
          return render_template('login.html',name = name,pagecode = pageCode,words=words)
      elif(read_res=='null'):
          return "数据不存在！"
      return "请不要重复提交表单"

   else:
      name = request.args.get('Name')
      pageCode = request.args.get('referring_page')
      words = request.args.get('Words')
      words = words.replace('\r\n', '@@@')
      read_res = 读取数据(pageCode)
      if(read_res=='null_name'):
          更新数据(pageCode, name, words)
          return render_template('login.html',name = name,pagecode = pageCode,words=words)
      elif(read_res=='null'):
          return "数据不存在！"
      return "请不要重复提交表单"

def is_prime(n):
    """判断一个数是否是质数"""
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

if __name__ == '__main__':
    if(新建数据库()):
        primes = []
        n = 2
        while len(primes) < 100:
            if is_prime(n):
                primes.append(n)
            n += 1
        for i in range(20,100):
            s = f'{primes[i]}'
            codepage = hashlib.md5(s.encode()).hexdigest()
            插入单条数据(codepage, 'null', 'null')
    app.run(host='0.0.0.0')


# ('d2ddea18f00665ce8623e36bd4e3c7c5', 'null', 'null')
# ('d1fe173d08e959397adf34b1d77e88d7', 'null', 'null')
# ('fe9fc289c3ff0af142b6d3bead98a923', 'null', 'null')
# ('7647966b7343c29048673252e490f736', 'null', 'null')
# ('e2ef524fbf3d9fe611d5a8e90fefdc9c', 'null', 'null')
# ('38b3eff8baf56627478ec76a704e9b52', 'null', 'null')
# ('6974ce5ac660610b44d9b9fed0ff9548', 'null', 'null')
# ('a97da629b098b75c294dffdc3e463904', 'null', 'null')
# ('2723d092b63885e0d7c260cc007e8b9d', 'null', 'null')
# ('73278a4a86960eeb576a8fd4c9ec6997', 'null', 'null')
# ('ec5decca5ed3d6b8079e2e7e7bacc9f2', 'null', 'null')
# ('1afa34a7f984eeabdbb0a7d494132ee5', 'null', 'null')
# ('3988c7f88ebcb58c6ce932b957b6f332', 'null', 'null')
# ('e00da03b685a0dd18fb6a08af0923de0', 'null', 'null')
# ('f2217062e9a397a1dca429e7d70bc6ca', 'null', 'null')
# ('a8f15eda80c50adb0e71943adc8015cf', 'null', 'null')
# ('6c4b761a28b734fe93831e3fb400ce87', 'null', 'null')
# ('0777d5c17d4066b82ab86dff8a46af6f', 'null', 'null')
# ('5878a7ab84fb43402106c575658472fa', 'null', 'null')
# ('f7e6c85504ce6e82442c770f7c8606f0', 'null', 'null')
# ('8f53295a73878494e9bc8dd6c3c7104f', 'null', 'null')
# ('fc221309746013ac554571fbd180e1c8', 'null', 'null')
# ('0aa1883c6411f7873cb83dacb17b0afc', 'null', 'null')
# ('bd686fd640be98efaae0091fa301e613', 'null', 'null')
# ('85d8ce590ad8981ca2c8286f79f59954', 'null', 'null')
# ('84d9ee44e457ddef7f2c4f25dc8fa865', 'null', 'null')
# ('eb163727917cbba1eea208541a643e74', 'null', 'null')
# ('115f89503138416a242f40fb7d7f338e', 'null', 'null')
# ('705f2172834666788607efbfca35afb3', 'null', 'null')
# ('57aeee35c98205091e18d1140e9f38cf', 'null', 'null')
# ('e165421110ba03099a1c0393373c5b43', 'null', 'null')
# ('555d6702c950ecb729a966504af0a635', 'null', 'null')
# ('f340f1b1f65b6df5b5e3f94d95b11daf', 'null', 'null')
# ('19f3cd308f1455b3fa09a282e0d496f4', 'null', 'null')
# ('d96409bf894217686ba124d7356686c9', 'null', 'null')
# ('8c19f571e251e61cb8dd3612f26d5ecf', 'null', 'null')
# ('06138bc5af6023646ede0e1f7c1eac75', 'null', 'null')
# ('7f100b7b36092fb9b06dfb4fac360931', 'null', 'null')
# ('20f07591c6fcb220ffe637cda29bb3f6', 'null', 'null')
# ('e3796ae838835da0b6f6ea37bcf8bcb7', 'null', 'null')
# ('0f49c89d1e7298bb9930789c8ed59d48', 'null', 'null')
# ('53c3bce66e43be4f209556518c2fcb54', 'null', 'null')
# ('8e98d81f8217304975ccb23337bb5761', 'null', 'null')
# ('9dfcd5e558dfa04aaf37f137a1d9d3e5', 'null', 'null')
# ('158f3069a435b314a80bdcb024f8e422', 'null', 'null')
# ('5b8add2a5d98b1a652ea7fd72d942dac', 'null', 'null')
# ('6da37dd3139aa4d9aa55b8d237ec5d4a', 'null', 'null')
# ('357a6fdf7642bf815a88822c447d9dc4', 'null', 'null')
# ('c5ff2543b53f4cc0ad3819a36752467b', 'null', 'null')
# ('0bb4aec1710521c12ee76289d9440817', 'null', 'null')
# ('138bb0696595b338afbab333c555292a', 'null', 'null')
# ('c058f544c737782deacefa532d9add4c', 'null', 'null')
# ('05049e90fa4f5039a8cadc6acbb4b2cc', 'null', 'null')
# ('ffd52f3c7e12435a724a8f30fddadd9c', 'null', 'null')
# ('a02ffd91ece5e7efeb46db8f10a74059', 'null', 'null')
# ('beed13602b9b0e6ecb5b568ff5058f07', 'null', 'null')
# ('c86a7ee3d8ef0b551ed58e354a836f2b', 'null', 'null')
# ('e46de7e1bcaaced9a54f1e9d0d2f800d', 'null', 'null')
# ('816b112c6105b3ebd537828a39af4818', 'null', 'null')
# ('a96b65a721e561e1e3de768ac819ffbb', 'null', 'null')
# ('7eacb532570ff6858afd2723755ff790', 'null', 'null')
# ('e0c641195b27425bb056ac56f8953d24', 'null', 'null')
# ('66368270ffd51418ec58bd793f2d9b1b', 'null', 'null')
# ('019d385eb67632a7e958e23f24bd07d7', 'null', 'null')
# ('eed5af6add95a9a6f1252739b1ad8c24', 'null', 'null')
# ('13f3cf8c531952d72e5847c4183e6910', 'null', 'null')
# ('d61e4bbd6393c9111e6526ea173a7c8b', 'null', 'null')
# ('42998cf32d552343bc8e460416382dca', 'null', 'null')
# ('0353ab4cbed5beae847a7ff6e220b5cf', 'null', 'null')
# ('428fca9bc1921c25c5121f9da7815cde', 'null', 'null')
# ('ab817c9349cf9c4f6877e1894a1faa00', 'null', 'null')
# ('d18f655c3fce66ca401d5f38b48c89af', 'null', 'null')
# ('a516a87cfcaef229b342c437fe2b95f7', 'null', 'null')
# ('559cb990c9dffd8675f6bc2186971dc2', 'null', 'null')
# ('3cf166c6b73f030b4f67eeaeba301103', 'null', 'null')
# ('285e19f20beded7d215102b49d5c09a0', 'null', 'null')
# ('e2230b853516e7b05d79744fbd4c9c13', 'null', 'null')
# ('07563a3fe3bbe7e3ba84431ad9d055af', 'null', 'null')
# ('2bb232c0b13c774965ef8558f0fbd615', 'null', 'null')
# ('16c222aa19898e5058938167c8ab6c57', 'null', 'null')


