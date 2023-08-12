import pandas as pd
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

d = 获取图片链接数据("江滩公园")
print(d[0][])
