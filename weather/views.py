import requests
from django.shortcuts import render, redirect
from .models import City
from .forms import LocForm

# Create your views here.
def index(request):
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=bc31e2ebac716e0f1832bbed990b7cbd&lang=fi'



    message_if_error = ''
    toast = ''
    toast_css = ''

    if request.method == 'POST':
        form = LocForm(request.POST)

        if form.is_valid():
            loc_filter = form.cleaned_data['name']
            exists = City.objects.filter(name=loc_filter).count()

            if exists == 0:
                response = requests.get(url.format(loc_filter)).json()
                if response['cod'] == 200:
                    form.save()
                else:
                    message_if_error = 'You are either from the future or stuck in the past'
            else:
                message_if_error = 'Location already exists'

        if message_if_error:
                toast = message_if_error
                toast_css = 'is-danger'
        else:
            toast = 'Location is valid'
            toast_css = 'is-success'

    print(message_if_error)
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

  
    context = {
        'data_dic' : data_dic,
        'form' : form,
        'toast' : toast,
        'toast_css' : toast_css
    }

    return render(request, 'weather/weather.html', context)

def delete(request, city_name):
    City.objects.get(name=city_name).delete()

    return redirect('home')