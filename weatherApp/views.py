from django.shortcuts import render
from django.contrib import messages
import requests
import datetime


def home(request):
    #city is the variable we use to fetch from API
    if 'city' in request.POST:
        city = request.POST['city']
    else:
        city = 'trivandrum'
        
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=b1543d62c0f71e311b5c15d9b85378de'
    PARAMS = {'units':'metric'}  #converts temp to celsium and fh
    
    API_KEY = 'AIzaSyDZ_quspLkx__zJRV7L6CJlVRdMXywAobs'
    SEARCH_ENGINE_ID ='961ef23123c314e7a'
    
    query = city + ' 1920x1080' #space is imp or else eg: trivandrum1920x1080
    page = 1
    start = (page - 1) * 10+1
    searchType = 'image'
    city_url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}&searchType={searchType}&imgSize=xlarge"

    data = requests.get(city_url).json()
    count = 1
    search_items = data.get("items")
    image_url = search_items[1]['link']
    
    try:
        data = requests.get(url,PARAMS).json() #send get request and parse all json responses

        description = data['weather'][0]['description'] #0 is the index of json by default
        icon = data['weather'][0]['icon']
        temp = data['main']['temp']

        day = datetime.date.today()
        context = {
            'description': description,
            'icon': icon,
            'temp': temp,
            'day' : day,
            'city' : city,
            'exception_occured' : False,
            'image_url': image_url
            
            }
        return render (request,'index.html',context)
        
    except:
        exception_occured = True
        messages.error(request,'entered data is not available in API')
        day = datetime.date.today()
        
        context = {
            'description':'clear sky',
            'icon': '01d',
            'temp': 25,
            'day' : day,
            'city' :'trivandrum',
            'exception_occured' : True
            }
    return render (request,'index.html',context)
        