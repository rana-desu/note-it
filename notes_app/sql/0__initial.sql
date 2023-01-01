-- A singleton table containing the database version
CREATE TABLE database_version(
    unique_value ENUM('unique') UNIQUE NOT NULL DEFAULT 'unique',
    database_version INTEGER NOT NULL
);

-- insert inital value
INSERT INTO database_version(database_version)
VALUES(0);

-- users registered data
CREATE TABLE IF NOT EXISTS users (
    user_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    username VARCHAR(150) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password_hash VARCHAR(150) NOT NULL
);

-- notes
CREATE TABLE IF NOT EXISTS notes (
    note_id int PRIMARY KEY NOT NULL AUTO_INCREMENT,
    owner_id int NOT NULL,
    title varchar(500) NOT NULL,
    description varchar(1000),
    date_created timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP(),
    INDEX (owner_id),
    FOREIGN KEY (owner_id)
      REFERENCES users(user_id)
      ON DELETE CASCADE
);
