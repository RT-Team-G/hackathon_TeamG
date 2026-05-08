from flask import abort
import pymysql
from util.DB import DB

#接続
db_pool = DB.init_db_pool()

# Commentsクラス
class Comments:
    @classmethod
    #コメント作成
    def create(cls, user_id, post_id, content):
        conn = db_pool.get_conn()
        try:
            #カーソル作成
            with conn.cursor() as cur:
                #SQL文
                sql = "INSERT INTO Comments (user_id, post_id, content) VALUES (%s, %s, %s);"
                #実行
                cur.execute(sql, (user_id, post_id, content))
                #コミットする
                conn.commit()
        except pymysql.Error as e:
            print(f"エラーが発生しました{e}")
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    #IDを検索
    def get_by_post_id(cls, post_id):
        conn = db_pool.get_conn()
        try:
            #カーソル作成
            with conn.cursor() as cur:
                #SQL文
                sql = "SELECT * FROM comments WHERE post_id=%s ORDER BY created_at DESC;"
                #実行
                cur.execute(sql, (post_id,))
                #全件取得
                comments = cur.fetchall()
            return comments
        except pymysql.Error as e:
            print(f"エラーが発生しました:{e}")
            abort(500)
        finally:
            db_pool.release(conn)