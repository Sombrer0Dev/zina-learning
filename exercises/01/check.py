import re
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).parent
SCHEMA = (HERE / "schema.sql").read_text()
ANSWERS_FILE = HERE / "answers.sql"

EXPECTED_QUERIES = {
    "2.1": "SELECT * FROM students;",
    "2.2": "SELECT name, grade FROM students;",
    "2.3": "SELECT * FROM students WHERE grade >= 4;",
    "2.4": "SELECT * FROM students WHERE grade < 3 OR grade > 4.5;",
    "2.5": "SELECT * FROM students WHERE name LIKE 'А%';",
    "2.6": "SELECT * FROM students WHERE grade BETWEEN 3 AND 4;",
    "3.1": "SELECT * FROM students ORDER BY grade DESC;",
    "3.2": "SELECT name FROM students ORDER BY grade DESC LIMIT 3;",
    "3.3": "SELECT name FROM students WHERE grade IS NOT NULL ORDER BY grade ASC LIMIT 2;",
    "4.1": "SELECT * FROM students WHERE grade IS NULL;",
    "4.2": "SELECT * FROM students WHERE grade IS NOT NULL;",
    "5.1": "SELECT COUNT(*) FROM students;",
    "5.2": "SELECT COUNT(grade) FROM students;",
    "5.3": "SELECT AVG(grade) FROM students;",
    "5.4": "SELECT MAX(grade), MIN(grade) FROM students;",
    "5.5": "SELECT SUM(grade) FROM students;",
}

ORDERED_TASKS = {"3.1", "3.2", "3.3"}
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


def check_task_1_1(student_sql):
    conn = fresh_connection()
    conn.executescript(student_sql)
    columns = {row[1]: row for row in conn.execute("PRAGMA table_info(courses);")}
    assert "id" in columns, "нет столбца id"
    assert "title" in columns, "нет столбца title"
    assert "hours" in columns, "нет столбца hours"
    assert columns["title"][3] == 1, "title должен быть NOT NULL"
    assert columns["id"][5] == 1, "id должен быть PRIMARY KEY"


def main():
    answers = parse_answers(ANSWERS_FILE.read_text())
    task_ids = ["1.1"] + sorted(
        EXPECTED_QUERIES, key=lambda t: tuple(map(int, t.split(".")))
    )

    passed, failed = [], []
    for task_id in task_ids:
        student_sql = answers.get(task_id, "")
        if not student_sql:
            failed.append((task_id, "нет ответа"))
            continue
        try:
            if task_id == "1.1":
                check_task_1_1(student_sql)
            else:
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
