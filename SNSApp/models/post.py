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
    def get_all(cls):
        #プールから接続
        conn = db_pool.get_conn()
        try:
            #カーソル作成
            with conn.cursor() as cur:
                #SQL 削除がないのえ最新版(DESC)で全件取得
                sql = "SELECT * FROM Posts  ORDER BY created_at DESC;"
                #実行
                cur.execute(sql)
                #postsで受け取る(1件)
                posts = cur.fetchall()
            return posts
        
        except pymysql.Error as e:
            print(f'エラーが発生しています:{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    #投稿の新規作成
    @classmethod
    def create(cls, user_id, content):
        #プールから取得
        conn = db_pool.get_conn()
        try:
            #カーソル作成
            with conn.cursor() as cur:
                #SQL 
                sql = "INSERT INTO Posts (user_id, content) VALUES (%s, %s);"
                #実行
                cur.execute(sql, (user_id, content))
                #コミットする
                conn.commit()
                #生成されたIDを返すAUTO
            return cur.lastrowid
        except pymysql.Error as e:
            print(f"エラーが発生しています:{e}")
            abort(500)
        finally:
            db_pool.release(conn)

    #特定の投稿を検索
    @classmethod
    def find_by_id(cls, post_id):
        #プールから取得
        conn = db_pool.get_conn()
        try:
            #カーソル作成
            with conn.cursor() as cur:
                #SQL
                sql = "SELECT * FROM Posts WHERE id = %s;"
                #実行
                cur.execute(sql, (post_id,))
                #1件受け取る
                post = cur.fetchone()
            return post
        except pymysql.Error as e:
            print(f"エラーが発生しています:{e}")
            abort(500)
        finally:
            db_pool.release(conn)