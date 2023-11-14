# main.py
import setup
import keygen
import hash
import check
import sign
import verify

def main():
    # セキュリティパラメータを設定
    𝜆 = 128  # セキュリティパラメータとして 128 を仮定
    print("𝜆:", 𝜆)

    # セットアップ: システムパラメータを設定
    print("システムパラメータの設定")
    system_params = setup.setup_security_parameters(𝜆)
    print("システムパラメータ:", system_params)
    
    # 鍵生成: カメレオン署名の鍵ペアを生成
    print("カメレオン署名の鍵ペアの生成")
    private_key, public_key = keygen.key_generation(system_params)
    print("公開鍵 (p_k):", public_key)
    print("秘密鍵 (s_k):", private_key)

    # メッセージの設定
    message = "Hello, world!"
    
    # カメレオンハッシュの生成
    print("カメレオンハッシュの生成")
    chameleon_hash, chameleon_check_param = hash.chameleon_hash_generation(public_key, message, system_params)
    print("カメレオンハッシュ (h):", chameleon_hash)
    print("検証パラメータ (R):", chameleon_check_param)
    
    # カメレオンハッシュの検査
    print("カメレオンハッシュの検査")
    b = check.chameleon_hash_check(public_key, chameleon_hash, message, chameleon_check_param, system_params)
    print("検証結果 (b):", b)
    
    if b == 1:
        print("カメレオンハッシュは有効です。")
        
        # カメレオン署名の生成
        print("カメレオン署名の生成")
        chameleon_signature = sign.chameleon_sign(private_key, chameleon_hash, message, system_params)
        print("カメレオン署名パラメータ R' (署名):", chameleon_signature)
        
        # メッセージを変更
        message_prime = "Hello, OpenAI!"
        chameleon_hash_prime, chameleon_check_param_prime = hash.chameleon_hash_generation(public_key, message_prime, system_params)
        
        # カメレオン署名の検証
        print("カメレオン署名の検証")
        verification_result = verify.chameleon_verify(public_key, chameleon_hash, message, chameleon_signature, message_prime, chameleon_check_param_prime, system_params)
        print("検証結果 (b):", verification_result)

        if verification_result == 1:
            print("カメレオン署名は有効です。")
        else:
            print("カメレオン署名は無効です。")
    else:
        print("カメレオンハッシュは無効です。")

if __name__ == "__main__":
    main()
