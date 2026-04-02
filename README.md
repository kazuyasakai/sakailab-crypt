環境設定とはじめにすること
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install --upgrade pip
$ pip install cryptography
$ pip freeze > requirement.txt

環境から抜けるとき
$ deactivate


-- 01_classic フォルダ（古典暗号論） --
・ceaser.py シーザー暗号
・mono_alphabetic.py 単一換字暗号
・freq_analysis.py 頻度分析（精度が悪い）、message.txt の文章から頻度表を作成
・enigma_lite.py 簡易版エニグマ暗号機

-- 02_privkey フォルダ（秘密鍵暗号） --
・bbs_stream.py 疑似乱数生成器 Blum-Blum-Shub (BBS)
・cpa_enc.py 擬似ランダム関数を用いたCPA暗号
・ebc_image_attack.py
・cbc_enc.py CBCモード
・ctr_enc.py CTRモード
・iv_collision_attack.py 誕生日パラドックスと IV 衝突攻撃

-- 03_hash_mac フォルダ（HASHとMAC） --
・cbcmac_forgery.py CBC-MACの偽造
・etm_auth_enc.py 認証付き暗号 Encrypt-then-MAC
・birthday_attack.py 誕生日攻撃

-- 04_pubkey フォルダ（公開鍵暗号とRSA） --
・rsa_math.py 拡張グリッド法、逆元計算、平方乗算法
・rsa_crypt.py
・rsa_factor_attack.py
・rsa_sign.py
