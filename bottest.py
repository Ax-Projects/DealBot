import asyncio
import telegram
import keys

# First, send a message in your Telegram bot's chat, so this script can extract your user ID to send you messages with the main.py script
async def main():
    bot = telegram.Bot(keys.token)
    async with bot:
        update = (await bot.get_updates())[0]
        print(update.message.chat.id)

if __name__ == "__main__":
    asyncio.run(main())
