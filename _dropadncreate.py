from database import DataBase

db = DataBase("collisions.db")
db.execute("DROP TABLE IF EXISTS STUDENTS")
db.execute("DROP TABLE IF EXISTS COLLISIONS")
db.execute(
    """
CREATE TABLE Students (id INTEGER NOT NULL PRIMARY KEY UNIQUE AUTOINCREMENT, full_name TEXT, code TEXT);
    """
)

# Таблица с подписками
db.execute(
    """
CREATE TABLE COLLISIONS
( 
    id INTEGER NOT NULL PRIMARY KEY UNIQUE AUTOINCREMENT,
    first_student_id INTEGER NOT NULL,
    second_student_id INTEGER NOT NULL,
    FOREIGN KEY (first_student_id) REFERENCES Students,
    FOREIGN KEY (second_student_id) REFERENCES Students,
    Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
    """
)

db.connection.commit()