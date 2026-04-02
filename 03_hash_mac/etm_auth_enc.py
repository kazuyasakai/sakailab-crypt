#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Topic: Authenticated Encryption (Encrypt-then-MAC)
Description: 機密性(CBC)と真正性(HMAC)を組み合わせた、CCAセキュアな構成の実装。
"""

import os
import hashlib
import hmac

def get_hmac(key, data):
    """HMAC-SHA256 を使用した真正性の担保"""
    return hmac.new(key, data, hashlib.sha256).digest()

def encrypt_then_mac(plaintext, enc_key, mac_key):
    """
    Encrypt-then-MAC (EtM) の実装
    1. 平文を暗号化 (CBCモード風の簡易実装)
    2. 暗号文に対して MAC を計算
    """
    # --- 1. Encryption (Confidentiality) ---
    iv = os.urandom(16)
    # 実習用の簡易的な暗号化（本来はAES等を使用）
    # 暗号文 C = m ^ Fk(IV)
    keystream = hashlib.sha256(enc_key + iv).digest()[:len(plaintext)]
    ciphertext = bytes([p ^ k for p, k in zip(plaintext, keystream)])
    
    # --- 2. MAC Generation (Authenticity) ---
    # IV と Ciphertext の両方を認証対象に含めるのが鉄則
    auth_data = iv + ciphertext
    tag = get_hmac(mac_key, auth_data)
    
    return iv, ciphertext, tag

def decrypt_verify(iv, ciphertext, tag, enc_key, mac_key):
    """復号と検証：必ず検証を先に行う"""
    # --- 1. Verify (Authenticity Check) ---
    # 受信したデータから再度タグを計算
    expected_tag = get_hmac(mac_key, iv + ciphertext)
    
    # 定数時間比較でタグをチェック（タイミング攻撃防止）
    if not hmac.compare_digest(tag, expected_tag):
        print("[!] MAC verification failed! Message was tampered with.")
        return None
    
    print("[+] MAC verification successful. Proceeding to decryption...")
    
    # --- 2. Decryption (Confidentiality) ---
    keystream = hashlib.sha256(enc_key + iv).digest()[:len(ciphertext)]
    plaintext = bytes([c ^ k for c, k in zip(ciphertext, keystream)])
    return plaintext

if __name__ == "__main__":
    # 独立した2つの鍵を使用することが極めて重要
    encryption_key = b"Hino_Encryption_Key_2026"
    authentication_key = b"Hino_Auth_Key_2026"
    
    message = b"Transfer $10,000 to Alice"
    print(f"Original Message: {message.decode()}")

    # 送信：暗号化 + タグ付与
    iv, cipher, tag = encrypt_then_mac(message, encryption_key, authentication_key)
    print(f"Sent Ciphertext: {cipher.hex()}")
    print(f"Sent Tag: {tag.hex()}\n")

    # シナリオ1: 正常な通信
    print("--- Scenario 1: Normal Communication ---")
    result1 = decrypt_verify(iv, cipher, tag, encryption_key, authentication_key)
    if result1: print(f"Decrypted: {result1.decode()}\n")

    # シナリオ2: 改ざんが発生した場合
    print("--- Scenario 2: Tampering Attack ---")
    # tampered_cipher の最初の 1バイト に対して XOR を行う
    tampered_cipher = bytearray(cipher)
    tampered_cipher[0] ^= 0x01
    print(f"Tampered cipher: {bytes(tampered_cipher).hex()}")
    
    # 検証と復号を試みる
    result2 = decrypt_verify(iv, bytes(tampered_cipher), tag, encryption_key, authentication_key)
    if result2 is None:
        print("Result: Attack successfully blocked by MAC verification.")