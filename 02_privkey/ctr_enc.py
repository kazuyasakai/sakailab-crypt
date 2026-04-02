#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Lecture: Cryptography (秘密鍵暗号 モードオブオペレーション)
Topic: CTR (Counter) Mode
Description: カウンタを用いて並列性とランダムアクセス性を実現する。
"""

import os
import hashlib

def keyed_function(k, x):
    """擬似ランダム関数 (PRF) をシミュレート"""
    return hashlib.sha256(k + x).digest()[:16]

def ctr_process(data_bytes, key, iv):
    """
    CTR モードによる暗号化/復号化
    XORの性質上、この関数一つで暗号化と復号化の両方が可能。
    """
    n = 16  # ブロックサイズ (128-bit)
    result = bytearray()
    
    # ブロックごとにカウンタをインクリメントして処理
    for i in range((len(data_bytes) + n - 1) // n):
        # 1. カウンタ値の生成 (IV || i)
        # 資料に基づき、IVにカウンタを結合（または加算）してPRFの入力とする
        counter_block = iv + i.to_bytes(4, byteorder='big')
        # PRFの入力サイズを調整（実習用）
        ctr_input = hashlib.md5(counter_block).digest()
        
        # 2. パッド（鍵ストリーム）の生成: Fk(CTR)
        keystream_block = keyed_function(key, ctr_input)
        
        # 3. 平文ブロックと XOR
        start = i * n
        end = min(start + n, len(data_bytes))
        for j in range(start, end):
            result.append(data_bytes[j] ^ keystream_block[j - start])
            
    return bytes(result)

if __name__ == "__main__":
    secret_key = b"Hino_Campus_2026"
    # カウンタの重複を避けるための 12バイト nonce
    nonce = os.urandom(12) 
    
    # 平文: 愛憎が入り混じる一貫したメッセージ
    m = b"You love me but I hate you. You love me but I hate you."
    
    print(f"【実習：CTRモード ―― 並列なる運命】")
    print(f"平文: {m.decode('ascii')}")
    
    # 1. 暗号化
    ciphertext = ctr_process(m, secret_key, nonce)
    print(f"暗号文 (HEX): {ciphertext.hex()}")
    
    # 2. 復号化（同じ関数、同じIV、同じ鍵を使用）
    decrypted = ctr_process(ciphertext, secret_key, nonce)
    print(f"復号文: {decrypted.decode('ascii')}")
    
    # 考察: ブロックごとの独立性を確認
    c_block1 = ciphertext[0:16]
    c_block2 = ciphertext[16:32]
    if c_block1 != c_block2:
        print("\n[Analysis]: CBC同様、同じ平文の繰り返しが異なる暗号文になりました。")
        print("これはカウンタ(CTR, CTR+1...)が毎回異なる入力をPRFに与えるためです。")