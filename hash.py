# hash.py
import random
import hashlib

def chameleon_hash_generation(public_key, message, system_params):
    # 入力: public_key (p_k) と message (M)
    y = public_key  # y は公開鍵, q は関連付けられた素数次数
    q = system_params['𝑞']
    G = system_params['G']
    m = hash_G(message)  # メッセージをハッシュして m を生成
    r_R = random.randint(1, q - 1)  # 1から q-1 の範囲でランダムな r_R を選択

    # カメレオンハッシュを計算
    h = (m * pow(y, r_R, q)) % q

    # 対応する検証パラメータ R を計算
    R = pow(G, r_R, q)  # g^r_R mod q

    return h, R

def hash_G(message):
    # メッセージを SHA-256 ハッシュして整数 m に変換
    sha256_hash = hashlib.sha256()
    sha256_hash.update(message.encode('utf-8'))
    hash_hex = sha256_hash.hexdigest()
    m = int(hash_hex, 16)
    return m