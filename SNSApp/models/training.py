from flask import abort
import pymysql
from util.DB import DB

# DB接続
db_pool = DB.init_db_pool()

#Trainigクラス作成
class Training:
    @classmethod
    #筋トレ内容作成
    def create(cls, menu_name):
        #プールから接続
        conn = db_pool.get_conn()
        try:
            #カーソル作成
            with conn.cursor() as cur:
                #SQL登録処理
                sql = "INSERT INTO Training(menu_name) VALUES (%s);"
                #実行
                cur.execute(sql, (menu_name,))
                #コミットする
                conn.commit()
             #AUTO_INCREMENTされたIDを返す
            return cur.lastrowid
        except pymysql.Error as e:
            print(f"エラーが発生しました{e}")
            abort(500)
        finally:
            db_pool.release(conn)