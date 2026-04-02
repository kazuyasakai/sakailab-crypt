#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Topic: IV Collision Attack in CTR Mode
Description: 同じIVを使用することで、平文のXORが露出する脆弱性を実証する。
"""

import hashlib

def keyed_function(k, x):
    """擬似ランダム関数 (PRF) [cite: 1254-1262]"""
    return hashlib.sha256(k + x).digest()[:16]

def ctr_encrypt_fixed_iv(m_bytes, key, iv):
    """
    検証用の固定IV版CTR暗号化。
    c = m ^ Fk(iv || counter) [cite: 1840-1845]
    """
    n = 16
    # 簡略化のため最初の1ブロック(counter=0)のみ処理
    counter_block = iv + (0).to_bytes(4, byteorder='big')
    keystream = keyed_function(key, counter_block)
    
    # c = m ^ keystream
    return bytes([a ^ b for a, b in zip(m_bytes, keystream)])

if __name__ == "__main__":
    secret_key = b"Hino_Campus_2026"
    # 本来はランダムに変えるべきIVを、誤って再利用してしまうシナリオ
    reused_iv = b"SAME_IV_1234" 

    # 1. ターゲットの暗号文 (攻撃者が傍受したもの)
    # 平文 m1: "SecretMessageA" (14 bytes)
    m1 = b"SecretMessageA"
    c1 = ctr_encrypt_fixed_iv(m1, secret_key, reused_iv)
    
    # 2. 攻撃者がオラクルに投げた自分の平文とその暗号文
    # 攻撃者は自分の平文 m2: "I_am_an_attacker" (16 bytes) に対する暗号文 c2 を得る
    m2 = b"I_am_an_attacker"
    c2 = ctr_encrypt_fixed_iv(m2, secret_key, reused_iv)

    print(f"【実験】IV衝突攻撃 (CTRモードの崩壊)")
    print(f"平文ブロックm1: {m1.decode()}")
    print(f"平文ブロックm2: {m2.decode()}")
    print(f"再利用されたIV: {reused_iv.decode()}\n")

    # 3. 攻撃の実行 
    # c1 ^ c2 = (m1 ^ key) ^ (m2 ^ key) = m1 ^ m2
    # したがって、 m1 = c1 ^ c2 ^ m2 となり、鍵を知らなくても平文が漏洩する
    
    diff_c = bytes([a ^ b for a, b in zip(c1, c2)])
    recovered_m1 = bytes([a ^ b for a, b in zip(diff_c, m2)])

    print(f"傍受した暗号文c1: {c1.hex()}")
    print(f"攻撃者の暗号文c2: {c2.hex()}")
    print(f"復元された平文m1: {recovered_m1[:len(m1)].decode('ascii')}")

    if recovered_m1[:len(m1)] == m1:
        print("\n[Critical]: 鍵を一切使わずにターゲットの平文を解読しました。")
        print("原因: IVの再利用により鍵ストリームが相殺されたため。")