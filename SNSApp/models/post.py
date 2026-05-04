# いつもの
from flask import abort
import pymysql
from util.DB import DB

# DB.接続
db_pool = DB.init_db_pool()

#Postクラスの定義
class Post:
    #投稿の全件取得
    @classmethod
    def get_All(cls):
        #プールから接続
        conn = db_pool.get_conn()
        try:
            #カーソル作成
            with conn.cursor() as cur:
                #SQL 削除がないのえ最新版(DESC)で全件取得
                sql = "SELECT * FROM Posts  ORDEY BY created_at DESC;"
                #実行
                cur.execute(sql)
                #postsで受け取る(1件)
                posts = cur.fetchall()
            return posts
        
        except pymysql.Error as e:
            print(f'エラーが発生しました{e}')
            abort(500)
        finally:
            db_pool.release(conn)