from requests import get

with open('api_key.txt', 'r') as file:
	api_key = file.readline()
data = {
	'login': 'ibaali',
	'api_key': api_key.replace('\n', '')
}

response = get('http://we-hack-things.com/get_data.php', params=data)

print(response.json())