
-- ============================================================
-- WEATHER RISK PIPELINE
-- Business Analysis Queries
-- ============================================================


-- ============================================================
-- 1. Top 10 most risky forecasts
-- Question:
-- Which city/date has the highest weather risk?
-- ============================================================

SELECT
    c.name AS city,
    wf.forecast_date,
    wr.risk_score,
    wr.risk_level
FROM weather_risks wr
JOIN weather_forecasts wf
    ON wr.weather_id = wf.id
JOIN cities c
    ON wf.city_id = c.id
ORDER BY wr.risk_score DESC
LIMIT 10;


-- ============================================================
-- 2. Average risk score by city
-- Question:
-- Which cities have the highest average weather risk?
-- ============================================================

SELECT
    c.name AS city,
    ROUND(AVG(wr.risk_score), 2) AS average_risk_score
FROM weather_risks wr
JOIN weather_forecasts wf
    ON wr.weather_id = wf.id
JOIN cities c
    ON wf.city_id = c.id
GROUP BY c.name
ORDER BY average_risk_score DESC;


-- ============================================================
-- 3. Highest temperature
-- Question:
-- Which cities/dates have the highest temperatures?
-- ============================================================

SELECT
    c.name AS city,
    wf.forecast_date,
    wf.temperature_max
FROM weather_forecasts wf
JOIN cities c
    ON wf.city_id = c.id
ORDER BY wf.temperature_max DESC
LIMIT 10;


-- ============================================================
-- 4. Highest precipitation
-- Question:
-- Which cities/dates have the highest expected rainfall?
-- ============================================================

SELECT
    c.name AS city,
    wf.forecast_date,
    wf.precipitation_sum
FROM weather_forecasts wf
JOIN cities c
    ON wf.city_id = c.id
ORDER BY wf.precipitation_sum DESC
LIMIT 10;


-- ============================================================
-- 5. Highest wind speed
-- Question:
-- Which cities/dates have the strongest expected winds?
-- ============================================================

SELECT
    c.name AS city,
    wf.forecast_date,
    wf.wind_speed_max,
    wf.wind_gusts_max
FROM weather_forecasts wf
JOIN cities c
    ON wf.city_id = c.id
ORDER BY wf.wind_speed_max DESC
LIMIT 10;


-- ============================================================
-- 6. Critical risk forecasts
-- Question:
-- How many forecasts are classified as Critical?
-- ============================================================

SELECT
    COUNT(*) AS critical_forecasts
FROM weather_risks
WHERE risk_level = 'Critique';


-- ============================================================
-- 7. Number of forecasts by risk level
-- Question:
-- What is the distribution of weather risks?
-- ============================================================

SELECT
    risk_level,
    COUNT(*) AS number_of_forecasts
FROM weather_risks
GROUP BY risk_level
ORDER BY number_of_forecasts DESC;


-- ============================================================
-- 8. Most risky day overall
-- Question:
-- Which forecast dates have the highest average risk?
-- ============================================================

SELECT
    wf.forecast_date,
    ROUND(AVG(wr.risk_score), 2) AS average_risk_score
FROM weather_risks wr
JOIN weather_forecasts wf
    ON wr.weather_id = wf.id
GROUP BY wf.forecast_date
ORDER BY average_risk_score DESC;


-- ============================================================
-- 9. Cities with heavy precipitation
-- Question:
-- Which cities have forecasts with precipitation >= 15 mm?
-- ============================================================

SELECT
    c.name AS city,
    wf.forecast_date,
    wf.precipitation_sum,
    wr.risk_score,
    wr.risk_level
FROM weather_forecasts wf
JOIN cities c
    ON wf.city_id = c.id
JOIN weather_risks wr
    ON wr.weather_id = wf.id
WHERE wf.precipitation_sum >= 15
ORDER BY wf.precipitation_sum DESC;


-- ============================================================
-- 10. High-risk forecasts
-- Question:
-- Which forecasts require operational attention?
-- ============================================================

SELECT
    c.name AS city,
    wf.forecast_date,
    wf.temperature_max,
    wf.precipitation_sum,
    wf.wind_speed_max,
    wr.risk_score,
    wr.risk_level
FROM weather_forecasts wf
JOIN cities c
    ON wf.city_id = c.id
JOIN weather_risks wr
    ON wr.weather_id = wf.id
WHERE wr.risk_score >= 50
ORDER BY wr.risk_score DESC;

