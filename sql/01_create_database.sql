-- ============================================================================
-- 01_create_database.sql
-- Database and Schema Initialization for Olist E-Commerce Analytics Platform
-- ============================================================================

-- Create Database (Run as superuser/postgres)
-- CREATE DATABASE olist_analytics;

-- Connect to database
-- \c olist_analytics;

-- Create Schemas for Multi-Tier Data Architecture
CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS analytics;

-- Grant Schema Permissions
GRANT ALL ON SCHEMA raw TO CURRENT_USER;
GRANT ALL ON SCHEMA staging TO CURRENT_USER;
GRANT ALL ON SCHEMA analytics TO CURRENT_USER;

COMMENT ON SCHEMA raw IS 'Raw ingestion layer directly mirroring source CSV files';
COMMENT ON SCHEMA staging IS 'Cleaned, typed, and standardized intermediate data layer';
COMMENT ON SCHEMA analytics IS 'Dimensional star schema optimized for BI reporting and SQL analytics';
