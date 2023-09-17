import os
import sys
import requests
from bs4 import BeautifulSoup

def scarica_contenuto(url_base, tipo_mbti, nome_file, cartella_destinazione):
    url_completo = url_base + tipo_mbti.lower()
    response = requests.get(url_completo)
    
    # Verifica che la richiesta sia andata a buon fine
    if response.status_code != 200:
        print(f"Errore durante il download da {url_completo}")
        return

    # Estrae il contenuto specificato dalla pagina
    soup = BeautifulSoup(response.content, 'html.parser')
    blocchi = soup.find_all('blockquote')
    
    contenuto_relevante = ""
    for blocco in blocchi:
        # Estrai tutti i tag <p> successivi a <blockquote>
        for p in blocco.find_next_siblings('p'):
            contenuto_relevante += p.get_text() + "\n"

    # Crea un file con il nome specificato e scrive il contenuto
    with open(os.path.join(cartella_destinazione, f"{nome_file}.txt"), 'w', encoding='utf-8') as file:
        file.write(contenuto_relevante)

def main():
    # Controllo dei parametri da riga di comando
    if len(sys.argv) != 2:
        print("Uso: script.py <cartella_destinazione>")
        sys.exit(1)

    cartella_destinazione = sys.argv[1]
    
    # Crea la cartella se non esiste
    if not os.path.exists(cartella_destinazione):
        os.makedirs(cartella_destinazione)

    url_base = "https://www.typeinmind.com/"
    mapping_tipi = {
        "FiSe": "isfp",
        "TiNe": "intp",
        "FiNe": "infp",
        "TiSe": "istp",
        "NiFe": "infj",
        "NiTe": "intj",
        "SiFe": "isfj",
        "SiTe": "istj",
        "FeNi": "enfj",
        "FeSi": "esfj",
        "TeNi": "entj",
        "TeSi": "estj",
        "NeFi": "enfp",
        "NeTi": "entp",
        "SeFi": "esfp",
        "SeTi": "estp"
    }

    for tipo, nome_file in mapping_tipi.items():
        scarica_contenuto(url_base, tipo, nome_file, cartella_destinazione)
        print(f"Scaricato {nome_file}")

if __name__ == "__main__":
    main()
