from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from shelf_life.models import Product

def landing(request):
    return render(request, 'shelf_life/landing.html')

def search(request):
    query = request.GET.get("q", "").strip()
    results = []

    if query:
        results = Product.objects.filter(item_name__icontains=query)

    return render(request, "shelf_life/search_results.html", {
        "query": query,
        "results": results,
    })

# def product_detail(request, product_id):
#     product = get_object_or_404(Product, pk=product_id)
#     query = request.GET.get("q", "")
#     return render(request, "shelf_life/product_detail.html", {
#         "product": product,
#         "query": query,
#     })
def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    came_from = request.GET.get('from', '')   # e.g. 'search' or 'baby_food'
    query = request.GET.get('q', '')           # search query if any

    context = {
        'product': product,
        'came_from': came_from,
        'query': query,
    }
    return render(request, 'shelf_life/product_detail.html', context)


def category_select(request):
    return render(request, "shelf_life/category_select.html")

def baby_food_list(request):
    products = Product.objects.filter(baby_food_shelf_life__isnull=False).exclude(baby_food_shelf_life="").order_by("item_name")
    return render(request, "shelf_life/baby_food_list.html", {"products": products})

def shelf_stable(request):
    return render(request, "shelf_life/shelf_stable.html")

def dry_goods(request):
    dry_goods_subcategories = [
        "Baking",
        "Cereals / Grains",
        "Pasta & Noodles",
        "Snacks & Sweets",
        "Proteins / Legumes",
        "Prepared Mixes",
        "Bread & Baked Goods"
    ]
    return render(request, 'shelf_life/dry_goods.html', {'subcategories': dry_goods_subcategories})