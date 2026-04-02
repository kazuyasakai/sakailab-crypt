#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Lecture: Cryptography (古典暗号論)
Topic: Row Permutation Cipher (列転置暗号)
Description: 文字の順序を入れ替え、意味を「攪拌」する。
"""

import math

def encrypt(plaintext, key):
    """
    列転置暗号による暗号化。
    平文を行列に書き込み、鍵（列の読み出し順）に従って再構成する。
    """
    # 空白をアンダーバーに置換
    text = plaintext.replace(" ", "_").upper()
    key_len = len(key)
    row_count = math.ceil(len(text) / key_len)
    
    # 行列の作成（足りない部分は 'X' でパディング）
    padded_text = text.ljust(row_count * key_len, 'X')
    matrix = [padded_text[i:i+key_len] for i in range(0, len(padded_text), key_len)]
    
    # 鍵（列番号のリスト）に従って列を読み出す
    ciphertext = ""
    for k in key:
        col_idx = int(k) - 1
        for row in matrix:
            ciphertext += row[col_idx]
        ciphertext += " " # 視認性のために列ごとに区切る
        
    return ciphertext.strip()

def decrypt(ciphertext, key):
    """
    列転置暗号の復号。
    """
    key_len = len(key)
    chars = ciphertext.replace(" ", "")
    row_count = len(chars) // key_len
    
    matrix = [['' for _ in range(key_len)] for _ in range(row_count)]
    
    current_char_idx = 0
    for k in key:
        col_idx = int(k) - 1
        for row_idx in range(row_count):
            matrix[row_idx][col_idx] = chars[current_char_idx]
            current_char_idx += 1
            
    return "".join(["".join(row) for row in matrix])

if __name__ == "__main__":
    # 平文
    m = "The attack postponed until tomorrow"
    # 鍵：3521476 (スライド 45枚目の例)
    k = "3521476"
    
    print("【実習：列転置暗号 ―― 構造の攪拌】")
    print(f"平文 (m): {m}")
    print(f"鍵 (k):   {k}")
    
    c = encrypt(m, k)
    print(f"暗号 (c): {c}")
    print(f"復号:     {decrypt(c, k)}")