import os
import sys
import subprocess
import telebot

def main():
    # Read token from environment variable with error handling
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not token:
        print("Error: TELEGRAM_BOT_TOKEN environment variable not found!")
        print("Please set the token using: set TELEGRAM_BOT_TOKEN=your_token_here")
        sys.exit(1)
    
    # Security: Authorized chat ID (set to None to accept anyone temporarily)
    AUTHORIZED_CHAT_ID = None  # Replace with your chat ID later for security
    
    # Initialize the bot
    bot = telebot.TeleBot(token)
    
    # Handler for /start command
    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        # Check authorization
        if AUTHORIZED_CHAT_ID and message.chat.id != AUTHORIZED_CHAT_ID:
            bot.reply_to(message, "غير مصرح لك بالوصول")
            return
        
        bot.reply_to(message, "مرحباً بك أيها القائد، محطة الأشباح متصلة وتنتظر أوامرك")
    
    # Handler for all text messages (command execution)
    @bot.message_handler(func=lambda message: True, content_types=['text'])
    def execute_command(message):
        # Check authorization
        if AUTHORIZED_CHAT_ID and message.chat.id != AUTHORIZED_CHAT_ID:
            bot.reply_to(message, "غير مصرح لك بالوصول")
            return
        
        command = message.text
        print(f"Executing command: {command}")
        
        try:
            # Execute command in Windows command prompt
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30,
                encoding='utf-8',
                errors='replace'
            )
            
            # Prepare response
            output = result.stdout.strip() if result.stdout else ""
            error = result.stderr.strip() if result.stderr else ""
            
            if output:
                response = f"✅ Output:\n{output}"
            elif error:
                response = f"❌ Error:\n{error}"
            else:
                response = "✅ Command executed successfully (no output)"
            
            # Telegram has a message length limit, so split if needed
            if len(response) > 4096:
                for i in range(0, len(response), 4096):
                    bot.reply_to(message, response[i:i+4096])
            else:
                bot.reply_to(message, response)
                
        except subprocess.TimeoutExpired:
            bot.reply_to(message, "❌ Command timeout (exceeded 30 seconds)")
        except Exception as e:
            error_msg = f"❌ Error executing command:\n{str(e)}"
            print(f"Error: {error_msg}")
            bot.reply_to(message, error_msg)
    
    # Print console message
    print("Bot is listening...")
    
    # Start polling
    bot.infinity_polling()

if __name__ == '__main__':
    main()
