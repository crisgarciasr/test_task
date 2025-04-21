-- TODO: Add here all the necessary variables

-- =======================================
-- Feature Engineering: Client-Level Metrics
-- =======================================
-- This query calculates 5 features for a given client_id:
-- 1. Ratio of payments to microfinance/gambling merchants (12 months)
-- 2. Ratio of grocery/utilities transactions (9 months)
-- 3. Flag indicating delayed payments on any loan (6 months)
-- 4. Ratio of recent income payments to total payment history (9 months)
-- 5. Average loan profit margin for loans issued in the last 12 months
-- If no data is available, features are returned as NULL (as required)
-- =======================================

-- =======================================
-- Feature Engineering: Client-Level Metrics
-- =======================================
-- This query calculates 5 features for a given client_id:
-- 1. vendor_microfinance_gambling_payment_ratio_l12m
-- 2. vendor_grocery_utilities_transaction_ratio_l9m
-- 3. history_payment_delay_flag_l6m
-- 4. history_payment_ratio_l9m_to_total
-- 5. history_average_loan_profit_margin_l12m
-- If the client has no relevant data, the features are returned as NULL.
-- =======================================

WITH

-- 1. Microfinance & Gambling Payments (last 12 months)
vmg AS (
  SELECT
    vt.phone_number,
    SUM(
      CASE
        -- Microfinance
        WHEN UPPER(vt.merchant) LIKE 'FA%' AND UPPER(vt.merchant) LIKE '%Y' THEN vt.amount
        WHEN UPPER(vt.merchant) LIKE 'EV%' AND UPPER(vt.merchant) LIKE '%Y' THEN vt.amount
        WHEN UPPER(vt.merchant) LIKE 'CH%' AND UPPER(vt.merchant) LIKE '%G' THEN vt.amount
        WHEN UPPER(vt.merchant) LIKE 'EL%' AND UPPER(vt.merchant) LIKE '%N' THEN vt.amount
        WHEN UPPER(vt.merchant) LIKE 'MO%' AND UPPER(vt.merchant) LIKE '%E' THEN vt.amount
        -- Gambling
        WHEN UPPER(vt.merchant) LIKE 'IF%' AND UPPER(vt.merchant) LIKE '%Y' THEN vt.amount
        WHEN UPPER(vt.merchant) LIKE 'YO%' AND UPPER(vt.merchant) LIKE '%G' THEN vt.amount
        WHEN UPPER(vt.merchant) LIKE 'CA%' AND UPPER(vt.merchant) LIKE '%S' THEN vt.amount
        WHEN UPPER(vt.merchant) LIKE 'PO%' AND UPPER(vt.merchant) LIKE '%E' THEN vt.amount
        WHEN UPPER(vt.merchant) LIKE 'VE%' AND UPPER(vt.merchant) LIKE '%R' THEN vt.amount
        ELSE 0
      END
    ) * 1.0 / NULLIF(SUM(vt.amount), 0) AS vendor_microfinance_gambling_payment_ratio_l12m
  FROM vendor_transactions vt
  WHERE vt.transaction_date >= DATE('now', '-12 months')
  GROUP BY vt.phone_number
),

