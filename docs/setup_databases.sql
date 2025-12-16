-- PostgreSQL Database Setup for EmotionSense
-- Run this script as PostgreSQL superuser (postgres)

-- Create development database
CREATE DATABASE emotionsense_dev
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'English_United States.1252'
    LC_CTYPE = 'English_United States.1252'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;

-- Create production database
CREATE DATABASE emotionsense_prod
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'English_United States.1252'
    LC_CTYPE = 'English_United States.1252'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;

-- Grant all privileges
GRANT ALL PRIVILEGES ON DATABASE emotionsense_dev TO postgres;
GRANT ALL PRIVILEGES ON DATABASE emotionsense_prod TO postgres;

-- Display created databases
SELECT datname FROM pg_database WHERE datname LIKE 'emotionsense%';
