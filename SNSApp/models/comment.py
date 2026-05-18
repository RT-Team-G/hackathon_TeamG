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
    #post_idでコメントを全件取得
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

    @classmethod
    # コメント数を取得
    def count_by_comment(cls, post_id):
        conn = db_pool.get_conn()
        try:
            # カーソル作成
            with conn.cursor() as cur:
                # SQL文
                sql = "SELECT COUNT(*) FROM Comments WHERE post_id=%s;"
                # executeでsqlクエリを実行
                cur.execute(sql, (post_id,))
                # コメント数を取得
                result = cur.fetchone()
                # resultに何も入っていない場合は0を返す resultが辞書でもタプルでもいいように両方考慮
                if result is None:
                    return 0
                elif isinstance(result, dict):
                    return result.get('cnt', 0)
                else:
                    return result[0]
        except pymysql.Error as e:
            print(f"エラーが発生しました:{e}")
            abort(500)
        finally:
            db_pool.release(conn)