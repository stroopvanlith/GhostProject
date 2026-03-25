import os
import sys
import telebot

def main():
    # Read token from environment variable with error handling
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not token:
        print("Error: TELEGRAM_BOT_TOKEN environment variable not found!")
        print("Please set the token using: set TELEGRAM_BOT_TOKEN=your_token_here")
        sys.exit(1)
    
    # Initialize the bot
    bot = telebot.TeleBot(token)
    
    # Handler for /start command
    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        bot.reply_to(message, "مرحباً بك أيها القائد، محطة الأشباح متصلة وتنتظر أوامرك")
    
    # Print console message
    print("Bot is listening...")
    
    # Start polling
    bot.infinity_polling()

if __name__ == '__main__':
    main()
