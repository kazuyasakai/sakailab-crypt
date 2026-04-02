#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Lecture: Cryptography (古典暗号論)
Topic: Caesar Cipher - The Bittersweet Reality
Environment: MacBook Pro (ret2root) / sakailab-crypt
"""

def encrypt(plaintext, shift):
    """
    シーザー暗号による暗号化 (置換暗号の基本)
    """
    ciphertext = ""
    for char in plaintext:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            ciphertext += chr((ord(char) - start + shift) % 26 + start)
        else:
            ciphertext += char
    return ciphertext

def decrypt(ciphertext, shift):
    """
    シーザー暗号による復号 (逆置換)
    """
    return encrypt(ciphertext, -shift)

def brute_force_attack(ciphertext):
    """
    全数探索（Brute-force attack）による秘密の暴露
    """
    print(f"\n[!] 傍受された暗号文: {ciphertext}")
    print("[!] 全数探索を開始します... 隠された本心を見つけ出せ。")
    for key in range(26):
        attempt = decrypt(ciphertext, key)
        # 学生へのヒント: 意味の通じる英文が出てきたら、それが解読成功。
        print(f"Key {key:02d}: {attempt}")

if __name__ == "__main__":
    # --- 授業用デモンストレーション: 伝えられない本音 ---
    
    # 1. 秘匿したいメッセージの設定
    # 「あなたは私を愛している、でも私はあなたを嫌い」という残酷な真実
    target_text = "You love me, but I hate you."
    secret_key = 12  # 適当なシフト数
    
    # 2. 暗号化プロセスの実行 (Substitution)
    c_text = encrypt(target_text, secret_key)
    
    print("--- 講義デモ: シーザー暗号の実装と脆弱性 ---")
    print(f"送信者の本音: {target_text}")
    print(f"暗号化された文: {c_text} (Key: {secret_key})")
    
    # 3. 復号のテスト
    p_text = decrypt(c_text, secret_key)
    print(f"正規の受信者が復号: {p_text}")
    
    # 4. 攻撃者による解読試行 (Cryptanalysis)
    # シラバスの「単独暗号文攻撃 (COA)」の実演として提示
    brute_force_attack(c_text)