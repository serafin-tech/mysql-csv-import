-- definition of schema and table for testing

CREATE DATABASE `testy-importu` DEFAULT CHARACTER SET utf8 COLLATE utf8_polish_ci;

CREATE TABLE `testowa` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `col_char` varchar(45) NOT NULL DEFAULT 'col_a',
  `col_int` int(11) DEFAULT NULL,
  `col_date` date DEFAULT cast(current_timestamp() as date),
  PRIMARY KEY (`id`)
);

INSERT INTO `testowa`(col_char,col_int,col_date) VALUES('predefined', 99, date(now()));
