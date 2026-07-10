from flask import abort
import pymysql
from util.DB import DB

# DB接続
db_pool = DB.init_db_pool()

# Reactionsクラス reactionをDBから取得
class Reactions:
# リアクション表示と数のカウント
    @classmethod
    def get_reaction(cls, post_id):
        # プールから接続
        conn = db_pool.get_conn()
        try:
            # カーソル作成
            with conn.cursor() as cur:
                sql = """
                        SELECT r.id,r.reaction,COUNT(pr.reaction_id) AS count
                        FROM Reactions r LEFT JOIN Post_Reaction pr 
                        ON r.id=pr.reaction_id AND pr.post_id=%s 
                        GROUP BY r.id, r.reaction 
                        ORDER BY r.id ASC;
                """
                # 実行
                cur.execute(sql, (post_id))
                # 結果
                get_reaction = cur.fetchall()
            return get_reaction

        except pymysql.Error as e:
            print(f"エラーが発生しました:{e}")
            abort(500)
        finally:
            db_pool.release(conn)

# Reactionsクラス reactionをDBに登録
    @classmethod
    def add_reaction(cls, user_id, post_id, select_reaction):
        # プールから接続
        conn = db_pool.get_conn()
        try:
            #カーソル作成
            with conn.cursor() as cur:
                # 既に登録があるか確認のため抽出
                sql = "SELECT * FROM Post_Reaction WHERE user_id=%s AND post_id=%s AND reaction_id=%s;"
                # 実行
                cur.execute(sql,(user_id, post_id, select_reaction))
                # 結果
                result = cur.fetchone()
                # 条件分岐
                if result is None:
                # SQL文(登録)
                    sql = "INSERT INTO Post_Reaction(user_id, post_id, reaction_id) VALUES (%s, %s, %s);"
                    # 実行
                    cur.execute(sql,(user_id, post_id, select_reaction))
                    # 確定
                    conn.commit()
                # 既に存在した時は何もしないためelseは書かない

        except pymysql.Error as e:
            print(f"エラーが発生しました:{e}")
            abort(500)
        finally:
            db_pool.release(conn)
