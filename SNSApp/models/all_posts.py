from flask import abort # HTTPExceptionで強制的に処理を終了させる
import pymysql
from util.DB import DB

# 初期起動時にコネクションプールを作成し接続を確立
db_pool = DB.init_db_pool()

# All_Postクラス
class All_Post:
    @classmethod
    def get_all(cls):
        conn = db_pool.get_conn()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cur:
                sql = """
                        SELECT pt.post_id, JSON_ARRAYAGG(t.menu_name) AS menu_name, JSON_ARRAYAGG(pt.reps) AS reps, JSON_ARRAYAGG(pt.set_count) AS set_count, MAX(pt.created_at) AS created_at, ANY_VALUE(p.content) AS content, ANY_VALUE(p.user_id) AS user_id 
                        FROM Post_Training pt LEFT OUTER JOIN Training t ON pt.training_id = t.id 
                        LEFT OUTER JOIN Posts p ON pt.post_id = p.id 
                        GROUP BY pt.post_id 
                        ORDER BY created_at DESC;
                """
                cur.execute(sql)
                posts = cur.fetchall()
            return posts
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)
