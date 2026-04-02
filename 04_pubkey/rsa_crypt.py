#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Topic: RSA Cryptosystem Implementation
Description: 鍵生成、暗号化、復号のフルサイクル・シミュレーション。
"""

from rsa_math import mod_inverse, square_and_multiply

def rsa_key_gen(p, q, e):
    """
    RSA鍵生成 
    p, q: 素数, e: 公開指数
    """
    # 1. N = p * q [cite: 1757]
    n = p * q
    # 2. φ(N) = (p-1)(q-1) [cite: 1679, 1768]
    phi = (p - 1) * (q - 1)
    
    # 3. 秘密鍵 d の計算 (ed ≡ 1 mod φ(N)) [cite: 1760]
    try:
        d = mod_inverse(e, phi)
    except ValueError:
        raise ValueError(f"e={e} は φ(N)={phi} と互いに素ではありません。別の e を選んでください。")
        
    return (e, n), (d, n), phi

def rsa_encrypt(m, public_key):
    """暗号化: c = m^e mod N """
    e, n = public_key
    return square_and_multiply(m, e, n)

def rsa_decrypt(c, private_key):
    """復号: m = c^d mod N """
    d, n = private_key
    return square_and_multiply(c, d, n)

if __name__ == "__main__":
    print("【実習：RSA暗号システムの全体実装】\n")

    # 講義資料 24ページの例題パラメータ
    p, q = 3, 5
    e = 3
    m = 7
    
    print(f"1. パラメータ設定:")
    print(f"   p = {p}, q = {q}, 平文 m = {m}")
    
    # 鍵生成
    pub_key, priv_key, phi = rsa_key_gen(p, q, e)
    
    print(f"\n2. 鍵生成結果:")
    print(f"   N = {pub_key[1]}, φ(N) = {phi}")
    print(f"   公開鍵 (e, N): {pub_key}")
    print(f"   秘密鍵 (d, N): {priv_key}")

    # 暗号化
    c = rsa_encrypt(m, pub_key)
    print(f"\n3. 暗号化実行:")
    print(f"   c = {m}^{pub_key} mod {pub_key[1]} = {c}")

    # 復号
    m_dec = rsa_decrypt(c, priv_key)
    print(f"\n4. 復号実行:")
    print(f"   m = {c}^{priv_key} mod {priv_key[1]} = {m_dec}")

    if m == m_dec:
        print("\n[Success]: 暗号化と復号のサイクルが正しく完了しました。")