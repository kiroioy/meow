import config
import telebot
from telebot import types
import pygsheets
import sys
reload(sys)

bot = telebot.TeleBot(config.token)

try:
    gc=pygsheets.authorize(service_file=config.CREDENTIALS_FILE)
    sh = gc.open_by_key(config.SPREADSHEET_ID)
    worksheet = sh.worksheet_by_title(config.SHEET_NAME)
    print('успешно подключились к гугл таблице, урааа')
except Exception as e:
    print(f"ошибка подключения к гугл таблице: {e}")
    worksheet = None

def get_ideas_from_sheet():
    try:
        if not worksheet:
            return []
        ideas = worksheet.get_col(1, include_tailing_empty=False)
        print(f"получены идеи из таблицы: {ideas}")
        return ideas
    except Exception as e:
        print(f"ошибка получения данных: {e}")
        return []

def add_idea_to_sheet(idea_text):
    try:
        if not worksheet:
            return False

        worksheet.append_table([idea_text], dimension='ROWS', overwrite=False)
        print("идея успешно добавлена!! спасибо:)")
        return True

    except Exception as e:
        print(f"капец!! ошибка добавления идеи: {e}")
        return False

def delete_idea_from_sheet(index):
    try:
        if not worksheet:
            return False

        worksheet.delete_rows(index+1)
        print("идея успешно удалена!")
        return True

    except Exception as e:
        print(f"ошибка удаления идеи: {e}")
        return False

@bot.message_handler(commands=['start'])
def welcome_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    item1=types.KeyboardButton("добавить новую идею")
    item2 = types.KeyboardButton("удалить идею")
    item3 = types.KeyboardButton("просмотреть все идеи")
    item4 = types.KeyboardButton("о боте")

    markup.add(item1, item2, item3, item4)

    bot.send_message(message.chat.id,
                     "здравствуйте! перед вами бот для ведения таблицы гугл с идеями для свиданий\n\n"
                     "с помощью бота ты можешь добавить новую идею или удалить уже существующую, а также просмотреть полный список сохраненных идей\n\n"
                     "для этого нужно выбрать необходимое действие в меню ниже\n"
                     "приятного пользования!!",
                     reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "добавить новую идею")
def add_idea(message):
    msg = bot.send_message(message.chat.id, "введите текст новой идеи")
    bot.register_next_step_handler(msg, idea_process)

def idea_process(message):
    try:
        idea_text = message.text
        if add_idea_to_sheet(idea_text):
            bot.send_message(message.chat.id, "ураа!! идея добавлена!! спасибо:)")
        else:
            bot.send_message(message.chat.id, 'не удалось добавить идею:(\n'
                                              'пожалуйста, попробуй еще раз')
    except Exception as e:
        bot.send_message(message.chat.id, "ошибка, но ты можешь опробовать еще раз!!")


@bot.message_handler(func=lambda message: message.text == "удалить идею")
def delete_idea_start(message):
    try:
        ideas = get_ideas_from_sheet()

        if not ideas:
            bot.send_message(message.chat.id, "пока нет идей для удаления:(")
            return

        ideas_list = 'список идей:\n\n'
        for i, idea in enumerate(ideas, 1):
            ideas_list += f'{i}.  {idea}\n\n'

        ideas_list += "введи номер идеи, которую хочешь удалить!!"

        bot.send_message(message.chat.id, ideas_list)
        bot.register_next_step_handler(message, idea_delete, ideas)

    except Exception as e:
        bot.send_message(message.chat.id, "ошибка при получении списка идей:((")

def idea_delete(message, ideas):
    try:
        try:
            index = int(message.text) - 1
            if 0 <= index < len(ideas):
                idea_to_delete = ideas[index]

                if delete_idea_from_sheet(index):
                    bot.send_message(message.chat.id, f'идея {idea_to_delete} удалена!!')
                else:
                    bot.send_message(message.chat.id, 'к сожалению, не удалось удалить идею')
            else:
                bot.send_message(message.chat.id, 'неверный номер, такой идеи нет:(')

        except ValueError:
            bot.send_message(message.chat.id, "введи число!")

    except Exception as e:
        print(f"ошибка: {e}")
        bot.send_message(message.chat.id, "ошибка при удалении идеи")

@bot.message_handler(func=lambda message: message.text == "просмотреть все идеи")
def show_all_ideas(message):
     try:
         ideas = get_ideas_from_sheet()
         if not ideas:
             bot.send_message(message.chat.id, 'идей пока нет:(')
             return
         ideas_text = ('список всех сохраненных идей:\n\n')
         for i, idea in enumerate(ideas, 1):
             ideas_text += f'{i}.  {idea}\n\n'

         bot.send_message(message.chat.id, ideas_text)

     except Exception as e:
         print(f"произошла ошибка при показе идей: {e}")
         bot.send_message(message.chat.id, "не удалось загрузить идеи, попробуй позже!!")

@bot.message_handler(func=lambda message: message.text == "о боте")
def about_us(message):
    text_about_us = ("информация о боте:\n\n"
                     "данный бот создан для удобного ведения списка идей для свиданий и автоматического сохранения их в google-таблицу\n\n"
                     "бот позволяет добавлять, просматривать и удалять записи\n"
                     "приятного использования!")
    bot.send_message(message.chat.id, text_about_us)
    try:
        with open('guineapig.jpg', 'rb') as photo:
            bot.send_photo(message.chat.id, photo, caption='морская свинка')
    except FileNotFoundError:
        bot.send_message(message.chat.id, "морская свинка куда-то убежала...(файл не найден)")
    except Exception as e:
        print(f"ошибка при отправке фото: {e}")

if __name__ == '__main__':
    print("бот запущен...")
    bot.infinity_polling(none_stop=True)