import requests
from urllib.parse import quote

def genera_url(ricerca):
    """Prende la parola chiave e crea il link per l'API usando il sort corretto."""
    testo_formattato = quote(ricerca)
    # CORREZIONE: 'sort_by' è la chiave corretta per l'API, non 'order'
    return f"https://www.vinted.it/api/v2/catalog/items?search_text={testo_formattato}&sort_by=newest_first"


def controlla_annunci(ricerca):
    """Si connette a Vinted, scarica i dati e gestisce eventuali blocchi del server."""
    url_api = genera_url(ricerca)
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    
    try:
        session = requests.Session()
        session.get("https://www.vinted.it", headers=headers)
        risposta_raw = session.get(url_api, headers=headers)
        
        if risposta_raw.status_code != 200:
            print(f"⚠️ Vinted ha rifiutato la richiesta. Codice di stato HTTP: {risposta_raw.status_code}")
            return []
            
        risposta = risposta_raw.json()
        annunci_puliti = []
        
        # CORREZIONE: Mettiamo un limite di 10 elementi per analizzare solo la cima del feed cronologico
        for item in risposta.get("items", [])[:10]:
            
            # --- ESTRAZIONE SICURA DEL PREZZO ---
            campo_prezzo = item.get("price")
            if isinstance(campo_prezzo, dict):
                valore = campo_prezzo.get("amount", "0.00")
                valuta = campo_prezzo.get("currency_code", "EUR")
                prezzo_finale = f"{valore} {valuta}"
            else:
                prezzo_finale = str(campo_prezzo) if campo_prezzo else str(item.get("total_item_price", "N/D"))
            
            url_originale = item.get("url", "")
            link_completo = url_originale if url_originale.startswith("http") else f"https://www.vinted.it{url_originale}"

            dati_annuncio = {
                "id": str(item["id"]),
                "titolo": item["title"],
                "prezzo": prezzo_finale,
                "link": link_completo
            }
            annunci_puliti.append(dati_annuncio)  
        return annunci_puliti
        
    except Exception as e:
        print(f"❌ Errore imprevisto durante lo scraping di Vinted: {e}")
        return []

# (Il blocco di test sotto rimane invariato...)