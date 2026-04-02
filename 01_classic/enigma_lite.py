#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Lecture: Cryptography (第2回 古典暗号論)
Topic: Rotor Cipher (Enigma Lite)
Description: 1文字ごとに「置換ルール」が回転する、多表換字の極致。
"""

import string

class EnigmaLite:
    def __init__(self, key_shift=0):
        # 標準的なアルファベット
        self.alphabet = string.ascii_lowercase
        # 固定のローター（置換表）: スライドの「複雑な接続」を模倣
        self.rotor = "hguitwbspzcfrqevdomxkyjnal"
        # ローターの初期位置（秘密鍵）
        self.position = key_shift % 26

    def _rotate(self):
        """1文字処理するごとにローターを1ステップ回転させる"""
        self.position = (self.position + 1) % 26

    def process_char(self, char, mode='encrypt'):
        """1文字の暗号化または復号化を行う"""
        if char.lower() not in self.alphabet:
            return char

        # 入力文字のインデックスに現在のポジションを加味
        idx = self.alphabet.index(char.lower())
        shift_idx = (idx + self.position) % 26
        
        if mode == 'encrypt':
            # 換字（Substitution）を実行
            res_char = self.rotor[shift_idx]
        else:
            # 逆換字（Decryption）を実行
            target_idx = self.rotor.index(char.lower())
            res_char = self.alphabet[(target_idx - self.position) % 26]

        # 処理後にローターを物理的に回転（これが多表換字の核心）
        self._rotate()
        
        return res_char.upper() if char.isupper() else res_char

    def run(self, text, mode='encrypt'):
        return "".join([self.process_char(c, mode) for c in text])

if __name__ == "__main__":
    # ターゲット：二度と会わないという、一方向かつ断絶的な決別
    plaintext = "I will never see you"
    initial_key = 13  # 初期位置（秘密鍵）

    print("【実習：エニグマ・ライト ―― 刻一刻と変わる真実】")
    print(f"平文: {plaintext}")
    print(f"初期鍵（ポジション）: {initial_key}")

    # 暗号化
    enigma_enc = EnigmaLite(initial_key)
    ciphertext = enigma_enc.run(plaintext, 'encrypt')
    print(f"暗号: {ciphertext}")

    # 復号化（同じ初期鍵からスタートする必要がある）
    enigma_dec = EnigmaLite(initial_key)
    decrypted = enigma_dec.run(ciphertext, 'decrypt')
    print(f"復号: {decrypted}")