from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from .models import DATABASE


def products_view(request):
    if request.method == "GET":
        id_= request.GET.get("id")
        if id_:
            product = DATABASE.get(id_)
        if product:
            data = product
        else:
            return HttpResponseNotFound("Данного продукта нет в базе данных")
    else:
        data = DATABASE()
    return JsonResponse(data, json_dumps_params={'ensure_ascii': False,'indent': 4})
    # Вернуть JsonResponse с объектом DATABASE и параметрами отступов и кодировок,
    # как в приложении app_weather

def shop_view(request):
    if request.method == "GET":
        with open('store/shop.html', encoding="utf-8") as f:
            data = f.read()  # Читаем HTML файл
    return HttpResponse(data)  # Отправляем HTML файл как ответ

def product_page_view(request, page):
    if request.method == "GET":
        if isinstance(page, str):
            for data in DATABASE.values():
                if data['html'] == page:  # Если значение переданного параметра совпадает именем html файла
                    with open(f'store/products/{page}.html', encoding="utf-8") as f:
                    page = f.read()
                    return HttpResponse(page)
        elif isinstance(page, int):
            data = DATABASE.get(str(page))  # Получаем какой странице соответствует данный id
            if data:  # Если по данному page было найдено значение
                with open(f'store/products/{data["html"]}.html', encoding="utf-8")as f:
                data = f.read()
            return HttpResponse(data)
        else:
        # Если за всё время поиска не было совпадений, то значит по данному имени нет соответствующей
        # страницы товара и можно вернуть ответ с ошибкой HttpResponse(status=404)
        return HttpResponse(status=404)

