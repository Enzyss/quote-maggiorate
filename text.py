from telethon.sync import TelegramClient
from telethon.tl.types import InputMessagesFilterPhotos
#import pytesseract
#from PIL import Image
#from io import BytesIO
import re

api_id = '3778637'
api_hash = '27b204b5e5a74a77ec977f9cc951ae0b'
phone_number = '+393342033166'

# Imposta il percorso per il file dove verranno memorizzate le immagini scaricate
download_path = '/'

pattern_maggiorata = r'Maggiorata Q (\d+\.\d+)'
pattern_campionato = r'⚽️ (.+)$'
pattern_partita = r'🔄 (.+)$'
pattern_data_ora = r'🕖 (.+)$'
pattern_bookmaker = r'🌐 (BULLIBET|ADMIRALBET)'
pattern_mercato = r'(BANCA|PUNTA) (.+)'



def estrai_informazioni(messaggio):
    maggiorata = re.search(pattern_maggiorata, messaggio, re.MULTILINE).group(1)
    campionato = re.search(pattern_campionato, messaggio, re.MULTILINE).group(1)
    partita = re.search(pattern_partita, messaggio, re.MULTILINE).group(1)
    data_ora = re.search(pattern_data_ora, messaggio, re.MULTILINE).group(1)
    bookmaker = re.search(pattern_bookmaker, messaggio, re.MULTILINE).group(1)
    mercato_match = re.search(pattern_mercato, messaggio, re.MULTILINE)
    mercato = mercato_match.group(1)
    quota = mercato_match.group(2)
    
    return {
        "maggiorata": maggiorata,
        "campionato": campionato,
        "partita": partita,
        "data_ora": data_ora,
        "bookmaker": bookmaker,
        "mercato": mercato,
        "quota": quota
    }

# Funzione per scaricare le immagini dal canale Telegram
def download_images_from_channel(channel_username):
    with TelegramClient('session_name', api_id, api_hash) as client:
        # Effettua l'accesso
        client.start(phone_number)
        
        # Trova l'ID del canale
        #channel = client.get_entity(channel_username)
    
        # Filtra solo le foto
        filter_photos = InputMessagesFilterPhotos()

        dialogs = client.get_dialogs()
        
        # Stampare l'ID di ogni chat
        for dialog in dialogs:
            chat = dialog.entity
            if hasattr(chat, 'title'):
                #print(chat.id, ' ' , chat.title)
                if chat.id == 1926114410:
                    messages = client.get_messages(chat.id, limit=10)
                    for message in messages:
                        print("Messaggio:", message.text)
            # Scarica le immagini dal canale
                #for message in client.iter_messages(chat):
                    # Controllo se il messaggio ha un'immagine
                    #test = estrai_informazioni(message)
                    #print(test)
                    # if message.photo:
                    #     print('riga 26')
                    #     # Ottieni la dimensione dell'immagine più grande
                    #     photo = message.photo
                    #     print(photo)
                     
                    #     # Scarica l'immagine
                    #     image_path = client.download_media(message.media)
                    #     #print(f"Downloaded: {image_path}")
                    #     image = Image.open(image_path)

                    #     # Utilizza pytesseract per leggere il testo
                    #     text = pytesseract.image_to_string(image)

                    #     # Stampa il testo
                    #     print(text)

# Chiama la funzione con il nome utente del canale da cui desideri scaricare le immagini
download_images_from_channel(2118058600)



def print_chat_ids():
    with TelegramClient('session_name', api_id, api_hash) as client:
        # Effettua l'accesso
        client.start(phone_number)
        
        # Ottieni tutte le chat
        dialogs = client.get_dialogs()
        
        # Stampare l'ID di ogni chat
        for dialog in dialogs:
            chat = dialog.entity
            print(f"Chat ID: {chat.id}, Title: {chat.title}")




