import os
from dotenv import load_dotenv, find_dotenv
import telebot
from telebot import types
from database import DB
from mailsandler import MailSandler

load_dotenv(find_dotenv())  # Загрузка переменных окружения

db = DB(os.environ.get('DATABASE_URL'))  # Экземпляр
sandler = MailSandler(os.environ.get('MAIL_LOGIN'), os.environ.get('MAIL_PASS'))

global a_and_q, num_of_question, status, score, choice

num_of_question = 0
score = [-2, -2, -3]
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


@bot.message_handler(commands=['start'])
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


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	global status, num_of_question, score, code, choice
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
			types.InlineKeyboardButton(text = 'Поведение в социальных сетях и мессенджерах', callback_data = 'choice0'),
			types.InlineKeyboardButton(text = 'Пароли и учётные записи', callback_data = 'choice1'),
			types.InlineKeyboardButton(text = 'Электронная почта', callback_data = 'choice2'),
			types.InlineKeyboardButton(text = 'Назад', callback_data = 'mainmenu')
		]
		for i in bttns:
			next_menu.add(i)

		bot.edit_message_text('Выберите курс:', call.message.chat.id, call.message.message_id,
							  reply_markup = next_menu)

	elif call.data == 'choice0':
		status = 2
		choice = 'social_networking'
		next_menu3 = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(text = 'Вернуться в начало', callback_data = 'mainmenu'))
		bot.edit_message_text('Чтобы записаться на тренинг пришлите свою почту', call.message.chat.id, call.message.message_id,
							  reply_markup = next_menu3)

	elif call.data == 'choice1':
		status = 2
		choice = 'passwords'
		next_menu3 = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(text = 'Вернуться в начало', callback_data = 'mainmenu'))
		bot.edit_message_text('Чтобы записаться на тренинг пришлите свою почту', call.message.chat.id, call.message.message_id,
							  reply_markup = next_menu3)

	elif call.data == 'choice2':
		status = 2
		choice = 'email'
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
		if score == [3,3,4]:
			status = 4 #Тут подправить статус на статус пройденного теста
			next_menu4 = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(text = 'Вернуться в начало', callback_data = 'mainmenu'))
			bot.send_message(call.message.chat.id, f'Тест завершен, вы набрали максимум баллов!\nУ вас хороший уровень знаний\nДля завершения подготовки остается пройти финальный тест!', reply_markup = next_menu4)
		else:
			next_menu5 = types.InlineKeyboardMarkup()
			if score[0] != 1:
				next_menu5.add(types.InlineKeyboardButton(text = 'Электронная почта', callback_data = 'theme1'))
			if score[1] != 1:
				next_menu5.add(types.InlineKeyboardButton(text = 'Пароли и учетный записи', callback_data = 'theme2'))
			if score[2] != 1:
				next_menu5.add(types.InlineKeyboardButton(text = 'Соц сети и мессенджеры', callback_data = 'theme3'))
			summ = score[0] + score[1] + score [2] + 7
			bot.send_message(call.message.chat.id, f'Вы набрали {summ} баллов, тест показал что некоторые темы вам незнакомы. Вам стоит узнать больше о правилах поведения в интернете.', reply_markup = next_menu5)

		score = 0

	elif call.data == 'accept':
		bot.edit_message_reply_markup(call.message.chat.id, message_id = call.message.message_id, reply_markup = '')
		status = 10
	elif call.data == 'resend':
		status = 11
		global users_mail
		code = sandler.sendMail(message.text)
		accept = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(text = 'Ввести код', callback_data = 'accept'))
		bot.send_message(message.from_user.id, 'Мы отправили повторно на вашу почту код подтверждения, когда вы его получите, нажмите кнопку "Ввести код" и введите код', reply_markup = accept)
	elif call.data == 'change_mail':
		status = 2

	else:
		pass

  
@bot.message_handler(content_types=['text'])
def get_text_message(message):

	global status, num_of_question, score
	if (status == 3) and (message.text in a_and_q[num_of_question][1:-1]):
		if num_of_question != 9:
			stage1 = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(text = 'Следующий вопрос!', callback_data = 'key3'))
			if message.text == a_and_q[num_of_question][a_and_q[num_of_question][5]]:
				if num_of_question in [0,1,2]:
					score[0] += 1
				elif num_of_question in [3,4,5]:
					score[1] += 1
				elif num_of_question in [6,7,8,9]:
					score[2] += 1
				bot.send_message(message.from_user.id, 'Ответ правильный!', reply_markup = stage1)
			else:
				bot.send_message(message.from_user.id, 'Ответ неверный :с', reply_markup = stage1) #Написать почему!
			print(score)
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
			if message.text.split('@')[1] == 'yandex.ru': #Прописать поиск по базе
				bot.edit_message_reply_markup(message.chat.id, message_id = message.message_id - 1, reply_markup = '')
				global code, users_mail
				users_mail = message.text
				code = sandler.sendMail(users_mail)
				accept = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(text = 'Ввести код', callback_data = 'accept'))
				bot.send_message(message.from_user.id, 'Мы отправили на вашу почту код подтверждения, когда вы его получите, нажмите кнопку "Ввести код" и введите код', reply_markup = accept)
			else:
				bot.send_message(message.from_user.id, 'Неверная почта')
		except Exception as e:
			status = 0
			print(e)
	elif status == 10:
		if code == message.text:
			bot.send_message(message.from_user.id, 'Хорошо, мы вас записали')
			db.registerUser(users_mail, message.from_user.id, choice)
			status = 2
		else:
			resend = types.ReplyKeyboardMarkup(one_time_keyboard = True, resize_keyboard = True,).row('Отправить заново').row('Исправить почту').row('Повторить ввод кода')
			bot.send_message(message.from_user.id, 'Неверный код', reply_markup = resend)
			status = 11
	elif status == 11 and message.text == 'Исправить почту':
		change_mail = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(text = 'Изменить почту', callback_data = 'change_mail'))
		bot.send_message(message.from_user.id, 'Нажмите кнопку "Изменить почту" и отправьте новую.', reply_markup = change_mail)
	elif status == 11 and message.text == 'Отправить заново':
		code = sandler.sendMail(users_mail)
		accept = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(text = 'Ввести код', callback_data = 'accept'))
		bot.send_message(message.from_user.id, 'Мы отправили повторно на вашу почту код подтверждения, когда вы его получите, нажмите кнопку "Ввести код" и введите код', reply_markup = accept)
	elif status == 11 and message.text == 'Повторить ввод кода':
		accept = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(text = 'Ввести код', callback_data = 'accept'))
		bot.send_message(message.from_user.id, 'Хорошо, попробуйте еще раз.', reply_markup = accept)
	else:
		bot.send_message(message.from_user.id, 'Я вас не понимаю... :с')

bot.polling(none_stop = True, interval = 0)
#.