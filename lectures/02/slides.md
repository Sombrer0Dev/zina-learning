---
title: GROUP BY и JOIN
sub_title: Урок 2 — связывание таблиц и агрегация по группам
author: Zina Learning
---

<!-- jump_to_middle -->

# Урок 2

## GROUP BY и JOIN

<!-- end_slide -->

# Проблема одной таблицы

```
id | name | course   | grade
1  | Аня  | Python   | 5.0
2  | Аня  | SQL      | 4.5
3  | Борис| Python   | 3.5
```

<!-- pause -->

Имя "Аня" дублируется. Один студент — несколько курсов, одна оценка на каждый.

<!-- pause -->

**Решение — нормализация:** разбить на несколько таблиц, связанных ссылками.

<!-- end_slide -->

# Три таблицы вместо одной

```sql
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
```

<!-- pause -->

`enrollments` — таблица-связка: студент + курс + оценка.

<!-- end_slide -->

# Зачем нормализация: аномалии

Если хранить всё как одну широкую таблицу "студент + курс + оценка":

<!-- pause -->

- **вставка** — нельзя добавить курс, если на него никто не записан
<!-- pause -->
- **обновление** — переименовали курс → нужно исправить во всех строках
<!-- pause -->
- **удаление** — удалили последнего студента курса → потеряли сам курс

<!-- pause -->

Нормализация устраняет все три: каждый факт живёт в одной строке одной таблицы.

<!-- end_slide -->

# Уровни нормализации

Нормализация — не одно действие, а лестница всё более строгих правил.

<!-- pause -->

Каждая следующая форма = предыдущая форма + своё дополнительное требование.

<!-- pause -->

1NF → 2NF → 3NF — то, что нужно знать и уметь применять на практике.

<!-- end_slide -->

# 1NF — первая нормальная форма

**Требование:** каждый столбец хранит одно атомарное значение. Нет списков, нет повторяющихся групп в одной ячейке.

<!-- pause -->

**Нарушение:**

```
id | name | courses
1  | Аня  | "Python, SQL, Математика"
```

Три курса слиплись в одну строку одной ячейки — чтобы найти "кто записан на SQL", придётся разбирать текст внутри ячейки.

<!-- pause -->

**Исправление:** одна строка = один факт "студент записан на курс":

```
student_id | course
1          | Python
1          | SQL
1          | Математика
```

<!-- pause -->

Это ровно то, что делает наша таблица `enrollments` — по одной строке на пару (студент, курс).

<!-- end_slide -->

# 2NF — вторая нормальная форма

**Требование:** 1NF + каждый неключевой столбец зависит от **всего** составного ключа, а не только от его части.

<!-- pause -->

Правило вступает в игру только когда первичный ключ составной (из нескольких столбцов).

<!-- pause -->

**Нарушение:** ключ `enrollments` — пара `(student_id, course_id)`, и в этой же таблице хранится `course_title`:

```
student_id | course_id | course_title | grade
1          | 2         | "SQL"        | 4.5
3          | 2         | "SQL"        | 5.0
```

<!-- pause -->

`course_title` зависит только от `course_id` — то есть от **части** ключа, а не от пары целиком. Значение "SQL" дублируется для каждого студента на этом курсе.

<!-- pause -->

**Исправление:** вынести `course_title` в таблицу `courses`, где `course_id` — целый первичный ключ сам по себе.

<!-- pause -->

В нашей схеме `enrollments.id` — отдельный суррогатный ключ, не составной, поэтому частичных зависимостей там в принципе не бывает — 2NF выполняется автоматически.

<!-- end_slide -->

# 3NF — третья нормальная форма

**Требование:** 2NF + нет транзитивных зависимостей между неключевыми столбцами (один неключевой столбец не должен зависеть от другого неключевого столбца).

<!-- pause -->

**Нарушение:** если бы в `students` хранились ещё `city` и `city_population`:

```
id | name | city    | city_population
1  | Аня  | Москва  | 13000000
2  | Борис| Москва  | 13000000
```

<!-- pause -->

`city_population` зависит от `city`, а `city` — не ключ. Получается цепочка: `id → city → city_population` — зависимость транзитивная, через другой неключевой столбец. И снова дублирование: население Москвы повторяется в каждой строке студента из Москвы.

<!-- pause -->

**Исправление:** вынести `city`/`city_population` в отдельную таблицу `cities`, а в `students` оставить только `city_id`.

<!-- end_slide -->

# Более высокие уровни (кратко)

3NF хватает почти всегда. Что есть дальше — скорее для общего кругозора:

<!-- pause -->

- **BCNF** (Boyce-Codd NF) — усиленная версия 3NF для редкого случая, когда у таблицы несколько потенциальных ключей, пересекающихся по столбцам
<!-- pause -->
- **4NF** — убирает многозначные зависимости (когда один столбец определяет не одно значение другого, а целый независимый набор)
<!-- pause -->
- **5NF** — убирает избыточность, которая проявляется только при разбиении таблицы на несколько частей и обратном соединении (join dependency)

<!-- pause -->

На практике до них добираются редко — это скорее академический предел, чем повседневный инструмент.

<!-- end_slide -->

# Принцип за всеми формами

**Неключевой столбец должен зависеть от ключа своей таблицы — и только от него.**

