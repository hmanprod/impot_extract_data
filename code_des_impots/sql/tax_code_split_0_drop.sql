-- Drop existing content from the code_sections table

-- Delete all records from code_sections table
DELETE FROM code_sections;

-- Reset the sequence for the id column
ALTER SEQUENCE code_sections_id_seq RESTART WITH 1;
