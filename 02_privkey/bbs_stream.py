#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Lecture: Cryptography (秘密鍵暗号)
Topic: Blum-Blum-Shub (BBS) PRG & Stream Cipher
Description: 資料 46ページ のパラメータを用いたビット単位の暗号化。
"""

class BBSStreamCipher:
    def __init__(self, p, q, seed):
        self.n = p * q
        self.x = seed
        # 初期の x_0 を計算 (x_i = x_{i-1}^2 mod N)
        # 資料の例 に合わせ、最初のビット生成前に一度計算
        self.x = (self.x**2) % self.n

    def _next_bit(self):
        """ハードコア述語 b(x) = LSB を用いて 1ビット生成 """
        bit = self.x % 2 # 最下位ビット (LSB) を取得 
        self.x = (self.x**2) % self.n # 次の状態へ遷移
        return bit

    def encrypt(self, plaintext):
        """平文をビット列に展開し、BBSストリームとXOR演算を行う"""
        ciphertext_bits = []
        # 文字列をバイナリ（ビット列）に変換
        for char in plaintext:
            # 1文字を8ビットの数値として扱う
            byte_val = ord(char)
            for i in range(8):
                # 1ビットずつ取り出す (MSBから)
                plain_bit = (byte_val >> (7 - i)) & 1
                key_bit = self._next_bit() # BBSによる疑似乱数
                ciphertext_bits.append(plain_bit ^ key_bit) # XOR演算
        return ciphertext_bits

if __name__ == "__main__":
    # 資料のパラメータ
    P, Q = 29, 31
    SEED = 100
    
    # 平文 (メッセージ)
    m = "You love me but I hate you"
    
    print(f"【実習：BBSストリーム暗号 ―― 1ビットの機密】")
    print(f"平文: {m}")
    # format(..., 'x') を使うことで、0x を除いた純粋な16進数文字列として統一
    print(f"平文（HEX）: {m.encode('ascii').hex()}")
    print(f"N = {P*Q}, Seed = {SEED}\n")

    # 暗号化
    cipher_engine = BBSStreamCipher(P, Q, SEED)
    c_bits = cipher_engine.encrypt(m)
    
    # 暗号文を16進数で表示
    # zfill を使うことで、ビット長に応じた正確な桁数を維持
    c_hex = format(int(''.join(map(str, c_bits)), 2), f'0{len(c_bits)//4}x')
    print(f"暗号文 (HEX): {c_hex}")

    # 復号化 (同じシードで再生成)
    # 暗号文(c_bits)に対して再度BBSストリームをXORする
    dec_engine = BBSStreamCipher(P, Q, SEED)
    
    # 修正ポイント: encryptメソッドに平文ではなく「暗号文のビット列」を渡す必要があります
    # XORの性質(m ^ k ^ k = m)を利用するため、中身は同じロジックで動きます
    # ※もし既存のencryptが「文字列」を引数に取るなら、別途ビット列用の処理が必要です
    
    # ビット列から直接復号する場合の簡易実装例
    recovered_bits = []
    bit_gen = BBSStreamCipher(P, Q, SEED)
    for bit in c_bits:
        recovered_bits.append(bit ^ bit_gen._next_bit())
    
    # 復号したビット列をHEXに戻す
    recovered_hex = format(int(''.join(map(str, recovered_bits)), 2), f'0{len(recovered_bits)//4}x')
    print(f"復号した平文（HEX）: {recovered_hex}")

    # 検証
    if m.encode('ascii').hex() == recovered_hex:
        print("\n[Verification Success]: 平文と復号文のHEXが完全に一致しました。")