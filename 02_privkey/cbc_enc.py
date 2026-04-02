#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Lecture: Cryptography (秘密鍵暗号 モードオブオペレーション)
Topic: CBC (Cipher Block Chaining) Mode 
Description: 前の暗号ブロックをフィードバックすることで、統計的パターンを破壊する。
"""

import os
import hashlib

def block_encrypt(block, key):
    """16バイトのブロック暗号 (PRP) をシミュレート"""
    # 実習用として決定的な出力を得るためにハッシュを使用
    return hashlib.sha256(key + block).digest()[:16]

def block_decrypt(block, key):
    """
    注意: 実際のCBC復号にはブロック暗号の逆関数 (Fk^-1) が必要です。
    このシミュレータでは簡略化のため、暗号化の成否確認に留めます。
    """
    raise NotImplementedError("復号には逆関数(PRPの逆変換)の実装が必要です。")

def cbc_encrypt(plaintext_bytes, key):
    """CBCモードによる暗号化"""
    n = 16  # ブロックサイズ (128-bit)
    
    # 1. 初期ベクトル (IV) の生成
    iv = os.urandom(n)
    
    # パディング (PKCS#7風)
    pad_len = n - (len(plaintext_bytes) % n)
    padded_m = plaintext_bytes + bytes([pad_len] * pad_len)
    
    cipher_blocks = [iv]
    prev_cipher = iv
    
    # 2. ブロックごとに連鎖処理を実行
    for i in range(0, len(padded_m), n):
        m_i = padded_m[i:i+n]
        
        # 前の暗号ブロック(またはIV)とXORを取る 
        xored_m = bytes([a ^ b for a, b in zip(m_i, prev_cipher)])
        
        # 暗号化関数を通す
        c_i = block_encrypt(xored_m, key)
        cipher_blocks.append(c_i)
        prev_cipher = c_i
        
    return b"".join(cipher_blocks)

if __name__ == "__main__":
    secret_key = b"Hino_Campus_2026"
    # 前回のLab #07と同じ「一貫した」平文
    m = b"You love me but I hate you. You love me but I hate you."
    
    print(f"【実習：CBCモード ―― 運命の連鎖】")
    print(f"平文: {m.decode('ascii')}")
    
    # 暗号化
    c = cbc_encrypt(m, secret_key)
    
    print(f"IV: {c[:16].hex()}")
    print(f"暗号文: {c[16:].hex()}")
    
    # 考察: ECBと違い、同じ単語の繰り返しが異なる暗号文になっているか確認
    block1 = c[16:32]
    block2 = c[32:48]
    if block1 != block2:
        print("\n[Analysis]: 同じ平文ブロックの繰り返しが、異なる暗号文へと変換されました。")
        print("これが連鎖（Chaining）による統計的パターンの破壊です。")