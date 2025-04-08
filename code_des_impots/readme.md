# Tax Code Data Processing

This repository contains tools and data for processing the Madagascar Tax Code and inserting it into a PostgreSQL database.

## Overview

The system extracts tax code articles and structure from text files and generates SQL insert statements to populate the `code_sections` table in the database. The hierarchical structure of the tax code (livres, parties, titres, chapitres, sections, and articles) is preserved with proper parent-child relationships.

## Directory Structure

- `/code_des_impots/` - Main directory for tax code processing
  - `/pdf/` - Contains the source text files extracted from PDFs
  - `/sql/` - Contains SQL scripts for database operations
  - `extract_from_text.py` - Main script for extracting tax code data from text files
  - `clean_and_convert.py` - Script to clean and convert text files to markdown format
  - `md_to_sql.py` - Script to convert markdown to SQL insert statements

## SQL Files

The tax code data is split into six SQL files for easier management:

- `tax_code_split_0_drop.sql` - Drops existing content from the code_sections table and resets the ID sequence
- `tax_code_split_1_header.sql` - Contains header information and disables triggers for faster insertion
- `tax_code_split_2_structure.sql` - Contains top-level structure elements (livres, parties, titres)
- `tax_code_split_3_chapters.sql` - Contains chapter-level elements (sous_titres, chapitres, sections)
- `tax_code_split_4_articles.sql` - Contains all article content with proper parent relationships
- `tax_code_split_5_footer.sql` - Re-enables triggers and updates the search vector for all inserted records

## Procedure for Creating SQL Files

The process of creating SQL files from the tax code involves several steps:

1. **Extract Text from PDF**
   - Extract the tax code text from PDF files (manually or using PDF extraction tools)
   - Save the extracted text in `/code_des_impots/pdf/code_des_impot_2025_extract.txt`

2. **Clean and Convert to Markdown**
   - Run the `clean_and_convert.py` script to clean the text and convert it to markdown format
   - This script converts French ordinal text to Roman numerals (e.g., "CHAPITRE PREMIER" to "CHAPITRE I")
   - The output is saved as `/code_des_impots/pdf/code_des_impot_2025_extract_clean.md`

   ```bash
   cd code_des_impots
   python clean_and_convert.py
   ```

3. **Generate SQL Files**
   - Run the `md_to_sql.py` script to parse the markdown file and generate SQL insert statements
   - The script extracts the hierarchical structure and articles from the markdown file
   - It creates parent-child relationships between elements (all types have a parent except for "livre")
   - The output is saved as multiple SQL files in the `/code_des_impots/sql/` directory

   ```bash
   python md_to_sql.py
   ```

4. **Import into Database**
   - Execute the generated SQL files in the correct order to populate the database
   - This can be done using the PostgreSQL command-line tool or a database management interface

   ```bash
   psql -U your_username -d your_database -f code_des_impots/sql/tax_code_split_0_drop.sql
   psql -U your_username -d your_database -f code_des_impots/sql/tax_code_split_1_header.sql
   psql -U your_username -d your_database -f code_des_impots/sql/tax_code_split_2_structure.sql
   psql -U your_username -d your_database -f code_des_impots/sql/tax_code_split_3_chapters.sql
   psql -U your_username -d your_database -f code_des_impots/sql/tax_code_split_4_articles.sql
   psql -U your_username -d your_database -f code_des_impots/sql/tax_code_split_5_footer.sql
   ```

## Database Schema

The tax code data is stored in the `code_sections` table with the following structure:

```sql
CREATE TABLE code_sections (
  id SERIAL PRIMARY KEY,
  parent_id INT REFERENCES code_sections(id) ON DELETE CASCADE,
  type VARCHAR(50) NOT NULL CHECK (type IN (
    'livre', 'partie', 'titre', 'chapitre', 'section', 'sous_titre', 'article','annexe'
  )),
  code VARCHAR(50) UNIQUE NOT NULL,
  title TEXT NOT NULL,
  content TEXT,
  page_number_start INT,
  page_number_end INT,
  version_date DATE DEFAULT CURRENT_DATE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Usage

### Extracting Tax Code Data

To extract tax code data from a text file and generate SQL files:

```bash
python3 extract_from_text.py path/to/text_file.txt
```

This will generate:
- A JSON file with the parsed data (`parsed_tax_code_from_text.json`)
- Five SQL files in the `sql/` directory for database insertion
- A combined SQL file (`tax_code_from_text_inserts.sql`) for backward compatibility

### Inserting Data into the Database

To insert the tax code data into the database, run the SQL files in the following order:

```bash
psql -d your_database -f sql/drop_content.sql
psql -d your_database -f sql/tax_code_split_1_header.sql
psql -d your_database -f sql/tax_code_split_2_structure.sql
psql -d your_database -f sql/tax_code_split_3_chapters.sql
psql -d your_database -f sql/tax_code_split_4_articles.sql
psql -d your_database -f sql/tax_code_split_5_footer.sql
```

## Features

- Converts French ordinal text to Roman numerals (e.g., "CHAPITRE PREMIER" to "CHAPITRE I")
- Properly formats article codes and titles, including subsection markers
- Handles special cases like "bis" designations
- Ensures all structure types have a parent except for "livre"
- Maintains page number references for navigation
- Creates a search vector for full-text search capabilities

## Troubleshooting

If you encounter issues with special characters in the SQL files, make sure to:
1. Use the `E` prefix for string literals containing special characters
2. Properly escape single quotes with backslashes
3. Run the SQL files in the correct order

## License

This project is proprietary and confidential.