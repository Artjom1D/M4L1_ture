from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from logic import *
import schedule
import threading
import time
from config import *
bot = TeleBot(API_TOKEN)

def gen_markup(id):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Получить!", callback_data=id))
    return markup

def gea_markup(id):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Купить", callback_data="buy"))
    return markup

def geo_markup(id):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Продать", callback_data="sell"))
    return markup


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):

    user_id = call.message.chat.id
    prize_id = call.data
    if call.data == "buy":

        result = manager.buy_img(manager.money)
        if not result:
            bot.send_message(user_id, "Нет доступных картинок для покупки!")
            return
            
        prize_id, img = result
        with open(f'img/{img}', 'rb') as photo:
            bot.send_photo(user_id, photo, caption="Поздравляем с покупкой!")
            manager.prize_amount += 1
        return
    
    elif call.data == "sell":
        result = manager.sell_img()
        if result == None:
            bot.send_message(user_id, "Ошибка при продаже картинки!")
            return
        manager.money += 5     
        bot.send_message(user_id, f"Картинка продана! Получено 5 монет. Баланс: {manager.money}")
        return
    else:
        img = manager.get_prize_img(prize_id)
        manager.prize_amount += 1
        with open(f'img/{img}', 'rb') as photo:
            bot.send_photo(user_id, photo)


def send_message():
    prize_id, img = manager.get_random_prize()[:2]
    manager.mark_prize_used(prize_id)
    hide_img(img)
    for user in manager.get_users():
        with open(f'hidden_img/{img}', 'rb') as photo:
            bot.send_photo(user, photo, reply_markup=gen_markup(id = prize_id))
        

def shedule_thread():
    schedule.every(2).minutes.do(send_message) # Здесь ты можешь задать периодичность отправки картинок
    while True:
        schedule.run_pending()
        time.sleep(1)

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.chat.id
    if user_id in manager.get_users():
        bot.reply_to(message, "Ты уже зарегестрирован!")
    else:
        manager.add_user(user_id, message.from_user.username)
        bot.reply_to(message, """Привет! Добро пожаловать! 
Тебя успешно зарегистрировали!
Каждый час тебе будут приходить новые картинки и у тебя будет шанс их получить!
Для этого нужно быстрее всех нажать на кнопку 'Получить!'

Только три первых пользователя получат картинку!)""")
        
@bot.message_handler(commands=['rating'])
def handle_rating(message):
    res = manager.get_rating() 
    res = [f'| @{x[0]:<11} | {x[1]:<11}|\n{"_"*26}' for x in res]
    res = '\n'.join(res)
    res = f'|USER_NAME    |COUNT_PRIZE|\n{"_"*26}\n' + res
    bot.send_message(message.chat.id, res)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):

    prize_id = call.data
    user_id = call.message.chat.id

    if manager.get_winners_count() < 3:
        res = manager.add_winner()
        if res:
            img = manager.get_random_prize()
            with open(f'img/{img}', 'rb') as photo:
                bot.send_photo(user_id, photo, caption="Поздравляем! Ты получил картинку!")
        else:
            bot.send_message(user_id, 'Ты уже получил картинку!')
    else:
        bot.send_message(user_id, "К сожалению, ты не успел получить картинку! Попробуй в следующий раз!)")
    

@bot.message_handler(commands = ["shop"])
def shop(message):
    bot.send_message(message.chat.id, f"Ваш баланс: {manager.money} монет")
    bot.send_message(message.chat.id, "Магазин: \n 1. Купить случайную картину за 10 монет \n 2. Продать случайную картину за 5 монет")
    if manager.money >= 10:
        bot.send_message(message.chat.id, "Вы можете купить картину", reply_markup=gea_markup(id="buy"))
    else:
        bot.send_message(message.chat.id, "У вас недостаточно монет для покупки картины")

    if manager.prize_amount != 0:
        bot.send_message(message.chat.id, "Вы можете продать картину", reply_markup=geo_markup(id="sell"))
    else:
        bot.send_message(message.chat.id, "У вас нет картин для продажи")
def polling_thread():
    bot.polling(none_stop=True)

if __name__ == '__main__':
    manager = DatabaseManager(DATABASE)
    manager.create_tables()

    polling_thread = threading.Thread(target=polling_thread)
    polling_shedule  = threading.Thread(target=shedule_thread)

    polling_thread.start()
    polling_shedule.start()
  
