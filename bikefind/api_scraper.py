from flask import Flask, render_template
import requests



r = requests.get('https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=6e19678db44aa0bfdb4632faba1f58723758a2c4')
for obj in r.json()[:20]:
    print(obj)
    print('\n')
    
r2 = requests.get('http://api.openweathermap.org/data/2.5/weather?q=Dublin&appid=416123cec041d7c358e497cd73c9657e').json()
print(r2)