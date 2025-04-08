-- Auto-generated SQL inserts for tax code from markdown file (Part 5: Footer)
-- Generated on: 2025-04-08

-- Re-enable triggers after all inserts
ALTER TABLE code_sections ENABLE TRIGGER tsvectorupdate;

-- Update the search vector for all inserted records
UPDATE code_sections 
SET search_vector = to_tsvector('french', coalesce(title, '') || ' ' || coalesce(content, ''))
WHERE search_vector IS NULL;
