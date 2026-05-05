import os #パスワードやポート番号を引っ張る
import pymysql 
from pymysqlpool import Pool

class DB:
    @classmethod
    def init_db_pool(cls):
        pool = Pool(
            # データベースホスト
            host=os.getenv('DB_HOST'),
            # データベースユーザー
            user=os.getenv('DB_USER'),
            # データベースパスワード
            password=os.getenv('DB_PASSWORD'),
            # データベース名
            database=os.getenv('DB_DATABASE'),
            # 最大コネクション
            max_size=5, #同時に５人まで接続
            # 文字コード
            charset="utf8mb4",
            # カーソルクラス (辞書型でフェッチ) {'id': 1, 'name': 'hoge'}
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True #確定させる


        )
        #コネクションプールの初期化
        pool.init()
        return pool