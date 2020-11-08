from kivymd.app 				import MDApp
from kivymd.uix.screen 			import Screen
from kivy.lang 					import Builder
from kv_variables				import login_helper, password_helper
from kivymd.uix.button			import MDRoundFlatButton, MDFlatButton
from kivymd.uix.dialog			import MDDialog
from kivy.core.window			import Window
from hashlib					import sha256
from requests					import post

class notifApp(MDApp):
	def build(self):
		Window.size = (360, 640)
		screen = Screen()
		self.theme_cls.primary_palette= "Green"
		self.login = Builder.load_string(login_helper)
		self.password = Builder.load_string(password_helper)
		sing_in_btn = MDRoundFlatButton(text="Sing in",
									  	pos_hint={"center_x": 0.5, "center_y": 0.4},
									   on_release=self.click_sing_in_btn)
		screen.add_widget(self.login)
		screen.add_widget(self.password)
		screen.add_widget(sing_in_btn)
		return screen

	def close_dialog_func(self, obj):
		self.dialog.dismiss()

	def click_sing_in_btn(self, obj):
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
			response = post(url, params=params)
			data = response.json()
			# you need to remove that
			print(data)
			if data['code'] == 200:
				with open('api_key.txt', 'w') as file:
					file.write(data['api_key'])
			elif data['code'] == 404:
				self.dialog = MDDialog(	title="Login Erreur:",
										text=data['err'],
										size_hint=(0.7, 1),
										buttons=[close_dialog_btn])
				self.dialog.open()


notifApp().run()