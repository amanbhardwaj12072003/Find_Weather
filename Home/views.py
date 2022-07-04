from django.http import Http404
from django.shortcuts import render , HttpResponse
import requests

# Create your views here.

def get_html_content(request):
        USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
        LANGUAGE = "en-US,en;q=0.5"
        session = requests.Session()
        session.headers['User-Agent'] = USER_AGENT
        session.headers['Accept-Language'] = LANGUAGE
        session.headers['Content-Language'] = LANGUAGE
        city = request.GET.get('City')
        city = city.replace(" " , "+")
        html_content = session.get(f'https://www.google.com/search?q=weather+{city}').text
        return html_content


def home(request):
    weather_data = None
    if 'City' in request.GET:
        # Fetch Weather data from google site by scrapping 
        # city = request.GET.get('City')
        html_content = get_html_content(request)
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_content , 'html.parser')
        weather_data = dict()

        weather_data['region'] = soup.find("span", attrs={"class": "BNeawe tAd8D AP7Wnd"}).text
        # weather_data['daytime'] = soup.find('div' , attrs={'id' : 'wob_dts'}).text
        # weather_data['status'] = soup.find('div' , attrs={'id' : 'wob_dcp'}).text
        weather_data['daytime'], weather_data['status'] = soup.find("div", attrs={"class": "BNeawe tAd8D AP7Wnd"}).text.split(
            '\n')
        weather_data['temp'] = soup.find("div", attrs={"class": "BNeawe iBp4i AP7Wnd"}).text


    return render(request , 'index.html' , {'weather' : weather_data})
    