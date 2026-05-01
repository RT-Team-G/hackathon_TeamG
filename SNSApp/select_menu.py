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
    # クラスメソッド - clsを通じてクラスの属性にアクセス
    def get_menu(cls):
        conn = db_pool.get_conn()
        # 例外処理
        try:
            with conn.cursor() as cur:  #connでDB接続→カーソル取得 カーソル通じてクエリを実行
                sql = 'SELECT * FROM Training'
                cur.execute(sql) #execute()でクエリ実行
                menu_all = cur.fetchall() #クエリの結果を取得(辞書のリスト)
            return menu_all
        except pymysql.Error as e:  #pythonでMySQL操作時の例外
            print(f'エラーが発生しています：{e}')
            abort(500)  *サーバーエラー
        finally:
            db_pool.release(conn) #DB接続の解放

class Rec:
    @classmethod
    def record_DB(menus, menus_reps, menu_sets, menu, rep, set_count, content):
        # メニュー・回数・セット数を順番にDBに登録
        for i in range(len(menus)): #len関数でメニュー数分繰り返し
            menu_name = request.form.get(menu[i])
            reps = request.form.get(rep[i])
            set_count = request.form.get(set_count[i])

            conn = db_pool.get_conn()
            try:
                with conn.cursor() as cur:
                    sql_1 = "INSERT INTO Posts (user_id, content) VALUES (%s, %s);"
                    cur.execute(sql_1, (user_id, content))

                    user_id = cursor.lastrowid

                    sql_2 = "INSERT INTO Post_Training (user_id, post_id, training_id, reps, set_count) VALUES (%s, %s, %s, %s, %s);"
                    cur.execute(sql_2, (user_id, post_id, training_id, reps, set_count)) 
    
                    conn.commit()

            except pymysql.Error as e:
                print(f'エラーが発生しています：{e}')
                abort(500)
            finally:
                db_pool.release(conn)
