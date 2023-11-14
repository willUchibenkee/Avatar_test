# check.py
import hashlib

def chameleon_hash_check(public_key, chameleon_hash, message, R, system_params):
    # 入力: public_key (p_k), chameleon_hash (h), message (M), R (検証パラメータ), system_params
    y= public_key  # y は公開鍵, q は関連付けられた素数次数
    q = system_params['𝑞']
    m = hash_G(message)  # メッセージをハッシュして m を生成

    # 双線形写像 G𝑇 を取得
    G𝑇 = system_params['G𝑇']

    # (y, h, m, R) が互換性があるかどうかを確認
    compatibility = (e_hat(G𝑇, chameleon_hash, m, q) == e_hat(G𝑇, R, y, q))

    # 互換性がある場合は b = 1、そうでない場合は b = 0
    b = 1 if compatibility else 0

    return b

def hash_G(message):
    # メッセージを SHA-256 ハッシュして整数 m に変換
    sha256_hash = hashlib.sha256()
    sha256_hash.update(message.encode('utf-8'))
    hash_hex = sha256_hash.hexdigest()
    m = int(hash_hex, 16)
    return m

def e_hat(G𝑇, x, y, q):
    # 双線形写像 e_hat を計算
    return pow(G𝑇, x * y, q)
