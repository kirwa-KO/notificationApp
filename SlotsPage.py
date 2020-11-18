from kivymd.uix.list			import ThreeLineIconListItem, IconLeftWidget, OneLineIconListItem
from kivy.properties			import ObjectProperty
from os							import remove, path
from kivy.uix.screenmanager 	import Screen
from kivymd.uix.button			import MDFlatButton
from kivymd.uix.dialog			import MDDialog
# from plyer						import notification


cluster_one = []
cluster_two = []
timeToSendGetRequest = 5
timeForSlotsToNotify = set()

def writeNotifySlotElementInFile():
	with open('notify_slots.txt', 'w') as file:
		for i in timeForSlotsToNotify:
			file.write(i + '|')

class SlotsPage(Screen):
	global timeToSendGetRequest

	full_name = ""

	slots = []
	box = ObjectProperty(None)
	cluster = cluster_one

	def on_touch_down(self, *args):
		if path.isfile('./api_key.txt') == False:
			self.manager.current = 'singin'
		else:
			super(SlotsPage, self).on_touch_down(*args)

	def choose_cluster_one(self, obj):

		# print(cluster_one)
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
		if path.isfile('./api_key.txt'):
			with open('api_key.txt', 'r') as file:
				self.full_name = file.readline().replace('\n', '')

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
				# if 'night' in timeForSlotsToNotify:
				# 	notification.notify(title="Free Slot", message=begin + '\n' + end + '\n' + place)
			elif "15:00:00" in  begin:
				icon = IconLeftWidget(icon='weather-cloudy')
				# if 'evening' in timeForSlotsToNotify:
				# 	notification.notify(title="Free Slot", message=begin + '\n' + end + '\n' + place)
			else:
				icon = IconLeftWidget(icon='weather-sunny')
				# if 'morning' in timeForSlotsToNotify:
				# 	notification.notify(title="Free Slot", message=begin + '\n' + end + '\n' + place)

			item = ThreeLineIconListItem(text=begin, secondary_text=end, tertiary_text=place)
			item.add_widget(icon)
			self.slots.append(item)
			self.box.add_widget(item)

	def logout(self):
		remove('api_key.txt')
		self.manager.current = 'singin'

	def close_dialog_func(self, obj):
		self.dialog.dismiss()


	def makePopUpAndOpen(self, text):
		close_dialog_btn = MDFlatButton(text="Close", on_release=self.close_dialog_func)
		self.dialog = MDDialog(	title="Add or Remove Slots Notif:",
					text=text,
					size_hint=(0.7, 1),
					buttons=[close_dialog_btn])
		self.dialog.open()

	def add_morning_notification(self):

		if 'morning' in timeForSlotsToNotify:
			timeForSlotsToNotify.remove('morning')
			self.makePopUpAndOpen("Morning Notivy Removed..!!")
		else:
			timeForSlotsToNotify.add('morning')
			self.makePopUpAndOpen("Morning Notivy Added..!!")
		writeNotifySlotElementInFile()

	def add_evening_notification(self):
		if 'evening' in timeForSlotsToNotify:
			timeForSlotsToNotify.remove('evening')
			self.makePopUpAndOpen("Evening Notivy Removed..!!")
		else:
			timeForSlotsToNotify.add('evening')
			self.makePopUpAndOpen("Evening Notivy Added..!!")
		writeNotifySlotElementInFile()

	def add_night_notification(self):
		if 'night' in timeForSlotsToNotify:
			timeForSlotsToNotify.remove('night')
			self.makePopUpAndOpen("Night Notivy Removed..!!")
		else:
			timeForSlotsToNotify.add('night')
			self.makePopUpAndOpen("Night Notivy Added..!!")
		writeNotifySlotElementInFile()


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
