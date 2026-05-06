from flask import abort
import pymysql
from util.DB import DB

# DB接続
db_pool = DB.init_db_pool()

# Reactionsテーブル作成
class Reactions:
    @classmethod
    #全件検索
    def get_all(cls):
        # プールから接続
        conn = db_pool.get_conn()
        try:
            #カーソル作成
            with conn.cursor() as cur:
                # SQL文(登録されているスタンプ全部だす)
                sql = "SELECT * FROM Reactions ORDER BY id ASC;"
                #実行
                cur.execute(sql)
                # 全件表示
                result = cur.fetchall()
            return result
        except pymysql.Error as e:
            print(f"エラーが発生しました:{e}")
            abort(500)
        finally:
            db_pool.release(conn)