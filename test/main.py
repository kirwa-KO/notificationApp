from kivymd.app 				import MDApp
from kivy.lang.builder 			import Builder
from kivy.uix.screenmanager 	import ScreenManager, Screen
from kivy.core.window			import Window
from kivy.properties			import ObjectProperty

class SingInPage(Screen):
	login    = ObjectProperty(None)
	password = ObjectProperty(None)
	def click_sing_in_btn(self):
		print(self.login.text, self.password.text)

class SlotsPage(Screen):
	pass

sm = ScreenManager()
sm.add_widget(SingInPage(name='singin'))
sm.add_widget(SlotsPage(name="slots"))
class mainApp(MDApp):
	def build(self):
		Window.size = (360, 640)
		self.theme_cls.primary_palette= "Green"
		screen = Builder.load_file('gui.kv')
		return screen

mainApp().run()