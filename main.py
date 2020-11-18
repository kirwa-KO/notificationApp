from kivy.uix.screenmanager 	import ScreenManager
from requests					import get
from kivy.lang.builder 			import Builder
# from kivy.core.window			import Window
from os							import path
from threading					import Thread
from time						import sleep
from kivymd.app 				import MDApp
from slotspage					import SlotsPage, cluster_one, cluster_two, timeToSendGetRequest
from singinpage					import SingInPage

from json						import loads
from kivy.clock 				import Clock
from kivy.network.urlrequest 	import UrlRequest
from plyer						import notification

sm = ScreenManager()
login = ''
fullName = ""

def sendGetRequestToGetEvents():
	global login

	if path.isfile('./api_key.txt'):
		with open('api_key.txt', 'r') as file:
			fullName = file.readline().replace('\n', '')
			login = file.readline().replace('\n', '')
			api_key = file.readline().replace('\n', '')

		url = 'http://we-hack-things.com/get_data.php?login=' + login + '&api_key=' + api_key
		# print(url)
		req = UrlRequest(url, got_json)


def sendNotification(slot, cluster, notif):
	slot_splited = slot.split('|')
	if int(slot_splited[2]) < 50:

		begin = "Begin: " + slot_splited[0]
		end = "End:    " + slot_splited[1]
		if cluster == 47:
			place = "Place: " + slot_splited[2] + " Cluster: E1"
		else:
			place = "Place: " + slot_splited[2] + " Cluster: E2"

		if "21:00:00" in begin:
			if 'night' in notif:
				notification.notify(title="Free Slot", message=begin + '\n' + end + '\n' + place)
		elif "15:00:00" in  begin:
			if 'evening' in notif:
				notification.notify(title="Free Slot", message=begin + '\n' + end + '\n' + place)
		else:
			if 'morning' in notif:
					notification.notify(title="Free Slot", message=begin + '\n' + end + '\n' + place)

def got_json(req, result):
	events = loads(result)
	# print(events)
	if path.isfile('./notify_slots.txt'):
		with open('notify_slots.txt', 'r') as file:
			notif = file.readline()
		nofit = notif.split('|')
	else:
		notif = []

	for event in events['raw_data'].split(';'):
		if '|47|' in event:
			cluster_one.append(event)
			sendNotification(event, 47, notif)
		elif '|48|' in event:
			cluster_two.append(event)
			sendNotification(event, 48, notif)


sm.add_widget(SlotsPage(name="slots"))
scr = SingInPage(name='singin')
sm.add_widget(scr)

class mainApp(MDApp):
	def build(self):
		# Window.size = (360, 640)
		self.theme_cls.primary_palette= "Red"
		screen = Builder.load_file('gui.kv')
		return screen

# threadToSendGetRequest()

Clock.schedule_once(lambda x: sendGetRequestToGetEvents())

Clock.schedule_interval(lambda x: sendGetRequestToGetEvents(), timeToSendGetRequest)



if __name__ == "__main__":
	mainApp().run()
