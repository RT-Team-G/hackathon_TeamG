from flask import abort # HTTPExceptionで強制的に処理を終了させる
import pymysql
from util.DB import DB

# 初期起動時にコネクションプールを作成し接続を確立
db_pool = DB.init_db_pool()

# Postクラス
class Post:
    @classmethod
    def get_all(cls):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT t.menu_name, pt.reps, pt.set_count, pt.created_at, p.content FROM Post_Training pt LEFT OUTER JOIN Training t ON pt.training_id = t.id LEFT OUTER JOIN Posts p ON pt.post_id = p.id ORDER BY created_at DESC;"
                cur.execute(sql)
                posts = cur.fetchall()
            return posts
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)
