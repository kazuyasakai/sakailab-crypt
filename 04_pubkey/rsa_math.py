#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Topic: RSA Mathematical Foundations
Description: 拡張ユークリッド法、逆元計算、および平方乗算法の実装。
"""

def extended_gcd(a, b):
    """
    拡張ユークリッド法
    ax + by = gcd(a, b) を満たす (gcd, x, y) を返す
    """
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = extended_gcd(b % a, a)
        return gcd, y - (b // a) * x, x

def mod_inverse(e, phi):
    """
    モジュロ逆元の計算
    ed ≡ 1 (mod phi) となる秘密鍵 d を求める
    """
    gcd, x, y = extended_gcd(e, phi)
    if gcd != 1:
        raise ValueError("Modular inverse does not exist (gcd != 1)")
    else:
        # 結果が負の場合は phi を足して正の範囲にする [cite: 2304]
        return x % phi

def square_and_multiply(x, c, n):
    """
    平方乗算法
    x^c mod n を効率的に計算する
    """
    z = 1
    # 指数 c を 2進数文字列に変換 (最上位ビットから順に処理) [cite: 2321]
    binary_c = bin(c)[2:]
    
    for bit in binary_c:
        # 常に自乗を行う (Square) [cite: 2326]
        z = (z * z) % n
        # ビットが 1 の場合のみ x を掛ける (Multiply) [cite: 2331]
        if bit == '1':
            z = (z * x) % n
            
    return z

if __name__ == "__main__":
    print("--- Test 1: Extended GCD ---")
    # 例題: gcd(299, 221) = 13 = 3*299 - 4*221
    g, x, y = extended_gcd(299, 221)
    print(f"gcd(299, 221) = {g}, x = {x}, y = {y}")

    print("\n--- Test 2: Modular Inverse ---")
    # 例題: 15^-1 mod 47 = 22
    inv = mod_inverse(15, 47)
    print(f"15^-1 mod 47 = {inv}")

    print("\n--- Test 3: Square and Multiply ---")
    # 例題: 11^5 mod 37 = 27
    res = square_and_multiply(11, 5, 37)
    print(f"11^5 mod 37 = {res}")