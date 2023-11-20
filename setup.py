# setup.py
import hashlib
import random
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend
from sympy import randprime
from Crypto.Util.number import getPrime

def mod_exp(base, exponent, modulus):
    result = 1
    base = base % modulus

    while exponent > 0:
        # exponent の最下位ビットが 1 のとき、result を更新
        if exponent % 2 == 1:
            result = (result * base) % modulus

        # base を二乗し、exponent を右に1ビットシフト
        base = (base * base) % modulus
        exponent = exponent // 2

    return result

def setup_security_parameters(𝜆):
    # セキュリティパラメータ 𝜆 を受け取ります

    #テストメッセージ
    M = "test"

    # 素数次数 q を計算 (q >= 2**𝜆 λビット以上)
    q = calculate_prime_order(𝜆)

    # G の乗法的循環群を生成
    G = generate_cyclic_group(q)

    # # 生成元 𝑔 を選択
    # 𝑔 = select_generator(G, q)

    # 双線形写像 𝑒ˆ を定義
    G𝑇 = define_bilinear_map(G)

    # グローバルアンチコリジョンハッシュ関数 𝐻G を選択
    𝐻G = select_anti_collision_hash(M, G, q)

    # システムパラメータを辞書として返す
    system_params = {
        'G': G,
        'G𝑇': G𝑇,
        # '𝑔': 𝑔,
        '𝑞': q,
        '𝐻G': 𝐻G,
        'M' : M
    }

    return system_params

def calculate_prime_order(bit_length, num_parts=64):
    # 各部分のビット数を計算
    part_bit_length = max(bit_length // num_parts, 1)

    # 最終的な素数を部分素数から構築
    q = 1
    for _ in range(num_parts):
        part_prime = getPrime(part_bit_length * 2)
        q *= part_prime

    q_bit = int(q.bit_length())  # 素数 q のビット数を確認
    print("素数 q のビット数:", q_bit)
    print("生成された素数q:", q)

    return q

# def select_generator(G, q):
#     # 生成元を選択するロジック
#     group = set()
#     current = G % q
#     group.add(1)  # 単位元 (identity element)

#     for i in range(1, q):
#         group.add(current)
#         current = (current * G) % q

#     return group

def prime_factors(n):
    factors = []
    p = 2
    while p * p <= n:
        if n % p == 0:
            factors.append(p)
            while n % p == 0:
                n //= p
        p += 1
    if n > 1:
        factors.append(n)
    return factors

def generate_cyclic_group(q):
    for candidate_g in range(2, q):
        if mod_exp(candidate_g, q - 1, q) == 1:
            if mod_exp(candidate_g, (q - 1) // 2, q) != 1:  # q - 1の素因数が2のときには生成元
                return candidate_g
    return None

def define_bilinear_map(G):
    # 楕円曲線上の点とスカラー値のペアを使用して双線形写像を構築
    bilinear_map = pow(G, G, G)

    return bilinear_map


def select_anti_collision_hash(M, G, q):
    # アンチコリジョンハッシュ関数を選択するロジック
    # ハッシュ関数 (SHA-256) を初期化
    sha256_hash = hashlib.sha256()

    # 入力文字列をハッシュ関数に追加
    sha256_hash.update(M.encode('utf-8'))

    # ハッシュ値を16進数文字列として取得
    hash_hex = sha256_hash.hexdigest()

    # ハッシュ値を整数に変換
    hash_int = int(hash_hex, 16)

    # G の要素にマッピング
    mapped_element = pow(G, hash_int, q)

    return mapped_element


