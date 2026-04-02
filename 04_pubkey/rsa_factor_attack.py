#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Topic: RSA Factorization Attack
Description: 公開鍵 N を素因数分解し、秘密鍵 d を不正に復元する。
"""

from rsa_math import extended_gcd, mod_inverse

def factorize_n(n):
    """単純な試し割り法による素因数分解"""
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return i, n // i
    return None

def find_appropriate_e(phi):
    """φ(N) と互いに素な最小の e を探す """
    for e in range(3, phi, 2):
        g, _, _ = extended_gcd(e, phi)
        if g == 1:
            return e
    return None

if __name__ == "__main__":
    # ユーザーが指定した新しいパラメータ
    p, q = 31, 41
    n = p * q
    phi = (p - 1) * (q - 1)
    
    # 適切な e を選択
    e = find_appropriate_e(phi)

    print(f"【実習：RSA因数分解攻撃 ―― 崩れ去る迷宮】")
    print(f"ターゲットの公開鍵: (e={e}, N={n})")

    # 1. 因数分解の実行 [cite: 1780-1781]
    print(f"\n1. N を素因数分解中...")
    factors = factorize_n(n)
    
    if factors:
        p, q = factors
        print(f"   成功！ 発見された素数: p = {p}, q = {q}")
        
        # 2. φ(N) の算出 [cite: 1679, 1752]
        phi = (p - 1) * (q - 1)
        print(f"2. φ(N) = (p-1)(q-1) = {phi} を特定")
        
        # 3. 秘密鍵 d の復元 [cite: 1760]
        stolen_d = mod_inverse(e, phi)
        print(f"3. 秘密鍵 d = e^-1 mod φ(N) = {stolen_d} を奪取")
        
        print(f"\n[Result]: 鍵をゲット。秘密鍵は ({stolen_d}, {n}) です。")
        print("原因: 運命の因数分解が、今、始まったため。")