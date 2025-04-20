#!/usr/bin/env python3
"""
Markdown to SQL Converter
This script converts a markdown file of the tax code to SQL insert statements
with proper parent relationships based on the hierarchical structure.
"""
import os
import re
from datetime import datetime
from collections import defaultdict

def extract_from_markdown(markdown_file_path):
    """
    Extract hierarchical structure and articles from the markdown file
    """
    print(f"Extracting content from {markdown_file_path}...")
    
    # Read the markdown file
    with open(markdown_file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Split the content into lines
    lines = content.split('\n')
    
    # Initialize variables to track the current hierarchy
    current_hierarchy = {
        'livre': None,
        'partie': None,
        'titre': None,
        'sous_titre': None,
        'chapitre': None,
        'section': None
    }
    
    # Initialize lists to store articles and structure items
    articles = []
    structure_items = []
    
    # Track which structure items we've already seen to avoid duplicates
    seen_structure_items = {}
    
    # Track the current page number
    current_page = 0
    
    # Process the content line by line
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Check for page numbers
        page_match = re.match(r'Page\s+(\d+)', line)
        if page_match:
            current_page = int(page_match.group(1))
            i += 1
            continue
        
        # Check for structure elements
        if line.startswith('# '):  # LIVRE
            # Extract the code and title
            match = re.match(r'# (LIVRE\s+[IVX]+)\s+-\s+(.+)', line)
            if match:
                code = match.group(1)
                title = match.group(2)
                
                # Check if we've already seen this structure item
                if code in seen_structure_items:
                    i += 1
                    continue
                
                # Add to structure items
                structure_items.append({
                    'type': 'livre',
                    'code': code,
                    'title': title,
                    'content': '',
                    'parent_code': None,
                    'page_number_start': current_page,
                    'page_number_end': None,
                    'version_date': datetime.now().strftime('%Y-%m-%d')
                })
                
                # Update current hierarchy
                current_hierarchy['livre'] = code
                current_hierarchy['partie'] = None
                current_hierarchy['titre'] = None
                current_hierarchy['sous_titre'] = None
                current_hierarchy['chapitre'] = None
                current_hierarchy['section'] = None
                
                # Mark this structure item as seen
                seen_structure_items[code] = True
        
        elif line.startswith('## '):  # PARTIE
            match = re.match(r'## (PREMIERE PARTIE|DEUXIEME PARTIE|TROISIEME PARTIE)\s+-\s+(.+)', line)
            if match:
                code = match.group(1)
                title = match.group(2)
                
                # Check if we've already seen this structure item
                if code in seen_structure_items:
                    i += 1
                    continue
                
                structure_items.append({
                    'type': 'partie',
                    'code': code,
                    'title': title,
                    'content': '',
                    'parent_code': current_hierarchy['livre'],
                    'page_number_start': current_page,
                    'page_number_end': None,
                    'version_date': datetime.now().strftime('%Y-%m-%d')
                })
                
                current_hierarchy['partie'] = code
                current_hierarchy['titre'] = None
                current_hierarchy['sous_titre'] = None
                current_hierarchy['chapitre'] = None
                current_hierarchy['section'] = None
                
                # Mark this structure item as seen
                seen_structure_items[code] = True
        
        elif line.startswith('### '):  # TITRE
            match = re.match(r'### (TITRE\s+[A-Z]+)\s+-\s+(.+)', line)
            if match:
                code = match.group(1)
                title = match.group(2)
                
                # Check if we've already seen this structure item
                if code in seen_structure_items:
                    i += 1
                    continue
                
                structure_items.append({
                    'type': 'titre',
                    'code': code,
                    'title': title,
                    'content': '',
                    'parent_code': current_hierarchy['partie'],
                    'page_number_start': current_page,
                    'page_number_end': None,
                    'version_date': datetime.now().strftime('%Y-%m-%d')
                })
                
                current_hierarchy['titre'] = code
                current_hierarchy['sous_titre'] = None
                current_hierarchy['chapitre'] = None
                current_hierarchy['section'] = None
                
                # Mark this structure item as seen
                seen_structure_items[code] = True
        
        elif line.startswith('#### '):  # SOUS TITRE
            match = re.match(r'#### (SOUS TITRE\s+[A-Z]+)\s+-\s+(.+)', line)
            if match:
                code = match.group(1)
                title = match.group(2)
                
                # Check if we've already seen this structure item
                if code in seen_structure_items:
                    i += 1
                    continue
                
                structure_items.append({
                    'type': 'sous_titre',
                    'code': code,
                    'title': title,
                    'content': '',
                    'parent_code': current_hierarchy['titre'],
                    'page_number_start': current_page,
                    'page_number_end': None,
                    'version_date': datetime.now().strftime('%Y-%m-%d')
                })
                
                current_hierarchy['sous_titre'] = code
                current_hierarchy['chapitre'] = None
                current_hierarchy['section'] = None
                
                # Mark this structure item as seen
                seen_structure_items[code] = True
        
        elif line.startswith('##### '):  # CHAPITRE
            match = re.match(r'##### (CHAPITRE\s+[A-Z]+)\s+-\s+(.+)', line)
            if match:
                code = match.group(1)
                title = match.group(2)
                
                # Check if we've already seen this structure item
                if code in seen_structure_items:
                    i += 1
                    continue
                
                structure_items.append({
                    'type': 'chapitre',
                    'code': code,
                    'title': title,
                    'content': '',
                    'parent_code': current_hierarchy['sous_titre'] or current_hierarchy['titre'],
                    'page_number_start': current_page,
                    'page_number_end': None,
                    'version_date': datetime.now().strftime('%Y-%m-%d')
                })
                
                current_hierarchy['chapitre'] = code
                current_hierarchy['section'] = None
                
                # Mark this structure item as seen
                seen_structure_items[code] = True
        
        elif line.startswith('###### '):  # SECTION
            match = re.match(r'###### SECTION\s+([IVX]+)\s+-\s+(.+)', line)
            if match:
                section_number = match.group(1)
                title = match.group(2)
                code = f"SECTION {section_number}"
                
                # Check if we've already seen this structure item
                if code in seen_structure_items:
                    i += 1
                    continue
                
                structure_items.append({
                    'type': 'section',
                    'code': code,
                    'title': title,
                    'content': '',
                    'parent_code': current_hierarchy['chapitre'],
                    'page_number_start': current_page,
                    'page_number_end': None,
                    'version_date': datetime.now().strftime('%Y-%m-%d')
                })
                
                current_hierarchy['section'] = code
                
                # Mark this structure item as seen
                seen_structure_items[code] = True
        
        elif line.startswith('####### '):  # Article
            match = re.match(r'####### Article\s+(\d+\.\d+\.\d+)\.', line)
            if match:
                article_code = match.group(1)
                
                # Get the article content (all lines until the next heading)
                article_content = []
                j = i + 1
                while j < len(lines) and not lines[j].strip().startswith('#'):
                    article_content.append(lines[j])
                    j += 1
                
                # Join the content lines
                content_text = '\n'.join(article_content).strip()
                
                # Remove "Page XXX" from the content
                content_text = re.sub(r'Page \d+\s*', '', content_text)
                
                # Check for "bis" at the beginning of the content
                bis_match = re.match(r'^bis\s*-\s*(.*)', content_text, re.DOTALL)
                
                if bis_match:
                    # Append "bis" to the article title and code
                    article_title = f"Article {article_code}-bis"
                    article_code = f"{article_code}-bis"
                    # Remove the "bis -" from the content
                    content_text = bis_match.group(1).strip()
                else:
                    # First check if the content starts with a letter subsection like "A-" after a Roman numeral subsection
                    letter_subsection_match = None
                    
                    # Check for subsections at the beginning of the content (I-, I-A-, etc.)
                    subsection_match = re.match(r'^([IVX]+-(?:[A-Z]+-)?|[A-Z]+-)\s*(.*)', content_text, re.DOTALL)
                    article_title = f"Article {article_code}"
                    
                    if subsection_match:
                        # Append the subsection to the article title and code
                        subsection = subsection_match.group(1).strip()
                        # Remove any spaces between parts of the subsection (e.g., "I- A-" becomes "I-A-")
                        subsection = re.sub(r'\s+', '', subsection)
                        # Remove trailing dashes from the subsection
                        subsection = re.sub(r'-+$', '', subsection)
                        
                        # Check if subsection has a letter part
                        if '-' in subsection:
                            # For cases like "I-A", make sure there's no trailing dash
                            parts = subsection.split('-')
                            if len(parts) > 1:
                                # Remove any trailing dash from the last part
                                parts[-1] = re.sub(r'-+$', '', parts[-1])
                                subsection = '-'.join(parts)
                        
                        article_title = f"Article {article_code}-{subsection}"
                        article_code = f"{article_code}-{subsection}"
                        # Remove the subsection from the content
                        content_text = subsection_match.group(2).strip()
                    
                    # Now check if the content starts with a letter subsection like "A-" after we've processed any other subsections
                    letter_subsection_match = re.match(r'^([A-Z])-\s*(.*)', content_text, re.DOTALL)
                    if letter_subsection_match:
                        letter_subsection = letter_subsection_match.group(1)
                        # If we already have a subsection, append the letter to it
                        if subsection_match:
                            article_title = f"Article {article_code}-{letter_subsection}"
                            article_code = f"{article_code}-{letter_subsection}"
                        else:
                            # Otherwise, create a new subsection
                            article_title = f"Article {article_code}-{letter_subsection}"
                            article_code = f"{article_code}-{letter_subsection}"
                        # Remove the letter subsection from the content
                        content_text = letter_subsection_match.group(2).strip()
                
                # Create the article object
                article = {
                    'code': f"ART. {article_code}",
                    'code_number': article_code,
                    'title': article_title,
                    'content': content_text,
                    'page_number': current_page,
                    'version_date': datetime.now().strftime('%Y-%m-%d')
                }
                
                articles.append(article)
                
                # Skip the content lines we've already processed
                i = j - 1
        
        i += 1
    
    # Update page_number_end for structure items
    for i in range(len(structure_items) - 1):
        if structure_items[i]['type'] == structure_items[i+1]['type']:
            structure_items[i]['page_number_end'] = structure_items[i+1]['page_number_start'] - 1
    
    return articles, structure_items

def generate_sql_inserts(articles, structure_items, output_dir):
    """Generate SQL insert statements for the articles and structure, split into multiple files"""
    print(f"Generating split SQL inserts to {output_dir}...")
    
    # Ensure the sql directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Define the paths for the split files
    header_file = os.path.join(output_dir, 'tax_code_split_1_header.sql')
    structure_file = os.path.join(output_dir, 'tax_code_split_2_structure.sql')
    chapters_file = os.path.join(output_dir, 'tax_code_split_3_chapters.sql')
    articles_file = os.path.join(output_dir, 'tax_code_split_4_articles.sql')
    footer_file = os.path.join(output_dir, 'tax_code_split_5_footer.sql')
    drop_file = os.path.join(output_dir, 'tax_code_split_0_drop.sql')
    
    # Create a dictionary to store the mapping of codes to IDs
    code_to_id = {}
    current_id = 1
    
    # First pass: assign IDs to each structure item
    for item in structure_items:
        code = item['code'].strip()
        code_to_id[code] = current_id
        current_id += 1
    
    # Write the drop content file
    with open(drop_file, 'w', encoding='utf-8') as f:
        f.write("-- Drop existing content from the code_sections table\n")
        f.write("\n-- Delete all records from code_sections table\n")
        f.write("DELETE FROM code_sections;\n")
        f.write("\n-- Reset the sequence for the id column\n")
        f.write("ALTER SEQUENCE code_sections_id_seq RESTART WITH 1;\n")
    
    # Write the header file
    with open(header_file, 'w', encoding='utf-8') as f:
        f.write("-- Auto-generated SQL inserts for tax code from markdown file (Part 1: Header)\n")
        f.write(f"-- Generated on: {datetime.now().strftime('%Y-%m-%d')}\n\n")
        f.write("-- Disable triggers for faster insertion\n")
        f.write("ALTER TABLE code_sections DISABLE TRIGGER tsvectorupdate;\n")
    
    # Track the most recent livre for parenting
    most_recent_livre = None
    
    # Write the structure file (livres, parties, titres)
    with open(structure_file, 'w', encoding='utf-8') as f:
        f.write("-- Auto-generated SQL inserts for tax code from markdown file (Part 2: Structure - Livres, Parties, Titres)\n")
        f.write(f"-- Generated on: {datetime.now().strftime('%Y-%m-%d')}\n\n")
        
        # Filter structure items for top-level elements
        top_level_items = [item for item in structure_items if item['type'] in ['livre', 'partie', 'titre']]
        
        # Generate SQL without explicit IDs, using subqueries instead
        for item in top_level_items:
            code = item['code'].strip()
            
            # Clean up the title and content for SQL
            title = item['title'].strip().replace("'", "''")
            content = item['content'].replace("'", "''")
            
            # Set page numbers
            page_start = item['page_number_start'] if item['page_number_start'] else 0
            page_end = item['page_number_end'] if item['page_number_end'] else "NULL"
            
            if item['type'] == 'livre':
                # Insert livre without parent reference
                insert_sql = f"INSERT INTO code_sections (type, code, title, content, page_number_start, page_number_end, version_date) VALUES ('{item['type']}', '{code}', '{title}', '{content}', {page_start}, {page_end}, '{item['version_date']}');\n"
                most_recent_livre = code  # Update the most recent livre
            elif item['type'] == 'partie':
                # Insert partie with parent reference to livre
                parent_code = item['parent_code'].strip() if item['parent_code'] else None
                if parent_code:
                    insert_sql = f"INSERT INTO code_sections (parent_id, type, code, title, content, page_number_start, page_number_end, version_date) VALUES ((SELECT id FROM code_sections WHERE code = '{parent_code}' LIMIT 1), '{item['type']}', '{code}', '{title}', '{content}', {page_start}, {page_end}, '{item['version_date']}');\n"
                else:
                    # If no parent, assign to the most recent livre
                    if most_recent_livre:
                        insert_sql = f"INSERT INTO code_sections (parent_id, type, code, title, content, page_number_start, page_number_end, version_date) VALUES ((SELECT id FROM code_sections WHERE code = '{most_recent_livre}' LIMIT 1), '{item['type']}', '{code}', '{title}', '{content}', {page_start}, {page_end}, '{item['version_date']}');\n"
                    else:
                        # If no livre exists yet, this is an error case but we'll insert without parent
                        insert_sql = f"INSERT INTO code_sections (type, code, title, content, page_number_start, page_number_end, version_date) VALUES ('{item['type']}', '{code}', '{title}', '{content}', {page_start}, {page_end}, '{item['version_date']}');\n"
            elif item['type'] == 'titre':
                # Insert titre with parent reference to partie or livre
                parent_code = item['parent_code'].strip() if item['parent_code'] else None
                if parent_code:
                    insert_sql = f"INSERT INTO code_sections (parent_id, type, code, title, content, page_number_start, page_number_end, version_date) VALUES ((SELECT id FROM code_sections WHERE code = '{parent_code}' LIMIT 1), '{item['type']}', '{code}', '{title}', '{content}', {page_start}, {page_end}, '{item['version_date']}');\n"
                else:
                    # If no parent, assign to the most recent livre
                    if most_recent_livre:
                        insert_sql = f"INSERT INTO code_sections (parent_id, type, code, title, content, page_number_start, page_number_end, version_date) VALUES ((SELECT id FROM code_sections WHERE code = '{most_recent_livre}' LIMIT 1), '{item['type']}', '{code}', '{title}', '{content}', {page_start}, {page_end}, '{item['version_date']}');\n"
                    else:
                        # If no livre exists yet, this is an error case but we'll insert without parent
                        insert_sql = f"INSERT INTO code_sections (type, code, title, content, page_number_start, page_number_end, version_date) VALUES ('{item['type']}', '{code}', '{title}', '{content}', {page_start}, {page_end}, '{item['version_date']}');\n"
            
            f.write(insert_sql)
    
    # Track the most recent titre for parenting chapters and sections
    most_recent_titre = None
    most_recent_chapitre = None
    
    # Write the chapters and sections file
    with open(chapters_file, 'w', encoding='utf-8') as f:
        f.write("-- Auto-generated SQL inserts for tax code from markdown file (Part 3: Chapters and Sections)\n")
        f.write(f"-- Generated on: {datetime.now().strftime('%Y-%m-%d')}\n\n")
        
        # Filter structure items for chapter-level elements
        chapter_level_items = [item for item in structure_items if item['type'] in ['sous_titre', 'chapitre', 'section']]
        
        # First, get the most recent titre from top_level_items
        for item in reversed(top_level_items):
            if item['type'] == 'titre':
                most_recent_titre = item['code'].strip()
                break
        
        # Generate SQL without explicit IDs, using subqueries instead
        for item in chapter_level_items:
            code = item['code'].strip()
            
            # Clean up the title and content for SQL
            title = item['title'].strip().replace("'", "''")
            content = item['content'].replace("'", "''")
            
            # Set page numbers
            page_start = item['page_number_start'] if item['page_number_start'] else 0
            page_end = item['page_number_end'] if item['page_number_end'] else "NULL"
            
            # Insert with parent reference
            parent_code = item['parent_code'].strip() if item['parent_code'] else None
            
            if parent_code:
                insert_sql = f"INSERT INTO code_sections (parent_id, type, code, title, content, page_number_start, page_number_end, version_date) VALUES ((SELECT id FROM code_sections WHERE code = '{parent_code}' LIMIT 1), '{item['type']}', '{code}', '{title}', '{content}', {page_start}, {page_end}, '{item['version_date']}');\n"
            else:
                # If no parent, assign based on type
                if item['type'] == 'sous_titre':
                    # Sous titre should be under a titre
                    if most_recent_titre:
                        insert_sql = f"INSERT INTO code_sections (parent_id, type, code, title, content, page_number_start, page_number_end, version_date) VALUES ((SELECT id FROM code_sections WHERE code = '{most_recent_titre}' LIMIT 1), '{item['type']}', '{code}', '{title}', '{content}', {page_start}, {page_end}, '{item['version_date']}');\n"
                    else:
                        # If no titre exists yet, assign to the most recent livre
                        insert_sql = f"INSERT INTO code_sections (parent_id, type, code, title, content, page_number_start, page_number_end, version_date) VALUES ((SELECT id FROM code_sections WHERE code = '{most_recent_livre}' LIMIT 1), '{item['type']}', '{code}', '{title}', '{content}', {page_start}, {page_end}, '{item['version_date']}');\n"
                elif item['type'] == 'chapitre':
                    # Chapitre should be under a titre or sous_titre
                    if most_recent_titre:
                        insert_sql = f"INSERT INTO code_sections (parent_id, type, code, title, content, page_number_start, page_number_end, version_date) VALUES ((SELECT id FROM code_sections WHERE code = '{most_recent_titre}' LIMIT 1), '{item['type']}', '{code}', '{title}', '{content}', {page_start}, {page_end}, '{item['version_date']}');\n"
                    else:
                        # If no titre exists yet, assign to the most recent livre
                        insert_sql = f"INSERT INTO code_sections (parent_id, type, code, title, content, page_number_start, page_number_end, version_date) VALUES ((SELECT id FROM code_sections WHERE code = '{most_recent_livre}' LIMIT 1), '{item['type']}', '{code}', '{title}', '{content}', {page_start}, {page_end}, '{item['version_date']}');\n"
                    most_recent_chapitre = code  # Update the most recent chapitre
                elif item['type'] == 'section':
                    # Section should be under a chapitre
                    if most_recent_chapitre:
                        insert_sql = f"INSERT INTO code_sections (parent_id, type, code, title, content, page_number_start, page_number_end, version_date) VALUES ((SELECT id FROM code_sections WHERE code = '{most_recent_chapitre}' LIMIT 1), '{item['type']}', '{code}', '{title}', '{content}', {page_start}, {page_end}, '{item['version_date']}');\n"
                    elif most_recent_titre:
                        # If no chapitre exists yet, assign to the most recent titre
                        insert_sql = f"INSERT INTO code_sections (parent_id, type, code, title, content, page_number_start, page_number_end, version_date) VALUES ((SELECT id FROM code_sections WHERE code = '{most_recent_titre}' LIMIT 1), '{item['type']}', '{code}', '{title}', '{content}', {page_start}, {page_end}, '{item['version_date']}');\n"
                    else:
                        # If no titre exists yet, assign to the most recent livre
                        insert_sql = f"INSERT INTO code_sections (parent_id, type, code, title, content, page_number_start, page_number_end, version_date) VALUES ((SELECT id FROM code_sections WHERE code = '{most_recent_livre}' LIMIT 1), '{item['type']}', '{code}', '{title}', '{content}', {page_start}, {page_end}, '{item['version_date']}');\n"
            
            f.write(insert_sql)
            
            # Update tracking variables
            if item['type'] == 'titre':
                most_recent_titre = code
            elif item['type'] == 'chapitre':
                most_recent_chapitre = code
    
    # Create a mapping of article codes to their parent chapters/sections
    article_parents = {}
    
    # For each article, find its parent chapter or section
    for article in articles:
        code_number = article['code_number']
        parent_found = False
        
        # Try to find a matching chapter or section based on the article code
        prefix = code_number.split('.')[0]
        
        # First look for chapters that might contain this article
        for item in structure_items:
            if item['type'] in ['chapitre', 'section'] and prefix in item['code']:
                article_parents[article['code']] = item['code']
                parent_found = True
                break
        
        # If no direct match, use the first chapter as default parent
        if not parent_found:
            for item in structure_items:
                if item['type'] == 'chapitre':
                    article_parents[article['code']] = item['code']
                    break
    
    # Write the articles file using PL/pgSQL
    with open(articles_file, 'w', encoding='utf-8') as f:
        f.write("-- Auto-generated SQL inserts for tax code from markdown file (Part 4: Articles)\n")
        f.write(f"-- Generated on: {datetime.now().strftime('%Y-%m-%d')}\n\n")
        
        # Use PL/pgSQL to handle parent references
        f.write("-- Insert articles with parent references\n")
        f.write("-- We'll use a different approach here to avoid explicit IDs\n")
        f.write("-- Instead, we'll reference the parent chapter by its code\n\n")
        
        f.write("-- First, let's create a temporary variable to store the parent ID for the articles\n")
        f.write("DO $$\n")
        f.write("DECLARE\n")
        f.write("    parent_id_var INTEGER;\n")
        f.write("BEGIN\n")
        
        # Group articles by their parent chapter/section
        articles_by_parent = {}
        for article in articles:
            parent_code = article_parents.get(article['code'])
            if parent_code:
                if parent_code not in articles_by_parent:
                    articles_by_parent[parent_code] = []
                articles_by_parent[parent_code].append(article)
        
        # If no parent mapping was found, group all articles under the first chapter
        if not articles_by_parent:
            first_chapter = next((item['code'] for item in structure_items if item['type'] == 'chapitre'), None)
            if first_chapter:
                articles_by_parent[first_chapter] = articles
        
        # Generate SQL for each group of articles
        for parent_code, article_group in articles_by_parent.items():
            if not article_group:
                continue
            
            # Get the parent ID
            f.write(f"    -- Get the ID of the chapter/section that will contain these articles\n")
            f.write(f"    SELECT id INTO parent_id_var FROM code_sections \n")
            f.write(f"    WHERE code = '{parent_code}'\n")
            f.write(f"    LIMIT 1;\n\n")
            
            # Insert the articles
            f.write(f"    -- Insert articles for {parent_code}\n")
            f.write(f"    INSERT INTO code_sections (parent_id, type, code, title, content, page_number_start, page_number_end, version_date) \n")
            f.write(f"    VALUES \n")
            
            # Generate the VALUES clause for each article
            for i, article in enumerate(article_group):
                # Clean up the title and content for SQL
                title = article['title'].strip().replace("'", "''")
                
                # Properly escape content for PostgreSQL
                content = article['content'].replace("'", "''")
                # Replace problematic characters that might cause truncation
                content = content.replace('\\', '\\\\')  # Escape backslashes
                content = content.replace('\n', '\\n')     # Preserve newlines for SQL
                content = content.replace('\r', '')      # Remove carriage returns
                
                # Use E prefix for escaping special characters and properly handle newlines
                f.write(f"    (parent_id_var, 'article', '{article['code']}', E'{title}', E'{content}', {article['page_number']}, NULL, '{datetime.now().strftime('%Y-%m-%d')}')")
                
                if i < len(article_group) - 1:
                    f.write(",\n")
                else:
                    f.write(";\n\n")
        
        f.write("END $$;\n")
    
    # Write the footer file
    with open(footer_file, 'w', encoding='utf-8') as f:
        f.write("-- Auto-generated SQL inserts for tax code from markdown file (Part 5: Footer)\n")
        f.write(f"-- Generated on: {datetime.now().strftime('%Y-%m-%d')}\n\n")
        
        # Re-enable triggers
        f.write("-- Re-enable triggers after all inserts\n")
        f.write("ALTER TABLE code_sections ENABLE TRIGGER tsvectorupdate;\n\n")
        
        # Update the search vector for all records
        f.write("-- Update the search vector for all inserted records\n")
        f.write("UPDATE code_sections \n")
        f.write("SET search_vector = to_tsvector('french', coalesce(title, '') || ' ' || coalesce(content, ''))\n")
        f.write("WHERE search_vector IS NULL;\n")
    
    print(f"Generated split SQL files in {output_dir}:")
    print(f"  - {os.path.basename(header_file)}")
    print(f"  - {os.path.basename(structure_file)}")
    print(f"  - {os.path.basename(chapters_file)}")
    print(f"  - {os.path.basename(articles_file)}")
    print(f"  - {os.path.basename(footer_file)}")
    print(f"  - {os.path.basename(drop_file)}")

def main():
    """Main function to run the script"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    markdown_file = os.path.join(base_dir, "pdf", "code_des_impot_2025_extract_clean.md")
    sql_dir = os.path.join(base_dir, "sql")
    
    # Extract articles and structure from the markdown file
    articles, structure_items = extract_from_markdown(markdown_file)
    
    # Generate SQL inserts
    generate_sql_inserts(articles, structure_items, sql_dir)
    
    print("Generated split SQL files in {}:".format(sql_dir))
    print("  - tax_code_split_0_drop.sql")
    print("  - tax_code_split_1_header.sql")
    print("  - tax_code_split_2_structure.sql")
    print("  - tax_code_split_3_chapters.sql")
    print("  - tax_code_split_4_articles.sql")
    print("  - tax_code_split_5_footer.sql")
    print("Conversion complete!")

if __name__ == "__main__":
    main()
