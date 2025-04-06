# Python Task - Business Logic for a New Scorecard

We have implemented a new model and are now receiving scores from it. It's time to start making production decisions based on it.

---

## 🎯 Goal

For each client, we need to make a product decision. We use microservices that will later be integrated as blocks within a BPMN process. The microservice takes a `Request` model as input and outputs a `Response`. The structure of the models can be found in `python_task/src/models`.

## 📋 Decision Strategies

### 1. Pure Stream Strategy

Applied to all clients, randomly assigned to 5% of the flow.

- **Name**: `pure_stream_strategy`
- **Result**: always "1" (approval)
- **Score**: taken from the PythonScoring file
- **Loan Amount**: 8000
- **Loan Term**: 6 months

### 2. New Client Strategy

- **Name**: `new_client_strategy`
- **Result**: "1" if score < 0.15, otherwise "0"
- **Score**: taken from the PythonScoring file
- **Loan Amount**: 6000 if result is "1", otherwise None
- **Loan Term**: 3 months if result is "1", otherwise None

### 3. Repeat Client Strategy

- **Name**: `repeat_client_strategy`
- **Result**: "1" if score < 0.20, otherwise "0"
- **Score**: taken from the PythonScoring file
- **Loan Amount**: 12000 if result is "1", otherwise None
- **Loan Term**: 6 months if result is "1", otherwise None

### 4. Pilot Strategy for Repeat Clients

Applied to repeat clients whose phone number from the SQL integration ends with the digit 2 or 4.

- **Name**: `pilot_repeat_client_strategy`
- **Result**: "1" if score < 0.18, otherwise "0"
- **Score**: taken from the PythonScoring file
- **Loan Amount**: 24000 if result is "1", otherwise None
- **Loan Term**: 12 months if result is "1", otherwise None

---

## 📊 Data Structure

Test data is used in JSON format in the following directories:

### 📁 `Application`

Contains information about the client's application.

| Field         | Type   | Description                     |
| ------------- | ------ | ------------------------------- |
| `request_id`  | String | Unique application identifier   |
| `client_type` | String | Client type (`new` or `repeat`) |

### 📁 `SqlIntegration`

Contains basic client data.

| Field          | Type    | Description      |
| -------------- | ------- | ---------------- |
| `name`         | String  | Client's name    |
| `age`          | Integer | Client's age     |
| `sex`          | String  | Client's gender  |
| `document_id`  | Integer | Document ID      |
| `address`      | String  | Client's address |
| `phone_number` | String  | Client's phone   |

### 📁 `PythonScoring-v{version}`

Scoring model results.

| Field   | Type  | Description                 |
| ------- | ----- | --------------------------- |
| `score` | Float | Client's scoring evaluation |

## 🧩 Data Models

The main classes for working with data are located in the `src/models` directory:

### 📌 `Request`

Input model for the microservice.

| Field        | Type   | Description                         |
| ------------ | ------ | ----------------------------------- |
| `request_id` | String | Unique application identifier       |
| `context`    | Path   | Path to the client's data directory |

### 📌 `Response`

Output model of the microservice.

| Field           | Type                       | Description                                  |
| --------------- | -------------------------- | -------------------------------------------- |
| `result`        | Literal["1", "0", "error"] | Decision result (1 = approved, 0 = rejected) |
| `score`         | Float                      | Client's scoring score                       |
| `strategy_name` | String                     | Name of the applied strategy                 |
| `loan_term`     | Optional[Integer]          | Loan term in months (if approved)            |
| `loan_amount`   | Optional[Float]            | Loan amount (if approved)                    |
| `created_at`    | Datetime                   | Response creation time                       |

## 🔍 Decision Algorithm

1. Retrieve data from all sources (Application, SqlIntegration, PythonScoring)
2. Determine the client type (new/repeat) from Application
3. If the client falls into the 5% random flow → apply the pure stream strategy
4. For the regular flow:
   - For new clients → apply the new client strategy
   - For repeat clients → check the phone number:
     - If it ends with 2 or 4 → apply the pilot strategy
     - Otherwise → apply the regular repeat client strategy
5. Return the result according to the rules of the selected strategy

## 🛠 How to Use

1. Implement the business logic in the `scoring.py` file
2. Use models from `src/models` to work with input data
3. Generate test data using the command:

```bash
python -m python_task.data_generator
```

This will create a directory with test data in JSON format.

4. Run your solution:

```bash
python -m python_task.runner
```

5. Then you can check the distribution of strategies:

```bash
python -m python_task.result_lookup
```

## 📝 Solution Requirements

- Code must be clean and well-structured
- Possible errors must be handled
- Strategy selection logic must be clear and follow the described rules
- The solution must work correctly with different versions of PythonScoring

> 💡 **Tip:** For random distribution of 5% of the flow, you can use a hash function on the request_id with an appropriate threshold to ensure deterministic results.
