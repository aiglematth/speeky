CREATE DATABASE IF NOT EXISTS "messages";
CREATE TABLE IF NOT EXISTS "messages" (
	user    varchar(30),
	message text(4096)
);

CREATE USER IF NOT EXISTS 'speeky'@'localhost' IDENTIFIED BY 'speeky';
GRANT ALL ON `messages`.* TO 'speeky'@'localhost' IDENTIFIED BY 'speeky';

