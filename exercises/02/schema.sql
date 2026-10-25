CREATE TABLE students (
    id   INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE courses (
    id    INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    hours REAL
);

CREATE TABLE enrollments (
    id         INTEGER PRIMARY KEY,
    student_id INTEGER NOT NULL REFERENCES students(id),
    course_id  INTEGER NOT NULL REFERENCES courses(id),
    grade      REAL
);

INSERT INTO students (name) VALUES
    ('Аня'),      -- 1
    ('Борис'),    -- 2
    ('Вера'),     -- 3
    ('Глеб'),     -- 4
    ('Дина'),     -- 5
    ('Егор');     -- 6 — ни на один курс не записан

INSERT INTO courses (title, hours) VALUES
    ('Python', 40),      -- 1
    ('SQL', 30),         -- 2
    ('Математика', 50),  -- 3
    ('История', 20);     -- 4 — на курс никто не записан

INSERT INTO enrollments (student_id, course_id, grade) VALUES
    (1, 1, 5.0),   -- Аня — Python
    (1, 2, 4.5),   -- Аня — SQL
    (1, 3, 4.0),   -- Аня — Математика
    (2, 1, 3.5),   -- Борис — Python
    (3, 2, 5.0),   -- Вера — SQL
    (3, 3, NULL),  -- Вера — Математика, оценка ещё не выставлена
    (4, 1, 2.5),   -- Глеб — Python
    (4, 2, 3.0),   -- Глеб — SQL
    (5, 3, 4.5);   -- Дина — Математика
