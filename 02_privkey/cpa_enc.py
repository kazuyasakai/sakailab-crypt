#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import hashlib

"""
Topic: CPA-Secure Encryption using PRF
Description: 資料 30枚目の構造 c = <r, Fk(r) ^ m> を実装。
"""

def keyed_function(k, x):
    """資料 22枚目の鍵付き関数 Fk(x) の例"""
    # 簡易的なPRFとしてHMAC風の構造を利用
    return hashlib.sha256(k + x).digest()[:len(x)]

def cpa_encrypt(m_bytes, k_bytes):
    # 1. 乱数 r を生成 [cite: 1192, 1346]
    r = os.urandom(len(k_bytes))
    
    # 2. パッド Fk(r) を計算 [cite: 1177, 1355]
    pad = keyed_function(k_bytes, r)
    
    # 3. XOR 演算 [cite: 1178, 1357]
    s = bytes([a ^ b for a, b in zip(m_bytes, pad)])
    
    # 暗号文 <r, s> を出力 [cite: 1193, 1347]
    return r, s

if __name__ == "__main__":
    key = os.urandom(16)
    plaintext = b"I love you but I hate you"
    
    print(f"【実験】CPAセキュアな暗号化（確率的アルゴリズム）")
    print(f"平文: {plaintext}")
    
    # 同じメッセージを2回暗号化
    r1, s1 = cpa_encrypt(plaintext, key)
    r2, s2 = cpa_encrypt(plaintext, key)
    
    print(f"1回目暗号文: <r:{r1.hex()}, s:{s1.hex()}>")
    print(f"2回目暗号文: <r:{r2.hex()}, s:{s2.hex()}>")
    
    # 異なる暗号文になることを確認 [cite: 1110]
    if s1 != s2:
        print("\n結果: 暗号文が異なります。")
        print("これにより、決定的な暗号の弱点（複数暗号文識別不可能性の欠如）を克服している。")