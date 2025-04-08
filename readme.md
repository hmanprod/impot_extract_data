# Tax Code Data Processing

This repository contains tools and data for processing the Madagascar Tax Code and inserting it into a PostgreSQL database.

## Overview

The system extracts tax code articles and structure from text files and generates SQL insert statements to populate the `code_sections` table in the database. The hierarchical structure of the tax code (livres, parties, titres, chapitres, sections, and articles) is preserved with proper parent-child relationships.

## Directory Structure

- `/code_des_impots/` - Main directory for tax code processing
  - `/pdf/` - Contains the source text files extracted from PDFs
  - `/sql/` - Contains SQL scripts for database operations
  - `extract_from_text.py` - Main script for extracting tax code data from text files

## SQL Files

The tax code data is split into five SQL files for easier management:

1. `tax_code_split_1_header.sql` - Contains the header and disables triggers for faster insertion
2. `tax_code_split_2_structure.sql` - Contains top-level structure (livres, parties, titres)
3. `tax_code_split_3_chapters.sql` - Contains chapters and sections
4. `tax_code_split_4_articles.sql` - Contains articles with their content
5. `tax_code_split_5_footer.sql` - Re-enables triggers and updates the search vector

Additionally, there's a `drop_content.sql` script to clear existing data before inserting new content.

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

- Extracts hierarchical structure from text files
- Handles special characters and encoding issues
- Establishes proper parent-child relationships
- Avoids duplicate entries
- Uses PostgreSQL's SERIAL type for auto-generating IDs
- Optimizes insertion performance by disabling/enabling triggers

## Troubleshooting

If you encounter issues with special characters in the SQL files, make sure to:
1. Use the `E` prefix for string literals containing special characters
2. Properly escape single quotes with backslashes
3. Run the SQL files in the correct order

## License

This project is proprietary and confidential.