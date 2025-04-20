#!/usr/bin/env python3
"""
Script to clean up the tax code text file and convert it to markdown format.
"""

import re
import os

def convert_french_ordinal_to_roman(text):
    """
    Convert French ordinal text to Roman numerals
    
    Args:
        text (str): Text containing French ordinals
        
    Returns:
        str: Text with French ordinals converted to Roman numerals
    """
    # Define replacements
    replacements = [
        (r'CHAPITRE\s+PREMIER', 'CHAPITRE I'),
        (r'PREMIERE\s+PARTIE', 'PARTIE I'),
        (r'DEUXIEME\s+PARTIE', 'PARTIE II'),
        (r'TROISIEME\s+PARTIE', 'PARTIE III'),
        (r'QUATRIEME\s+PARTIE', 'PARTIE IV'),
        (r'CINQUIEME\s+PARTIE', 'PARTIE V'),
        (r'SIXIEME\s+PARTIE', 'PARTIE VI'),
        (r'SEPTIEME\s+PARTIE', 'PARTIE VII'),
        (r'HUITIEME\s+PARTIE', 'PARTIE VIII'),
        (r'NEUVIEME\s+PARTIE', 'PARTIE IX'),
        (r'DIXIEME\s+PARTIE', 'PARTIE X'),
        (r'PREMIER\s+TITRE', 'TITRE I'),
        (r'PREMIER\s+LIVRE', 'LIVRE I'),
        (r'PREMIERE\s+SECTION', 'SECTION I'),
        (r'SOUS\s+TITRE\s+PREMIER', 'SOUS TITRE I'),
    ]
    
    # Apply replacements
    for pattern, replacement in replacements:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    
    return text

def clean_and_convert_to_markdown(input_file, output_file):
    """
    Clean up the tax code text file and convert it to markdown format.
    
    Args:
        input_file (str): Path to the input text file
        output_file (str): Path to the output markdown file
    """
    # Read the input file
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace "Code des impôts" with "Page"
    content = re.sub(r'Code des impôts\s+(\d+)', r'Page \1', content)
    
    # Remove C.D.I headers
    content = re.sub(r'C\.\s*D\.\s*I', '', content)
    
    # Clean up extra whitespace
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    # Convert French ordinal text to Roman numerals
    content = convert_french_ordinal_to_roman(content)
    
    # Format structural elements with dashes
    content = re.sub(r'(LIVRE\s+[IVX]+)\s*\n+([A-Z\s]+)', r'# \1 - \2', content)
    content = re.sub(r'(PARTIE\s+[IVX]+)\s*\n+([A-Z\s]+)', r'## \1 - \2', content)
    content = re.sub(r'(TITRE\s+[IVX]+)\s*\n+([A-Z\s]+)', r'### \1 - \2', content)
    content = re.sub(r'(SOUS TITRE\s+[IVX]+)\s*\n+([A-Z\s]+)', r'#### SOUS TITRE \1 - \2', content)
    content = re.sub(r'(CHAPITRE\s+[IVX]+)\s*\n+([A-Z\s]+)', r'##### \1 - \2', content)
    content = re.sub(r'(SECTION\s+[IVX]+)\s*\n+([A-Z\s]+)', r'###### SECTION \1 - \2', content)
    
    # Fix the double "SECTION" issue
    content = re.sub(r'###### SECTION SECTION', r'###### SECTION', content)
    
    # Format articles with 7 hash marks (####### instead of ######)
    content = re.sub(r'Article\s+(\d+\.\d+\.\d+)\s*-\s*', r'####### Article \1.\n', content)
    
    # Write the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Conversion complete. Output saved to {output_file}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(base_dir, "pdf", "code_des_impot_2025_extract_corrige.txt")
    output_file = os.path.join(base_dir, "pdf", "code_des_impot_2025_extract_clean.md")
    
    clean_and_convert_to_markdown(input_file, output_file)
