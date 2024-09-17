import os
import re
import unicodedata

def get_bairros(names):
    def remove_accented_chars(text):
        # Remove acentos e transforma o texto em ASCII
        normalized_text = unicodedata.normalize('NFD', text)
        return ''.join(char for char in normalized_text if unicodedata.category(char) != 'Mn')
    
    def replace_bairro(bairro):
        # Define os mapeamentos para substituição
        replacements = {
            'VALE DO ARICANDUVA': 'ARICANDUVA',
            'VILA BRASILANDIA': 'BRASILANDIA',
            'VILA CARRAO': 'CARRAO',
            'CIDADE ADEMAR': 'CID ADEMAR',
            'CIDADE DUTRA': 'CID DUTRA',
            'CIDADE TIRADENTES': 'CID TIRADENTES',
            'GUAIANAZES': 'GUAIANASES',
            'ALTO DA MOOCA': 'MOOCA',
            'PORTAL DO MORUMBI': 'MORUMBI',
            'PENHA DE FRANCA': 'PENHA',
            'PARQUE SAO LUCAS': 'SAO LUCAS',
            'SAO MIGUEL PAULISTA': 'SAO MIGUEL',
            'PARQUE SAO RAFAEL': 'SAO RAFAEL'
        }
        
        # Print para depuração
        print(f"Original bairro: '{bairro}'")
        
        bairro = remove_accented_chars(bairro)
        
        for old, new in replacements.items():
            if old in bairro:
                print(f"Replacing '{old}' with '{new}'")
                bairro = bairro.replace(old, new)
        
        return bairro
    
    bairros = [re.search(r'(?<=- )[^_]+', ocorrencia).group(0) for ocorrencia in names]
    
    bairros = [
        replace_bairro(
            bairro.upper()
        )
        for bairro in bairros
    ]
    
    # Write to file
    with open('bairros.txt', 'w') as f:
        for bairro in bairros:
            f.write(f"{bairro}\n")

    return bairros

def get_names_files(path):
    names = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.xlsx'):
                names.append(file)
    return names
