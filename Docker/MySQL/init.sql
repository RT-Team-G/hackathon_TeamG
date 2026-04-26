-- もしも古いsnsappがあったらいったん消す(やり直し用)
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
        id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
        name VARCHAR(255) NOT NULL, 
        email VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL,
        created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
        updated_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
        -- 主キー
        PRIMARY KEY (id)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- Postテーブル作成
CREATE TABLE 
    Posts (
        id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT ,
        user_id BIGINT UNSIGNED NOT NULL, 
        content TEXT,
        created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
        -- 主キー
        PRIMARY KEY (id),
        -- インデックス(索引)の作成：検索を速くするため
        KEY idx_posts_user_id (user_id),
        -- 外部キー制約：Usersテーブルのidと紐付け
        CONSTRAINT fk_posts_user FOREIGN KEY (user_id) REFERENCES Users (id)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;


-- Trainingテーブル作成
CREATE TABLE 
    Training (
        id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
        menu_name VARCHAR(255) NOT NULL,
        -- 主キー
        PRIMARY KEY (id)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- Reactions テーブルの作成
CREATE TABLE 
    Reactions (
       id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
       reaction TEXT,
       created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
       --主キー
       PRIMARY KEY (id) 
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- Commentsテーブル作成
CREATE TABLE 
    Comments (
        id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
        user_id BIGINT UNSIGNED NOT NULL,
        post_id BIGINT UNSIGNED NOT NULL,
        content TEXT,
        created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
        --主キー
        PRIMARY KEY (id),
        --インデックス索引
        KEY idx_comments_user_id (user_id),
        KEY idx_comments_post_id (post_id),
        --外部キー
        CONSTRAINT fk_comments_user FOREIGN KEY (user_id) REFERENCES Users (id),
        CONSTRAINT fk_comments_post FOREIGN KEY (post_id) REFERENCES Posts (id)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- Post_Reactionテーブルの作成
CREATE TABLE 
    PostReaction (
        id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
        user_id BIGINT UNSIGNED NOT NULL,
        post_id BIGINT UNSIGNED NOT NULL,
        reaction_id BIGINT UNSIGNED NOT NULL,
        created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
        --主キー
        PRIMARY KEY (id),
        --インデクス索引
        KEY idx_post_reaction_user_id (user_id),
        KEY idx_post_reaction_post_id (post_id),
        KEY idx_post_reaction_reaction_id (reaction_id),
        --外部キー
        CONSTRAINT fk_post_reaction_user FOREIGN KEY (user_id) REFERENCES Users (id),
        CONSTRAINT fk_post_reaction_post FOREIGN KEY (post_id) REFERENCES Posts (id),
        CONSTRAINT fk_post_reaction_reaction FOREIGN KEY (reaction_id) REFERENCES Reactions (id)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- Post_Trainingテーブル作成
CREATE TABLE 
   Post_Training (
        id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
        user_id BIGINT UNSIGNED NOT NULL,
        post_id BIGINT UNSIGNED NOT NULL,
        training_id BIGINT UNSIGNED NOT NULL,
        reps INT,
        time INT,
        set INT,
        created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
        --主キー
        PRIMARY KEY (id),
        --インデックス索引
        KEY idx_post_training_user_id (user_id),
        KEY idx_post_training_post_id (post_id),
        KEY idx_post_training_training_id (training_id),
        --外部キー
        CONSTRAINT fk_post_training_user FOREIGN KEY (user_id) REFERENCES Users (id),
        CONSTRAINT fk_post_training_post FOREIGN KEY (post_id) REFERENCES Posts (id),
        CONSTRAINT fk_post_training_training FOREIGN KEY (training_id) REFERENCES Training (id)
   ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

--テスト用 Users
INSERT INTO Users (name, email, password) VALUES 
('佐藤一郎', 'sato@example', '12345'),
('鈴木次郎', 'suzuki@example', '98765')

-- Posts
INSERT INTO Posts (user_id, content) VALUES 
(1, 'こんにちは!初めての投稿です'),
(1, '今日は腕立てふせ10回やりました！'),
(2, '今日はスクワット1000かいやりました。')
