from flask import Flask, request, redirect, render_template, session, flash, abort, url_for
from flask_wtf.csrf import CSRFProtect
from datetime import timedelta
import hashlib
import uuid
import re
import os

from models import User, Post, Comment

# 定数定義
EMAIL_PATTERN = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
SESSION_DAYS = 30

app = Flask(__name__) # Flaskアプリのインスタンス生成
app.secret_key = os.getenv('SECRET_KEY', uuid.uuid4().hex) # セッションの暗号化とCSRFトークン生成に使う秘密鍵を環境変数から読み取る　一意のランダムなUUIDを生成
app.permanent_session_lifetime = timedelta(days=SESSION_DAYS) # (days=30) -> 30日保存

csrf = CSRFProtect(app)

# ルートページのリダイレクト処理
@app.route('/', methods=['GET'])
def index():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('login_view'))
    return redirect(url_for('post_view'))

# サインアップページの表示

# サインアップ処理

# ログインページの表示

# ログイン処理

# トレーニングメニュー選択・投稿作成画面表示

# 投稿処理

# 投稿一覧表示画面の表示

# 投稿詳細画面表示

# 投稿に対するコメント処理

# タイマー画面表示

# リアクション機能