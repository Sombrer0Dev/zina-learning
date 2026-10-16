-- 1.1
CREATE TABLE courses (
    id    INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    hours REAL
);

-- 2.1
SELECT * FROM students;

-- 2.2
SELECT name, grade FROM students;

-- 2.3
SELECT * FROM students WHERE grade >= 4;

-- 2.4
SELECT * FROM students WHERE grade < 3 OR grade > 4.5;

-- 2.5
SELECT * FROM students WHERE name LIKE 'А%';

-- 2.6
SELECT * FROM students WHERE grade BETWEEN 3 AND 4;

-- 3.1
SELECT * FROM students ORDER BY grade DESC;

-- 3.2
SELECT name FROM students ORDER BY grade DESC LIMIT 3;

-- 3.3
SELECT name FROM students WHERE grade IS NOT NULL ORDER BY grade ASC LIMIT 2;

-- 4.1
SELECT * FROM students WHERE grade IS NULL;

-- 4.2
SELECT * FROM students WHERE grade IS NOT NULL;

-- 4.3
-- NULL означает "неизвестное значение". Сравнение NULL = NULL (и NULL с чем угодно)
-- само возвращает NULL, а не true — поэтому WHERE grade = NULL не находит строк,
-- даже если grade действительно NULL. Нужно использовать IS NULL / IS NOT NULL.

-- 5.1
SELECT COUNT(*) FROM students;

-- 5.2
SELECT COUNT(grade) FROM students;

-- 5.3
SELECT AVG(grade) FROM students;

-- 5.4
SELECT MAX(grade), MIN(grade) FROM students;

-- 5.5
SELECT SUM(grade) FROM students;
