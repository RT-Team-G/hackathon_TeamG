from flask import abort
import pymysql
from util.DB import DB

# 初期起動時にコネクションプールを作成し接続を設立
db_pool = DB.init_db_pool()

# ユーザークラス 
class User:
    @classmethod
    #登録
    def create(cls, name, email, password):
        # 新しくユーザーをDBに登録する
        conn = db_pool.get_conn()
        try:
            # カーソルを作成withで終わったら自動で閉じてくれる
            with conn.cursor() as cur:
                # SQL文の指示%はSQLインジェクションの対策
                sql = "INSERT INTO Users (name, email, password) VALUES (%s, %s, %s);"
                #実行したら受け取った名前、メール、パスをDBに叩き込む
                cur.execute(sql, (name, email, password))
                #コミットする
                conn.commit()
                # AUTO_INCREMENTされたidを返す
                return cur.lastrowid
            
        except pymysql.Error as e:
            #もし失敗したらエラーを表紙して内容を表示してサーバーから一時停止
            print(f'エラーが発生してます:{e}')
            abort(500)

        finally:
            #成功しても失敗しても終了する
            db_pool.release(conn)

    @classmethod
    #検索(email)
    def find_by_email(cls, email):
        #接続する
        conn = db_pool.get_conn()
        try:
            #SQLを実行するカーソル
            with conn.cursor() as cur:
                #SQL文
                sql = "SELECT * FROM Users WHERE email=%s;"
                #実行(email,)はタプルの型にするため
                cur.execute(sql, (email,))
                #見つかった結果を１件取り出す
                user = cur.fetchone()
            #ユーザーを呼び出す
            return user
        except pymysql.Error as e:
            print(f'エラーが発生しています:{e}')
            abort(500)
        
        finally:
            #成功、失敗しても終了
            db_pool.release(conn)

    @classmethod
    #IDを検索
    def get_name_by_id(cls, user_id):
        #接続する
        conn = db_pool.get_conn()
        try:
            #SQLを実行するカーソル
            with conn.corsor() as cur:
                #SQL文
                sql = "SELECT * FROM Users WHERE id =%s;"
                #実行
                cur.execute(sql, (user_id,))
                #受け取る(1件)
                user = cur.fetchone()
                #もしデータがあれば名前を返し、なければNoneを返す
                return user['name'] if user else None
        except pymysql.Error as e:
            print(f'エラーが発生しています:{e}')
            abort(500)

        finally:
            db_pool.release(conn)