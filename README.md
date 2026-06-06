Bot di monitoraggio di siti di e-commerce in tempo reale sviluppato in python.
Il sistema interroga periodicamente le piattaforme per rilevare nuovi annunci pubblicati in base a parole chiave specifiche.
Una volta che viene trovato un nuovo annuncio il sistema invia una notifica ad un bot telegram il quale può essere incorporato in un canale dedicato oppure in un gruppo.
L'architettura è stata proggettata seguendo un approccio modulare: la ricerca su un sito, la gestione delle notifiche e la logica principale sono componenti indipendenti l'una dall'altra.
Questa struttura permette l'integrazione futura di nuovi e-commerce da visionare senza dover modificare i componenti precedenti e a zero il rischio di introdurre nuovi bug nel sistema

Real-time e-commerce monitoring bot developed in Python.

The system periodically queries the platforms to detect new listings published based on specific keywords. Once a new listing is found, the system sends a notification to a Telegram bot, which can be integrated into either a dedicated channel or a group.

The architecture was designed following a modular approach: the platform search/scraping, the notification management, and the main core logic are entirely independent components. This structure allows for the future integration of new e-commerce websites to be monitored without modifying pre-existing components, reducing the risk of introducing new bugs into the system to zero.
