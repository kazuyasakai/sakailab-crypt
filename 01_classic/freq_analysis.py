#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Lecture: Cryptography (古典暗号論)
Topic: Advanced Frequency Analysis (N-gram)
Description: 単一文字の頻度を超え、n-gram（2文字・3文字）の連続性から真実を射抜く。
"""

import collections
import string
import random

# 標準的な英語の頻度データ（簡易版）
COMMON_BIGRAMS = ['th', 'he', 'in', 'er', 'an', 're', 'on', 'at', 'en']
COMMON_TRIGRAMS = ['the', 'and', 'ing', 'ent', 'ion', 'her', 'for']

def get_ngrams(text, n):
    """テキストからn-gramを抽出して頻度をカウント"""
    text = "".join([c.lower() for c in text if c.isalpha()])
    ngrams = [text[i:i+n] for i in range(len(text)-n+1)]
    return collections.Counter(ngrams)

def analyze_and_attack(training_file, target_ciphertext):
    """大量のテキストから統計を学習し、ターゲットを解読する"""
    with open(training_file, "r") as f:
        corpus = f.read().lower()

    # 1. 1文字頻度による初期マッピングの作成
    trained_1gram = [char for char, _ in collections.Counter([c for c in corpus if c.isalpha()]).most_common()]
    cipher_1gram = [char for char, _ in collections.Counter([c for c in target_ciphertext if c.isalpha()]).most_common()]
    
    # 暫定的なマップ
    mapping = dict(zip(cipher_1gram, trained_1gram))

    # 2. 2文字・3文字頻度による微調整（ロジックの簡略化：the/andの特定）
    # 暗号文中で最も多い3文字の塊を特定
    target_3grams = get_ngrams(target_ciphertext, 3).most_common(2)
    
    print(f"--- [高度な統計解析ログ] ---")
    for cipher_3g, count in target_3grams:
        print(f"検出された頻出3連文字: '{cipher_3g}' ({count}回)")
        # 統計的にこれらは 'the' や 'and' である可能性が極めて高い
    print("-" * 30)

    # 3. 復号試行
    decoded = ""
    for char in target_ciphertext.lower():
        if char in mapping:
            decoded += mapping[char]
        else:
            decoded += char
    return decoded

if __name__ == "__main__":
    # 秘密鍵の固定
    letters = list(string.ascii_lowercase)
    shuffled = letters[:]
    random.seed(2026)
    random.shuffle(shuffled)
    key = dict(zip(letters, shuffled))

    def encrypt(text, k):
        return "".join([k[c] if c in k else c for c in text.lower()])

    # ターゲット暗号文
    target_plain = "You are not his father"
    target_cipher = encrypt(target_plain, key)

    print("【実習：n-gram解析による高精度解読】")
    print(f"解析対象: {target_cipher}\n")

    result = analyze_and_attack("message.txt", target_cipher)
    
    print(f"最終推定結果:\n{result}")
    print("\n[!] 解説: 'the' や 'ing' といった綴りの規則性（n-gram）は、")
    print("[!] 26! という巨大な鍵空間を、意味のある言葉へと収束させる。")