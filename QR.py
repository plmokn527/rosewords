import hashlib

import qrcode
import os
def is_prime(n):
    """判断一个数是否是质数"""
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

# 生成二维码图片的目录
OUTPUT_DIR = './qrcodes/'

# 如果输出目录不存在，则创建它
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

primes = []
n = 2
while len(primes) < 100:
    if is_prime(n):
        primes.append(n)
    n += 1
for i in range(20, 100):
    s = f'{primes[i]}'
    codepage = hashlib.md5(s.encode()).hexdigest()
    url='http://47.120.42.84:5000/rose_words/'+codepage
    img = qrcode.make(url)
    filename = f'编号{codepage}.png'
    img.save(os.path.join(OUTPUT_DIR, filename))
    print(f'QR code saved to {os.path.join(OUTPUT_DIR, filename)}')
