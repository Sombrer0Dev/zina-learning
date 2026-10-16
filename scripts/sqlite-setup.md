# Установка и базовая настройка SQLite

## Ubuntu / Debian

```bash
sudo apt update
sudo apt install sqlite3
```

Проверка версии:

```bash
sqlite3 --version
```

## Fedora

```bash
sudo dnf install sqlite
```

Проверка версии:

```bash
sqlite3 --version
```

## Python и SQLite

Отдельно устанавливать ничего не нужно — модуль `sqlite3` входит в стандартную библиотеку Python. Проверить можно так:

```bash
python3 -c "import sqlite3; print(sqlite3.sqlite_version)"
```

Если команда вывела номер версии — всё готово к работе.

## Создание и открытие базы данных

SQLite-база — это один файл. Файл создаётся автоматически при первом обращении:

```bash
sqlite3 school.db
```

Эта команда открывает интерактивную консоль SQLite (если файла `school.db` не было — он будет создан после первой записи данных).

Выйти из консоли:

```sql
.quit
```

## Базовые настройки консоли (dot-команды)

Внутри `sqlite3` полезно сразу включить человекочитаемый вывод таблиц:

```sql
.mode column
.headers on
```

Чтобы не вводить это каждый раз, можно сохранить настройки в файл `~/.sqliterc` — он подхватывается автоматически при каждом запуске `sqlite3`:

```bash
cat > ~/.sqliterc << 'EOF'
.mode column
.headers on
.timeout 5000
EOF
```

Полезные dot-команды внутри консоли:

| Команда | Назначение |
|---|---|
| `.tables` | список таблиц в текущей базе |
| `.schema имя_таблицы` | показать структуру таблицы (CREATE TABLE) |
| `.open файл.db` | открыть другой файл базы |
| `.quit` | выйти из консоли |

## Графический клиент (опционально)

Для визуальной работы с базой (особенно удобно на первых занятиях) можно поставить DB Browser for SQLite:

**Ubuntu / Debian:**

```bash
sudo apt install sqlitebrowser
```

**Fedora:**

```bash
sudo dnf install sqlitebrowser
```

## Проверка, что всё работает

```bash
sqlite3 test.db "CREATE TABLE t (id INTEGER PRIMARY KEY, name TEXT); INSERT INTO t (name) VALUES ('ok'); SELECT * FROM t;"
```

Ожидаемый вывод — одна строка с `id = 1` и `name = ok`. После проверки файл `test.db` можно удалить:

```bash
rm test.db
```
