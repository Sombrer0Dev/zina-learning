---
title: Введение в SQL
sub_title: Урок 1 — реляционные базы данных и SQLite
author: Zina Learning
---

<!-- jump_to_middle -->

# Урок 1

## Введение в SQL и реляционные базы данных

<!-- end_slide -->

# Зачем нужен SQL

Данные в Python живут в памяти программы: списки, словари, объекты.

Это ломается, когда:

<!-- pause -->

- данных больше, чем помещается в память
<!-- pause -->
- с данными одновременно работает несколько процессов
<!-- pause -->
- данные должны переживать перезапуск программы

<!-- pause -->

**Решение — база данных.** SQL — язык для описания структуры данных и работы с ними.

<!-- end_slide -->

# А почему не просто файлы?

Логичная идея: сохранять данные в CSV / JSON / текст.

Переживает перезапуск — но:

<!-- pause -->

- **поиск** — нужно читать и парсить весь файл целиком, индексов нет
<!-- pause -->
- **параллельная запись** — два процесса пишут в файл одновременно → повреждённые данные
<!-- pause -->
- **целостность** — формат файла ничего не проверяет
<!-- pause -->
- **надёжность** — падение программы посреди записи → неконсистентный файл
<!-- pause -->
- **разбор** — парсинг/сериализацию пишешь и отлаживаешь сама

<!-- pause -->

Ок для мелких скриптов. Не масштабируется.

<!-- end_slide -->

# Императивный vs декларативный

## Python (императивно: *как* получить результат)

```python
result = []
for student in students:
    if student["grade"] >= 4:
        result.append(student["name"])
```

<!-- pause -->

## SQL (декларативно: *что* хочу получить)

```sql
SELECT name FROM students WHERE grade >= 4;
```

<!-- pause -->

СУБД сама решает, *как* выполнить запрос.

<!-- end_slide -->

# Реляционная модель

| Реляционная модель | Аналог в Python |
|---|---|
| Таблица | список словарей / DataFrame |
| Строка | один словарь |
| Столбец | ключ словаря + тип |
| Схема | заранее описанная структура |

<!-- pause -->

Главное отличие: у таблицы есть **строгая схема** — все строки обязаны ей соответствовать.

<!-- end_slide -->

# Первичный ключ и NULL

<!-- pause -->

**PRIMARY KEY** — уникальный идентификатор строки.

<!-- pause -->

**NULL** — это отсутствие значения, а не 0 и не пустая строка.

```sql
NULL = NULL   -- НЕ true, результат NULL ("неизвестно")
```

<!-- pause -->

Проверка на отсутствие значения:

```sql
WHERE column IS NULL
WHERE column IS NOT NULL
```

<!-- end_slide -->

# SQLite vs PostgreSQL

<!-- column_layout: [1, 1] -->

<!-- column: 0 -->

## SQLite

- embedded, вся БД — один файл
- не требует установки
- гибкая типизация
- для обучения и прототипов

<!-- column: 1 -->

## PostgreSQL

- client-server
- нужен отдельный сервер
- строгая типизация
- права доступа, роли
- production-системы

<!-- reset_layout -->

<!-- pause -->

Сегодня — SQLite. Концепции те же, дальше перейдём на PostgreSQL.

<!-- end_slide -->

# Описание структуры: CREATE TABLE

```sql
CREATE TABLE students (
    id    INTEGER PRIMARY KEY,
    name  TEXT NOT NULL,
    grade REAL
);
```

<!-- pause -->

- `id` — первичный ключ
- `name` — обязательное текстовое поле
- `grade` — число с плавающей точкой

<!-- end_slide -->

# SELECT — базовый синтаксис

```sql
SELECT столбцы
FROM таблица
WHERE условие
ORDER BY столбец
LIMIT N;
```

<!-- end_slide -->

# SELECT — примеры

```sql
SELECT * FROM students;
```

```sql
SELECT name, grade FROM students;
```

<!-- pause -->

```sql
SELECT * FROM students WHERE grade >= 4;
```

<!-- pause -->

```sql
SELECT * FROM students ORDER BY grade DESC LIMIT 5;
```

<!-- end_slide -->

# WHERE: операторы сравнения

- `=`, `!=` (`<>`), `>`, `<`, `>=`, `<=`
- `AND`, `OR`
- `BETWEEN`
- `IN`
- `LIKE` — поиск по шаблону в тексте

<!-- end_slide -->

# Агрегатные функции

```sql
SELECT COUNT(*) FROM students;
SELECT AVG(grade) FROM students;
SELECT MAX(grade), MIN(grade) FROM students;
SELECT SUM(grade) FROM students;
```

<!-- pause -->

Группировку (`GROUP BY`) разберём на следующем занятии.

<!-- end_slide -->

# Мостик к Python

```python
import sqlite3

conn = sqlite3.connect("school.db")
cursor = conn.cursor()
cursor.execute("SELECT name FROM students WHERE grade >= 4;")
for row in cursor.fetchall():
    print(row)
conn.close()
```

<!-- pause -->

SQL — это инструмент, который дальше будет использоваться прямо из кода.

<!-- end_slide -->

# Что дальше

- `GROUP BY` / `HAVING`
- `JOIN` — связывание таблиц
- `INSERT` / `UPDATE` / `DELETE`
- Переход на PostgreSQL

<!-- end_slide -->

# Практика

Открываем SQLite, пишем первые запросы.
