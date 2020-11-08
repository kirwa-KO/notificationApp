login_helper = '''
MDTextField:
	hint_text: "Enter your login"
	pos_hint: {"center_x": 0.5, "center_y": 0.6}
	size_hint_x: None
	width: 400
	helper_text: "or click forget password"
	helper_text_mode: "on_focus"
	icon_right: "shield-account"
	icon_right_color: app.theme_cls.primary_color
'''

password_helper = '''
MDTextField:
	hint_text: "Enter your password"
	pos_hint: {"center_x": 0.5, "center_y": 0.5}
	size_hint_x: None
	width: 400
	icon_right: "key"
	password: True
	icon_right_color: app.theme_cls.primary_color
'''
