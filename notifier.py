import json
import requests

class TelegramNotifier:
    def __init__(self, config_path = "config.json"):
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)

        self.token = config["telegram_token"]
        self.chat_id = config["telegram_chatID"]
        self.api_url = f"https://api.telegram.org/bot{self.token}"
    
    def invia_messaggio(self, testo):
        """Invia un messaggio di testo formattato in Markdown a Telegram."""
        url = f"{self.api_url}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": testo,
            "parse_mode": "Markdown"
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                return True
            else:
                print(f"❌ Errore Telegram ({response.status_code}): {response.text}")
                return False
        except Exception as e:
            print(f"❌ Errore di connessione: {e}")
            return False

# Questo file ora è a posto e non deve fare altro.