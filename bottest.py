import asyncio
import telegram
import keys


# async def main():
#     bot = telegram.Bot(keys.token)
#     async with bot:
#         print(await bot.get_me())
#         print(await bot.get_chat(chat_id=6174623243))


async def main():
    bot = telegram.Bot(keys.token)
    async with bot:
        update = (await bot.get_updates())[0]
        print(update.message.chat.id)

if __name__ == "__main__":
    asyncio.run(main())
