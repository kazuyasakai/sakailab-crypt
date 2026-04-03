# 暗号論演習リポジトリ (sakailab-crypt)

現代暗号の基礎理論から実装、そして攻撃手法までを網羅した、酒井研究室（Sakai Lab）の演習用ソースコード群です。

## 1. 環境設定
本演習では Python 3.x を使用します。以下のコマンドで仮想環境を構築し、必要なライブラリをインストールしてください。

```bash
### 1. 仮想環境の作成
$ python3 -m venv .venv

### 2. 仮想環境の有効化
$ source .venv/bin/activate

### 3. パッケージマネージャの更新
$ pip install --upgrade pip

### 4. ライブラリの一括導入
$ pip install -r requirements.txt

### 5. 現在の環境を記録（任意）
$ pip freeze > requirement.txt

### 6. 環境から抜けるとき
$ deactivate
```

## 2. 01_classic フォルダ（古典暗号論）

・ceaser.py シーザー暗号

・mono_alphabetic.py 単一換字暗号

・freq_analysis.py 頻度分析（精度が悪い）、message.txt の文章から頻度表を作成

・enigma_lite.py 簡易版エニグマ暗号機

## 3. 02_privkey フォルダ（秘密鍵暗号）

・bbs_stream.py 疑似乱数生成器 Blum-Blum-Shub (BBS)

・cpa_enc.py 擬似ランダム関数を用いたCPA暗号

・ebc_image_attack.py

・cbc_enc.py CBCモード

・ctr_enc.py CTRモード

・iv_collision_attack.py 誕生日パラドックスと IV 衝突攻撃

## 4. 03_hash_mac フォルダ（HASHとMAC）

・cbcmac_forgery.py CBC-MACの偽造

・etm_auth_enc.py 認証付き暗号 Encrypt-then-MAC

・birthday_attack.py 誕生日攻撃

## 5. 04_pubkey フォルダ（公開鍵暗号とRSA）

・rsa_math.py 拡張グリッド法、逆元計算、平方乗算法

・rsa_crypt.py

・rsa_factor_attack.py

・rsa_sign.py
