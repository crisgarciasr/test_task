-- TODO: Add here all the necessary variables
-- Example of a query to get the number of loans in the last 12 months for a specific client
SELECT clients.id as client_id,
    SUM(
        CASE
            WHEN DATE(loans.start_date) >= DATE('now', '-6 months') THEN 1
            ELSE NULL
        END
    ) AS loans_count_l12m
FROM clients
    JOIN loans ON clients.id = loans.client_id
WHERE clients.id = :client_id
GROUP BY clients.id;