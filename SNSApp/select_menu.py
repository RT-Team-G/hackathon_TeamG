from flask import abort
import pymysql
from util.DB import DB


# 初期起動時にコネクションプールを作成し接続を確立
db_pool = DB.init_db_pool()


# <セレクトボックス反映>
    # menu.py
    # SELECT文でIDとmenu_name全件取得
    # Menuクラス
class Menu:
    @classmethod
    def get_menu(cls):
        conn = db_pool.get_conn()
        # 例外処理
        try:
            with conn.cursor() as cur:  #connでDB接続→カーソル取得 カーソル通じてクエリを実行
                sql = 'SELECT * FROM Training'
                cur.execute(sql) #execute()でクエリ実行
                menu_all = cursor.fetchall() #クエリの結果を取得(辞書のリスト)
            return menu_all
        except pymysql.Error as e:  #pythonでMySQL操作時の例外
            print(f'エラーが発生しています：{e}')
            abort(500)  *サーバーエラー
        finally:
            db_pool.release(conn) #DB接続の解放
