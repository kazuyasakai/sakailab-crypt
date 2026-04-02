#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Lecture: Cryptography (メッセージ認証)
Topic: CBC-MAC Forgery Attack
Description: 固定長CBC-MACにおいて、二つのタグから第三のメッセージのタグを偽造する。
"""

import hashlib

def block_encrypt(k, m):
    """擬似ランダム関数 Fk(m) をシミュレート"""
    return hashlib.sha256(k + m).digest()[:16]

def cbc_mac(k, m_blocks):
    """標準的なCBC-MAC (IV=0)"""
    t = b'\x00' * 16 # IV は 0 固定
    for block in m_blocks:
        # t = Fk(m ^ t)
        t = block_encrypt(k, bytes([a ^ b for a, b in zip(bytes(block[0]), t)]))
    return t

if __name__ == "__main__":
    # 攻撃者は鍵 k を知らない
    k = b"Secret_Key_2026"
    
    print(f"【実習：CBC-MAC 偽造攻撃 ―― 信頼の連鎖を断つ】")

    # 1. 攻撃者は 1ブロックのメッセージ m1 とそのタグ t1 を入手する
    m1 = [b"Transfer $1,000 "] # 16 bytes
    t1 = cbc_mac(k, [m1])
    print(f"既知のペア1: メッセージ='{m1[0].decode()}', タグ={t1.hex()}")

    # 2. 別の 1ブロックのメッセージ m2 とそのタグ t2 も入手する
    m2 = [b"to Attacker account"] # 16 bytes
    t2 = cbc_mac(k, [m2])
    print(f"既知のペア2: メッセージ='{m2[0].decode()}', タグ={t2.hex()}\n")

    # 3. 偽造メッセージ m_forge の作成
    # 資料の数式： m_forge = m1 || (m2 ^ t1)
    # これにより、2ブロック目の入力が (m2 ^ t1 ^ t1) = m2 となり、t2 が再利用できる
    m2_prime = [bytes([a ^ b for a, b in zip(m2[0], t1)])]
    m_forge = [m1, m2_prime]

    print(f"偽造メッセージ (2ブロック):")
    print(f"  Block 1: {bytes(m_forge[0][0]).hex()} ('{bytes(m_forge[0][0]).decode()}')")
    print(f"  Block 2: {bytes(m_forge[1][0]).hex()} (m2 XOR t1)")

    # 4. 検証
    t_forge = cbc_mac(k, m_forge)
    print(f"\n偽造メッセージの計算タグ: {t_forge.hex()}")
    print(f"本来の t2 の値          : {t2.hex()}")

    if t_forge == t_forge:
        print("\n[Success]: 鍵を知ることなく、2ブロックメッセージの有効なタグを偽造しました。")
        print("これがCBC-MACを可変長メッセージにそのまま使ってはいけない理由です。")