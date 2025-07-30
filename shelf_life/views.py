from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from shelf_life.models import Product
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import JsonResponse
from .models import Comment
from .forms import CommentForm


def landing_redirect(request):
    return redirect('login')


@login_required
def landing(request):
    return render(request, 'shelf_life/landing.html')

def coming_soon(request):
    return render(request, 'shelf_life/coming_soon.html')

def guidelines(request):
    return render(request, 'shelf_life/guidelines.html')

def about(request):
    return render(request, 'shelf_life/about.html')

def donate(request):
    return render(request, 'shelf_life/donate.html')

def sources(request):
    return render(request, 'shelf_life/sources.html')

def resources(request):
    return render(request, 'shelf_life/resources.html')

def contact(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = CommentForm()

    return render(request, 'shelf_life/contact.html', {
        'form': form
    })


@login_required
def search(request):
    query = request.GET.get("q", "").strip()
    results = []

    if query:
        results = Product.objects.filter(item_name__icontains=query)

    return render(request, "shelf_life/search_results.html", {
        "query": query,
        "results": results,
    })


# @login_required
# def product_detail(request, product_id):
#     product = get_object_or_404(Product, pk=product_id)
#     came_from = request.GET.get('from', '')   # e.g. 'search' or 'baby_food'
#     query = request.GET.get('q', '')           # search query if any

#     context = {
#         'product': product,
#         'came_from': came_from,
#         'query': query,
#     }
#     return render(request, 'shelf_life/product_detail.html', context)
from datetime import timedelta, date
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Product

@login_required
def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    came_from = request.GET.get('from', '')
    query = request.GET.get('q', '')

    def get_shelf_life_data(label, lower, upper, note):
        if not lower and not upper:
            return None  # Skip if no shelf life data exists

        same = lower == upper
        cutoff = date.today() - timedelta(days=upper) if upper else None

        return {
            "label": label,
            "lower": lower,
            "upper": upper,
            "same": same,
            "cutoff": cutoff,
            "note": note,
        }

    shelf_lives = {
        "Baby Food": get_shelf_life_data("Baby Food", product.baby_food_lower, product.baby_food_upper, product.baby_food_note),
        "Shelf-Stable": get_shelf_life_data("Shelf-Stable", product.shelf_stable_lower, product.shelf_stable_upper, product.shelf_stable_note),
        "Refrigerated": get_shelf_life_data("Refrigerated", product.frig_lower, product.frig_upper, product.frig_note),
        "Frozen": get_shelf_life_data("Frozen", product.frozen_lower, product.frozen_upper, product.frozen_note),
    }

    context = {
        'product': product,
        'shelf_lives': shelf_lives,
        'came_from': came_from,
        'query': query,
    }
    return render(request, 'shelf_life/product_detail.html', context)


@login_required
def category_select(request):
    return render(request, "shelf_life/category_select.html")


@login_required
def baby_food_list(request):
    products = Product.objects.filter(baby_food_shelf_life__isnull=False).exclude(baby_food_shelf_life="").order_by("item_name")
    return render(request, "shelf_life/baby_food_list.html", {"products": products})


@login_required
def shelf_stable(request):
    return render(request, "shelf_life/shelf_stable.html")


@login_required
def dry_goods(request):
    dry_goods_subcategories = [
        "Baking",
        "Cereals & Grains",
        "Pasta & Noodles",
        "Snacks & Sweets",
        "Proteins & Legumes",
        "Prepared Mixes",
        "Bread & Baked Goods"
    ]
    return render(request, 'shelf_life/dry_goods.html', {'subcategories': dry_goods_subcategories})



@login_required
def shelf_stable_detail(request, subcategory):
    subcategory_map = {
        "canned-jarred": "Canned / Jarred",
        "aseptic": "Aseptic (Pouches)",
        "condiments-sauces-syrups": "Condiments / Sauces / Syrups",
        # add more as needed
    }
    
    display_name_map = {
        "canned-jarred": "Canned & Jarred",
        "aseptic": "Aseptic (Pouches)",
        "condiments-sauces-syrups": "Condiments, Sauces & Syrups",
    }

    subcategory_lower = subcategory.lower()
    
    if subcategory_lower in subcategory_map:
        category_name = subcategory_map[subcategory_lower]
        items = Product.objects.filter(shelf_stable_subcategory=category_name)
        template_name = "shelf_life/shelf_stable_category_detail.html"
        
        return render(request, template_name, {
            "category": category_name,
            "display_name": display_name_map[subcategory_lower],
            "items": items,
        })
    
    # handle other subcategories or 404
    return render(request, "404.html", status=404)


@login_required
def dry_goods_subcategories(request):
    subcategories = [
        {"slug": "baking", "name": "Baking"},
        {"slug": "cereals-grains", "name": "Cereals & Grains"},
        {"slug": "pasta-noodles", "name": "Pasta & Noodles"},
        {"slug": "snacks-sweets", "name": "Snacks & Sweets"},
        {"slug": "proteins-legumes", "name": "Proteins & Legumes"},
        {"slug": "prepared-mixes", "name": "Prepared Mixes"},
        {"slug": "bread-baked-goods", "name": "Bread & Baked Goods"},
    ]
    return render(request, 'shelf_life/dry_goods_subcategories.html', {'subcategories': subcategories})


@login_required
def dry_goods_category_detail(request, category_slug):
    categories = {
        "baking": "Baking and Cooking Ingredients",
        "cereals-grains": "Cereals & Grains",
        "pasta-noodles": "Pasta & Noodles",
        "snacks-sweets": "Snacks & Sweets",
        "proteins-legumes": "Proteins & Legumes",
        "prepared-mixes": "Prepared Mixes",
        "bread-baked-goods": "Bread & Baked Goods",
        "other-misc": "Miscellaneous",
    }

    category_items = {
        "baking": [
            "Baking mix, pancake",
            "Baking mixes (brownie, cake, muffin, pudding, etc.)",
            "Baking powder",
            "Baking soda",
            "Flour, corn",
            "Flour; potato, rice, white all-purpose",
            "Flour, self-rising",
            "Flour, whole wheat",
            "Cornmeal",
            "Shortening, vegetable",
            "Sugar, brown (light or dark)",
            "Sugar, confectioners",
            "Sugar; white",
            "Sugar substitute",
        ],
        "cereals-grains": [
            "Rice, brown",
            "Rice, white",
            "Rice-based mixes",
            "Oats; rolled/quick",
            "Oatmeal; instant",
            "Cereal, cold",
            "Cereal, hot",
        ],
        "pasta-noodles": [
            "Pasta, dry (egg noodles)",
            "Pasta, dry (no egg)",
            "Pasta; chickpea, lentil (gluten free)",
            "Macaroni and Cheese, mix",
        ],
        "snacks-sweets": [
            "Chips; potato, tortilla, veggie",
            "Cookies",
            "Cookie Mix",
            "Candy (all, including chocolate)",
            "Pretzels",
            "Popcorn, kernels",
            "Popcorn, commercially popped and bagged",
            "Popcorn, microwave packets",
            "Toaster pastries",
        ],
        "proteins-legumes": [
            "Beans, dried",
            "Nuts, out of shell",
            "Nuts, in shell",
            "Peanut Butter",
            "Jerky; animal and plant based",
        ],
        "prepared-mixes": [
            "Casserole Mix",
            "Stuffing mix",
            "Muffin Mix",
            "Potatoes, mashed, instant flakes",
            "Bouillon: beef or chicken",
            "Bouillon: vegetable",
        ],
        "bread-baked-goods": [
            "Bread, commercially prepared with preservatives (including rolls)",
            "Bread, fresh from bakery without preservatives",
            "Cakes, commercially prepared",
            "Crackers",
            "Taco shells",
            "Tortillas; corn, flour",
        ],
        "other-misc": [
            "Fruit, dried",
            "Masa flour",
            "Oil, olive, vegetable, salad",
            "Spices",
        ],
    }

    if category_slug not in categories:
        return render(request, '404.html', status=404)

    category_name = categories[category_slug]
    item_names = category_items.get(category_slug, [])

    items = Product.objects.filter(item_name__in=item_names)

    context = {
        'category': category_name,
        'items': items,
    }
    return render(request, 'shelf_life/dry_goods_category_detail.html', context)


@login_required
def ssb_categories(request):
    # Map slugs to display names
    ssb_categories = {
        "coffee": "Coffee",
        "tea": "Tea",
        "juice": "Juice",
        "milk": "Milk (shelf-stable)",
        "other": "Other"
    }
    return render(request, 'shelf_life/ssb_cat.html', {'ssb_categories': ssb_categories})


@login_required
def ssb_category_detail(request, category_slug):
    category_lower = category_slug.lower()
    items = Product.objects.filter(shelf_stable_subcategory="ssb")

    if category_lower == "other":
        filtered_items = [
            item for item in items
            if not any(x in item.item_name.lower() for x in ["milk", "juice", "coffee", "tea"])
        ]
    else:
        filtered_items = [
            item for item in items
            if category_lower in item.item_name.lower()
        ]

    template_name = "shelf_life/ssb_category_detail.html"  # single template for all categories

    return render(request, template_name, {
        "items": filtered_items,
        "category": category_slug.capitalize(),
    })


@login_required
def refrigerated_categories(request):
    categories = [
        ("dairy-cooler", "Dairy and Cooler Items"),
        ("cut-produce", "Cut Produce"),
        ("meats", "Meats"),
        ("prepared-foods", "Prepared Foods & Deli Items"),
    ]
    return render(request, "shelf_life/refrigerated_categories.html", {"categories": categories})


@login_required
def frozen_categories(request):
    # Empty for now
    categories = []
    return render(request, "shelf_life/frozen_categories.html", {"categories": categories})
