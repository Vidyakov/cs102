import datetime
import requests
import config
import telebot
from bs4 import BeautifulSoup
# import html5lib

bot = telebot.TeleBot(config.access_token)
web_pages = {}

def get_page(group, week=''):
    if week:
        week = str(week) + '/'
    url = '{domain}/{group}/{week}raspisanie_zanyatiy_{group}.htm'.format(
        domain=config.domain,
        week=week,
        group=group)
    response = requests.get(url)
    web_page = response.text
    return web_page


def parse_schedule(web_page, day):
    day = f"{day}day"
    soup = BeautifulSoup(web_page, "html5lib")

    # Получаем таблицу с расписанием
    schedule_table = soup.find("table", attrs={"id": day})

    # Время проведения занятий
    times_list = schedule_table.find_all("td", attrs={"class": "time"})
    times_list = [time.span.text for time in times_list]

    # Место проведения занятий
    locations_list = schedule_table.find_all("td", attrs={"class": "room"})
    locations_list = [room.span.text for room in locations_list]

    # Аудитория
    rooms_list = schedule_table.find_all("td", attrs={"class": "room"})
    rooms_list = [room.dd.text for room in rooms_list]

    # Название дисциплин и имена преподавателей
    lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
    lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
    lessons_list = [', '.join([info for info in lesson_info if info]) for lesson_info in lessons_list]

    return times_list, locations_list, lessons_list, rooms_list


@bot.message_handler(commands=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'])
def get_schedule(message):
    """ Получить расписание на указанный день """
    weekday, week_number, group = message.text.split()
    now = datetime.datetime.now()
    weekday = weekday[1:]
    if weekday == 'monday':
        day = 1
    elif weekday == 'tuesday':
        day = 2
    elif weekday == 'wednesday':
        day = 3
    elif weekday == 'thursday':
        day = 4
    elif weekday == 'friday':
        day = 5
    elif weekday == 'saturday':
        day = 6
    else:
        day = 1

    web_page = web_pages.get(f"{group}{now.date()}")
    if web_page == None:
        web_page = get_page(group, week_number)
        web_pages[f"{group}{now.date()}"] = web_page


    times_lst, locations_lst, lessons_lst, rooms_lst = \
        parse_schedule(web_page, day)
    resp = ''
    for time, location, lession, rooms in zip(times_lst, locations_lst, lessons_lst, rooms_lst):
        resp += '<b>{}</b>, {}, {} {}\n'.format(time, location, lession, rooms)
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['near'])
def get_near_lesson(message):
    """ Получить ближайшее занятие """
    _, group = message.text.split()
    today = datetime.datetime.now()
    day = today.isoweekday()

    now = datetime.datetime.now()
    if (now.isocalendar()[1] - 35) % 2 == 0:
        week_number = str(1)
    else:
        week_number = str(2)

    web_page = web_pages.get(f"{group}{now.date()}")
    if web_page == None:
        web_page = get_page(group, week_number)
        web_pages[f"{group}{now.date()}"] = web_page

    try:
        times_lst, locations_lst, lessons_lst, rooms_lst = \
            parse_schedule(web_page, day)
        resp = ''
        for time, location, lession, rooms in zip(times_lst, locations_lst, lessons_lst, rooms_lst):
            hour, minute = time[:5].split(":")
            lesson_time = datetime.time(int(hour), int(minute))
            if lesson_time >= today.time():
                resp += '<b>{}</b>, {}, {} {}\n'.format(time, location, lession, rooms)
                break
        bot.send_message(message.chat.id, resp, parse_mode='HTML')
    except: # AttributeError:   # Крашится, если не ловить все ошибки
        bot.send_message(message.chat.id, 'На сегодня больше занятий нет')


@bot.message_handler(commands=['tommorow'])
def get_tommorow(message):
    """ Получить расписание на следующий день """
    _, group = message.text.split()
    today = datetime.datetime.now()  # объект даты
    day = today.isoweekday() + 1  # завтрашней день
    if day == 7 or day == 8:
        day = 1

    now = datetime.datetime.now()
    if (now.isocalendar()[1] - 35) % 2 == 0:
        week_number = str(1)
    else:
        week_number = str(2)


    web_page = web_pages.get(f"{group}{now.date()}")
    if web_page == None:
        web_page = get_page(group, week_number)
        web_pages[f"{group}{now.date()}"] = web_page

    times_lst, locations_lst, lessons_lst, rooms_lst = \
        parse_schedule(web_page, day)
    resp = ''
    for time, location, lession, rooms in zip(times_lst, locations_lst, lessons_lst, rooms_lst):
        resp += '<b>{}</b>, {}, {} {}\n'.format(time, location, lession, rooms)
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['all'])
def get_all_schedule(message):
    """ Получить расписание на всю неделю для указанной группы """
    _,  week_number, group = message.text.split()

    now = datetime.datetime.now()
    web_page = web_pages.get(f"{group}{now.date()}")
    if web_page == None:
        web_page = get_page(group, week_number)
        web_pages[f"{group}{now.date()}"] = web_page

    for day in range(1, 7):
        try:      # Если на день нет занятий
            times_lst, locations_lst, lessons_lst, rooms_lst = \
                parse_schedule(web_page, day)
            resp = ''
            for time, location, lession, rooms in zip(times_lst, locations_lst, lessons_lst, rooms_lst):
                resp += '<b>{}</b>, {}, {} {}\n'.format(time, location, lession, rooms)
            bot.send_message(message.chat.id, resp, parse_mode='HTML')
        except AttributeError:
            continue


while True:
    if __name__ == '__main__':
        bot.polling(none_stop=True)
