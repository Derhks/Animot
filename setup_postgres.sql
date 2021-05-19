-- prepares a PostgreSQL server for the project
-- Replace username and password, password must be in quotation marks

DROP DATABASE IF EXISTS animot_db;
CREATE DATABASE animot_db;
DROP USER IF EXISTS username;
CREATE USER username WITH ENCRYPTED PASSWORD 'password';
ALTER ROLE username SET client_encoding TO 'utf8';
ALTER ROLE username SET default_transaction_isolation TO 'read committed';
ALTER ROLE username SET default_transaction_isolation TO 'read committed';
GRANT ALL PRIVILEGES ON DATABASE animot_db TO username;
