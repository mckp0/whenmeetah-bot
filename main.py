import config
import telebot
import requests
from telebot.types import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup
import json
from datetime import datetime, timedelta

bot = telebot.TeleBot(config.API_KEY)

names = {}

date_dict = {
    'Mon' : 0,
    'Tue' : 1,
    'Wed' : 2,
    'Thu' : 3,
    'Fri' : 4,
    'Sat' : 5,
    'Sun' : 6,
}

def get_key(val):
    for key, value in date_dict.items():
        if val == value:
            return key
    return "There is no such Key"

#commands
bot.set_my_commands([
    BotCommand('start', 'Start the bot'),
    BotCommand('decidedate',"Find the best date"),
    BotCommand('whereyall', 'Input your destination'),
    BotCommand('eta', 'Find out your ETA to the destination'),
    BotCommand('answered', 'Find out who has responded'),
    BotCommand('done', 'Generate the most ideal date')
])

def request_start(chat_id):
    """
    Helper function to request user to execute command /start
    """
    if chat_id not in names:
        bot.send_message(chat_id=chat_id, text='Please start the bot by sending /start')


@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    if message.chat.type == 'private':
        chat_user = message.chat.first_name
    else:
        chat_user = message.from_user.first_name

    names[chat_id] = dict()
    names[chat_id]['dest_postal'] = ""
    names[chat_id]['origin_postal'] = ""
    names[chat_id]['transport'] = ""
    names[chat_id]['availability'] = {}
    names[chat_id]['answered'] = []
    print("dest_postal = str created")
    message_text = f'Welcome!\n/decidedate to find a common time. \nOn the day itself, use /whereyall to locate your friends.'
    bot.send_message(chat_id, message_text)  

@bot.message_handler(commands=['decidedate'])
def decidedate(message):
    chat_id = message.chat.id
    if message.chat.type == 'private':
        chat_user = message.chat.first_name
    else:
        chat_user = message.from_user.first_name
    message_text = f'Hi {chat_user}, please reply to this message with the event title.'
    sent = bot.send_message(chat_id, message_text)
    bot.register_next_step_handler(sent, eventTitle)

def eventTitle(message):
    title = message.text
    buttons = []
    timerange = ['This Weekend', 'This Week']
    for select_method in timerange:
        row = []
        button = InlineKeyboardButton(
        text=select_method,
        callback_data = f'{select_method} {title}' 
        )
        row.append(button)
        buttons.append(row)
    bot.send_message(
        chat_id=message.chat.id,
        text=f'Select time range to meet up for {title}.',
        reply_markup=InlineKeyboardMarkup(buttons)
    )
  


# CALENDAR
# @bot.message_handler(commands=['decidewhen'])
# def decidewhen(m):
#     calendar, step = DetailedTelegramCalendar().build()
#     bot.send_message(m.chat.id,
#                      f"Select {LSTEP[step]}",
#                      reply_markup=calendar)

    
# @bot.callback_query_handler(func=DetailedTelegramCalendar.func())
# def cal(c):
#     result, key, step = DetailedTelegramCalendar().process(c.data)
#     if not result and key:
#         bot.edit_message_text(f"Select {LSTEP[step]}",
#                               c.message.chat.id,
#                               c.message.message_id,
#                               reply_markup=key)
#     elif result:
#         bot.edit_message_text(f"You selected {result}.\n\n"
#         "Do you wish to select another date?",
#                               c.message.chat.id,
#                               c.message.message_id)

