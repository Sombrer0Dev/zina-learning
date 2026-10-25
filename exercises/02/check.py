import re
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).parent
SCHEMA = (HERE / "schema.sql").read_text()
ANSWERS_FILE = HERE / "answers.sql"

EXPECTED_QUERIES = {
    "0.1": "SELECT title FROM courses ORDER BY hours DESC;",
    "0.2": "SELECT COUNT(*) FROM enrollments WHERE grade IS NULL;",
    "1.1": """
        SELECT students.name, courses.title
        FROM enrollments
        JOIN students ON students.id = enrollments.student_id
        JOIN courses ON courses.id = enrollments.course_id;
    """,
    "1.2": """
        SELECT students.name, courses.title, enrollments.grade
        FROM enrollments
        JOIN students ON students.id = enrollments.student_id
        JOIN courses ON courses.id = enrollments.course_id
        WHERE enrollments.grade IS NOT NULL;
    """,
    "1.3": """
        SELECT courses.title
        FROM enrollments
        JOIN students ON students.id = enrollments.student_id
        JOIN courses ON courses.id = enrollments.course_id
        WHERE students.name = 'Аня';
    """,
    "2.1": """
        SELECT students.name, courses.title
        FROM students
        LEFT JOIN enrollments ON enrollments.student_id = students.id
        LEFT JOIN courses ON courses.id = enrollments.course_id;
    """,
    "2.2": """
        SELECT students.name
        FROM students
        LEFT JOIN enrollments ON enrollments.student_id = students.id
        WHERE enrollments.id IS NULL;
    """,
    "2.3": """
        SELECT courses.title
        FROM courses
        LEFT JOIN enrollments ON enrollments.course_id = courses.id
        WHERE enrollments.id IS NULL;
    """,
    "3.1": """
        SELECT students.name, COUNT(enrollments.id)
        FROM students
        LEFT JOIN enrollments ON enrollments.student_id = students.id
        GROUP BY students.id;
    """,
    "3.2": """
        SELECT courses.title, AVG(enrollments.grade)
        FROM enrollments
        JOIN courses ON courses.id = enrollments.course_id
        GROUP BY courses.id;
    """,
    "3.3": """
        SELECT courses.title, COUNT(enrollments.grade)
        FROM enrollments
        JOIN courses ON courses.id = enrollments.course_id
        GROUP BY courses.id;
    """,
    "3.4": """
        SELECT courses.title, MAX(enrollments.grade), MIN(enrollments.grade)
        FROM enrollments
        JOIN courses ON courses.id = enrollments.course_id
        GROUP BY courses.id;
    """,
    "4.1": """
        SELECT courses.title, AVG(enrollments.grade)
        FROM enrollments
        JOIN courses ON courses.id = enrollments.course_id
        GROUP BY courses.id
        HAVING AVG(enrollments.grade) >= 4;
    """,
    "4.2": """
        SELECT students.name, COUNT(enrollments.id)
        FROM students
        JOIN enrollments ON enrollments.student_id = students.id
        GROUP BY students.id
        HAVING COUNT(enrollments.id) >= 2;
    """,
    "5.1": """
        SELECT courses.title, AVG(enrollments.grade) AS avg_grade
        FROM enrollments
        JOIN courses ON courses.id = enrollments.course_id
        GROUP BY courses.id
        ORDER BY avg_grade DESC;
    """,
    "5.2": """
        SELECT students.name, COUNT(*)
        FROM enrollments
        JOIN students ON students.id = enrollments.student_id
        WHERE enrollments.grade IS NULL
        GROUP BY students.id;
    """,
}

ORDERED_TASKS = {"0.1", "5.1"}
MANUAL_TASKS = {"4.3"}


def parse_answers(text):
    marker = re.compile(r"^-- (\d+\.\d+)\s*$", re.MULTILINE)
    markers = list(marker.finditer(text))
    answers = {}
    for i, m in enumerate(markers):
        start = m.end()
        end = markers[i + 1].start() if i + 1 < len(markers) else len(text)
        answers[m.group(1)] = text[start:end].strip()
    return answers


def fresh_connection():
    conn = sqlite3.connect(":memory:")
    conn.executescript(SCHEMA)
    return conn


def check_query_task(task_id, student_sql):
    conn = fresh_connection()
    actual = conn.execute(student_sql).fetchall()
    expected = conn.execute(EXPECTED_QUERIES[task_id]).fetchall()
    if task_id in ORDERED_TASKS:
        assert actual == expected, f"ожидалось {expected}, получено {actual}"
    else:
        assert sorted(actual) == sorted(expected), (
            f"ожидалось (в любом порядке) {sorted(expected)}, получено {sorted(actual)}"
        )


def main():
    answers = parse_answers(ANSWERS_FILE.read_text())
    task_ids = sorted(
        set(EXPECTED_QUERIES) | MANUAL_TASKS, key=lambda t: tuple(map(int, t.split(".")))
    )

    passed, failed = [], []
    for task_id in task_ids:
        if task_id in MANUAL_TASKS:
            continue
        student_sql = answers.get(task_id, "")
        if not student_sql:
            failed.append((task_id, "нет ответа"))
            continue
        try:
            check_query_task(task_id, student_sql)
            passed.append(task_id)
        except AssertionError as e:
            failed.append((task_id, str(e)))
        except sqlite3.Error as e:
            failed.append((task_id, f"ошибка SQL: {e}"))

    print(f"Пройдено: {len(passed)}, провалено: {len(failed)}")
    for task_id, reason in failed:
        print(f"  [FAIL] {task_id}: {reason}")
    print("\nЗадание 4.3 — текстовый ответ, проверяется вручную.")

    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
