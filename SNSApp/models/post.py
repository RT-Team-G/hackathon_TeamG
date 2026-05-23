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
                sql = """
                        SELECT pt.post_id AS id, JSON_ARRAYAGG(t.menu_name) AS menu_name, JSON_ARRAYAGG(pt.reps) AS reps, JSON_ARRAYAGG(pt.set_count) AS set_count, MAX(pt.created_at) AS created_at, ANY_VALUE(p.content) AS content, ANY_VALUE(p.user_id) AS user_id 
                        FROM Post_Training pt LEFT OUTER JOIN Training t ON pt.training_id = t.id 
                        LEFT OUTER JOIN Posts p ON pt.post_id = p.id 
                        WHERE p.id = %s 
                        GROUP BY pt.post_id 
                        ORDER BY created_at DESC;
                """
                #実行
                cur.execute(sql, (post_id,))
                post = cur.fetchone()
            return post
        except pymysql.Error as e:
            print(f"エラーが発生しました:{e}")
            abort(500)
        finally:
            db_pool.release(conn)