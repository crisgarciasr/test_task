# SQL Task – Feature Engineering for New Model

Our data science team has prepared a new scoring model, and now it needs to be deployed to production as quickly as possible 🚀

---

## 🎯 Goal

For each client, calculate the following features to be used in the model. All calculations must be performed using SQL.

| Feature Name                                      | Feature Description                                                                                                                                    |
| ------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `vendor_microfinance_gambling_payment_ratio_l12m` | The ratio of the total amount of payments to microfinance and gambling merchants to the total amount of all vendor payments over the last 12 months    |
| `vendor_grocery_utilities_transaction_ratio_l9m`  | The ratio of the number of transactions related to grocery and utility merchants to the total number of all vendor transactions over the last 9 months |
| `history_payment_delay_flag_l6m`                  | Boolean flag indicating whether any loan payment was delayed within the last 6 months                                                                  |
| `history_payment_ratio_l9m_to_total`              | Ratio of the total amount of income-type payments over the past 9 months to the total payment history                                                  |
| `history_average_loan_profit_margin_l12m`         | Average profit margin (loan amount - total payments) / loan amount for loans issued in the last 12 months                                              |
|                                                   |

If a client has no relevant data for a specific feature (e.g., no vendor transactions or payments in the given period), the feature value must be returned as NULL.

---

## 📊 Database Structure

The project uses a **SQLite** database with four main tables: `clients`, `loans`, `cash_flows`, and `vendor_transactions`.

### 🧑‍💼 `clients`

Contains basic client information.

| Field          | Type    | Description                                          |
| -------------- | ------- | ---------------------------------------------------- |
| `id`           | Integer | Unique client identifier                             |
| `first_name`   | String  | Client's first name                                  |
| `last_name`    | String  | Client's last name                                   |
| `phone_number` | String  | Client's phone number (used to link to transactions) |
| `email`        | String  | Client's email                                       |

---

### 💳 `loans`

Contains information about loans issued to clients.

| Field            | Type    | Description                 |
| ---------------- | ------- | --------------------------- |
| `id`             | Integer | Unique loan ID              |
| `client_id`      | Integer | Foreign key to `clients.id` |
| `amount`         | Numeric | Loan amount                 |
| `payment_amount` | Numeric | Monthly payment amount      |
| `term`           | Integer | Loan term (months)          |
| `start_date`     | Date    | Loan issue date             |

---

### 💸 `cash_flows`

Contains records of loan-related cash flow events.

| Field            | Type    | Description               |
| ---------------- | ------- | ------------------------- |
| `id`             | Integer | Unique record ID          |
| `loan_id`        | Integer | Foreign key to `loans.id` |
| `type`           | String  | `"income"` or `"expense"` |
| `amount`         | Numeric | Payment amount            |
| `scheduled_date` | Date    | Scheduled payment date    |
| `payment_date`   | Date    | Actual payment date       |

> `expense` = loan issuance, `income` = client payment.

---

### 🏪 `vendor_transactions`

Represents external client transactions with vendors (e.g. stores or service providers).

| Field              | Type    | Description                                         |
| ------------------ | ------- | --------------------------------------------------- |
| `id`               | UUID    | Unique transaction ID                               |
| `phone_number`     | String  | Client’s phone number (used to link with `clients`) |
| `amount`           | Numeric | Transaction amount                                  |
| `merchant`         | String  | Vendor/merchant name                                |
| `transaction_date` | Date    | Date of the transaction                             |

---

## 🧠 Data Notes

- **Vendor features (`vendor_*`)**: derived from the `vendor_transactions` table. Examples:

  - `vendor_microfinance_gambling_payment_ratio_l12m`
  - `vendor_grocery_utilities_transaction_ratio_l9m`

- **History features (`history_*`)**: calculated based on `loans` and `cash_flows`. Examples:

  - `history_payment_delay_flag_l6m`
  - `history_payment_ratio_l9m_to_total`

- **Merchant masking**: some merchants appear with **masked names**, such as:

  - `"CASINOSLOTS"` → `"CA*****S"`
  - `"FASTMONEY"` → `"FA*****Y"`

  These should be handled via partial matching (`LIKE`, regex, etc.).

- **Merchant categories**: available in the external file `fake_merchants.json`.

- **Linking `vendor_transactions` to clients**: is done via the `phone_number` field, not via `client_id`.

---

## 🛠 How to Use

Write your SQL in query.sql.
The query must return client_id and all required features as columns.

Generate the data by running from root:

```bash
python -m sql_task.data_generator
```

This will create a database file with all necessary tables and test data.

Then run the checker to validate your solution:

```bash
python -m sql_task.runner
```

This will run your query for one random client_id and print the result to the console.

> Query will be executed per client, with :client_id being substituted by the runner.
> Make sure all calculations are scoped to the given client and return exactly one row per execution.
