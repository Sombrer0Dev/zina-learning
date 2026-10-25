-- 0.1
SELECT title FROM courses ORDER BY hours DESC;

-- 0.2
SELECT COUNT(*) FROM enrollments WHERE grade IS NULL;

-- 1.1
SELECT students.name, courses.title
FROM enrollments
JOIN students ON students.id = enrollments.student_id
JOIN courses ON courses.id = enrollments.course_id;

-- 1.2
SELECT students.name, courses.title, enrollments.grade
FROM enrollments
JOIN students ON students.id = enrollments.student_id
JOIN courses ON courses.id = enrollments.course_id
WHERE enrollments.grade IS NOT NULL;

-- 1.3
SELECT courses.title
FROM enrollments
JOIN students ON students.id = enrollments.student_id
JOIN courses ON courses.id = enrollments.course_id
WHERE students.name = 'Аня';

-- 2.1
SELECT students.name, courses.title
FROM students
LEFT JOIN enrollments ON enrollments.student_id = students.id
LEFT JOIN courses ON courses.id = enrollments.course_id;

-- 2.2
SELECT students.name
FROM students
LEFT JOIN enrollments ON enrollments.student_id = students.id
WHERE enrollments.id IS NULL;

-- 2.3
SELECT courses.title
FROM courses
LEFT JOIN enrollments ON enrollments.course_id = courses.id
WHERE enrollments.id IS NULL;

-- 3.1
SELECT students.name, COUNT(enrollments.id)
FROM students
LEFT JOIN enrollments ON enrollments.student_id = students.id
GROUP BY students.id;

-- 3.2
SELECT courses.title, AVG(enrollments.grade)
FROM enrollments
JOIN courses ON courses.id = enrollments.course_id
GROUP BY courses.id;

-- 3.3
SELECT courses.title, COUNT(enrollments.grade)
FROM enrollments
JOIN courses ON courses.id = enrollments.course_id
GROUP BY courses.id;

-- 3.4
SELECT courses.title, MAX(enrollments.grade), MIN(enrollments.grade)
FROM enrollments
JOIN courses ON courses.id = enrollments.course_id
GROUP BY courses.id;

-- 4.1
SELECT courses.title, AVG(enrollments.grade)
FROM enrollments
JOIN courses ON courses.id = enrollments.course_id
GROUP BY courses.id
HAVING AVG(enrollments.grade) >= 4;

-- 4.2
SELECT students.name, COUNT(enrollments.id)
FROM students
JOIN enrollments ON enrollments.student_id = students.id
GROUP BY students.id
HAVING COUNT(enrollments.id) >= 2;

-- 4.3
-- WHERE фильтрует строки ДО группировки — на этом этапе ещё нет значения
-- AVG(grade) для группы, есть только отдельные строки, поэтому агрегатную
-- функцию в WHERE использовать нельзя. HAVING фильтрует уже готовые группы
-- ПОСЛЕ GROUP BY, когда AVG(grade) по каждой группе уже посчитан — именно
-- поэтому условие на результат агрегатной функции пишут в HAVING.

-- 5.1
SELECT courses.title, AVG(enrollments.grade) AS avg_grade
FROM enrollments
JOIN courses ON courses.id = enrollments.course_id
GROUP BY courses.id
ORDER BY avg_grade DESC;

-- 5.2
SELECT students.name, COUNT(*)
FROM enrollments
JOIN students ON students.id = enrollments.student_id
WHERE enrollments.grade IS NULL
GROUP BY students.id;
