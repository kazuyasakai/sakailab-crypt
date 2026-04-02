#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Topic: Birthday Attack on Hash Functions
Description: ハッシュ値のビット長を制限し、衝突を発見するまでの試行回数を計測する。
"""

import hashlib
import os
import time

def short_hash(data, bit_length=24):
    """
    SHA-256の結果を特定のビット長に切り詰める (圧縮関数のシミュレート)
    """
    full_hash = hashlib.sha256(data).digest()
    # 指定ビット分だけ取り出す
    byte_length = (bit_length + 7) // 8
    temp_hash = int.from_bytes(full_hash[:byte_length], 'big')
    return temp_hash >> (byte_length * 8 - bit_length)

def find_collision(bit_length):
    hash_table = {}
    attempts = 0
    start_time = time.time()
    
    print(f"--- Searching for collision ({bit_length}-bit hash) ---")
    # 理論上の期待値は 2^(bit_length/2) 
    expected = 2 ** (bit_length / 2)
    print(f"Theoretical average attempts: {expected:.2f}")

    while True:
        attempts += 1
        # ランダムなメッセージを生成
        m = os.urandom(16)
        h = short_hash(m, bit_length)
        
        if h in hash_table:
            # 衝突発見！ 
            m_original = hash_table[h]
            if m_original != m:
                duration = time.time() - start_time
                print(f"[Success] Collision Found in {attempts} attempts!")
                print(f"  m1: {m_original.hex()}")
                print(f"  m2: {m.hex()}")
                print(f"  Hash (hex): {hex(h)}")
                print(f"  Time: {duration:.4f} sec\n")
                return attempts
        
        hash_table[h] = m

if __name__ == "__main__":
    # 32-bit程度なら一瞬、40-bitなら数秒で衝突します
    target_bits = 40
    find_collision(target_bits)