# Исследование влияния индексов на производительность запросов в SQL и NoSQL СУБД

Проект сравнивает PostgreSQL 17, MySQL 8.4 и MongoDB 8.0 на одном и том же наборе данных `student_activity`. Цель исследования — показать, когда индексы действительно ускоряют запросы, когда эффект слабый, а когда индексы дают накладные расходы.

Для всех трех СУБД используются одинаковые ресурсные ограничения Docker Compose:

```yaml
cpus: "2.0"
mem_limit: "3g"
```

## 1. Набор данных

Используется синтетический журнал учебной активности студентов. Основные поля:

- `activity_id` — идентификатор события;
- `student_id` — идентификатор студента;
- `course_id` — идентификатор курса;
- `faculty` — факультет;
- `group_code` — учебная группа;
- `activity_type` — тип учебной активности;
- `status` — статус события;
- `score` — оценка или числовой результат;
- `created_at` — дата создания события;
- `updated_at` — дата обновления события;
- `semester` — семестр.

По умолчанию генерируется `1_000_000` строк. Seed не является обязательной частью методики. Если нужен точный повтор конкретного датасета, можно явно передать `--seed`. После генерации сохраняется файл `data/student_activity_metadata.json` с фактически использованным seed.

## 2. Запросы исследования

Сравниваются семь типовых сценариев:

- `Q1` — поиск по `student_id`;
- `Q2` — фильтрация по диапазону `created_at`;
- `Q3` — фильтрация по `status`;
- `Q4` — фильтрация по `status` и `created_at`;
- `Q5` — сортировка по `created_at DESC` с `LIMIT 100`;
- `Q6` — агрегация по `course_id` для записей со статусом `graded`;
- `Q7` — широкий диапазон `score`, где индекс должен помогать слабо или не помогать вовсе.

Константы запросов зафиксированы в `scripts/config.py`.

## 3. Конфигурации индексов

Проект сравнивает не только режимы “без индексов” и “со всеми индексами”, но и отдельные конфигурации:

- `no_indexes`
- `idx_student_id_only`
- `idx_created_at_only`
- `idx_status_only`
- `idx_status_created_at_only`
- `idx_course_score_only`
- `all_indexes`

Идея такая:

- оценить, какой индекс помогает какому запросу;
- проверить, есть ли лишние индексы;
- увидеть случаи, где индекс почти не помогает или ухудшает результат.

## 4. Методика измерений

Актуальные параметры измерений по умолчанию:

```text
warmup_runs = 0
measured_runs = 1000
```

Все `1000` измеряемых запусков сохраняются в `results/benchmark_results.csv`. По ним считаются:

- `median`
- `mean`
- `min`
- `max`
- `std`
- `p95`
- `p99`

## 5. Что сохраняется после запуска

Технические результаты:

- `results/benchmark_results.csv` — все измеряемые прогоны;
- `results/benchmark_stats.csv` — агрегированная статистика;
- `results/index_effectiveness.csv` — сравнение каждой конфигурации с `no_indexes`;
- `results/load_performance.csv` — время загрузки данных без индексов и со всеми индексами;
- `results/experiment_metadata.json` — параметры прогона;
- `results/summary_ru.md` — русскоязычное краткое описание результатов.

Схема таблицы:

`charts/student_activity_schema.png`

Графики:

- `charts/load_time_comparison.png`
- `charts/postgres_median.jpg`
- `charts/mysql_median.jpg`
- `charts/mongo_median.jpg`
- `charts/q1_student_id_run_times_with_median_subplots.png`
- `charts/q1_student_id_run_times_all_dbms.png`

Планы выполнения:

- `explain_plans/postgres/`
- `explain_plans/mysql/`
- `explain_plans/mongo/`

## 6. Запуск на Windows через PowerShell

### Шаг 1. Перейти в папку проекта

```powershell
cd index-perfomance-research
```

### Шаг 2. Подготовить Python-окружение

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Если PowerShell блокирует активацию:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### Шаг 3. Поднять контейнеры

```powershell
docker compose up -d
docker compose ps
```

### Шаг 4. Полный запуск пайплайна

```powershell
python scripts/run_all.py
```

Эта команда:

1. ждет готовности сервисов;
2. генерирует CSV;
3. создает схемы;
4. загружает данные;
5. прогоняет benchmark по всем индексным конфигурациям;
6. строит графики;
7. измеряет влияние индексов на загрузку данных;
8. формирует русскоязычные выходы.

## 7. Поэтапный запуск

Если нужно выполнять этапы вручную:

```powershell
python scripts/wait_for_services.py
python scripts/generate_data.py --rows 1000000
python scripts/create_schema.py
python scripts/load_data.py
python scripts/check_counts.py
python scripts/benchmark.py --warmups 0 --runs 1000
python scripts/build_charts.py
python scripts/measure_load_performance.py
python scripts/build_readable_outputs.py
```

Для точного повтора конкретного датасета:

```powershell
python scripts/generate_data.py --rows 1000000
```

## 8. Быстрый smoke-test

Перед тяжелым прогоном удобно проверить пайплайн на короткой серии:

```powershell
python scripts/run_all.py --rows 10000 --runs 5 --skip-load-measurement
```

Такой тест не заменяет основной эксперимент, но помогает убедиться, что код и контейнеры работают корректно.

## 9. Проверка результатов

После запуска имеет смысл проверить:

```powershell
python scripts/check_counts.py
```

И убедиться, что появились файлы:

- `results/benchmark_results.csv`
- `results/benchmark_stats.csv`
- `results/index_effectiveness.csv`
- `results/summary_ru.md`
- `charts/*.png`

## 10. Очистка окружения

Остановить контейнеры без удаления данных:

```powershell
docker compose down
```

Полностью удалить контейнеры и volumes:

```powershell
docker compose down -v
```

После `down -v` данные в СУБД исчезнут, и загрузку нужно будет выполнять заново.
