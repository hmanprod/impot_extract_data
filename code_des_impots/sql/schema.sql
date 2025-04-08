-- Table principale pour les sections du code
CREATE TABLE code_sections (
  id SERIAL PRIMARY KEY,
  parent_id INT REFERENCES code_sections(id) ON DELETE CASCADE,
  type VARCHAR(50) NOT NULL CHECK (type IN (
    'livre', 'partie', 'titre', 'chapitre', 'section', 'sous_titre', 'article','annexe'
  )),
  code VARCHAR(50) UNIQUE NOT NULL, -- Ex: "LIVRE I", "ART. 01.01.01"
  title TEXT NOT NULL,
  content TEXT,
  page_number_start INT,
  page_number_end INT,
  version_date DATE DEFAULT CURRENT_DATE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table pour les versions historiques des articles
CREATE TABLE article_versions (
  id SERIAL PRIMARY KEY,
  article_id INT REFERENCES code_sections(id) ON DELETE CASCADE,
  version_content TEXT NOT NULL,
  effective_date DATE NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table de liaison pour les références croisées entre articles
CREATE TABLE article_references (
  source_article_id INT REFERENCES code_sections(id) ON DELETE CASCADE,
  target_article_id INT REFERENCES code_sections(id) ON DELETE CASCADE,
  PRIMARY KEY (source_article_id, target_article_id)
);

-- Index pour les recherches performantes
CREATE INDEX idx_code_sections_code ON code_sections(code);
CREATE INDEX idx_code_sections_type ON code_sections(type);
CREATE INDEX idx_code_sections_parent ON code_sections(parent_id);
CREATE INDEX idx_article_versions_date ON article_versions(effective_date);

-- Configuration de la recherche plein texte
ALTER TABLE code_sections ADD COLUMN search_vector TSVECTOR;
UPDATE code_sections SET search_vector = 
  to_tsvector('french', coalesce(title, '') || ' ' || coalesce(content, ''));

CREATE TRIGGER tsvectorupdate BEFORE INSERT OR UPDATE
ON code_sections FOR EACH ROW EXECUTE FUNCTION 
  tsvector_update_trigger(search_vector, 'pg_catalog.french', title, content);