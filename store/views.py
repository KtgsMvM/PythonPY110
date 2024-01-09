from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from .models import DATABASE
from logic.services import filtering_category

def products_view(request):
    if request.method == "GET":
        dict_ = request.GET
        id_= dict_.get("id")
        if id_ is not None:
            product = DATABASE.get(id_)
            if product is not None:
                data = product
            else:
                return HttpResponseNotFound("Данного продукта нет в базе данных")
        else:
            data = DATABASE
        return JsonResponse(data, json_dumps_params={'ensure_ascii': False,'indent': 4})
    # Вернуть JsonResponse с объектом DATABASE и параметрами отступов и кодировок,
    # как в приложении app_weather

        category_key = request.GET.get("category")  # Считали 'category'
        if ordering_key := request.GET.get("ordering"): # Если в параметрах есть 'ordering'
            if request.GET.get("reverse") in ('true', 'True'): # Если в параметрах есть 'ordering' и 'reverse'=True
                data = ... #  TODO Провести фильтрацию с параметрами
            else:
                data = ... #  TODO Провести фильтрацию с параметрами
        else:
            data = ... #  TODO Провести фильтрацию с параметрами
        # В этот раз добавляем параметр safe=False, для корректного отображения списка в JSON
        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False,
                                                                 'indent': 4})

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
                        data_page = f.read()
                    return HttpResponse(data_page)
        elif isinstance(page, int):
            data = DATABASE.get(str(page))  # Получаем какой странице соответствует данный id
            if data:  # Если по данному page было найдено значение
                with open(f'store/products/{data["html"]}.html', encoding="utf-8")as f:
                    data = f.read()
                return HttpResponse(data)
        # Если за всё время поиска не было совпадений, то значит по данному имени нет соответствующей
        # страницы товара и можно вернуть ответ с ошибкой HttpResponse(status=404)
        return HttpResponse(status=404)

