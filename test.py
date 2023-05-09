import hashlib
import sqlite3


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
def is_prime(n):
    """判断一个数是否是质数"""
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def 更新数据(页码,名字,话语):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("UPDATE User SET Name = ?, Words = ? WHERE PageCode = ?", (名字, 话语, 页码))
    conn.commit()
    conn.close()
primes = []
n = 2
while len(primes) < 100:
    if is_prime(n):
        primes.append(n)
    n += 1
for i in range(20, 100):
    s = f'{primes[i]}'
    codepage = hashlib.md5(s.encode()).hexdigest()
    ns = 读取数据(codepage)
    if( ns !='null_name'):
        print(ns)
        new = ns[2].replace('\r\n','@@@')
        更新数据(ns[0],ns[1],new)


