import requests

# API call
response = requests.get('http://localhost:8000/catalog/search', auth=('rileymorganwells@gmailcom', 'Password1'), params={
    #'page': 1,
    'name': 'a',
    'category': 'books',
    'maxprice': 500.00,
})
print('Status code', response.status_code)
print(response.json())