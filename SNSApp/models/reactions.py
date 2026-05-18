from flask import abort
import pymysql
from util.DB import DB

# DB接続
db_pool = DB.init_db_pool()

# Reactionsクラス reactionをDBに登録
class Reactions:
    @classmethod
    def add_reaction(cls, user_id, post_id, reaction_id):
        # プールから接続
        conn = db_pool.get_conn()
        try:
            #カーソル作成
            with conn.cursor() as cur:
                # SQL文(登録)
                sql = "INSERT INTO Post_Reactions (user_id, post_id, reaction_id) VALUES (%s, %s, %s);"
                #実行
                cur.execute(sql,(user_id, post_id, reaction_id))
                # 確定
                cur.commit()
            return result
        except pymysql.Error as e:
            print(f"エラーが発生しました:{e}")
            abort(500)
        finally:
            db_pool.release(conn)

# reactionの数をカウント
    # @classmethod
    # def count_reaction(cls, post_id):
    #     # プールから接続
    #     conn = db_pool.get_conn()
    #     try:
    #         # カーソル作成
    #         with conn.cursor() as cur:
    #             # SQL(count)
    #             sql = "SELECT COUNT(*) FROM Post_Reaction WHERE post_id=%s;"
    #             # 実行
    #             cur.execute(sql, (post_id))
    #             # count
    #             count_reaction = cur.fetchall()
    #         return count_reaction