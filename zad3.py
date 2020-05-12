import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    user = "admin",
    password = "admin1"
)

mysursor = mydb.cursor()

mysursor.execute("CREATE TABLE  `hasla` (\
    `id` int(10) NOT NULL auto_increment,\
    `tresc` varchar(255),\
    `kategoria` varchar(255),\
    PRIMARY KEY( `id` ),\
    UNIQUE(tresc)\
);")

cursor.execute("CREATE TABLE `zawodnicy` (\
    `id` INT NOT NULL AUTO_INCREMENT,\
    `imie` VARCHAR NOT NULL,\
    `nazwisko` VARCHAR NOT NULL,\
    `numer` INT,\
    PRIMARY KEY (`id`)\
);")



