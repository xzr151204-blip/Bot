import asyncio
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
from telethon import TelegramClient, events

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot ishlamoqda!")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    server.serve_forever()

threading.Thread(target=run_server, daemon=True).start()

API_ID = 34305022
API_HASH = '327e8ec05ad457e65ec5dfb73bccc9d3'
MY_CARD_DETAILS = "9860 0101 0221 5687"

CHANNELS_MAP = {
    -1004360113383: 'Pariii_776',
    -1002895859500: 'trade_matrixx',
    -1004335738485: 'trade_matrixx'
}

client = TelegramClient('speed_session', API_ID, API_HASH)

ADMIN_ENTITIES = {}
waiting_for_word = {}

@client.on(events.NewMessage(chats=list(CHANNELS_MAP.keys())))
async def fast_handler(event):
    chat_id = event.chat_id
    text = event.raw_text.strip()

    if "karta" in text.lower():
        asyncio.create_task(
            client.send_message(
                entity=chat_id,
                message=MY_CARD_DETAILS,
                comment_to=event.id
            )
        )
        return

    if text == "1":
        waiting_for_word[chat_id] = True
        return

    if waiting_for_word.get(chat_id, False):
        word_to_send = text
        waiting_for_word[chat_id] = False
        admin_target = ADMIN_ENTITIES.get(chat_id)
        
        if admin_target:
            asyncio.create_task(client.send_message(admin_target, word_to_send))

async def main():
    await client.start()
    for cid, admin_user in CHANNELS_MAP.items():
        try:
            entity = await client.get_input_entity(admin_user)
            ADMIN_ENTITIES[cid] = entity
        except Exception:
            pass
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
