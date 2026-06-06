import json
import time

# Importiamo il segnalatore di Telegram e lo scraper di Vinted
from notifier import TelegramNotifier
from siti.vinted import controlla_annunci as cerca_su_vinted

def avvia_bot():
    print("🚀 Avvio del Deal Monitor Bot in corso...")
    
    # Inizializziamo il sistema di notifiche Telegram
    notifier = TelegramNotifier()
    
    # Questa sarà la nostra memoria fotografica per gli ID visti
    annunci_visti = set()
    
    # Variabile d'appoggio per capire se è il primissimo giro del bot
    primo_avvio = True
    
    print("✅ Bot inizializzato correttamente. Inizio monitoraggio...\n")

    # Ciclo infinito: il bot girerà finché non lo blocchi tu dal terminale
    while True:
        try:
            # 1. Rileggiamo il config.json a ogni giro
            with open("config.json", "r", encoding="utf-8") as f:
                config = json.load(f)
            
            intervallo = config.get("intervallo_ricerca", 180)
            
            if primo_avvio:
                print("📥 Primo controllo in corso: invio la fotografia degli annunci attuali...")
            
            # 2. Giriamo su ogni ricerca presente nel file JSON
            for item in config["ricerche"]:
                parola_chiave = item["ricerca"]
                piattaforme = item["piattaforme"]
                
                # Se tra le piattaforme c'è Vinted, attiviamo lo scraper
                if "vinted" in piattaforme:
                    print(f"🔍 Controllo Vinted per: '{parola_chiave}'...")
                    annunci_trovati = cerca_su_vinted(parola_chiave)
                    
                    # Analizziamo gli annunci trovati uno per uno
                    for annuncio in annunci_trovati:
                        id_annuncio = annuncio["id"]
                        
                        # Se l'annuncio NON è nella nostra memoria...
                        if id_annuncio not in annunci_visti:
                            # Lo aggiungiamo subito alla memoria per il futuro
                            annunci_visti.add(id_annuncio)
                            
                            # MODIFICA: Gestiamo visivamente se è la fotografia o un annuncio nuovo reale
                            if primo_avvio:
                                print(f"📦 [FOTOGRAFIA] {annuncio['titolo']} - {annuncio['prezzo']}")
                                
                                messaggio = (
                                    f"📦 *Fotografia Iniziale (Già online):*\n\n"
                                    f"*Oggetto:* {annuncio['titolo']}\n"
                                    f"*Prezzo:* {annuncio['prezzo']}\n\n"
                                    f"[Apri l'annuncio qui]({annuncio['link']})"
                                )
                                notifier.invia_messaggio(messaggio)
                                time.sleep(0.5)  # Pausa di mezzo secondo per non intasare i server di Telegram
                            else:
                                print(f"✨ NUOVO ANNUNCIO: {annuncio['titolo']} - {annuncio['prezzo']}")
                                
                                messaggio = (
                                    f"✨ *Nuovo annuncio su Vinted!*\n\n"
                                    f"*Oggetto:* {annuncio['titolo']}\n"
                                    f"*Prezzo:* {annuncio['prezzo']}\n\n"
                                    f"[Apri l'annuncio qui]({annuncio['link']})"
                                )
                                notifier.invia_messaggio(messaggio)
            
            # 3. Finito il controllo di tutte le parole chiave...
            if primo_avvio:
                print("\n✅ Fotografia iniziale inviata con successo! Da adesso monitoro il tempo reale.")
                primo_avvio = False 
            
            print(f"Controllo completato. Prossimo giro tra {intervallo} secondi...\n")
            time.sleep(intervallo)
            
        except KeyboardInterrupt:
            print("\nBot fermato correttamente")
            break
        except Exception as e:
            print(f"Errore nel ciclo principale: {e}")
            print("Riprovo tra 30 secondi...")
            time.sleep(30)

if __name__ == "__main__":
    avvia_bot()