from kivymd.uix.list			import ThreeLineIconListItem, IconLeftWidget, OneLineIconListItem
from kivy.uix.screenmanager 	import ScreenManager, Screen
from kivy.properties			import ObjectProperty
from kivymd.uix.button			import MDFlatButton
from requests					import post, get
from kivymd.uix.dialog			import MDDialog
from kivymd.uix.label			import MDLabel
from kivy.lang.builder 			import Builder
from kivy.core.window			import Window
from hashlib					import sha256
from os							import remove
from threading					import Thread
from time						import sleep
from kivymd.app 				import MDApp

sm = ScreenManager()
timeToSendGetRequest = 5
login = ''
cluster_one = []
cluster_two = []

def sendGetRequestToGetEvents():
	global login
	with open('api_key.txt', 'r') as file:
		login = file.readline()
		api_key = file.readline()
	data = {
		'login': login.replace('\n', ''),
		'api_key': api_key.replace('\n', '')
	}
	while True:
		response = get('http://we-hack-things.com/get_data.php', params=data)
		events = response.json()

		for i in events['raw_data'].split(';'):
			if '|47|' in i:
				cluster_one.append(i)
			elif '|48|' in i:
				cluster_two.append(i)
		sleep(timeToSendGetRequest)


# def threadToSendGetRequest():
# 	getRequestThread = Thread(target=sendGetRequestToGetEvents, name="Send Get Request", args=())
# 	getRequestThread.start()

class SingInPage(Screen):
	login    = ObjectProperty(None)
	password = ObjectProperty(None)

	def close_dialog_func(self, obj):
		self.dialog.dismiss()

	def click_sing_in_btn(self):
		global login
		close_dialog_btn = MDFlatButton(text="Close", on_release=self.close_dialog_func)
		if self.login.text == "" or self.password.text == "":
			if self.login.text == "":
				check_string = "Please entre your login..!!"
			else:
				check_string = "Please entre your password..!!"
			self.dialog = MDDialog(	title="Incompleted Infos:",
					 				text=check_string,
						 			size_hint=(0.7, 1),
									buttons=[close_dialog_btn])
			self.dialog.open()
		else:
			url = 'http://we-hack-things.com/login_user.php'
			passwd_sha256 = sha256(self.password.text.encode("ascii")).hexdigest()
			params = {
				'login': self.login.text,
				'p_hash': passwd_sha256
			}
			login = self.login.text
			try:
				response = post(url, params=params)
				data = response.json()
				if data['code'] == 200:
					with open('api_key.txt', 'w') as file:
						file.write(self.login.text + '\n')
						file.write(data['api_key'])
					self.manager.current = "slots"
				elif data['code'] == 404:
					self.dialog = MDDialog(	title="Login Erreur:",
										text=data['err'],
										size_hint=(0.7, 1),
										buttons=[close_dialog_btn])
					self.dialog.open()
			except:
				self.dialog = MDDialog(	title="Server Erreur:",
										text="Server May Be Down Please\nTry agin later..!!",
										size_hint=(0.7, 1),
										buttons=[close_dialog_btn])
				self.dialog.open()


class SlotsPage(Screen):
	global timeToSendGetRequest
	full_name = "IMRAN BAALI"

	slots = []
	box = ObjectProperty(None)
	cluster = cluster_one

	def choose_cluster_one(self, obj):
		self.cluster = cluster_one
		for slot in self.slots:
			self.box.remove_widget(slot)
		self.slots = []
		self.on_box()

	def choose_cluster_two(self, obj):
		self.cluster = cluster_two
		for slot in self.slots:
			self.box.remove_widget(slot)
		self.slots = []
		self.on_box()

	def on_box(self, *args):

		icon = IconLeftWidget(icon='laptop')
		item = OneLineIconListItem(text="Cluster One", on_release=self.choose_cluster_one)
		item.add_widget(icon)
		self.box.add_widget(item)
		self.slots.append(item)

		icon = IconLeftWidget(icon='laptop')
		item = OneLineIconListItem(text="Cluster Two", on_release=self.choose_cluster_two)
		item.add_widget(icon)
		self.box.add_widget(item)
		self.slots.append(item)

		for slot in self.cluster:
			slot_splited = slot.split('|')
			begin = "Begin: " + slot_splited[0]
			end = "End:    " + slot_splited[1]
			if slot_splited[3] == '47':
				place = "Place: " + slot_splited[2] + " Cluster: E1"
			else:
				place = "Place: " + slot_splited[2] + " Cluster: E2"

			if "21:00:00" in begin:
				icon = IconLeftWidget(icon='weather-night')
			elif "15:00:00" in  begin:
				icon = IconLeftWidget(icon='weather-windy')
			else:
				icon = IconLeftWidget(icon='weather-sunny')

			item = ThreeLineIconListItem(text=begin, secondary_text=end, tertiary_text=place)
			item.add_widget(icon)
			self.slots.append(item)
			self.box.add_widget(item)
			# break

	def logout(self):
		remove('api_key.txt')
		self.manager.current = 'singin'

	def oneLineListItemClicked_5_Second(self):
		timeToSendGetRequest = 5

	def oneLineListItemClicked_30_Seconds(self):
		timeToSendGetRequest = 30

	def oneLineListItemClicked_60_Seconds(self):
		timeToSendGetRequest = 60

	def oneLineListItemClicked_300_Seconds(self):
		timeToSendGetRequest = 300

	def oneLineListItemClicked_600_Seconds(self):
		timeToSendGetRequest = 600

	def oneLineListItemClicked_3600_Seconds(self):
		timeToSendGetRequest = 3600


sm.add_widget(SingInPage(name='singin'))
sm.add_widget(SlotsPage(name="slots"))

class mainApp(MDApp):
	def build(self):
		Window.size = (360, 640)
		self.theme_cls.primary_palette= "Red"
		screen = Builder.load_file('gui.kv')
		return screen


# threadToSendGetRequest()

mainApp().run()
