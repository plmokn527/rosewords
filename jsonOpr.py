import sqlite3
import os
def 插入单条数据(名字,想说的话):
    # 打开数据库
    conn = sqlite3.connect('test.db')

    # 获取该数据库的游标
    cursor = conn.cursor()

    # 执行单条数据插入，并返回操作行数

    sql = "INSERT INTO User (Name, Words) VALUES (?, ?)"
    batchInsert = cursor.executemany(sql, [(名字, 想说的话)])
    # 关闭Cursor:
    cursor.close()

    # 提交事务:
    conn.commit()

    # 关闭Connection:
    conn.close()


def 新建数据库():
    if os.path.exists('test.db'):
        return
    # 若无该数据库，则创建Sqlite数据库并打开
    # 若有，则直接打开数据库
    conn = sqlite3.connect('test.db')
    # 获取该数据库的游标
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE User (ID INTEGER Primary KEY,Name TEXT, Words TEXT)')



    # 执行一条SQL语句，创建user表:


    # 关闭Cursor:
    cursor.close()

    # 提交事务:
    conn.commit()

    # 关闭Connection:
    conn.close()

def 读取数据(名字):
    # 打开数据库
    conn = sqlite3.connect('test.db')

    # 获取该数据库的游标
    cursor = conn.cursor()

    # 获取全部记录
    cursor.execute("SELECT * FROM User")
    allData = cursor.fetchall()
    print("直接获取全部记录：")
    for item in allData:
        print(item)

    # 获取前N条记录
    cursor.execute("SELECT * FROM User")
    manyData = cursor.fetchmany(2)
    print("获取部分结果：")
    for item in manyData:
        print(item)

    # 一次读取一条结果，循环获取所有记录
    cursor.execute("SELECT * FROM User")
    print("一次读取一条结果，循环获取所有记录：")
    while True:
        singleData = cursor.fetchone()
        if singleData is None:
            break
        if 名字 == singleData[1]:
            return singleData[2]
    return 'null'

    # 关闭Cursor:
    cursor.close()

    # 提交事务:
    conn.commit()

    # 关闭Connection:
    conn.close()
def 删除数据():
    pass

新建数据库()
插入单条数据("但是","橡树后的")
print(读取数据("d但是"))