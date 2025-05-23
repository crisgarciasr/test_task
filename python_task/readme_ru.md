# Задача на Python - Бизнес-логика для новой скоринговой карты

Мы внедрили новую модель и теперь получаем от неё скоринговые оценки. Пора начинать принимать производственные решения на их основе.

---

## 🎯 Цель

Для каждого клиента необходимо принять продуктовое решение. Мы используем микросервисы, которые позже будут интегрированы как блоки в процессе BPMN. Микросервис принимает модель `Request` в качестве входных данных и возвращает модель `Response`. Структура моделей находится в `python_task/src/models`.

## 📋 Стратегии принятия решений

### 1. Стратегия чистого потока

Применяется ко всем клиентам, случайным образом назначается 5% потока.

- **Название**: `pure_stream_strategy`
- **Результат**: всегда "1" (одобрение)
- **Скоринг**: берётся из файла PythonScoring
- **Сумма займа**: 8000
- **Срок займа**: 6 месяцев

### 2. Стратегия для новых клиентов

- **Название**: `new_client_strategy`
- **Результат**: "1", если скоринг < 0.15, иначе "0"
- **Скоринг**: берётся из файла PythonScoring
- **Сумма займа**: 6000, если результат "1", иначе None
- **Срок займа**: 3 месяца, если результат "1", иначе None

### 3. Стратегия для повторных клиентов

- **Название**: `repeat_client_strategy`
- **Результат**: "1", если скоринг < 0.20, иначе "0"
- **Скоринг**: берётся из файла PythonScoring
- **Сумма займа**: 12000, если результат "1", иначе None
- **Срок займа**: 6 месяцев, если результат "1", иначе None

### 4. Пилотная стратегия для повторных клиентов

Применяется к повторным клиентам, чей номер телефона из SQL-интеграции заканчивается на цифру 2 или 4.

- **Название**: `pilot_repeat_client_strategy`
- **Результат**: "1", если скоринг < 0.18, иначе "0"
- **Скоринг**: берётся из файла PythonScoring
- **Сумма займа**: 24000, если результат "1", иначе None
- **Срок займа**: 12 месяцев, если результат "1", иначе None

---

## 📊 Структура данных

Тестовые данные используются в формате JSON в следующих директориях:

### 📁 `Application`

Содержит информацию о заявке клиента.

| Поле          | Тип    | Описание                         |
| ------------- | ------ | -------------------------------- |
| `request_id`  | String | Уникальный идентификатор заявки  |
| `client_type` | String | Тип клиента (`new` или `repeat`) |

### 📁 `SqlIntegration`

Содержит основные данные о клиенте.

| Поле           | Тип     | Описание        |
| -------------- | ------- | --------------- |
| `name`         | String  | Имя клиента     |
| `age`          | Integer | Возраст клиента |
| `sex`          | String  | Пол клиента     |
| `document_id`  | Integer | ID документа    |
| `address`      | String  | Адрес клиента   |
| `phone_number` | String  | Телефон клиента |

### 📁 `PythonScoring-v{version}`

Результаты скоринговой модели.

| Поле    | Тип   | Описание                   |
| ------- | ----- | -------------------------- |
| `score` | Float | Скоринговая оценка клиента |

## 🧩 Модели данных

Основные классы для работы с данными находятся в директории `src/models`:

### 📌 `Request`

Входная модель для микросервиса.

| Поле         | Тип    | Описание                            |
| ------------ | ------ | ----------------------------------- |
| `request_id` | String | Уникальный идентификатор заявки     |
| `context`    | Path   | Путь к директории с данными клиента |

### 📌 `Response`

Выходная модель микросервиса.

| Поле            | Тип                        | Описание                                       |
| --------------- | -------------------------- | ---------------------------------------------- |
| `result`        | Literal["1", "0", "error"] | Результат решения (1 = одобрено, 0 = отказано) |
| `score`         | Float                      | Скоринговая оценка клиента                     |
| `strategy_name` | String                     | Название применённой стратегии                 |
| `loan_term`     | Optional[Integer]          | Срок займа в месяцах (если одобрено)           |
| `loan_amount`   | Optional[Float]            | Сумма займа (если одобрено)                    |
| `created_at`    | Datetime                   | Время создания ответа                          |

## 🔍 Алгоритм принятия решений

1. Получить данные из всех источников (Application, SqlIntegration, PythonScoring)
2. Определить тип клиента (new/repeat) из Application
3. Если клиент попадает в 5% случайного потока → применить стратегию чистого потока
4. Для основного потока:
   - Для новых клиентов → применить стратегию для новых клиентов
   - Для повторных клиентов → проверить номер телефона:
     - Если заканчивается на 2 или 4 → применить пилотную стратегию
     - В противном случае → применить обычную стратегию для повторных клиентов
5. Вернуть результат в соответствии с правилами выбранной стратегии

## 🛠 Как использовать

1. Реализуйте бизнес-логику в файле `scoring.py`
2. Используйте модели из `src/models` для работы с входными данными
3. Сгенерируйте тестовые данные с помощью команды:

```bash
python -m python_task.data_generator
```

Это создаст директорию с тестовыми данными в формате JSON.

4. Запустите решение:

```bash
python -m python_task.runner
```

5. Затем вы можете проверить распределение стратегий:

```bash
python -m python_task.result_lookup
```

## 📝 Требования к решению

- Код должен быть чистым и хорошо структурированным
- Возможные ошибки должны быть обработаны
- Логика выбора стратегии должна быть понятной и соответствовать описанным правилам
- Решение должно корректно работать с разными версиями PythonScoring

> 💡 **Совет:** Для случайного распределения 5% потока можно использовать хэш-функцию на основе request_id с соответствующим порогом, чтобы обеспечить детерминированные результаты.
