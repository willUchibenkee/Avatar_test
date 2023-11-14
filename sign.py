#sign.py
import hashlib

def chameleon_sign(private_key, chameleon_hash, message_prime, system_params):
    # 入力: private_key (s_k), chameleon_triple (h, M, R), message_prime (M')
    x = private_key  # x は秘密鍵, q は関連付けられた素数次数
    q = system_params['𝑞']
    h = chameleon_hash  # h はカメレオンハッシュ
    m_prime = hash_G(message_prime)  # メッセージ M' をハッシュして m' を生成

    # カメレオン署名パラメータ R' を計算
    R_prime = pow((h * pow(m_prime, -1, q)), x, q)  # (h/m')^x mod q

    return R_prime

def hash_G(message):
    # メッセージを SHA-256 ハッシュして整数 m に変換
    sha256_hash = hashlib.sha256()
    sha256_hash.update(message.encode('utf-8'))
    hash_hex = sha256_hash.hexdigest()
    m = int(hash_hex, 16)
    return m

