from quart import Quart, render_template, request
from telethon.sync import TelegramClient
import asyncio

API_ID = '3778637'
API_HASH = '27b204b5e5a74a77ec977f9cc951ae0b'
PHONE_NUMBER = '+393342033166'
CODE_HASH = ''

app = Quart(__name__)
telegram_code_sent = False

async def send_telegram_code():
    global telegram_code_sent
    if not telegram_code_sent:
        client = TelegramClient("session", API_ID, API_HASH)
        await client.connect()
        if await client.is_user_authorized():
            print("Sei già autorizzato!")
            #print('await client.get_me(): ' , client.get_me())

            dialogs = await client.get_dialogs()
            
            # Stampare l'ID di ogni chat
            for dialog in dialogs:
                chat = dialog.entity
                if hasattr(chat, 'title'):
                    print(chat.id, ' ' , chat.title)
                    if chat.id == 1926114410:
                        messages = await client.get_messages(chat.id, limit=10)
                        for message in messages:
                            print("Messaggio:", message.text)
                # Scarica le immagini dal canale

        else:
        
            phone_code = await client.send_code_request(PHONE_NUMBER)
            global CODE_HASH
            CODE_HASH = phone_code.phone_code_hash
            print('SMS INVIATO: ' , CODE_HASH)

        telegram_code_sent = True

@app.route('/')
async def index():
    await send_telegram_code()
    return await render_template('index.html')

@app.route('/verify', methods=['POST'])
async def verify():
    phone_code = (await request.form)['phone_code']
    print(phone_code)
    if phone_code:
        # Autenticazione con il codice inserito
        client = TelegramClient("session", API_ID, API_HASH)
        await client.connect()
        print('phone_code_hash: ' , CODE_HASH)
        await client.sign_in(PHONE_NUMBER, code=phone_code,phone_code_hash=CODE_HASH)
                # Ora l'utente è autorizzato, puoi eseguire qui la logica successiva
        print('await client.get_me(): ' , await client.get_me())
    return 'Codice verificato con successo!'

if __name__ == '__main__':
    app.run(host="0.0.0.0",port="5000")
