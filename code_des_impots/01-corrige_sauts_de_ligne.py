import re

input_file = "pdf/code_des_impot_2025_extract.txt"
output_file = "pdf/code_des_impot_2025_extract_corrige.txt"

def is_titre(line):
    texte = line.strip().replace('’', '').replace("'", '').replace('.', '').replace(';', '').replace(':', '').replace('-', '').replace(' ', '')
    return texte.isupper() and len(texte) > 2

def corrige_sauts_de_ligne(input_path, output_path):
    with open(input_path, encoding='utf-8') as f:
        lignes = f.readlines()
    resultat = []
    buffer = ''
    n = len(lignes)
    for i, ligne in enumerate(lignes):
        if is_titre(ligne) or ligne.strip() == '':
            if buffer:
                resultat.append(buffer.strip())
                buffer = ''
            # Ajoute la ligne titre telle quelle
            resultat.append(ligne.rstrip())
        else:
            if buffer == '':
                buffer = ligne.rstrip()
            else:
                if re.search(r'[.!?;:»”]\s*$', buffer):
                    resultat.append(buffer)
                    buffer = ligne.rstrip()
                else:
                    buffer += ' ' + ligne.strip()
    if buffer:
        resultat.append(buffer.strip())
    # Supprime les doublons de lignes vides
    resultat_final = []
    for l in resultat:
        if l == '' and (not resultat_final or resultat_final[-1] == ''):
            continue
        resultat_final.append(l)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(resultat_final))

if __name__ == "__main__":
    corrige_sauts_de_ligne(input_file, output_file)
    print(f"Fichier corrigé écrit dans {output_file}")
