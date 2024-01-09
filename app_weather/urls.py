#urls.py in app_weather
from django.urls import path
from .views import weather_view

def weather_view(request):
    if request.method == "GET":
        lat = request.GET.get('lat')  # данные придут в виде строки
        lon = request.GET.get('lon')  # данные придут в виде строки
        if lat and lon:
            data = current_weather(lat=lat, lon=lon)
        else:
            data = current_weather(59.93, 30.31)
        return JsonResponse(data, json_dumps_params={'ensure_ascii': False,
                                                     'indent': 4})

urlpatterns = [
             path('weather/', weather_view),
             path('', weather_view),
]