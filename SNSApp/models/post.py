from flask import abort
import pymysql
from util.DB import DB

# DB接続
db_pool = DB.init_db_pool()

# Postクラス作成
class Post:
    @classmethod
    #投稿をIDで一件検索
    def find_by_id(cls, post_id):
        conn = db_pool.get_conn()
        try:
            #カーソル作成
            with conn.cursor() as cur:
                #SQL文
                sql = "SELECT t.menu_name, pt.reps, pt.set_count, pt.created_at, p.content FROM Post_Training pt LEFT OUTER JOIN Training t ON pt.training_id = t.id LEFT OUTER JOIN Posts p ON pt.post_id = p.id WHERE pt.post_id = %s;"
                #実行
                cur.execute(sql, (post_id,))
                post = cur.fetchone()
            return post
        except pymysql.Error as e:
            print(f"エラーが発生しました:{e}")
            abort(500)
        finally:
            db_pool.release(conn)