-- 2. Grocery & Utilities Transaction Ratio (last 9 months)
vgu AS (
  SELECT
    vt.phone_number,
    COUNT(
      CASE
        -- Grocery
        WHEN UPPER(vt.merchant) LIKE 'KI%' AND UPPER(vt.merchant) LIKE '%E' THEN 1
        WHEN UPPER(vt.merchant) LIKE 'SE%' AND UPPER(vt.merchant) LIKE '%N' THEN 1
        WHEN UPPER(vt.merchant) LIKE 'EI%' AND UPPER(vt.merchant) LIKE '%E' THEN 1
        WHEN UPPER(vt.merchant) LIKE 'CO%' AND UPPER(vt.merchant) LIKE '%E' THEN 1
        WHEN UPPER(vt.merchant) LIKE 'MA%' AND UPPER(vt.merchant) LIKE '%X' THEN 1
        WHEN UPPER(vt.merchant) LIKE 'MR%' AND UPPER(vt.merchant) LIKE '%T' THEN 1
        -- Utilities
        WHEN UPPER(vt.merchant) LIKE 'RO%' AND UPPER(vt.merchant) LIKE '%D' THEN 1
        WHEN UPPER(vt.merchant) LIKE 'WA%' AND UPPER(vt.merchant) LIKE '%T' THEN 1
        WHEN UPPER(vt.merchant) LIKE 'EL%' AND UPPER(vt.merchant) LIKE '%Y' THEN 1
        WHEN UPPER(vt.merchant) LIKE 'OU%' AND UPPER(vt.merchant) LIKE '%K' THEN 1
        WHEN UPPER(vt.merchant) LIKE 'AW%' AND UPPER(vt.merchant) LIKE '%T' THEN 1
        WHEN UPPER(vt.merchant) LIKE 'BO%' AND UPPER(vt.merchant) LIKE '%T' THEN 1
        ELSE NULL
      END
    ) * 1.0 / NULLIF(COUNT(*), 0) AS vendor_grocery_utilities_transaction_ratio_l9m
  FROM vendor_transactions vt
  WHERE vt.transaction_date >= DATE('now', '-9 months')
  GROUP BY vt.phone_number
),

-- 3. Payment Delay Flag (last 6 months)
hpd AS (
  SELECT
    l.client_id,
    CASE
      WHEN COUNT(*) > 0 THEN 1 ELSE 0
    END AS history_payment_delay_flag_l6m
  FROM cash_flows cf
  JOIN loans l ON cf.loan_id = l.id
  WHERE
    cf.type = 'income'
    AND cf.payment_date > cf.scheduled_date
    AND cf.payment_date >= DATE('now', '-6 months')
  GROUP BY l.client_id
),

-- 4. Ratio of income payments in last 9 months to total income payments
hpr AS (
  SELECT
    l.client_id,
    SUM(
      CASE WHEN cf.payment_date >= DATE('now', '-9 months') THEN cf.amount ELSE 0 END
    ) * 1.0 / NULLIF(SUM(cf.amount), 0) AS history_payment_ratio_l9m_to_total
  FROM cash_flows cf
  JOIN loans l ON cf.loan_id = l.id
  WHERE cf.type = 'income'
  GROUP BY l.client_id
),

-- 5. Average profit margin for loans issued in the last 12 months
hpm AS (
  SELECT
    client_id,
    AVG(profit_margin) AS history_average_loan_profit_margin_l12m
  FROM (
    SELECT
      l.id AS loan_id,
      l.client_id,
      (l.amount - COALESCE(SUM(cf.amount), 0)) * 1.0 / NULLIF(l.amount, 0) AS profit_margin
    FROM loans l
    LEFT JOIN cash_flows cf ON cf.loan_id = l.id AND cf.type = 'income'
    WHERE l.start_date >= DATE('now', '-12 months')
    GROUP BY l.id
  ) sub
  GROUP BY client_id
)

-- ================================
-- Final query combining all features
-- ================================
SELECT
  c.id AS client_id,
  vmg.vendor_microfinance_gambling_payment_ratio_l12m,
  vgu.vendor_grocery_utilities_transaction_ratio_l9m,
  hpd.history_payment_delay_flag_l6m,
  hpr.history_payment_ratio_l9m_to_total,
  hpm.history_average_loan_profit_margin_l12m
FROM clients c
LEFT JOIN vmg ON vmg.phone_number = c.phone_number
LEFT JOIN vgu ON vgu.phone_number = c.phone_number
LEFT JOIN hpd ON hpd.client_id = c.id
LEFT JOIN hpr ON hpr.client_id = c.id
LEFT JOIN hpm ON hpm.client_id = c.id
WHERE c.id = :client_id;
