SELECT 
    customer_id, 
    COUNT(event_id) as total_events, 
    SUM(session_length_sec) as total_session_time 
FROM {{ ref('stg_telemetry') }} 
GROUP BY customer_id