# keygen.py
import random
from math import gcd

def key_generation(Parm):
    # システムパラメータ Parm を受け取ります

    # 整数 q をランダムに選択（Zq の要素となります）
    q = Parm['𝑞']  # システムパラメータを q として仮定
    x_R = random.randint(1, q - 1)  # 1から q-1 の範囲でランダムに選択

    while gcd(x_R, q) != 1:
        x_R = random.randint(1, q - 1)

    # 秘密鍵 s_k は x_R です
    s_k = x_R

    # 公開鍵 p_k を計算
    x_inverse = pow(x_R, -1, q)  # x_R の逆数を計算
    y = pow(Parm['G'], x_inverse, q)  # 関数 g を使用して公開鍵 y を計算

    # 公開鍵と秘密鍵のペアを返します
    return s_k, y 

