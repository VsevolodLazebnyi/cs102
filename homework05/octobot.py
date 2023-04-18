import datetime
import json
import re
from datetime import datetime, timedelta

import gspread
import pandas as pd
import requests
import telebot
from dateutil import parser

TOKEN = "6020229577:AAGGymHj5mrbslGk_VpSCgyK8hLM0dQCUBI"
bot = telebot.TeleBot(TOKEN)
is_connected = False


def is_valid_date(date: str = "01/01/00", divider: str = "/") -> bool:
    """Проверяем, что дата дедлайна валидна:
    - дата не может быть до текущей
    - не может быть позже, чем через год
    - не может быть такой, которой нет в календаре
    - может быть сегодняшним числом
    - пользователь не должен быть обязан вводить конкретный формат даты
    (например, только через точку или только через слеш)"""
    try:
        if "." in date and divider != ".":
            return False
        if "/" in date and divider != "/":
            return False
        if date == datetime.today().date().strftime("%d/%m/%y"):  # not Error!
            deadline = datetime.today()  # not Error!
        else:
            deadline = datetime.strptime(date, f"%d{divider}%m{divider}%y")  # not Error!
        current_date = datetime.today()  # not Error!
        future_date = current_date + timedelta(days=365)
        return current_date <= deadline <= future_date
    except (ValueError, OverflowError):
        return False



def is_valid_url(url: str = "") -> bool:
    """Проверяем, что ссылка рабочая"""
    try:
        if "en." in url and not url.startswith("https://"):
            return False
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
        response = requests.get(url)
        if response.status_code == 200:
            return True
        else:
            return False
    except (TypeError, requests.exceptions.RequestException):
        return False


def convert_date(date: str = "01/01/00"):
    """Конвертируем дату из строки в datetime"""
    try:
        dt = parser.parse(date)
        return dt.strftime("%d/%m/%y")
    except ValueError:
        print("Ошибка: Некорректный формат даты.")
        return None


def connect_table(message):
    """Подключаемся к Google-таблице"""
    url = message.text
    sheet_id = re.findall(r"/d/([a-zA-Z0-9-_]+)", url)
    if sheet_id:
        sheet_id = sheet_id[0]
        global is_connected
        is_connected = True
    else:
        bot.send_message(message.chat.id, "Ошибка! Неверный формат ссылки на Google-таблицу.")
    try:
        with open("tables.json") as json_file:
            tables = json.load(json_file)
        title = len(tables) + 1
        tables[title] = {"url": url, "id": sheet_id}
    except FileNotFoundError:
        tables = {0: {"url": url, "id": sheet_id}}
    with open("tables.json", "w") as json_file:
        json.dump(tables, json_file)
    bot.send_message(message.chat.id, "Таблица подключена!")
    worksheet, columns, _ = access_current_sheet()
    worksheet.update("A1", "Subject")
    worksheet.update("B1", "Link")
    worksheet.update("C1", "1")
    worksheet.update("D1", "2")
    worksheet.update("E1", "3")
    worksheet.update("F1", "4")
    worksheet.update("G1", "5")
    bot.clear_step_handler_by_chat_id(message.chat.id)
    start(message)


def access_current_sheet():
    """Обращаемся к Google-таблице"""
    with open("tables.json") as json_file:
        tables = json.load(json_file)

    sheet_id = tables[max(tables)]["id"]
    gc = gspread.service_account(filename="credentials.json")
    sh = gc.open_by_key(sheet_id)
    worksheet = sh.sheet1
    headers = worksheet.row_values(1)
    if len(headers) != len(set(headers)):
        for i, header in enumerate(headers):
            if headers.count(header) > 1:
                headers[i] = f"{header}_{i}"
        worksheet.update("1:1", [headers])
    df = pd.DataFrame(worksheet.get_all_records())
    return worksheet, tables[max(tables)]["url"], df


