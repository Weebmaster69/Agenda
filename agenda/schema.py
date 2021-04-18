instructions=[
    'SET FOREIGN_KEY_CHECKS=0;',
    'DROP TABLE IF EXISTS user;',
    'DROP TABLE IF EXISTS contacts;',
    'SET FOREIGN_KEY_CHECKS=1;',

    """
        CREATE TABLE user (
            id INT PRIMARY KEY AUTO_INCREMENT,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(100) NOT NULL
        )
    """
        ,
    """
        CREATE TABLE contact(
            id INT PRIMARY KEY AUTO_INCREMENT,
            created_by INT NOT NULL,
            name VARCHAR(50) NOT NULL,
            number VARCHAR(9) UNIQUE NOT NULL,
            job VARCHAR(50),
            FOREIGN KEY(created_by) REFERENCES user (id)
        );
    """

]