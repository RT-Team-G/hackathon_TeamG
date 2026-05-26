from flask import Flask, request, redirect, render_template, session, flash, abort, url_for
from flask_wtf.csrf import CSRFProtect
from datetime import timedelta
from util.DB import DB
import hashlib
import uuid
import re
import os
import pymysql.cursors
import json

from models.select_menu import Menu, Rec
from models.all_posts import All_Post
from models.post import Post
from models.user import User
from models.comment import Comments # コメント機能実装後にインポートする
from models.reactions import Reactions 

# 初期起動時にコネクションプールを作成し接続を確立
db_pool = DB.init_db_pool()

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
    return redirect(url_for('posts_list_view'))

# サインアップページの表示
@app.route('/signup', methods=['GET'])
def signup_view():
    if session.get('user_id') is not None: # セッション残ってない(Noneではない)場合
        return redirect(url_for('posts_list_view'))
    return render_template('auth/signup.html')

# サインアップ処理
@app.route('/signup', methods=['POST'])
def signup_process():
    name = request.form.get('name', '').strip() #POSTリクエストのパラメータ(form)
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '')
    password_confirmation = request.form.get('password_confirmation', '')

    # 空チェック
    if not name or not email or not password or not password_confirmation:
        flash("空のフォームがあります", 'error') # 第二引数はカテゴリ(デフォルトはmessage)
        return redirect(url_for('signup_view'))

    # パスワード一致チェック
    if password != password_confirmation:
        flash('パスワードが一致しません', 'error')
        return redirect(url_for('signup_view'))

    # メール形式チェック
    if re.match(EMAIL_PATTERN, email) is None: # マッチする文字列がない場合Noneを返す
        flash('メールアドレスの形式が正しくありません','error')
        return redirect(url_for('signup_view'))

    # 既存ユーザーチェック
    registered_user = User.find_by_email(email)
    if registered_user is not None:
        flash('既に登録されているメールアドレスです','error')
        return redirect(url_for('signup_view'))

    # パスワード生成
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

    # UserクラスのcreateメソッドでuserID取得
    user_id = User.create(name, email, hashed_password)

    # sessionに値(user_id)を書き込む
    session['user_id'] = user_id

    # リダイレクト
    return redirect(url_for('posts_list_view'))

# ログインページの表示
@app.route('/login', methods=['GET'])
def login_view():
    if session.get('user_id') is not None:
        return redirect(url_for('posts_list_view'))
    return render_template('auth/login.html')

# ログイン処理
@app.route('/login', methods=['POST'])
def login_process():
    email = request.form.get('email')
    password = request.form.get('password')

    if email == '' or password == '':
        flash('メールアドレスorパスワードが空です','error')
    else:
        user = User.find_by_email(email)
        if user is None:
            flash('メールアドレスorパスワードが違います','error')
        else:
            hashPassword = hashlib.sha256(password.encode('utf-8')).hexdigest()
            if hashPassword != user["password"]:
                flash('メールアドレスorパスワードが違います','error')
            else:
                session['user_id'] = user["id"]
                return redirect(url_for('posts_list_view'))
    return redirect(url_for('login_view'))

#ログアウト
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_view'))

# トレーニングメニュー選択・投稿作成画面表示
@app.route('/post', methods=['GET'])
def post_view():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('login_view'))
    else:
        choices = Menu.get_menu()
    return render_template('post/training-post.html', choices=choices)

# app.py(投稿処理)
    # request.form.getlist()でID＋回数(秒数)＋セット数取得
@app.route('/post', methods=['POST'])
def create_post():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('login_view'))
    
    # sec[]追加
    Rec.record_DB('content', 'menu[]', 'reps[]', 'set_count[]', 'sec[]', user_id)

    return redirect(url_for('posts_list_view'))


# 投稿一覧表示画面の表示(途中)
@app.route('/posts_list', methods=['GET'])
def posts_list_view():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('login_view'))
    else:
        posts = All_Post.get_all() # All_Postクラス・get_all()
        for post in posts:
            
            #これ↓5/26エラー対策で追加しました
            if 'sec' not in post:
                post['sec'] = []
                
            if isinstance(post['menu_name'], str):
                post['menu_name'] = json.loads(post['menu_name'])
            if isinstance(post['reps'], str):
                post['reps'] = json.loads(post['reps'])
            # こめんと削除 一部追加
            if 'sec' in post and isinstance(post['sec'], str):
                 post['sec'] = json.loads(post['sec'])
            if isinstance(post['set_count'], str):
                post['set_count'] = json.loads(post['set_count'])
            post['created_at'] = post['created_at'].strftime('%Y-%m-%d %H:%M')
            post['user_name'] = User.get_name_by_id(post['user_id'])
            # コメント数を取得
            post['comments_count'] = Comments.count_by_comment(post['id'])
            # post['reaction'] = Reactions.count_reaction(post['reaction'])

        return render_template('main/posts.html', posts=posts, user_id=user_id)
        
# 投稿詳細画面表示(途中)
@app.route('/posts_list/<int:post_id>', methods=['GET'])
def posts_list_detail_view(post_id):
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('login_view'))
    # 投稿
    post = Post.find_by_id(post_id) #Postクラス・find_by_id()
    if post is None:
        abort(404) #リクエストされた投稿が見つからない場合404エラーを出す

    if isinstance(post['menu_name'], str):
        post['menu_name'] = json.loads(post['menu_name'])
    if isinstance(post['reps'], str):
        post['reps'] = json.loads(post['reps'])
    #コメント削除
    if isinstance(post['sec'], str):
         post['sec'] = json.loads(post['sec'])
    if isinstance(post['set_count'], str):
        post['set_count'] = json.loads(post['set_count'])
    post['created_at'] = post['created_at'].strftime('%Y-%m-%d %H:%M')
    post['user_name'] = User.get_name_by_id(post['user_id'])
    # post['reaction'] = Reactions.count_reaction(post['reaction'])

    # リアクション表示(DBから取得→表示)
    reactions = Reactions.get_reaction(post_id)

    # コメント
    comments = Comments.get_by_post_id(post_id) #commentsクラス・get_by_post_id()
    for comment in comments:
        comment['created_at'] = comment['created_at'].strftime('%Y-%m-%d %H:%M')
        comment['user_name'] = User.get_name_by_id(comment['user_id'])

    # コメント数を取得
    post['comments_count'] = Comments.count_by_comment(post['id'])

    return render_template('post/post_detail.html', post=post, comments=comments, user_id=user_id, reactions = reactions)

# 投稿に対するコメント処理(途中)
@app.route('/posts_list/<int:post_id>/comments', methods=['POST'])
def create_comment(post_id):
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('login_view'))
    content = request.form.get('content', '').strip()
    if content == '':
        flash('コメント内容が空です','error')
    Comments.create(user_id, post_id, content) #Commentsクラス・create()
    return redirect(url_for('posts_list_detail_view', post_id=post_id))

# タイマー画面表示(htmlテンプレート確認要)
@app.route('/timer', methods=['GET'])
def timer_view():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('login_view'))
    return render_template('timer.html')

# リアクション機能
# 登録
@app.route('/posts_list/<int:post_id>/reaction', methods=['POST'])
def add_reaction(post_id):
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('login_view'))
    else:
        select_reaction = int(request.form.get('reaction_id'))
        Reactions.add_reaction(user_id, post_id, select_reaction)

    return redirect(url_for('posts_list_detail_view', post_id=post_id))

if __name__=='__main__':
    app.run(host="0.0.0.0", debug=True)