def choose_action(message):
    """Обрабатываем действия верхнего уровня"""
    if message.text == "Подключить Google-таблицу":
        bot.send_message(message.chat.id, "Пожалуйста, введите ссылку на Google-таблицу:")
        bot.register_next_step_handler(message, connect_table)
    elif message.text == "Редактировать предметы":
        start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        start_markup.row("Добавить новый предмет")
        start_markup.row("Редактирование")
        start_markup.row("Удалить имеющийся")
        start_markup.row("Удалить все")
        info = bot.send_message(message.chat.id, "Выберите действие:", reply_markup=start_markup)
        bot.register_next_step_handler(info, choose_subject_action)
    elif message.text == "Редактировать дедлайн":
        start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        start_markup.row("Добавить новый дедлайн")
        start_markup.row("Изменить дату дедлайна")
        info = bot.send_message(message.chat.id, "Выберите действие:", reply_markup=start_markup)
        bot.register_next_step_handler(info, choose_deadline_action)
    elif message.text == "Посмотреть дедлайны на этой неделе":
        worksheet, url, df = access_current_sheet()
        today = datetime.date.today()
        week_from_now = today + datetime.timedelta(days=7)
        filtered_df = df[(df["Дата"].dt.date > today) & (df["Дата"].dt.date <= week_from_now)]
        if not filtered_df.empty:
            bot.send_message(
                message.chat.id,
                f"Дедлайны за следующие 7 дней:\n{filtered_df['Дата'].dt.strftime('%d.%m.%Y').str.cat(filtered_df['1'], sep=' - ')}",
            )
            bot.send_message(
                message.chat.id,
                f"Дедлайны за следующие 7 дней:\n{filtered_df['Дата'].dt.strftime('%d.%m.%Y').str.cat(filtered_df['2'], sep=' - ')}",
            )
            bot.send_message(
                message.chat.id,
                f"Дедлайны за следующие 7 дней:\n{filtered_df['Дата'].dt.strftime('%d.%m.%Y').str.cat(filtered_df['3'], sep=' - ')}",
            )
            bot.send_message(
                message.chat.id,
                f"Дедлайны за следующие 7 дней:\n{filtered_df['Дата'].dt.strftime('%d.%m.%Y').str.cat(filtered_df['4'], sep=' - ')}",
            )
            bot.send_message(
                message.chat.id,
                f"Дедлайны за следующие 7 дней:\n{filtered_df['Дата'].dt.strftime('%d.%m.%Y').str.cat(filtered_df['5'], sep=' - ')}",
            )
        else:
            bot.send_message(message.chat.id, "Нет дедлайнов за следующие 7 дней")


def choose_subject_action(message):
    """Выбираем действие в разделе Редактировать предметы"""
    if message.text == "Добавить новый предмет":
        bot.send_message(message.chat.id, "Какой предмет вы хотите добавить?:")
        bot.register_next_step_handler(message, add_new_subject)
    elif message.text == "Редактирование":
        bot.send_message(message.chat.id, "Какой предмет вы хотите отредактировать?:")
        bot.register_next_step_handler(message, update_subject)
    elif message.text == "Удалить имеющийся":
        bot.send_message(message.chat.id, "Какой предмет вы хотите удалить?:")
        bot.register_next_step_handler(message, delete_subject)
    elif message.text == "Удалить все":
        start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        start_markup.row("Принять")
        start_markup.row("Отмена")
        info = bot.send_message(
            message.chat.id, "После удаления данные будут недоступны для восстановления:", reply_markup=start_markup
        )
        bot.register_next_step_handler(info, choose_removal_option)


def choose_deadline_action(message):
    """Выбираем действие в разделе Редактировать дедлайн"""
    if message.text == "Добавить новый дедлайн":
        bot.send_message(message.chat.id, "Какому предмету вы хотите добавить дедлайн?:")
        bot.register_next_step_handler(message, choose_subject)
    elif message.text == "Изменить дату дедлайна":
        bot.send_message(message.chat.id, "Какому предмету вы хотите отредактировать дедлайн?:")
        bot.register_next_step_handler(message, choose_subject)


def choose_removal_option(message):
    """Уточняем, точно ли надо удалить все"""
    start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    start_markup.row("Да")
    start_markup.row("Нет")
    info = bot.send_message(message.chat.id, "Вы уверены, что хотите удалить все данные?:", reply_markup=start_markup)
    bot.register_next_step_handler(info, clear_subject_list)


def choose_subject(message):
    """Выбираем предмет, у которого надо отредактировать дедлайн"""
    subject = message.text
    bot.send_message(message.chat.id, "Введите номер работы:")
    bot.register_next_step_handler(message, update_subject_deadline, subject)


def update_subject_deadline(message, subject):
    work_number = message.text
    info = bot.send_message(message.chat.id, "Введите новую дату дедлайна (лучше в формате дд/мм/гг):")
    bot.register_next_step_handler(info, update_subject_deadline_date, subject, work_number)


def update_subject_deadline_date(message, subject, work_number):
    worksheet, _, _ = access_current_sheet()
    x = worksheet.find(subject)
    y = worksheet.find(work_number)
    worksheet.update_cell(x.row, y.col, convert_date(message.text))
    bot.send_message(message.chat.id, "Дедлайн успешно обновлен!")
    bot.clear_step_handler_by_chat_id(message.chat.id)
    start(message)


def add_new_subject(message):
    """Вносим новое название предмета в Google-таблицу"""
    """ Вносим новое название предмета в Google-таблицу """
    title = message.text
    worksheet, _, _ = access_current_sheet()
    url = ""
    start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    start_markup.row("Да")
    start_markup.row("Нет")
    info = bot.send_message(
        message.chat.id, f"Хотите добавить ссылку для предмета '{title}'?", reply_markup=start_markup
    )
    bot.register_next_step_handler(info, add_new_subject_url, title, url)


