import os
import openai
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, executor

load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Initialize the Telegram bot
bot = Bot(token = os.getenv('TELEGRAM_TOKEN'))
dp = Dispatcher(bot)

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.WARN)
logger = logging.getLogger(__name__)

# Dictionary to store conversation history for each user
history = {}

# Handler for the /chatgpt command
@dp.message_handler(commands=["chatgpt"])
async def start(message: types.Message):
    await message.reply("Hello! I'm a chatbot based on GPT-3.5-turbo. Please type your message to start chatting.")

# Default message handler
@dp.message_handler()
async def message_handler(message: types.Message):
    user_id = message.from_user.id
    user_input = message.text

    # Initialize the conversation history for the user if not present
    if user_id not in history:
        history[user_id] = []

    messages = []

    # Construct the conversation history for the OpenAI API
    for input_text, completion_text in history[user_id]:
        messages.append({"role": "user", "content": input_text})
        messages.append({"role": "assistant", "content": completion_text})

    messages.append({"role": "user", "content": user_input})

    # Call the OpenAI API for generating a response
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    # Get the generated completion text
    completion_text = completion.choices[0].message.content

    # Send the generated response back to the user
    await message.reply(completion_text)

    # Update the conversation history
    history[user_id].append((user_input, completion_text))
    
# Entry point of the bot
def main():
    # Start the bot's event loop
    executor.start_polling(dp, skip_updates=True)

if __name__ == "__main__":
    main()
