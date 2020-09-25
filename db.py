import mysql.connector

# Database configuration
config = {
    'user': 'spotify-user',
    'password': 'spotify-user',
    'host': 'localhost',
    'database': 'top_charts'
}

# Connect to database
db = mysql.connector.connect(**config)

# Cursor object
cursor = db.cursor()


# Create database
def create_database():
    cursor.execute('''
        CREATE DATABASE IF NOT EXISTS top_charts DEFAULT CHARACTER SET 'utf8'
    ''')

# Create tables function
def create_table(table_name, second_col):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS `%s` (
            `id` int(11) NOT NULL AUTO_INCREMENT,
            `artist` VARCHAR(255),
            `%s` INT,
            PRIMARY KEY(id)
        )
    ''', (table_name, second_col))
    print(f"Table {table_name} was just created.")

# Create row function
def create_row(table_name, second_col, artist, position):
    cursor.execute('''
        INSERT INTO `%s` (artist, `%s`) VALUES (%s, %s)
    ''', (table_name, second_col, artist, position))

    db.commit()
    print(f"Row {cursor.lastrowid} was just created.")

# Check for duplicates function
def check_duplicates(name):
    cursor.execute('SHOW tables')
    tables = cursor.fetchall()

    for i in tables:
        for j in range(len(i)):
            if i[j] == f"'{name}'":
                return True
    return False