def add_new_subject_url(message, title, url):
    """Вносим новую ссылку на таблицу предмета в Google-таблицу"""
    response = message.text.lower()
    if response == "да":
        bot.send_message(message.chat.id, "Введите ссылку на таблицу предмета:")
        bot.register_next_step_handler(message, save_subject_url, title)
    elif response == "нет":
        worksheet, _, _ = access_current_sheet()
        worksheet.append_row([title, url])
        bot.send_message(message.chat.id, f"Предмет '{title}' успешно добавлен!")
        bot.clear_step_handler_by_chat_id(message.chat.id)
        start(message)
    else:
        bot.send_message(message.chat.id, "Некорректный ответ. Введите 'Да' или 'Нет'.")
        bot.register_next_step_handler(message, add_new_subject_url, title, url)


def save_subject_url(message, title):
    """Сохраняем ссылку на предмет в Google-таблицу"""
    url = message.text
    worksheet, _, _ = access_current_sheet()
    worksheet.append_row([title, url])
    bot.send_message(message.chat.id, f"Предмет '{title}' успешно добавлен с ссылкой '{url}'!")
    bot.clear_step_handler_by_chat_id(message.chat.id)
    start(message)


def update_subject(message):
    """Обновляем информацию о предмете в Google-таблице"""
    worksheet, url, df = access_current_sheet()
    M = message.text
    subjects = df["Subject"].tolist()
    if not subjects:
        bot.send_message(message.chat.id, "Список предметов пуст.")
        return
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    for subject in subjects:
        keyboard.add(telebot.types.KeyboardButton(subject))
    if M not in subjects:
        bot.send_message(message.chat.id, "Выберите предмет для редактирования:", reply_markup=keyboard)
        bot.register_next_step_handler(message, update_subject_name)
    else:
        bot.clear_step_handler_by_chat_id(message.chat.id)
        update_subject_name(message)


def update_subject_name(message):
    """Обновляем название предмета"""
    selected_subject = message.text
    bot.send_message(message.chat.id, f"Введите новое название для предмета '{selected_subject}':")
    bot.register_next_step_handler(message, update_subject_url, selected_subject)


def update_subject_url(message, selected_subject):
    """Обновляем ссылку предмета"""
    new_subject_name = message.text

    # Запрашиваем новую ссылку предмета
    bot.send_message(message.chat.id, f"Введите новую ссылку для предмета '{new_subject_name}':")
    bot.register_next_step_handler(message, update_subject_in_sheet, selected_subject, new_subject_name)


def update_subject_in_sheet(message, selected_subject, new_subject_name):
    """Обновляем информацию о предмете в Google-таблице"""
    worksheet, url, df = access_current_sheet()
    row_index = df.index[df["Subject"] == selected_subject].tolist()[0]
    worksheet.update_cell(row_index + 2, 1, new_subject_name)  # Обновляем название предмета
    worksheet.update_cell(row_index + 2, 2, message.text)  # Обновляем ссылку предмета
    bot.send_message(message.chat.id, f"Предмет '{selected_subject}' успешно обновлен.")
    bot.clear_step_handler_by_chat_id(message.chat.id)
    start(message)


def delete_subject(message):
    """Удаляем предмет в Google-таблице"""
    worksheet, url, df = access_current_sheet()
    title = message.text
    subjects = df["Subject"].tolist()
    if not subjects:
        bot.send_message(message.chat.id, "Список предметов пуст.")
        return
    if title not in subjects:
        bot.send_message(message.chat.id, "Нет предмета с таким названием.")
        bot.send_message(message.chat.id, "Какой предмет вы хотите удалить?:")
        bot.register_next_step_handler(message, delete_subject)
    row_index = subjects.index(title) + 2
    worksheet.delete_row(row_index)

    bot.send_message(message.chat.id, f"Предмет '{title}' успешно удален!")
    bot.clear_step_handler_by_chat_id(message.chat.id)
    start(message)


def clear_subject_list(message):
    """Удаляем все из Google-таблицы"""
    """Удаляем все предметы, URL и дедлайны в Google-таблице"""
    worksheet, url, df = access_current_sheet()
    num_rows, num_cols = worksheet.row_count, worksheet.col_count
    for row in range(1, num_rows):
        for col in range(8):
            worksheet.update_cell(row + 1, col + 1, "")

    bot.send_message(message.chat.id, "Все предметы, URL и дедлайны очищены!")
    bot.clear_step_handler_by_chat_id(message.chat.id)
    start(message)


@bot.message_handler(commands=["start"])
def start(message):
    if is_connected is True:
        start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        start_markup.row("Посмотреть дедлайны на этой неделе")
        start_markup.row("Редактировать дедлайн")
        start_markup.row("Редактировать предметы")
    else:
        start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        start_markup.row("Подключить Google-таблицу")
    info = bot.send_message(message.chat.id, "Что хотите сделать?", reply_markup=start_markup)
    bot.register_next_step_handler(info, choose_action)


bot.infinity_polling()
