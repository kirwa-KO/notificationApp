from kivy.uix.screenmanager 	import ScreenManager
from requests					import get
from kivy.lang.builder 			import Builder
from kivy.core.window			import Window
from os							import path
from threading					import Thread
from time						import sleep
from kivymd.app 				import MDApp
from SlotsPage					import SlotsPage, cluster_one, cluster_two, timeToSendGetRequest
from SingInPage					import SingInPage

from json						import loads
from kivy.clock 				import Clock
from kivy.network.urlrequest import UrlRequest

sm = ScreenManager()
login = ''
fullName = ""

def sendGetRequestToGetEvents():
	print("I am Here..!!")
	global login

	if path.isfile('./api_key.txt'):
		with open('api_key.txt', 'r') as file:
			fullName = file.readline()
			login = file.readline()
			api_key = file.readline()
		data = {
			'login': login.replace('\n', ''),
			'api_key': api_key.replace('\n', '')
		}
		while True:
			try:
				response = get('http://we-hack-things.com/get_data.php', params=data)
				events   = response.json()

				for i in events['raw_data'].split(';'):
					if '|47|' in i:
						cluster_one.append(i)
					elif '|48|' in i:
						cluster_two.append(i)
				
			except:
				print("Get Request Error")
			sleep(timeToSendGetRequest)
	else:
		print("api_key.txt file not exist")


# http://we-hack-things.com/get_data.php?login=ibaali&api_key=864a2dc2e97d473390fb4969f5b7edadUIxgcBgNVsWgbb769f2df7e65b5285da18f469a63ddbEmmc6J9DPiyJ

def threadToSendGetRequest():
	# getRequestThread = Thread(target=sendGetRequestToGetEvents, name="Send Get Request", args=())
	# getRequestThread.daemon = True
	# getRequestThread.start()
	url = 'http://we-hack-things.com/get_data.php?login=ibaali&api_key=864a2dc2e97d473390fb4969f5b7edadUIxgcBgNVsWgbb769f2df7e65b5285da18f469a63ddbEmmc6J9DPiyJ'
	req = UrlRequest(url, got_json)
	# print(req.result)
	
def got_json(req, result):
	events = loads(result)
	# print(events['raw_data'])
	for i in events['raw_data'].split(';'):
		if '|47|' in i:
			cluster_one.append(i)
		elif '|48|' in i:
			cluster_two.append(i)
	# you need to add here function to send notification

sm.add_widget(SlotsPage(name="slots"))
scr = SingInPage(name='singin')
sm.add_widget(scr)

class mainApp(MDApp):
	def build(self):
		Window.size = (360, 640)
		self.theme_cls.primary_palette= "Red"
		screen = Builder.load_file('gui.kv')
		return screen

threadToSendGetRequest()

Clock.schedule_interval(lambda x: threadToSendGetRequest(), 5)

# sm.current_screen = 'singin'

if __name__ == "__main__":
	mainApp().run()
