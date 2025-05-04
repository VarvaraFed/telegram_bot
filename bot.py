from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
import asyncio
import openai

# Токен вашего бота
API_TOKEN = '8077391297:AAHTBMILgWL3clASOUdUBAcAcUA-v2DwemU'

# Настройка OpenRouter API
openai.api_key = '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'
openai.api_base = "https://openrouter.ai/api/v1"

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Обработчик команды /start
@dp.message(Command("start"))
async def send_welcome(message: Message):
    await message.answer("Привет! Я ваш бот.")

# Обработчик команды /help
@dp.message(Command("help"))
async def send_help(message: Message):
    await message.answer("Это помощь.")

# Обработчик текстовых сообщений
@dp.message()
async def handle_message_with_context(message: Message):
    chat_id = message.chat.id
    user_text = message.text

    # Хранение истории диалога
    if not hasattr(dp, "chat_history"):
        dp.chat_history = {}

    if chat_id not in dp.chat_history:
        dp.chat_history[chat_id] = []

    dp.chat_history[chat_id].append({"role": "user", "content": user_text})

    try:
        # Отправка запроса в LLM
        client = openai.OpenAI(api_key=openai.api_key, base_url=openai.api_base)
        response = client.chat.completions.create(
            model="google/gemini-pro",
            messages=dp.chat_history[chat_id]
        )

        llm_response = response.choices[0].message.content
        dp.chat_history[chat_id].append({"role": "assistant", "content": llm_response})

        await message.reply(llm_response)
    except Exception as e:
        await message.reply(f"Произошла ошибка: {str(e)}")

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())