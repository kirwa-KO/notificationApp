from kivy.uix.screenmanager 	import Screen
from kivy.properties			import ObjectProperty
from kivymd.uix.dialog			import MDDialog
from hashlib					import sha256
from kivymd.uix.button			import MDFlatButton
from requests.exceptions		import ReadTimeout
from requests					import post, get

class SingInPage(Screen):
	login    = ObjectProperty(None)
	password = ObjectProperty(None)

	def close_dialog_func(self, obj):
		self.dialog.dismiss()

	def click_sing_in_btn(self):
		global login
		global fullName

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
				response = post(url, params=params, timeout=5)
				data = response.json()
				if data['code'] == 200:
					with open('api_key.txt', 'w') as file:
						file.write(data['full_name'].upper() + '\n')
						file.write(self.login.text + '\n')
						file.write(data['api_key'])
					self.manager.current = "slots"
				elif data['code'] == 404:
					self.dialog = MDDialog(	title="Login Erreur:",
										text=data['err'],
										size_hint=(0.7, 1),
										buttons=[close_dialog_btn])
					self.dialog.open()
			except ReadTimeout:
				self.dialog = MDDialog(	title="Server Erreur:",
										text="Server May Be Down Please\nTry agin later..!!",
										size_hint=(0.7, 1),
										buttons=[close_dialog_btn])
				self.dialog.open()
			except:
				self.dialog = MDDialog(	title="Erreur id 1024:",
										text="Please Try Again..!!",
										size_hint=(0.7, 1),
										buttons=[close_dialog_btn])
				self.dialog.open()