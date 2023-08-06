-- Create the Status enum type
CREATE TYPE status_enum AS ENUM ('active', 'inactive');
-- Create the StoreStatus table
CREATE TABLE store_status (
  store_id UUID NOT NULL,
  status status_enum NOT NULL,
  timestamp_utc TIMESTAMP NOT NULL
);
-- Create the StoreTimezone table
CREATE TABLE store_timezone (
  store_id UUID NOT NULL,
  timezone VARCHAR NOT NULL
);
-- Create the StoreBusinessHours table
CREATE TABLE store_business_hours (
  store_id UUID NOT NULL,
  day INT NOT NULL,
  start_time_local TIMESTAMP NOT NULL,
  end_time_local TIMESTAMP NOT NULL,
  PRIMARY KEY (store_id, day)
);
-- Create the ReportStatus enum type
-- CREATE TYPE report_status_enum AS ENUM ('RUNNING', 'COMPLETED');
-- Create the Report table
CREATE TABLE reports (
  id UUID PRIMARY KEY,
  status varchar NOT NULL,
  url VARCHAR
);