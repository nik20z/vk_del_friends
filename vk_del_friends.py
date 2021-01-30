import time
import vk_api

from pprint import pprint


settings = {'login': '',
			'password': '', 
			'shutdown_time': 30}
d = {i: {'count': 0, 'users': {}} for i in ['banned', 'deleted']}


def auth(login, password):
	vk_session = vk_api.VkApi(login, password)
	vk_session.auth()
	vk = vk_session.get_api()
	return vk

def accounts_banned(): # вход - id
	friends = vk.friends.get(user_id = vk.account.getProfileInfo()['id']) # список всех друзей ( вернет count - кол-во, items - данные)
	friends_items = friends['items']
	for j in [friends_items[d:d+1000] for d in range(0, len(friends_items), 1000)]: # перебираем друзей (по 1к)
		inf = vk.users.get(user_ids = j) # массив словарей с инфой о друзьях
		for user in inf: # перебираем друзей по одному
			if 'deactivated' in user: # если друг заблочен 
				for j in user['deactivated'].split(): # перебираем виды блокировок (banned, deleted)
					d[j]['count'] += 1
					user_id = user['id']
					user_name = user['first_name'] + ' ' + user['last_name']
					user_link = 'https://vk.com/id' + str(user_id)
					d[j]['users'][user_id] = [user_name, user_link]
	return d

def command_option(command):
	if command == '0':
		return ['banned', 'deleted']
	elif command == '1':
		return ['banned']
	elif command == '2':
		return ['deleted']
	else:
		return False

def __main__(vk):
	try:
		keys = command_option(input())
		if keys == False:
			print('Неверная команда')
			__main__(vk)
		else:
			time_sleep = settings['shutdown_time']
			[print(vk.friends.delete(user_id = user_id)) for key in keys for user_id in d[key]['users']]
			print('Работа программы завершена! Выключение произойдёт через ' + str(time_sleep) + ' с')
			time.sleep(time_sleep)
			run = False
	except vk_api.exceptions.ApiError as e:
		e = str(e)
		if 'list_id is undefined' in e:
			print('Вы выбрали пустой массив.. попробуйте ещё раз')
		else:
			print(e)


run = True
vk = auth(settings['login'], settings['password'])
d = accounts_banned()
pprint(d)

print('0 - удалить всех')
print('1 - только banned')
print('2 - только deleted')

while run:
	__main__(vk)