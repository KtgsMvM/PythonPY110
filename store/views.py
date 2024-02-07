from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from .models import DATABASE
from logic.services import filtering_category
from logic.services import view_in_cart, add_to_cart, remove_from_cart
from django.shortcuts import render

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
                data = filtering_category(DATABASE, category_key, ordering_key, True) #  TODO Провести фильтрацию с параметрами
            #else:
                #data = filtering_category(DATABASE, category_key, ordering_key) #  TODO Провести фильтрацию с параметрами
            else:
                data = filtering_category(DATABASE, category_key, rating, True)
        else:
            data = filtering_category(DATABASE, category_key) #  TODO Провести фильтрацию с параметрами
        # В этот раз добавляем параметр safe=False, для корректного отображения списка в JSON
        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False,
                                                                 'indent': 4})

#result = [product for product in database.values() if product['category'] == category_key]
#result.sort(key=lambda x: x[ordering_key], reverse=reverse)   # TODO Проведите сортировку result по ordering_key и параметру reverse
def shop_view(request):
    if request.method == "GET":
        return render(request,
                      'store/shop.html',
                      context={"products": DATABASE.values()})
    #     with open('store/shop.html', encoding="utf-8") as f:
    #         data = f.read()  # Читаем HTML файл
    # return HttpResponse(data)  # Отправляем HTML файл как ответ

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


def cart_view(request):
    if request.method == "GET":
        data = view_in_cart() # TODO Вызвать ответственную за это действие функцию
        if request.GET.get('format') =='JSON':
            return JsonResponse(data, json_dumps_params={'ensure_ascii': False,
                                                     'indent': 4})
        products = []  # Список продуктов
        for product_id, quantity in data['products'].items():
            product = DATABASE[product_id]   # 1. Получите информацию о продукте из DATABASE по его product_id. product будет словарём
            product["quantity"] = quantity
            # 2. в словарь product под ключом "quantity" запишите текущее значение товара в корзине
            product["price_total"] = f"{quantity * product['price_after']:.2f}"  # добавление общей цены позиции с ограничением в 2 знака
            # 3. добавьте product в список products
            products.append(product)

        return render(request, "store/cart.html", context={"products": products})


def cart_add_view(request, id_product):
    if request.method == "GET":
        result = add_to_cart(id_product) # TODO Вызвать ответственную за это действие функцию
        if result:
            return JsonResponse({"answer": "Продукт успешно добавлен в корзину"},
                                json_dumps_params={'ensure_ascii': False})

        return JsonResponse({"answer": "Неудачное добавление в корзину"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})


def cart_del_view(request, id_product):
    if request.method == "GET":
        result = remove_from_cart(id_product) # TODO Вызвать ответственную за это действие функцию
        if result:
            return JsonResponse({"answer": "Продукт успешно удалён из корзины"},
                                json_dumps_params={'ensure_ascii': False})

        return JsonResponse({"answer": "Неудачное удаление из корзины"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})

def coupon_check_view(request, name_coupon, is_valid):
    # DATA_COUPON - база данных купонов: ключ - код купона (name_coupon);
    # значение - словарь со значением скидки в процентах и
    # значением действителен ли купон или нет
    DATA_COUPON = {
        "coupon": {
            "value": 10,
            "is_valid": True},
        "coupon_old": {
            "value": 20,
            "is_valid": False},
    }
    if request.method == "GET":
        data = coupon_check_view()
        if is_valid is not None:
            name_coupon = DATA_COUPON()
            return JsonResponse(f' "Купон действителен! Размер скидки":{discount} %')

        # TODO Проверьте, что купон есть в DATA_COUPON, если он есть, то верните JsonResponse в котором по ключу "discount"
        # получают значение скидки в процентах, а по ключу "is_valid" понимают действителен ли купон или нет (True, False)

        return HttpResponseNotFound("Неверный купон")
        # TODO Если купона нет в базе, то верните HttpResponseNotFound("Неверный купон")


def delivery_estimate_view(request):
    # База данных по стоимости доставки. Ключ - Страна; Значение словарь с городами и ценами; Значение с ключом fix_price
    # применяется если нет города в данной стране
    DATA_PRICE = {
            "Россия": {"Москва": {"price": 80},
            "Санкт-Петербург": {"price": 80},
            "fix_price": 100,},
                }
    if request.method == "GET":
        data = request.GET
        country = data.get('country')
        city = data.get('city')
        # TODO Реализуйте логику расчёта стоимости доставки, которая выполняет следующее:
        if country and city
        # Если в базе DATA_PRICE есть и страна (country) и существует город(city),
    # то вернуть JsonResponse со словарём, {"price": значение стоимости доставки}
        # Если в базе DATA_PRICE есть страна, но нет города,
    # то вернуть JsonResponse со словарём, {"price": значение фиксированной стоимости доставки}
        # Если нет страны, то вернуть HttpResponseNotFound("Неверные данные")