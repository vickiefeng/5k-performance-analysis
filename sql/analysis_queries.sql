-- 5K Performance Analysis
-- Analytical queries for the SQLite race results database.


-- ============================================================
-- 1. Race and Event Coverage
-- ============================================================

SELECT
    races.race_name,
    COUNT(DISTINCT events.event_id) AS num_events,
    COUNT(results.result_id) AS num_results
FROM races
JOIN events
    ON races.race_id = events.race_id
JOIN results
    ON events.event_id = results.event_id
GROUP BY
    races.race_id,
    races.race_name
ORDER BY
    num_results DESC;

    
-- ============================================================
-- 2. Performance by Race and Gender
-- ============================================================

SELECT
    races.race_name,
    results.gender,
    COUNT(*) AS num_results,
    ROUND(AVG(results.chip_time_seconds) / 60.0, 2)
        AS mean_finish_time_minutes,
    ROUND(AVG(results.age_percentage_numeric), 2)
        AS mean_age_percentage
FROM results
JOIN events
    ON results.event_id = events.event_id
JOIN races
    ON events.race_id = races.race_id
WHERE
    results.chip_time_seconds IS NOT NULL
GROUP BY
    races.race_id,
    races.race_name,
    results.gender
ORDER BY
    races.race_name,
    results.gender;


-- ============================================================
-- 3. Performance by Age Group and Gender
-- ============================================================

WITH grouped_results AS (
    SELECT
        gender,
        CASE
            WHEN age < 10 THEN 'Under 10'
            WHEN age < 20 THEN '10-19'
            WHEN age < 30 THEN '20-29'
            WHEN age < 40 THEN '30-39'
            WHEN age < 50 THEN '40-49'
            WHEN age < 60 THEN '50-59'
            WHEN age < 70 THEN '60-69'
            ELSE '70+'
        END AS age_group,
        chip_time_seconds / 60.0 AS finish_time_minutes,
        age_percentage_numeric
    FROM results
    WHERE age IS NOT NULL
)

SELECT
    age_group,
    gender,
    COUNT(finish_time_minutes) AS num_finish_times,
    ROUND(AVG(finish_time_minutes), 2)
        AS mean_finish_time_minutes,
    ROUND(AVG(age_percentage_numeric), 2)
        AS mean_age_percentage
FROM grouped_results
GROUP BY
    age_group,
    gender
ORDER BY
    CASE age_group
        WHEN 'Under 10' THEN 1
        WHEN '10-19' THEN 2
        WHEN '20-29' THEN 3
        WHEN '30-39' THEN 4
        WHEN '40-49' THEN 5
        WHEN '50-59' THEN 6
        WHEN '60-69' THEN 7
        WHEN '70+' THEN 8
    END,
    gender;