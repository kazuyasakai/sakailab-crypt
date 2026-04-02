#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Lecture: Cryptography (古典暗号論)
Topic: Mono-alphabetic Substitution
Description: a-z の対応表（秘密鍵）を完全可視化。
"""

import random
import string

def generate_key():
    """
    ランダムな置換表（秘密鍵）を作成。
    """
    letters = list(string.ascii_lowercase)
    shuffled = letters[:]
    random.shuffle(shuffled)
    return dict(zip(letters, shuffled))

def print_key_table(key):
    """
    秘密鍵（置換表）を a-z の順で美しく表示する。
    """
    print("\n--- [秘密鍵: アルファベット置換表] ---")
    print("平文: ", " ".join(string.ascii_lowercase))
    print("      " + " ".join(["|" for _ in range(26)]))
    
    # 鍵をソートして暗号文字を並べる
    cipher_chars = [key[c] for c in string.ascii_lowercase]
    print("暗号: ", " ".join(cipher_chars))
    print("-" * 60)

def encrypt(plaintext, key):
    res = ""
    for char in plaintext.lower():
        if char in key:
            res += key[char]
        else:
            res += char
    return res

def decrypt(ciphertext, key):
    reverse_key = {v: k for k, v in key.items()}
    return encrypt(ciphertext, reverse_key)

if __name__ == "__main__":
    # 秘密鍵の生成
    my_key = generate_key()
    
    # ターゲットメッセージ
    m = "It is hard to define what is sexual harassment but I know it when I see it."
    
    # 実行
    print("【実習：単一換字暗号の可視化】")
    print_key_table(my_key)
    
    c = encrypt(m, my_key)
    print(f"平文: {m}")
    print(f"暗号: {c}")
    print(f"復号: {decrypt(c, my_key)}")