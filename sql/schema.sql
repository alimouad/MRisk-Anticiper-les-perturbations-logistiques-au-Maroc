CREATE TABLE cities(

    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    latitude DECIMAL(9,6) NOT NULL,
    longitude DECIMAL(9,6) NOT NULL
);

CREATE TABLE weather_forecasts (
    id SERIAL PRIMARY KEY,
    city_id INTEGER NOT NULL,
    forecast_date DATE NOT NULL,

    temperature_max DECIMAL(5,2),
    temperature_min DECIMAL(5,2),

    precipitation_sum DECIMAL(6,2),
    precipitation_probability INTEGER,

    wind_speed_max DECIMAL(6,2),
    wind_gusts_max DECIMAL(6,2),

    weather_code INTEGER,

    FOREIGN KEY (city_id) REFERENCES cities(id),

    UNIQUE (city_id, forecast_date)
);


CREATE TABLE weather_risks (
    id SERIAL PRIMARY KEY,
    weather_id INTEGER NOT NULL,

    temperature_category VARCHAR(50),
    precipitation_category VARCHAR(50),
    wind_category VARCHAR(50),

    risk_score DECIMAL(5,2) NOT NULL,
    risk_level VARCHAR(30) NOT NULL,

    FOREIGN KEY (weather_id)
        REFERENCES weather_forecasts(id),

    UNIQUE (weather_id)
);