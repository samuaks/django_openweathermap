import requests
from django.shortcuts import render
from .models import City
from .forms import LocForm

# Create your views here.
def index(request):
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=bc31e2ebac716e0f1832bbed990b7cbd&lang=fi'


    if request.method == 'POST':
        form = LocForm(request.POST)
        form.save()

    form = LocForm()

    cities = City.objects.all()

    data_dic = []

    for location in cities: 

        response = requests.get(url.format(location)).json()
        dic = {
            'location' : location.name,
            'temperature' : response['main']['temp'],
            'description' : response['weather'][0]['description'],
            'icon' : response['weather'][0]['icon'],
        }
        

        data_dic.append(dic)

    print(data_dic)
    context = {'data_dic' : data_dic, 'form' : form}

    return render(request, 'weather/weather.html', context)