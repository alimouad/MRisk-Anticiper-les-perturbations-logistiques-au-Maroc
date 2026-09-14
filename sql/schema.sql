
CREATE TABLE IF NOT EXISTS cities (
    city_id SERIAL PRIMARY KEY,
    city_name VARCHAR(100) NOT NULL UNIQUE,
    latitude DECIMAL(9, 6) NOT NULL,
    longitude DECIMAL(9, 6) NOT NULL
);

CREATE TABLE IF NOT EXISTS weather_forecasts (
    forecast_id SERIAL PRIMARY KEY,

    city_id INTEGER NOT NULL,

    forecast_date DATE NOT NULL,

    temperature_max DECIMAL(5, 2),
    temperature_min DECIMAL(5, 2),

    precipitation DECIMAL(8, 2),

    precipitation_probability INTEGER,

    wind_speed DECIMAL(8, 2),

    wind_gusts DECIMAL(8, 2),

    weather_code INTEGER,

    risk_score DECIMAL(5, 2),

    risk_level VARCHAR(20),

    FOREIGN KEY (city_id)
        REFERENCES cities(city_id),

    UNIQUE (city_id, forecast_date)
);