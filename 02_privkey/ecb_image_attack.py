#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Topic: ECB Mode Image Encryption (Visualizing Vulnerability) 
Description: ECBモードで画像を暗号化し、統計的パターンが残る様子を観察する。
"""

from PIL import Image
import os
import hashlib

def block_encrypt(block, key):
    """
    1ブロック(16バイト)を暗号化する擬似的なPRF [cite: 1254-1262]
    実習用として、鍵とブロックのハッシュをとることで決定的な出力を得る
    """
    return hashlib.sha256(key + block).digest()[:16]

def encrypt_image_ecb(input_path, output_path, key):
    # 画像を読み込み、RGBAならRGBに変換
    img = Image.open(input_path).convert("RGB")
    data = img.tobytes()
    
    # 16バイト(128-bit)単位のブロックに分割 [cite: 1645-1646]
    block_size = 16
    encrypted_data = bytearray()
    
    print(f"Encrypting {len(data)} bytes in ECB mode...")
    
    for i in range(0, len(data), block_size):
        block = data[i:i+block_size]
        # パディング（最後のブロックが足りない場合）
        if len(block) < block_size:
            block = block.ljust(block_size, b'\0')
        
        # ECBモード：各ブロックを独立して同じ鍵で暗号化 [cite: 1646, 1664]
        enc_block = block_encrypt(block, key)
        encrypted_data.extend(enc_block)
    
    # 暗号化されたバイト列から新しい画像を生成
    # 元の画像と同じサイズ、モードで作成
    enc_img = Image.frombytes("RGB", img.size, bytes(encrypted_data[:len(data)]))
    enc_img.save(output_path)
    print(f"Saved: {output_path}")

if __name__ == "__main__":
    # 1. 適当な画像（Tuxくんやロゴなど、背景が単色のものが望ましい）を用意
    # 2. 128-bitの鍵を生成
    secret_key = b"Hino_Campus_2026"
    
    # 実習用画像（input.png）を暗号化
    if os.path.exists("input.png"):
        encrypt_image_ecb("input.png", "output_ecb.png", secret_key)
    else:
        print("[!] input.png が見つかりません。適当な画像を用意してください。")