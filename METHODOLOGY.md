# Краткая методика эксперимента

## Цель

Проверить, как наличие индексов влияет на производительность типовых запросов в PostgreSQL, MySQL и MongoDB, а также оценить:

- какие индексы действительно нужны;
- какие индексы дают слабый эффект;
- где индексы могут замедлять загрузку данных;
- какие типы индексов подходят для текущей задачи.

## СУБД

- PostgreSQL 17
- MySQL 8.4
- MongoDB 8.0

Все СУБД запускаются через Docker Compose с одинаковыми ограничениями ресурсов: `2 CPU` и `3 GB RAM`.

## Данные

Используется синтетический набор данных `student_activity` объемом `1_000_000` строк.

Главное требование методики:

- в рамках одного прогона должен использоваться один и тот же CSV-файл;
- этот же CSV загружается в PostgreSQL, MySQL и MongoDB;
- запросы и их константы должны быть одинаковыми для всех СУБД.

Seed генерации не является обязательным элементом методики. При необходимости точного повторения конкретного датасета можно передать параметр `--seed`, а фактически использованное значение сохраняется в `data/student_activity_metadata.json`.

## Сценарии запросов

- `Q1` — точечный поиск по `student_id`;
- `Q2` — фильтрация по диапазону `created_at`;
- `Q3` — фильтрация по `status`;
- `Q4` — фильтрация по `status` и `created_at`;
- `Q5` — сортировка по `created_at DESC` с `LIMIT`;
- `Q6` — агрегация по `course_id`;
- `Q7` — широкий диапазон `score`, где индекс ожидаемо мало помогает.

## Конфигурации индексов

Сравниваются следующие режимы:

```text
no_indexes
idx_student_id_only
idx_created_at_only
idx_status_only
idx_status_created_at_only
idx_course_score_only
all_indexes
```

Это нужно для ответа на вопрос, все ли индексы действительно нужны, и не возникает ли лишняя нагрузка от избыточных индексов.

## Параметры измерений

Актуальная целевая схема измерений:

```text
warmup_runs = 0
measured_runs = 1000
```

Все `1000` измеряемых прогонов сохраняются в `results/benchmark_results.csv`.

По каждому сочетанию:

```text
СУБД × индексная конфигурация × запрос
```

считаются:

- медиана;
- среднее;
- минимум;
- максимум;
- стандартное отклонение;
- `p95`;
- `p99`.

## Анализ индексов

Для каждого индекса нужно ответить на четыре вопроса:

1. Какой запрос он должен ускорять?
2. Почему выбранное поле встречается в реальных сценариях?
3. Какова ожидаемая селективность?
4. Есть ли накладные расходы и риск бесполезности?

Минимальный набор выводов:

- `student_id` — кандидат для точечного высокоселективного поиска;
- `created_at` — важен для диапазона и сортировки;
- `status` — поле с более низкой селективностью, индекс может быть спорным;
- `status + created_at` — целевой составной индекс для комбинированной фильтрации;
- `course_id + score` — нужно отдельно проверить, нужен ли он вообще в текущем наборе запросов.

## Анализ деградации от индексов

Помимо SELECT-запросов нужно измерять стоимость загрузки данных:

1. Загрузка без пользовательских индексов.
2. Загрузка при заранее созданных индексах.

Результат сохраняется в `results/load_performance.csv`.

Этот блок нужен, чтобы показать, что индексы могут ускорять чтение, но замедлять вставку и массовую загрузку.

## Типы индексов

### PostgreSQL

Рассматриваются:

- `B-tree` — основной тип для равенства, диапазонов, сортировки и составных условий;
- `Hash` — возможен для равенства по `student_id`;
- `BRIN` — кандидат для `created_at`, если данные хорошо коррелируют со временем;
- `GIN` — для этой табличной структуры обычно не является основным выбором.

### MySQL

Для InnoDB основной практический тип в текущем исследовании — обычные и составные `B-tree` индексы.

### MongoDB

Рассматриваются:

- `single-field index`;
- `compound index`;
- `hashed index`.

Для текущих запросов наиболее важны `single-field` и `compound` индексы. `Hashed index` имеет смысл обсуждать прежде всего для равенства по `student_id`.

## Планы выполнения

Для интерпретации поведения оптимизатора сохраняются:

- PostgreSQL: `EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)`;
- MySQL: `EXPLAIN ANALYZE`;
- MongoDB: `explain` с `executionStats`.

## Итоговые артефакты

- `results/benchmark_results.csv`
- `results/benchmark_stats.csv`
- `results/benchmark_medians.csv`
- `results/index_effectiveness.csv`
- `results/load_performance.csv`
- `results/experiment_metadata.json`
- `results/benchmark_summary.md`
- `results/summary_ru.md`
- `results/benchmark_table_ru.csv`
- `results/index_effectiveness_ru.csv`
- `results/load_performance_ru.csv`
- `charts/postgres_boxplots.png`
- `charts/mysql_boxplots.png`
- `charts/mongo_boxplots.png`
- `charts/postgres_run_trends.png`
- `charts/mysql_run_trends.png`
- `charts/mongo_run_trends.png`
- `charts/postgres_relative_effect.png`
- `charts/mysql_relative_effect.png`
- `charts/mongo_relative_effect.png`
- `explain_plans/*`

## Дополнительные Q1-артефакты

Если запускать отдельные helper-скрипты для Q1, дополнительно создаются:

- `results/q1_student_id_median_times_all_dbms.csv`
- `results/q1_student_id_run_times_all_dbms.csv`
- `charts/q1_student_id_median_times_all_dbms.png`
- `charts/q1_student_id_median_times_all_dbms_log.png`
- `charts/q1_student_id_run_times_with_median_subplots.png`

Эти файлы не входят в базовый `run_all.py`, но полезны для более детального разбора запроса `Q1`.

## Воспроизводимость

Для воспроизведения эксперимента нужно зафиксировать:

- версии СУБД;
- Docker Compose;
- ограничения ресурсов;
- команды генерации данных;
- команды загрузки данных;
- команды запуска benchmark;
- местоположение всех результатов и графиков.

Подробные команды вынесены в `README.md`.
