/*改变字符集*/
charset utf8;

/*创建数据库*/
CREATE DATABASE IF NOT EXISTS qq CHARSET utf8;
use qq;
/*用户表*/
CREATE TABLE IF NOT EXISTS users (
       user_id varchar(80) not null,           /*用户id*/
       user_pwd varchar(25) not null,       /*用户密码*/
       user_name varchar(80) not null,       /*用户名*/
       user_icon varchar(100) not null,       /*用户头像*/
PRIMARY KEY (user_id));

CREATE TABLE IF NOT EXISTS users (user_id varchar(80) not null,user_pwd varchar(25) not null,user_name varchar(80) not null,user_icon varchar(100) not null,PRIMARY KEY (user_id)); 

CREATE TABLE IF NOT EXISTS friends(
    user_id1 varchar(80) not null,       /*用户id1*/
    user_id2 varchar(80) not null,       /*用户id2*/
PRIMARY KEY (user_id1,user_id2));

CREATE TABLE IF NOT EXISTS friends(user_id1 varchar(80) not null,user_id2 varchar(80) not null,PRIMARY KEY (user_id1,user_id2)); 

/*用户表数据*/
INSERT INTO users VALUES('111','1234','关云长','28');
INSERT INTO users VALUES('222','1234','赵子龙','25');
INSERT INTO users VALUES('444','1234','苏伯柟','18');
INSERT INTO users VALUES('888','1234','张子房','23');

/*用户好友id1和用户好友id2互为好友*/
INSERT INTO friends VALUES('111','222');
INSERT INTO friends VALUES('111','333');
INSERT INTO friends VALUES('888','111');
INSERT INTO friends VALUES('222','111');

/*更新数据*/
UPDATE users SET user_name="苏伯柟" WHERE user_name="苏叶";
/*删除数据*/
DELETE FROM users WHERE user_id='999';
