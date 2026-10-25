# Zina Learning

Материалы курса по SQL и базам данных: конспекты лекций, слайды для терминального показа и упражнения с автопроверкой.

## Структура

```
lectures/<N>/lecture.md   — развёрнутый конспект урока N
lectures/<N>/slides.md    — слайды для presenterm
exercises/<N>/            — упражнения к уроку N (задания, эталонные ответы, автопроверка)
scripts/                  — вспомогательные инструкции (установка окружения и т.п.)
plans/                    — планы занятий
```

## Урок 1 — Введение в SQL и реляционные базы данных

- [`lectures/01/lecture.md`](lectures/01/lecture.md) — конспект
- [`lectures/01/slides.md`](lectures/01/slides.md) — слайды
- [`exercises/01/`](exercises/01/) — упражнения по `CREATE TABLE`, `SELECT`/`WHERE`, `ORDER BY`/`LIMIT`, `NULL`, агрегатным функциям

## Урок 2 — GROUP BY и JOIN

- [`lectures/02/lecture.md`](lectures/02/lecture.md) — конспект
- [`lectures/02/slides.md`](lectures/02/slides.md) — слайды
- [`exercises/02/`](exercises/02/) — упражнения по `JOIN` (`INNER`/`LEFT`), `GROUP BY`, `HAVING`

## Слайды

Слайды написаны под [presenterm](https://github.com/mfontanini/presenterm) и показываются прямо в терминале:

```bash
presenterm lectures/01/slides.md
presenterm lectures/02/slides.md
```

## Упражнения

Каждая папка в `exercises/<N>/` — самостоятельный набор: SQL-схема с тестовыми данными, задания, эталонные ответы и скрипт автопроверки на Python (`assert` поверх встроенного модуля `sqlite3`). Подробности — в README внутри папки урока.

## Установка SQLite

См. [`scripts/sqlite-setup.md`](scripts/sqlite-setup.md).
