#Utworzenie bazy danych o nazwie "cinema_db"
CREATE SCHEMA `cinema_db` ;

#Utworzenie tabeli 'client'
CREATE TABLE `cinema_db`.`client` (
  `id_client` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(45) NOT NULL,
  `last_name` VARCHAR(45) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `type` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id_client`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = UTF8MB4
COMMENT = 'Client table';

#Utworzenie tabeli 'movie'
CREATE TABLE `cinema_db`.`movie` (
  `id_movie` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(100) NOT NULL,
  `director` VARCHAR(45) NOT NULL,
  `year_of_prod` INT NOT NULL,
  `country` VARCHAR(45) NOT NULL,
  `duration` INT NOT NULL,
  `language` VARCHAR(45) NOT NULL,
  `dimension` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id_movie`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = UTF8MB4
COMMENT = 'Movie table.';

#Utworzenie tabeli 'room'
CREATE TABLE `cinema_db`.`room` (
  `id_room` INT NOT NULL AUTO_INCREMENT,
  `num_of_rows` INT NOT NULL,
  `seats_per_row` INT NOT NULL,
  PRIMARY KEY (`id_room`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = UTF8MB4
COMMENT = 'Room table';

#Utworzenie tabeli 'transaction'
CREATE TABLE `cinema_db`.`transaction` (
  `id_transaction` INT NOT NULL AUTO_INCREMENT,
  `id_client` INT NOT NULL,
  `date` DATETIME NOT NULL,
  `amount` DECIMAL(5,2) NOT NULL,
  `currency` VARCHAR(45) NOT NULL,
  `status` VARCHAR(45) NOT NULL,
  `pay_method` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id_transaction`),
  CONSTRAINT `id_client`
    FOREIGN KEY (`id_client`)
    REFERENCES `cinema_db`.`client` (`id_client`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = UTF8MB4
COMMENT = 'Transactions table.';

#Utworzenie tabeli 'show'
CREATE TABLE `cinema_db`.`show` (
  `id_show` INT NOT NULL AUTO_INCREMENT,
  `id_movie` INT NOT NULL,
  `id_room` INT NOT NULL,
  `date` DATE NOT NULL,
  `time` TIME NOT NULL,
  PRIMARY KEY (`id_show`),
  CONSTRAINT `id_movie`
	FOREIGN KEY (`id_movie`)
	REFERENCES `cinema_db`.`movie` (`id_movie`)
	ON DELETE CASCADE
	ON UPDATE CASCADE,
  CONSTRAINT `id_room`
	FOREIGN KEY (`id_room`)
	REFERENCES `cinema_db`.`room` (`id_room`)
	ON DELETE CASCADE
	ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = UTF8MB4
COMMENT = 'Show table';

#Utworzenie tabeli 'ticket'
CREATE TABLE `cinema_db`.`ticket` (
  `id_ticket` INT NOT NULL AUTO_INCREMENT,
  `id_transaction` INT NOT NULL,
  `id_show` INT NOT NULL,
  `row` INT NOT NULL,
  `seat` INT NOT NULL,
  PRIMARY KEY (`id_ticket`),
  CONSTRAINT `id_transaction`
    FOREIGN KEY (`id_transaction`)
    REFERENCES `cinema_db`.`transaction` (`id_transaction`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `id_show`
    FOREIGN KEY (`id_show`)
    REFERENCES `cinema_db`.`show` (`id_show`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = UTF8MB4
COMMENT = 'Ticket table';


#Wypełnienie tabeli 'client' przykładowymi danymi
INSERT INTO `cinema_db`.`client` VALUES (1, "Adam", "Kowalski", "adamk@op.pl", "normal");
INSERT INTO `cinema_db`.`client` VALUES (2, "Maciej", "Wolski", "maciek123@gmail.com", "student");
INSERT INTO `cinema_db`.`client` VALUES (3, "Kamil", "Mak", "kamilmak@wp.pl", "normal");
INSERT INTO `cinema_db`.`client` VALUES (4, "Kajetan", "Pietrzak", "kajtopietrzak@gmail.com", "child");

#Wypełnienie tabeli 'movie' przykładowymi danymi
INSERT INTO `cinema_db`.`movie` VALUES (1, 'The Shawshank Redemption', 'Frank Darabont', 1994, 'USA', 142, 'English', '2D');
INSERT INTO `cinema_db`.`movie` VALUES (2, 'The Godfather', 'Francis Ford Coppola', 1972, 'USA', 175, 'English', '2D');
INSERT INTO `cinema_db`.`movie` VALUES (3, 'The Dark Knight', 'Christopher Nolan', 2008, 'USA', 152, 'English', '2D');
INSERT INTO `cinema_db`.`movie` VALUES (4, 'Pulp Fiction', 'Quentin Tarantino', 1994, 'USA', 154, 'English', '2D');
INSERT INTO `cinema_db`.`movie` VALUES (5, 'The Lord of the Rings: The Fellowship of the Ring', 'Peter Jackson', 2001, 'USA', 178, 'English', '2D');
INSERT INTO `cinema_db`.`movie` VALUES (6, 'Forrest Gump', 'Robert Zemeckis', 1994, 'USA', 142, 'English', '2D');

#Wypełnienie tabeli 'room' przykładowymi danymi
INSERT INTO `cinema_db`.`room` VALUES (1, 10, 15);
INSERT INTO `cinema_db`.`room` VALUES (2, 18, 25);
INSERT INTO `cinema_db`.`room` VALUES (3, 12, 18);
INSERT INTO `cinema_db`.`room` VALUES (4, 12, 20);

#Wypełnienie tabeli 'transaction' przykładowymi danymi
INSERT INTO `cinema_db`.`transaction` VALUES (1, 2, '2023-04-21 10:05:49', 25.99, 'USD', 'completed', 'on-site');
INSERT INTO `cinema_db`.`transaction` VALUES (2, 3, '2023-04-22 11:52:03', 10.50, 'EUR', 'completed', 'on-line');
INSERT INTO `cinema_db`.`transaction` VALUES (3, 1, '2023-04-23 18:27:45', 8.75, 'USD', 'pending', 'on-line');
INSERT INTO `cinema_db`.`transaction` VALUES (4, 1, '2023-04-23 19:09:38', 35.00, 'GBP', 'completed', 'on-site');
INSERT INTO `cinema_db`.`transaction` VALUES (5, 4, '2023-04-23 23:12:44', 16.99, 'EUR', 'completed', 'on_line');

#Wypełnienie tabeli 'show' przykładowymi danymi
INSERT INTO `cinema_db`.`show` VALUES (1, 3, 2, '2023-05-10', '15:30:00');
INSERT INTO `cinema_db`.`show` VALUES (2, 2, 1, '2023-05-11', '17:00:00');
INSERT INTO `cinema_db`.`show` VALUES (3, 1, 3, '2023-05-12', '19:30:00');
INSERT INTO `cinema_db`.`show` VALUES (4, 4, 2, '2023-05-13', '14:00:00');
INSERT INTO `cinema_db`.`show` VALUES (5, 2, 4, '2023-05-14', '21:00:00');

#Wypełnienie tabeli 'ticket' przykładowymi danymi
INSERT INTO `cinema_db`.`ticket` VALUES (1, 1, 2, 1, 12);
INSERT INTO `cinema_db`.`ticket` VALUES (2, 1, 2, 7, 13);
INSERT INTO `cinema_db`.`ticket` VALUES (3, 2, 1, 4, 7);
INSERT INTO `cinema_db`.`ticket` VALUES (4, 3, 3, 2, 5);
INSERT INTO `cinema_db`.`ticket` VALUES (5, 3, 4, 8, 6);
INSERT INTO `cinema_db`.`ticket` VALUES (6, 4, 4, 6, 10);
INSERT INTO `cinema_db`.`ticket` VALUES (7, 5, 5, 5, 4);
INSERT INTO `cinema_db`.`ticket` VALUES (8, 5, 5, 2, 5);

SELECT * FROM `cinema_db`.`ticket`;