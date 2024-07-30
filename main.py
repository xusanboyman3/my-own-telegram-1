from telethon import TelegramClient, events
import asyncio
from keep_alive import keep_alive  # Import the keep_alive function

keep_alive()
# Use your own values from my.telegram.org
api_id = 23564987
api_hash = 'a3a5bf88d985dbf6b39ecb8a8283b33b'
phone_number = '+998 95 953 12 08'

client = TelegramClient('session_name', api_id, api_hash)

@client.on(events.NewMessage)
async def handler(event):
    if event.raw_text.lower() == 'hi':
        await event.respond('Assalomu alaykum')
async def main():
    await client.start(phone_number)
    await client.run_until_disconnected()


if __name__ == '__main__':
    print("Client Created")
    keep_alive()
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print('Exit')
