import os
from dotenv import load_dotenv, find_dotenv
import telebot
from telebot import types
from database import DB

load_dotenv(find_dotenv())  # Загрузка переменных окружения

db = DB(os.environ.get('DATABASE_URL'))  # Экземпляр

global a_and_q, num_of_question, status, score

num_of_question = 0
score = [-2,-2,-2]
status = -1111
a_and_q = [
	[
		'Вопрос 1',
		'Ответ 1',
		'Ответ 2',
		'Ответ 3(Верный)',
		'Ответ 4',
		3
	],
	[
		'Вопрос 2',
		'Ответ 1',
		'Ответ 2',
		'Ответ 3',
		'Ответ 4(Верный)',
		4
	],
	[
		'Вопрос 3',
		'Ответ 1(верный)',
		'Ответ 2',
		'Ответ 3',
		'Ответ 4',
		1
	],
	[
		'Вопрос 4',
		'Ответ 1',
		'Ответ 2(Верный)',
		'Ответ 3',
		'Ответ 4',
		2
	],
	[
		'Вопрос 5',
		'Ответ 1',
		'Ответ 2',
		'Ответ 3',
		'Ответ 4(Верный)',
		4
	],
	[
		'Вопрос 6',
		'Ответ 1(верный)',
		'Ответ 2',
		'Ответ 3',
		'Ответ 4',
		1
	],
	[
		'Вопрос 7',
		'Ответ 1',
		'Ответ 2',
		'Ответ 3',
		'Ответ 4(Верный)',
		4
	],
	[
		'Вопрос 8',
		'Ответ 1',
		'Ответ 2(верный)',
		'Ответ 3',
		'Ответ 4',
		2
	],
	[
		'Вопрос 9',
		'Ответ 1',
		'Ответ 2',
		'Ответ 3(верный)',
		'Ответ 4',
		3
	],
	[
		'Вопрос 10',
		'Ответ 1(верный)',
		'Ответ 2',
		'Ответ 3',
		'Ответ 4',
		1
	]

]


token = os.environ.get('API_TOKEN')
bot = telebot.TeleBot(token)

start_message = '<бот-нэйм> создан для проверки уровня знаний о кибербезопасности и обучения сотрудников навыкам обхода угроз при использовании Интернета.\nХотите узнать больше о кибербезопасности или записаться на тренинг?\n'

@bot.message_handler(commands = ['start'])
def get_text_message(message):
	global status
	if status == 3:
		bot.send_message(message.from_user.id, 'Нельзя вернуться в меню во время теста')
	else:
		mainmenu = types.InlineKeyboardMarkup()
		key1 = types.InlineKeyboardButton(text = 'Записаться на тренинг', callback_data = 'key1')
		key2 = types.InlineKeyboardButton(text = 'Узнать о кибербезопасности', callback_data = 'key2')
		mainmenu.add(key1, key2)
		bot.send_message(message.from_user.id, start_message , reply_markup = mainmenu)

