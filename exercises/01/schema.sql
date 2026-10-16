CREATE TABLE students (
    id    INTEGER PRIMARY KEY,
    name  TEXT NOT NULL,
    grade REAL
);

INSERT INTO students (name, grade) VALUES
    ('Аня',     5.0),
    ('Борис',   3.5),
    ('Вера',    4.0),
    ('Глеб',    2.5),
    ('Дина',    4.5),
    ('Егор',    NULL),
    ('Жанна',   5.0),
    ('Игорь',   3.0),
    ('Катя',    4.0),
    ('Леша',    NULL),
    ('Маша',    4.5),
    ('Никита',  2.0);
