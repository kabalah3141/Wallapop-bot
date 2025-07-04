import requests
from bs4 import BeautifulSoup
import time
import telegram

# CONFIGURACIÓN
TOKEN = "7812212134:AAHzzoQvoCpDCWTTX7rtDw5WvKOe_LFbJRE"
CHAT_ID = 1824377931
BUSQUEDA = "iphone 13"
PRECIO_MAX = 260

bot = telegram.Bot(token=TOKEN)
productos_vistos = set()

def buscar_wallapop():
    url = f"https://es.wallapop.com/app/search?keywords={BUSQUEDA.replace(' ', '%20')}&latitude=41.3851&longitude=2.1734&distance=30"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        print("Error al obtener datos de Wallapop")
        return []
    soup = BeautifulSoup(resp.text, 'html.parser')
    items = soup.find_all("a", href=True)
    resultados = []

    for item in items:
        link = item['href']
        if "/item/" in link and link not in productos_vistos:
            productos_vistos.add(link)
            resultados.append("https://es.wallapop.com" + link)
    return resultados

def enviar_alerta(mensajes):
    for msg in mensajes:
        bot.send_message(chat_id=CHAT_ID, text=f"Nuevo iPhone 13 encontrado:\n{msg}")

def main():
    while True:
        nuevos = buscar_wallapop()
        if nuevos:
            enviar_alerta(nuevos)
        else:
            print("No hay nuevos productos")
        time.sleep(300)

if __name__ == "__main__":
    main()
