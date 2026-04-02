#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Topic: Digital Signature (Hash-then-Sign) 
Description: ハッシュ値に対して秘密鍵で署名し、公開鍵で真正性を検証する。
"""

import hashlib
from rsa_math import square_and_multiply
from rsa_crypt import rsa_key_gen

def hash_message(message):
    """メッセージをハッシュ化して整数に変換"""
    h_hex = hashlib.sha256(message).hexdigest()
    return int(h_hex, 16)

def sign_message(message, priv_key):
    """
    署名生成: sigma = H(m)^d mod N
    """
    d, n = priv_key
    # Hash-then-Sign: まずハッシュを取る
    m_hash = hash_message(message) % n
    # 秘密鍵 d でべき乗計算
    return square_and_multiply(m_hash, d, n)

def verify_signature(message, sigma, pub_key):
    """
    検証: H(m) == sigma^e mod N
    """
    e, n = pub_key
    m_hash = hash_message(message) % n
    # 公開鍵 e で復元
    recovered_hash = square_and_multiply(sigma, e, n)
    return m_hash == recovered_hash

if __name__ == "__main__":
    print("【実習：デジタル署名 ―― 改ざん不能な意志の証明】\n")

    # 1. 鍵生成 (少し大きめの素数を使用)
    p, q = 61, 53
    e = 65537
    pub_key, priv_key, _ = rsa_key_gen(p, q, e)
    
    print(f"1. 署名者の鍵ペア生成:")
    print(f"   公開鍵 (e, N): {pub_key}")
    print(f"   秘密鍵 (d, N): (秘密)")

    # 2. 署名の作成
    original_msg = b"I love you, but security first."
    signature = sign_message(original_msg, priv_key)
    
    print(f"\n2. 署名生成:")
    print(f"   メッセージ: {original_msg.decode()}")
    print(f"   署名 (sigma): {hex(signature)}")

    # 3. 第三者による検証
    print(f"\n3. 検証プロセス:")
    is_valid = verify_signature(original_msg, signature, pub_key)
    print(f"   検証結果: {'✅ 正当な署名' if is_valid else '❌ 不正な署名'}")

    # 4. 改ざんのシミュレーション
    tampered_msg = b"I love money, but security first."
    print(f"\n4. 改ざん試行:")
    print(f"   書き換えられたメッセージ: {tampered_msg.decode()}")
    is_valid_tampered = verify_signature(tampered_msg, signature, pub_key)
    print(f"   検証結果: {'✅ 正当な署名' if is_valid_tampered else '❌ 警告：改ざん検知！'}")