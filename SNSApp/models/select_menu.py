from flask import abort, request
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
            with conn.cursor(pymysql.cursors.DictCursor) as cur:  #connでDB接続→カーソル取得 カーソル通じてクエリを実行
                sql = 'SELECT * FROM Training'
                cur.execute(sql) #execute()でクエリ実行
                menu_all = cur.fetchall() #クエリの結果を取得(辞書のリスト)
            return menu_all
        except pymysql.Error as e:  #pythonでMySQL操作時の例外
            print(f'エラーが発生しています：{e}')
            abort(500)  *サーバーエラー
        finally:
            db_pool.release(conn) #DB接続の解放

# <登録処理>
class Rec:
    @classmethod #sec_key追加した
    def record_DB(cls, content_key, menu_key, reps_key, set_count_key, sec_key, user_id):
        
        content = request.form.get(content_key, '').strip()
        # メニュー選択項目を配列として入れる
        menus = request.form.getlist(menu_key)
        menus_reps = request.form.getlist(reps_key)
        menus_sets = request.form.getlist(set_count_key)
        #秒数追加
        menus_secs = request.form.getlist(sec_key)

        conn = db_pool.get_conn()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cur:
                sql_1 = "INSERT INTO Posts (user_id, content) VALUES (%s, %s);"
                cur.execute(sql_1, (user_id, content))

                post_id = cur.lastrowid #直前のINSERT文で自動生成されたIDを取得

                # メニュー・回数・セット数を順番にDBに登録
                for i in range(len(menus)): #len関数でメニュー数分繰り返し
                        #メニューが選択されていない場合はスキップ
                    if not menus[i]:
                        continue

                    menu_id = menus[i]
                    reps = menus_reps[i]
                    set_count = menus_sets[i]

                    #空文字なら0
                    sec_value = menus_secs[i] if i < len(menus_secs) else 0
                    training_time = int(sec_value) if sec_value else 0

                    # sql2にtrainng_time追加
                    sql_2 = "INSERT INTO Post_Training (user_id, post_id, training_id, reps, set_count, training_time) VALUES (%s, %s, %s, %s, %s, %s);"
                    cur.execute(sql_2, (user_id, post_id, menu_id, reps, set_count, training_time)) 
                conn.commit()

        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)
