# 🚀 Test Task – Feature Engineering & Scoring Microservice

This repository contains the solution to a two-part technical task focused on:
1. Feature engineering using SQL
2. Business decision logic implemented as a Python microservice

---

## 📊 Part 1: SQL Task – Feature Engineering

The goal is to calculate 5 features per client based on a SQLite database, using only SQL.

### ✅ Features Calculated

| Feature Name | Description |
|-------------|-------------|
| `vendor_microfinance_gambling_payment_ratio_l12m` | Ratio of payments to microfinance and gambling merchants vs. total vendor payments (last 12 months) |
| `vendor_grocery_utilities_transaction_ratio_l9m` | Ratio of grocery and utilities transactions vs. total vendor transactions (last 9 months) |
| `history_payment_delay_flag_l6m` | Boolean flag indicating if any payment was delayed (last 6 months) |
| `history_payment_ratio_l9m_to_total` | Ratio of income-type payments (last 9 months) to total historical income payments |
| `history_average_loan_profit_margin_l12m` | Average loan profit margin for loans issued in the last 12 months |

### 🛠 Tech

- SQL dialect: **SQLite**
- All queries are in `query.sql`
- Data is generated using:

### 🛠️ Usage

#### Generate the database

```bash
python -m sql_task.data_generator
```

#### Validate the query with:
```bash
python -m sql_task.runner
```

### 💡 Notes
- Vendor names are partially masked → handled using pattern matching with LIKE.

- Features return NULL if no relevant data is available.

- Calculations are scoped to the current :client_id.

## 🧠 Part 2: Python Task – Business Decision Microservice

Implements the logic for score-based decisions using a microservice.

### 🔁 Strategies Implemented

| Strategy                     | Description                                                                                       |
|-----------------------------|---------------------------------------------------------------------------------------------------|
| `pure_stream_strategy`      | Applied to 5% of requests (deterministically via hash). Always returns `"1"` with loan 8000 over 6 months |
| `new_client_strategy`       | Applied if `client_type == "new"`. Approves (`"1"`) if `score < 0.15`, with loan 6000 over 3 months |
| `repeat_client_strategy`    | Applied if `client_type == "repeat"` and phone does **not** end in 2 or 4. Approves if `score < 0.20`, loan 12000 over 6 months |
| `pilot_repeat_client_strategy` | Applied if `client_type == "repeat"` and phone **ends in 2 or 4**. Approves if `score < 0.18`, loan 24000 over 12 months |

### 🛠️ Usage

#### Generate test data:
```bash
python -m python_task.data_generator
```
#### Run the microservice:

```bash
python -m python_task.runner
```

#### Check strategy usage distribution:
```bash
python -m python_task.result_lookup
```

### 📁 Data Structure

#### The microservice reads:

| File                                  | Description                             |
|---------------------------------------|-----------------------------------------|
| `Application/Application.json`        | Contains `request_id`, `client_type`    |
| `SqlIntegration/SqlIntegration.json`  | Contains `phone_number`, `age`, `name`  |
| `PythonScoring-vX/PythonScoring.json` | Contains the `score` value (versioned)  |

### 🧱 Tech & Architecture
- Main logic: python_task/scoring.py

- Deterministic 5% stream using hash(request_id) % 100 < 5

- Uses Pydantic models for I/O (see src/models)

- Fully exception-safe and traceable

### ✅ Highlights
- Clean, modular structure

- Fully documented

- Robust to missing files and errors

- Compatible with any PythonScoring version folders

### 🤝 Author
Developed as part of a technical challenge, with focus on clarity, robustness and business logic alignment.