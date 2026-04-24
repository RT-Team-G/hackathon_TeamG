-- もしも古いsnsappがあったらいったん消す(やり直しよ用)
DROP DATABASE IF EXISTS snsapp;

-- もしtestuserがいたらいったん消す
DROP USER IF EXISTS 'testuser'@'%';


--　testuserを新しく作成
CREATE USER 'testuser'@'%' IDENTIFIED BY 'testuser';

-- snsappデータベースを新しく作成(日本語・絵文字対応)
CREATE DATABASE IF NOT EXISTS snsapp
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;

-- testuserにsnsappの全権限を付与
GRANT ALL PRIVILEGES ON snsapp. * TO 'testuser'@'%';

-- 設定を即座に反映させる
FLUSH PRIVILEGES;

--snsappで作業開始宣言
USE snsapp;

/*ユーザー管理テーブル
 テーブルのエンジン設定(データの整合性を守るInnoDBを使用)
 ENGINE = InnoDB
 文字コード設定
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_unicode_ci;
  */
CREATE TABLE 
    Users (
        id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL, 
        email VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL,
        created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
        updated_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;
