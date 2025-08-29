ATTACH 'data/tripadvisor.duckdb' AS db (READ_ONLY FALSE);
CREATE SCHEMA IF NOT EXISTS db.main;
USE db.main;

CREATE TABLE IF NOT EXISTS reviews AS
SELECT * FROM read_csv_auto('data/tripadvisor_hotel_reviews.csv', HEADER=TRUE);

CREATE OR REPLACE TABLE reviews AS
SELECT DISTINCT * FROM reviews;

COPY (SELECT * FROM reviews) TO 'data/reviews.parquet' (FORMAT PARQUET);