@bot.message_handler(commands=['whereyall'])
def whereyall(message):
    chat_id = message.chat.id
    names[chat_id]['dest_postal'] = ''
    if chat_id not in names:
        request_start(chat_id)
        return

    chat_text = 'Where are you all headed? Please input a valid postal code. \nYou can use Google Maps (https://www.google.com/maps/) for help.'
    buttons = []
    count = 0
    for i in range(3):
        row = []
        for i in range(3):
            count += 1
            quantity = str(count)
            button = InlineKeyboardButton(
            text=quantity,
            callback_data= f'destpostal {quantity}')
        
            row.append(button)
        buttons.append(row)
      
    buttons.append([InlineKeyboardButton(text = "", callback_data = "None"),
    InlineKeyboardButton(text = "0", callback_data = f'destpostal 0'),
    InlineKeyboardButton(text = "", callback_data = "None")])

    bot.send_message(
        chat_id=chat_id,
        text=chat_text,
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@bot.message_handler(commands=['eta'])
def eta(message):
    chat_id = message.chat.id
    names[chat_id]['origin_postal'] = ''

    if chat_id not in names:
        request_start(chat_id)
        return

    elif not names[chat_id]['dest_postal']:
        bot.send_message(chat_id = chat_id, text = "Please use the /whereyall command to input your destination first. Thank you.")

    else:
        chat_text = 'Please select your mode of transport towards the destination.'
        modes = ["Public Transport","Driving or Taxi", "Cycling","Walking"]

        buttons = []
        for i in modes:
            row = [InlineKeyboardButton(
                text = i,
                callback_data = f'transport {i}')]
            buttons.append(row)

        bot.send_message(
        chat_id=chat_id,
        text=chat_text,
        reply_markup=InlineKeyboardMarkup(buttons)
        )

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    """
    Handles the execution of the respective functions upon receipt of the callback query
    """
    
    call_id = call.id
    message_id = call.message.id
    chat_id = call.message.chat.id
    data = call.data
    user = call.from_user.first_name 
    purpose, data = data.split()[0], data.split()[1:]

    if purpose == 'destpostal':
        names[chat_id]['dest_postal'] += data[0]
        print(names[chat_id]['dest_postal'])
        bot.answer_callback_query(call.id,text=str(names[chat_id]['dest_postal']))

        if len(names[chat_id]['dest_postal']) == 6:
            bot.send_message(
                chat_id,
                text = f"Thank you. Your destination's postal code is {names[chat_id]['dest_postal']}. Everyone may now use /eta to estimate your remaining travelling time.",
            )
        
    elif purpose == 'originpostal':
        names[chat_id]['origin_postal'] += data[0]
        print(names[chat_id]['origin_postal'])
        bot.answer_callback_query(call.id,text=str(names[chat_id]['origin_postal']))

        if len(names[chat_id]['origin_postal']) == 6:
            bot.send_message(
                chat_id,
                text = f"Thank you. The nearest postal code to you is {names[chat_id]['origin_postal']}."
            )
            calculate_eta(chat_id,user)
    
    elif purpose == 'This':
        if data[0] == 'Weekend':
            print('run weekend function')
            weekendGenerator(data, chat_id)
            bot.answer_callback_query(call.id,text='')
        
        elif data[0] == "Week":
            print('run week function')
            weekGenerator(data,chat_id)
            bot.answer_callback_query(call.id,text='')

        else:
            print("gg")

  # elif purpose == 'select_specific_dates':
  #   print('run calendar select')

    elif purpose == 'availability':
        dateStr = f'{data[0]} {data[1]} {data[2]}'
        if user not in names[chat_id]['availability'][dateStr]:
            names[chat_id]['availability'][dateStr].append(user)
            #RESPONSE
            bot.answer_callback_query(call.id,text=f'{user} free on {dateStr}.')

            avail_text = avail_message()

            bot.send_message(
                chat_id = chat_id,
                text = f""
            )

        else:
            names[chat_id]['availability'][dateStr].remove(user)
            #RESPONSE
            bot.answer_callback_query(call.id,text=f'{user} not free on {dateStr}.')

            avail_text = avail_message(chat_id)

            bot.send_message(
                chat_id = chat_id,
                text = avail_text
            )

        if user not in names[chat_id]['answered']:
            names[chat_id]['answered'].append(user)


        #UPDATE MESSAGE
        #TO BE DONE IN THE FUTURE
        #REWORK
        
        print(names[chat_id]['availability'])
    

    elif purpose == 'transport':
        print('storing transport mode')
        mode = ""
        for i in data:
            mode += i
        names[chat_id]['transport'] = mode
        print(f"transport mode selected: {names[chat_id]['transport']}")
        bot.edit_message_text(f"Transport mode selected: {names[chat_id]['transport']}",chat_id,message_id)
        bot.answer_callback_query(call.id,text='')
        get_eta(chat_id, mode)


def get_eta(chat_id,transport):
    buttons = []
    count = 0
    for i in range(3):
        row = []
        for i in range(3):
            count += 1
            quantity = str(count)
            button = InlineKeyboardButton(
            text=quantity,
            callback_data= f'originpostal {quantity}')
      
            row.append(button)
        buttons.append(row)
      
    buttons.append([InlineKeyboardButton(text = "", callback_data = "None"),
    InlineKeyboardButton(text = "0", callback_data = f'originpostal 0'),
    InlineKeyboardButton(text = "", callback_data = "None")])

    chat_text = f"What is your nearest postal code? \nYou can use Google Maps (https://www.google.com/maps/) for help."

    bot.send_message(
        chat_id = chat_id,
        text = chat_text,
        reply_markup = InlineKeyboardMarkup(buttons)
    )

def avail_message(chat_id):
    message = "Selected Dates: \n"
    avail_dict = names[chat_id]['availability']

    for i in avail_dict:
        if len(avail_dict[i]) > 0:
            names_message = " ".join(avail_dict[i])
            message.append(f"{i}: {names_message} \n")

    return message

def calculate_eta(chat_id,user):
    source = names[chat_id]["origin_postal"]
    dest = names[chat_id]["dest_postal"]
    mode = names[chat_id]["transport"]
    mode_dict = {
        "Walking" : "walking",
        "DrivingorTaxi" : "driving",
        "Cycling": "bicycling",
        "PublicTransport" :"transit" 
    }
    print(mode_dict[mode])

    maps_API_KEY = os.getenv('maps_API_KEY')
    url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={source}&destinations={dest}&mode={mode_dict[mode]}&key={maps_API_KEY}"

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)
    print(f"response type is {type(response)}")
    eta_data = json.loads(response.text)
    origin_address = eta_data["origin_addresses"][0]
    dest_address = eta_data["destination_addresses"][0]

    if origin_address != "" and dest_address != "":
        
        if origin_address.split()[0] != dest_address.split()[0]:
            bot.send_message(
                chat_id = chat_id,
                text = f"You have entered a wrong postal code, please use the /whereyall and /eta commands again."
            )
        else:
            eta_time = eta_data["rows"][0]["elements"][0]["duration"]["text"]
            print(eta_time, type(eta_time))
            bot.send_message(
                chat_id = chat_id,
                text = f"{user}'s ETA to the destination is {eta_time}!"
            )
    else:
        bot.send_message(
        chat_id = chat_id,
        text = f"You have entered a wrong postal code, please use the /whereyall and /eta commands again."
        )