@bot.callback_query_handler(func = lambda call: True)
def callback_inline(call):
	global status, num_of_question, score
	if call.data == 'mainmenu':
		status = 0
		num_of_question = 0
		mainmenu  =  types.InlineKeyboardMarkup()
		bttns = [
			types.InlineKeyboardButton(text = 'Записаться на тренинг', callback_data = 'key1'),
			types.InlineKeyboardButton(text = 'Узнать о кибербезопасности', callback_data = 'key2')
		]
		mainmenu.add(*bttns)
		bot.edit_message_text(start_message, call.message.chat.id, call.message.message_id,
							  reply_markup = mainmenu)
	elif call.data == 'key1':
		next_menu = types.InlineKeyboardMarkup()
		bttns = [
			types.InlineKeyboardButton(text = 'Поведение в социальных сетях', callback_data = 'choice0'),
			types.InlineKeyboardButton(text = 'Безопасность банковских счетов', callback_data = 'choice1'),
			types.InlineKeyboardButton(text = 'Назад', callback_data = 'mainmenu')
		]
		for i in bttns:
			next_menu.add(i)

		bot.edit_message_text('Выберите курс:', call.message.chat.id, call.message.message_id,
							  reply_markup = next_menu)

	elif call.data == 'choice0':
		status = 2
		choice = 0
		next_menu3 = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(text = 'Вернуться в начало', callback_data = 'mainmenu'))
		bot.edit_message_text('Чтобы записаться на тренинг пришлите свою почту', call.message.chat.id, call.message.message_id,
							  reply_markup = next_menu3)

	elif call.data == 'choice1':
		status = 2
		choice = 1
		next_menu3 = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(text = 'Вернуться в начало', callback_data = 'mainmenu'))
		bot.edit_message_text('Чтобы записаться на тренинг пришлите свою почту', call.message.chat.id, call.message.message_id,
							  reply_markup = next_menu3)

	elif call.data == 'key2':
		next_menu2 = types.InlineKeyboardMarkup()
		bttns = [
			types.InlineKeyboardButton(text = 'Готов!', callback_data = 'key3'),
			types.InlineKeyboardButton(text = 'Назад', callback_data = 'mainmenu')
		]
		for i in bttns:
			next_menu2.add(i)
		bot.edit_message_text('Хотите узнать больше о кибербезопасности?\nДля начала выясним текущий уровень ваших знаний об опасностях в интернете. Готовы?', call.message.chat.id, call.message.message_id,
							  reply_markup = next_menu2)

	elif call.data == 'key3':
		bot.edit_message_reply_markup(call.message.chat.id, message_id = call.message.message_id, reply_markup = '')
		status = 3
		questions = types.ReplyKeyboardMarkup(True, one_time_keyboard = True)
		for i in a_and_q[num_of_question][1:-1]:
			questions.row(i)
		bot.send_message(call.message.chat.id, a_and_q[num_of_question][0], reply_markup = questions)

	elif call.data == 'key4':
		bot.edit_message_reply_markup(call.message.chat.id, message_id = call.message.message_id, reply_markup = '')
		num_of_question = 0
		themes = ''
		print(score)
		if score == [1,1,1]:
			status = 4 #Тут подправить статус на статус пройденного теста
			next_menu4 = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(text = 'Вернуться в начало', callback_data = 'mainmenu'))
			bot.send_message(call.message.chat.id, f'Тест завершен, вы набрали максимум баллов!\nУ вас хороший уровень знаний\nДля завершения подготовки остается пройти финальный тест!', reply_markup = next_menu4)
		else:
			next_menu5 = types.InlineKeyboardMarkup()
			if score[0] != 1:
				next_menu5.add(types.InlineKeyboardButton(text = 'Тема 1', callback_data = 'theme1'))
			elif score[1] != 1:
				next_menu5.add(types.InlineKeyboardButton(text = 'Тема 2', callback_data = 'theme2'))
			elif score[2] != 1:
				next_menu5.add(types.InlineKeyboardButton(text = 'Тема 3', callback_data = 'theme3'))
			summ = score[0] + score[1] + score [2] + 6
			bot.send_message(call.message.chat.id, f'Вы набрали {summ} баллов, тест показал что некоторые темы вам незнакомы. Вам стоит узнать больше о правилах поведения в интернете.', reply_markup = next_menu5)

		score = 0

	else:
		pass

@bot.message_handler(content_types = ['text'])
def get_text_message(message):
	global status, num_of_question, score
	if (status == 3) and (message.text in a_and_q[num_of_question][1:-1]): #прописать условие состояния
		if num_of_question != 9:
			stage1 = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(text = 'Следующий вопрос!', callback_data = 'key3'))
			if message.text == a_and_q[num_of_question][a_and_q[num_of_question][5]]:
				if num_of_question in [1,2,3]:
					score[0] += 1
				elif num_of_question in [4,6]:
					score[1] += 1
				elif num_of_question in [7,8,9]:
					score[2] += 1
				bot.send_message(message.from_user.id, 'Ответ правильный!', reply_markup = stage1)
			else:
				bot.send_message(message.from_user.id, 'Ответ неверный :с', reply_markup = stage1) #Написать почему!
		else:
			stage1 = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(text = 'Завершить тест', callback_data = 'key4'))
			if message.text == a_and_q[num_of_question][a_and_q[num_of_question][5]]:
				score[2] += 1
				bot.send_message(message.from_user.id, 'Ответ правильный!', reply_markup = stage1)
			else:
				bot.send_message(message.from_user.id, 'Ответ неверный :с', reply_markup = stage1) #Написать почему!
		num_of_question += 1

	elif status == 2:
		try:   
			if message.text.split('@')[1] == 'dvfu.ru': #Прописать поиск по базе
				bot.send_message(message.from_user.id, 'Хорошо, мы вас записали')
			else:
				bot.send_message(message.from_user.id, 'Неверная почта')
		except:
			bot.send_message(message.from_user.id, 'Неверная почта')

	else:
		bot.send_message(message.from_user.id, 'Я вас не понимаю... :с')

bot.polling(none_stop = True, interval = 0)
#.