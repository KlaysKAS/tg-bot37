# -*- coding: utf8 -*-
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
score = [-2, -3, -2]
status = -1111

def toStruct(filename):
	f = open(filename, 'r', encoding='utf-8')

	nodes = f.read().split('%\n')
	struct = []
	i = 0
	for node in nodes:
		struct.append(node.split('\n'))
	f.close()
	for i in range(len(struct)):
		struct[i] = struct[i][:-1]
	return struct
a_and_q = toStruct('Вопросы.txt')
# print(a_and_q)

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

	global status, num_of_question, score, code, choice, is_end_test

	if call.data == 'mainmenu':
		num_of_question = 0
		mainmenu  =  types.InlineKeyboardMarkup()
		bttns = [types.InlineKeyboardButton(text = 'Записаться на тренинг', callback_data = 'key1')]
		if is_end_test == 1 : 
			bttns.append(types.InlineKeyboardButton(text = 'Пройти финальный тест', callback_data = 'final_test'))
		else:
			bttns.append(types.InlineKeyboardButton(text = 'Узнать о кибербезопасности', callback_data = 'key2'))
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

	elif call.data == 'end_the_test':
		global themes
		bot.edit_message_reply_markup(call.message.chat.id, message_id = call.message.message_id, reply_markup = '')
		num_of_question = 0
		themes = [0, 0, 0]
		is_end_test = 1
		print(score)
		if score == [1,1,1]:
			next_menu4 = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(text = 'Вернуться в начало', callback_data = 'mainmenu'))
			bot.send_message(call.message.chat.id, f'Тест завершен, вы набрали максимум баллов!\nУ вас хороший уровень знаний\nДля завершения подготовки остается пройти финальный тест! Вернитесь в начало и нажмите "Пройти финальный тест"', reply_markup = next_menu4)
		else:
			next_menu5 = types.InlineKeyboardMarkup()
			if score[0] != 1:
				themes[0] = 1
				next_menu5.add(types.InlineKeyboardButton(text = 'Электронная почта', callback_data = 'theme_mails'))
			if score[1] != 1:
				themes[1] = 1
				next_menu5.add(types.InlineKeyboardButton(text = 'Пароли и учетный записи', callback_data = 'theme_passwords'))
			if score[2] != 1:
				themes[2] = 1
				next_menu5.add(types.InlineKeyboardButton(text = 'Соц сети и мессенджеры', callback_data = 'theme_social'))
			summ = score[0] + score[1] + score [2] + 7
			bot.send_message(call.message.chat.id, f'Вы набрали {summ} баллов, тест показал что некоторые темы вам незнакомы. Вам стоит узнать больше о правилах поведения в интернете.', reply_markup = next_menu5)

	#Подробности о темах
	elif call.data == 'theme_mails':
		next_menu6 = types.InlineKeyboardMarkup()
		themes [0] = 0
		bot.edit_message_reply_markup(call.message.chat.id, message_id = call.message.message_id, reply_markup = '')
		if themes[1] == 1:
			next_menu6.add(types.InlineKeyboardButton(text = 'Пароли и учетный записи', callback_data = 'theme_passwords'))
		if themes[2] == 1:
			next_menu6.add(types.InlineKeyboardButton(text = 'Соц сети и мессенджеры', callback_data = 'theme_passwords'))
		next_menu6.add(types.InlineKeyboardButton(text = 'Подробнее', callback_data = 'details_theme_mails'))
		next_menu6.add(types.InlineKeyboardButton(text = 'Вернуться в меню', callback_data = 'mainmenu'))
		bot.send_message(call.message.chat.id, 'Электронная почта:\nСледует осторожно обходиться в электронными письмами. Чтобы не стать жертвой обмана следует:\n1. Проверить адрес отправителя. Сверьтесь с адресом почты на сайте компании/портала от которого пришло письмо.\n2. Если письмо от частного лица, не нажимайте на ссылки и не отправляйте никому личные данные.', reply_markup = next_menu6)
	
	elif call.data == 'theme_passwords':
		next_menu6 = types.InlineKeyboardMarkup()
		themes [1] = 0
		bot.edit_message_reply_markup(call.message.chat.id, message_id = call.message.message_id, reply_markup = '')
		if themes[0] == 1:
			next_menu6.add(types.InlineKeyboardButton(text = 'Электронная почта', callback_data = 'theme_mails'))
		if themes[2] == 1:
			next_menu6.add(types.InlineKeyboardButton(text = 'Соц сети и мессенджеры', callback_data = 'theme_social'))
		next_menu6.add(types.InlineKeyboardButton(text = 'Подробнее', callback_data = 'details_theme_passwords'))
		next_menu6.add(types.InlineKeyboardButton(text = 'Вернуться в меню', callback_data = 'mainmenu'))
		bot.send_message(call.message.chat.id, 'Пароли и учётные записи: \nСледует использовать надежные пароли содержащие одновременно:\n•    заглавные буквы\n•    строчные буквы\n•    цифры\n•    особые знаки, такие как  ! @ # $ % ^ & * ( ) - _ + = ; : , ./ ? | ` ~ [ ] { }\nСтарайтесь каждый раз использовать разные пароли. Частая ошибка это использование имени и года рождения в пароле. Такие пароли очень легко взломать, так как эти данные зачастую в открытом доступе.', reply_markup = next_menu6)
	
	elif call.data == 'theme_social':
		next_menu6 = types.InlineKeyboardMarkup()
		themes [2] = 0
		bot.edit_message_reply_markup(call.message.chat.id, message_id = call.message.message_id, reply_markup = '')
		if themes[0] == 1:
			next_menu6.add(types.InlineKeyboardButton(text = 'Электронная почта', callback_data = 'theme_mails'))
		if themes[1] == 1:
			next_menu6.add(types.InlineKeyboardButton(text = 'Пароли и учетный записи', callback_data = 'theme_passwords'))
		next_menu6.add(types.InlineKeyboardButton(text = 'Подробнее', callback_data = 'details_theme_passwords'))
		next_menu6.add(types.InlineKeyboardButton(text = 'Вернуться в меню', callback_data = 'mainmenu'))
		bot.send_message(call.message.chat.id, 'Соц сети и мессенджеры:\nВ социальных сетях ни с кем не стоит делиться личными данными и переводить деньги кому-либо, даже если вас просят об этом знакомые.\nМошенники могут создавать поддельные профили, схожие с профилями ваших знакомых.', reply_markup = next_menu6)

	# Подробности о каждой теме
	elif call.data == 'details_theme_mails':
		bot.edit_message_reply_markup(call.message.chat.id, message_id = call.message.message_id, reply_markup = '')
		details = types.InlineKeyboardMarkup()
		if themes[1] == 1:
			details.add(types.InlineKeyboardButton(text = 'Пароли и учетный записи', callback_data = 'theme_passwords'))
		if themes[2] == 1:
			details.add(types.InlineKeyboardButton(text = 'Соц сети и мессенджеры', callback_data = 'theme_social'))
		details.add(types.InlineKeyboardButton(text = 'Вернуться в меню', callback_data = 'mainmenu'))
		bot.send_message(call.message.chat.id, 'Эксперты центра цифровой экспертизы Роскачества совместно с экспертами по кибербезопасности из Group-IB, подготовили алгоритм из десяти шагов, который поможет распознать мошенническое письмо:\n1. Проверьте адрес отправителя\nМошенники часто делают адрес максимально похожим на компанию или организацию, которую они имитируют. Сравните данный адрес с другими письмами от оригинального отправителя.\n2. Обратите внимание на приветствие\nОбезличенное «привет» или «здравствуйте» — признак того, что письмо отправили мошенники.\n3. Проверьте контактную информацию и сверьте даты\nВнизу письма обязательно должна содержаться информация о том, как связаться с адресантом. Электронная почта, адрес, номер телефона, соцсети — всё это обязательно должно быть в письме от оригинального отправителя. Часто мошенники забывают проверить даты. Если, к примеру, конкурс, о котором идёт речь, должен завершиться в 2017 году, когда на дворе — 2020, вероятно, вам попался невнимательный мошенник, который вставил в тело письма устаревший шаблон.\n4. Проверьте бренд\nМошенники часто вводят в заблуждение пользователя с помощью электронных писем, в которых они называют себя представителями крупного бренда, компании, ведомства или розничной сети. Чтобы не попасться на эту удочку, необходимо внимательно проверить качество и оригинальность фирменных логотипов.\n5. Проверьте подлинность сайта\nЕсли вы уже перешли на сайт, на который ведёт письмо, проверьте его подлинность. Если это крупный бренд или компания, просто откройте новую вкладку и найдите их официальную страницу, а затем сравните URL-адреса.\nЗлоумышленники всё чаще используют в письмах ссылки, запускающие загрузку вредоносных объектов. Избегайте соблазна быстро перейти по ссылке из письма, даже если вас просят сделать это, чтобы получить доступ к важной информации или сообщению в своем аккаунте.\n6. Игнорируйте запросы личных и, тем более, банковских реквизитов\nЕсли в электронном письме вас просят обновить или повторно ввести свои личные данные или банковские реквизиты, вероятнее всего, это мошенники. Запомните: номер вашей карты, пин-код или код безопасности карты, девичья фамилия вашей матери и прочие вопросы — это персональная информация, делиться которой нельзя. Крупные компании и организации дорожат своей репутацией и не будут собирать личную информацию по электронной почте.\n7. Проверьте письмо на грамотность и стилистику\nОшибки в тексте письма сигнализируют о том, что его создатель не утруждал себя проверкой орфографии. Организация с репутацией такого позволить себе не может. Различные стили и размеры шрифта, несоответствие логотипов, некачественные изображения — всё это говорит о том, что письмо фейковое, и сделано оно «на скорую руку».\n8. Обращайте внимание на слишком официальные письма\nВряд ли оригинальный крупный интернет-магазин или ведомство станут описывать в письмах, какие они важные и официальные.\n9. Торопят — закрывайте письмо\nМошенники будут пытаться давить на вас с помощью быстро сгорающих предложений и эксклюзивных сделок. Потратьте время, чтобы проверить подлинность письма и его содержания, за это время предложение от вас никуда не денется. Лучше упустить подлинное предложение, чем рисковать своими платёжными и другими персональными данными.\n10. Самое главное оружие — связь с реальной компанией\nЕсли вы хотите быстро убедиться в оригинальности письма, которое получили, самостоятельно свяжитесь с отправителем. Конечно, звонить вы должны по номеру, указанному не в письме, а оригинальном сайте.\nПомните, что в интернете нет ничего абсолютно безопасного.', reply_markup = details)

	elif call.data == 'details_theme_passwords':
		bot.edit_message_reply_markup(call.message.chat.id, message_id = call.message.message_id, reply_markup = '')
		details = types.InlineKeyboardMarkup()
		if themes[0] == 1:
			details.add(types.InlineKeyboardButton(text = 'Электронная почта', callback_data = 'theme_emails'))
		if themes[2] == 1:
			details.add(types.InlineKeyboardButton(text = 'Соц сети и мессенджеры', callback_data = 'theme_social'))
		details.add(types.InlineKeyboardButton(text = 'Вернуться в меню', callback_data = 'mainmenu'))
		bot.send_message(call.message.chat.id, 'Это основной способ защиты ваших личных данных в интернете, поэтому к нему нужно отнестись с особым вниманием.\nНе храните информацию о паролях на компьютере, который используется для выхода в интернет. Конечно, лучше всего держать пароли в голове. Если же пароль слишком сложный, лучше запишите его отдельно на лист бумаги или в блокнот, и храните в надёжном месте.\nПользуйтесь двухэтапной аутентификацией — так ваши аккаунты будут надёжно защищены. Регулярно проверяйте почту и SMS-сообщения — если вам приходят подозрительные уведомления, вы всегда сможете пресечь попытки злоумышленников.\nНе используйте для паролей информацию, которую злоумышленники могут найти самостоятельно: дату рождения, номера документов, телефонов, имена ваших друзей и родственников, адрес и так далее.\nПридумывайте сложные пароли длиной не менее 8 символов с использованием заглавных и строчных букв, цифр, специальных значков %$#.\nНе используйте одинаковые пароли на разных сайтах.\nРегулярно меняйте пароли.\n', reply_markup = details)

	elif call.data == 'details_theme_social':
		bot.edit_message_reply_markup(call.message.chat.id, message_id = call.message.message_id, reply_markup = '')
		details = types.InlineKeyboardMarkup()
		if themes[0] == 1:
			details.add(types.InlineKeyboardButton(text = 'Электронная почта', callback_data = 'theme_emails'))
		if themes[1] == 1:
			details.add(types.InlineKeyboardButton(text = 'Пароли и учётные записи', callback_data = 'theme_passwords'))
		details.add(types.InlineKeyboardButton(text = 'Вернуться в меню', callback_data = 'mainmenu'))
		bot.send_message(call.message.chat.id, 'Заполучить ваши данные из социальных сетей можно двумя способами: простым и сложным.\nСложный способ подразумевает непосредственный взлом вашего соединения или устройства. Если хакер знает ваш IP-адрес или ваше имя, ему не составит труда выяснить, кто вы такой. Если, к тому же, он узнает ваш номер телефона, привязанный к IP, то можете считать себя уже взломанным. Эти взломы – как раз та главная причина, по которой у вас должен быть VPN на всех устройствах, где установлены социальные сети.\nОднако есть и более простой способ стать жертвой кражи данных или личности. Сообщая кому-то номер телефона, который вы используете для двухфакторной аутентификации, а также напрямую делясь личной информацией, вы ставите себя под удар. Хакеру не нужно будет делать ничего, кроме как просто спросить.\nНеобходимо всегда скептически относиться к подозрительным профилям людей, с которыми вы лично не знакомы. Есть огромная вероятность того, что хакер скрывается за таким фейковым аккаунтом. Подобные аферисты – искусные психологи и манипуляторы, которые точно знают, как играть на чувствах и эмоциях людей.\nлавное правило интернета гласит: если что-то звучит слишком хорошо, чтобы быть правдой – это обман.', reply_markup = details)


	# Процесс подтверждения почты
	elif call.data == 'accept':
		bot.edit_message_reply_markup(call.message.chat.id, message_id = call.message.message_id, reply_markup = 'theme_social')
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
			if message.text == a_and_q[num_of_question][int(a_and_q[num_of_question][5])]:
				if num_of_question in [0,1,2]:
					score[0] += 1
				elif num_of_question in [3,4,5,6]:
					score[1] += 1
				elif num_of_question in [7,8,9]:
					score[2] += 1
				bot.send_message(message.from_user.id, 'Ответ правильный!', reply_markup = stage1)
			else:
				bot.send_message(message.from_user.id, 'Ответ неверный :с', reply_markup = stage1) #Написать почему!
		else:
			stage1 = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(text = 'Завершить тест', callback_data = 'end_the_test'))
			if message.text == a_and_q[num_of_question][int(a_and_q[num_of_question][5])]:
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