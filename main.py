import telebot
import database

bot = telebot.TeleBot("6183756309:AAG9o2rDAEzaEsuRayK5lPcGOFiIrv7zRZE")


@bot.message_handler(commands=["start"])
def start_handelr(message):
    bot.send_message(chat_id=message.chat.id, text="Бот запущен")


@bot.message_handler(commands=["register"])
def register_handler(message):
    database.register(message)
    bot.reply_to(message, "Вы зарегистрированы")


@bot.message_handler(commands=['deletetask'])
def deletetask_handler(message):
    bot.reply_to(message, database.deletetask(message))


@bot.message_handler(commands=["add_task"])
def add_task_handler(message):
    bot.reply_to(message, database.add_task(message))


@bot.message_handler(commands=["list_task"])
def get_tasks_hendler(message):
    bot.reply_to(message, database.list_task(message))


bot.set_my_commands([
    telebot.types.BotCommand("/start", "Перезапустить бота"),
    telebot.types.BotCommand("/list_task", "Список задач"),
    telebot.types.BotCommand("/register", "Рега"),
    telebot.types.BotCommand("/deletetask", "Удалить таск"),
    telebot.types.BotCommand("/add_task", "Добавить таск"),
])

 
bot.polling()
