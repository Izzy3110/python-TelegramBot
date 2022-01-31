import urllib
import telebot
import os
import requests
import threading

latest_users = []
current_bot = telebot.TeleBot(os.environ["BOT_TOKEN"],
                              parse_mode=None)  # You can set parse_mode by default. HTML or MARKDOWN


@current_bot.message_handler(func=lambda m: True)
def echo_all(message):
    if not message.from_user.is_bot:
        user_id = message.from_user.id
        if user_id not in latest_users:
            latest_users.append(user_id)
            for latest_user_id in latest_users:
                print("new id: " + str(latest_user_id))
                BotThread.send_announcments(latest_user_id, "new user: " + message.from_user.first_name)
    current_bot.reply_to(message, message.text)


@current_bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    current_bot.reply_to(message, "Howdy, how are you doing?")


class BotThread(threading.Thread):
    current_bot = None
    started = False
    running = True

    TELEGRAM_API_BASEURL = "https://api.telegram.org"

    def __init__(self, bot_instance):
        self.current_bot = bot_instance
        super(BotThread, self).__init__()

    @staticmethod
    def send_announcments(target_id, bot_message):
        send_text = BotThread.TELEGRAM_API_BASEURL + \
                    '/bot' + os.environ["BOT_TOKEN"] + \
                    '/sendMessage?' + \
                    'chat_id=' + str(target_id) + \
                    '&text=' + urllib.parse.quote(bot_message)
        
        if requests.get(send_text).status_code == 200:
            return True

    def run(self) -> None:
        while self.running:
            if not self.started:
                print("starting")
                self.start_bot()
                self.started = True

    def start_bot(self):
        print("starting bot")
        self.current_bot.infinity_polling()


if __name__ == '__main__':
    Bot_ = BotThread(current_bot)
    Bot_.start()