def weekendGenerator(title, chat_id):
    sgDate = getTodayDate()
    weeklist = []
    for i in range(7):
        weeklist.append(sgDate)
        sgDate += timedelta(days=1)
  
    buttons = []
    for days in weeklist:
        dateStr,day,day_value = getDayValue(days)
        names[chat_id]['availability'][dateStr] = []
        row = []
    
        if day_value > 4:
            button = InlineKeyboardButton(
                text = f"{dateStr}, {day}",
                callback_data = f"availability {dateStr}"
            )
            row.append(button)
        buttons.append(row)

    title_str = ' '.join(title)
    bot.send_message(
        chat_id,
        text=f'Select the dates when you are free for {title_str}!',
        reply_markup=InlineKeyboardMarkup(buttons)
    )

  
def weekGenerator(title,chat_id):
    sgDate = getTodayDate() #datetime object
    weeklist = []
    for i in range(7):
        weeklist.append(sgDate)
        sgDate += timedelta(days=1)

    buttons = []
    for days in weeklist:
        dateStr,day,day_value = getDayValue(days)
        names[chat_id]['availability'][dateStr] = []
        row = []
        button = InlineKeyboardButton(
            text = f"{dateStr}, {day}",
            callback_data = f"availability {dateStr}"
        )
        row.append(button)
        buttons.append(row)
  
  
    title_str = ' '.join(title)
  
    bot.send_message(
        chat_id,
        text=f'Select the dates when you are free for {title_str}!',
        reply_markup=InlineKeyboardMarkup(buttons)
    )
  
def getTodayDate():
    import pytz
    now_utc = datetime.utcnow()
    tz = pytz.timezone('Asia/Singapore')
    sg_time = now_utc.replace(tzinfo=pytz.utc).astimezone(tz) 
    return sg_time
  
def getDayValue(datevalue):
    dateStr = datevalue.strftime('%d %b %y')
    day_value = datevalue.weekday()
    day = get_key(day_value)
    return dateStr, day, day_value

@bot.message_handler(commands=['answered'])
def answered(message):
    chat_id = message.chat.id
    if chat_id not in names:
        request_start(chat_id)
        return
  
    message_text = f'List of people who have responded:\n\n'
  
    for name in names[chat_id]['answered']:
        message_text += f'{name}\n'

    bot.send_message(chat_id, message_text)


@bot.message_handler(commands=['done','d'])
def done(message):
    chat_id = message.chat.id
    if chat_id not in names:
        request_start(chat_id)
        return
  
    bestdates, n = bestDate(chat_id)

    if n < 2:
        message_text = 'No Dates Available :('

    else:
        if len(bestdates) == 1:
            message_text = f'Poll Closed! The best date is'
        else:
            message_text = f'Poll Closed! The best dates are'

        if n < len(names[chat_id]['answered']):
            for dates in bestdates:
                message_text += f'\n{dates} but'
                not_avail = [x for x in names[chat_id]['answered'] if x not in names[chat_id]['availability'][dates]]
                for y in not_avail:
                    message_text += f'\n- {y} cannot make it'
        else:
            for dates in bestdates:
                message_text += f'\n{dates}'
    bot.send_message(chat_id, message_text)

def bestDate(chat_id):
    n = max([len(i) for i in names[chat_id]['availability'].values()])
    print(n)
    best_dates = []
    for i in names[chat_id]['availability']:
        if len(names[chat_id]['availability'][i]) == n:
            best_dates.append(i)
    return best_dates, n

#do not delete please
print('bot is running')
#keeps the bot running
bot.infinity_polling()