<!-- pause -->

Не от части ключа (2NF), не от другого неключевого столбца (3NF), не от списка в одной ячейке (1NF).

<!-- end_slide -->

# Нормализация — это компромисс

Больше таблиц → больше `JOIN`'ов в запросах.

<!-- pause -->

Обратный приём — **денормализация** (сознательное дублирование ради скорости).

<!-- pause -->

Начинать стоит с нормализованной схемы, денормализовать — осознанно и по необходимости.

<!-- end_slide -->

# JOIN — склеиваем таблицы

```sql
SELECT students.name, courses.title
FROM enrollments
JOIN students ON students.id = enrollments.student_id
JOIN courses ON courses.id = enrollments.course_id;
```

<!-- pause -->

Для каждой строки `enrollments` находим строку `students` и строку `courses` с совпадающим `id`.

<!-- end_slide -->

# INNER JOIN — только совпадения

`JOIN` по умолчанию — это `INNER JOIN`.

<!-- pause -->

В результат попадают только строки, у которых пара нашлась **в обеих** таблицах.

<!-- pause -->

Курс без единого студента → не появится в `enrollments JOIN courses`.

<!-- end_slide -->

# LEFT JOIN — все строки слева

```sql
SELECT students.name, courses.title
FROM students
LEFT JOIN enrollments ON enrollments.student_id = students.id
LEFT JOIN courses ON courses.id = enrollments.course_id;
```

<!-- pause -->

Студент без курсов — остаётся в результате, но с `NULL` вместо курса.

<!-- end_slide -->

# Приём: "у кого чего-то нет"

```sql
SELECT students.name
FROM students
LEFT JOIN enrollments ON enrollments.student_id = students.id
WHERE enrollments.id IS NULL;
```

<!-- pause -->

`LEFT JOIN` + `WHERE правая.id IS NULL` — классический способ найти непарные строки.

<!-- end_slide -->

# INNER JOIN vs LEFT JOIN

<!-- column_layout: [1, 1] -->

<!-- column: 0 -->

## INNER JOIN

- только строки с парой в обеих таблицах
- непарные строки пропадают

<!-- column: 1 -->

## LEFT JOIN

- все строки левой таблицы
- нет пары → `NULL` справа

<!-- reset_layout -->

<!-- end_slide -->

# GROUP BY — агрегат для каждой группы

```sql
SELECT courses.title, AVG(enrollments.grade)
FROM enrollments
JOIN courses ON courses.id = enrollments.course_id
GROUP BY courses.id;
```

<!-- pause -->

Раньше агрегат сворачивал всю таблицу в одно число. `GROUP BY` — одно число **на группу**.

<!-- end_slide -->

# Правило GROUP BY

В `SELECT` при `GROUP BY` можно упоминать только:

<!-- pause -->

- столбцы, по которым идёт группировка
<!-- pause -->
- агрегатные функции

<!-- pause -->

Иначе непонятно, какое значение показывать для группы из нескольких строк.

<!-- end_slide -->

# COUNT(*) vs COUNT(столбец) + LEFT JOIN

```sql
SELECT students.name, COUNT(enrollments.id)
FROM students
LEFT JOIN enrollments ON enrollments.student_id = students.id
GROUP BY students.id;
```

<!-- pause -->

Студент без курсов: `LEFT JOIN` даёт строку с `enrollments.id = NULL`.

<!-- pause -->

`COUNT(*)` посчитал бы 1. `COUNT(enrollments.id)` игнорирует `NULL` → 0.

<!-- end_slide -->

# HAVING — фильтр по группам

`WHERE AVG(grade) >= 4` — ошибка: на момент `WHERE` агрегата ещё нет.

<!-- pause -->

```sql
SELECT courses.title, AVG(enrollments.grade)
FROM enrollments
JOIN courses ON courses.id = enrollments.course_id
GROUP BY courses.id
HAVING AVG(enrollments.grade) >= 4;
```

<!-- end_slide -->

# WHERE vs HAVING

| | Когда | Что фильтрует |
|---|---|---|
| `WHERE` | до `GROUP BY` | отдельные строки |
| `HAVING` | после `GROUP BY` | группы (можно агрегаты) |

<!-- pause -->

Можно использовать оба в одном запросе — за разные этапы отвечают.

<!-- end_slide -->

# Порядок выполнения запроса

```
FROM / JOIN → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT
```

<!-- pause -->

Пишем в одном порядке, выполняется — в другом. Поэтому `WHERE` не видит агрегаты, а `HAVING` видит.

<!-- end_slide -->

# Мостик к Python

```python
import sqlite3

conn = sqlite3.connect("school.db")
cursor = conn.cursor()
cursor.execute("""
    SELECT courses.title, AVG(enrollments.grade)
    FROM enrollments
    JOIN courses ON courses.id = enrollments.course_id
    GROUP BY courses.id
    HAVING AVG(enrollments.grade) >= 4;
""")
for title, avg_grade in cursor.fetchall():
    print(title, avg_grade)
conn.close()
```

<!-- end_slide -->

# Что дальше

- `INSERT` / `UPDATE` / `DELETE`
- Транзакции
- Переход на PostgreSQL

<!-- end_slide -->

# Практика

Открываем SQLite, пишем запросы с JOIN и GROUP BY.
