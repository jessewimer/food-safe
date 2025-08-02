from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from shelf_life.models import Product
from analytics.models import ProductView
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import JsonResponse
from .models import Comment
from .forms import CommentForm
from datetime import date, timedelta
from django.utils.timezone import now
from django.db.models import Count, Max

def landing_redirect(request):
    return redirect('login')


def get_client_ip(request):
    """Get the client's IP address from the request object."""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0]
    return request.META.get("REMOTE_ADDR")


@login_required
def landing(request):
    # --- 1. Most viewed products ---
    product_view_counts = (
        ProductView.objects.values("product")
        .annotate(view_count=Count("id"))
        .order_by("-view_count")
    )

    # --- 1. Most viewed products ---
    product_view_counts = (
        ProductView.objects.values("product")
        .annotate(view_count=Count("id"))
        .order_by("-view_count")
    )

    most_viewed_ids = [item["product"] for item in product_view_counts[:3]]
    most_viewed = Product.objects.filter(id__in=most_viewed_ids)
    most_viewed = sorted(most_viewed, key=lambda p: most_viewed_ids.index(p.id))

    print(f"Most viewed products: {most_viewed}")

    # --- 2. Recently viewed (unique, most recent first) ---
    user = request.user if request.user.is_authenticated else None
    ip = get_client_ip(request)

    recent_views_qs = (
        ProductView.objects.filter(user=user) if user else ProductView.objects.filter(ip_address=ip)
    ).order_by("-timestamp")

    seen = set()
    recent_product_ids = []

    for view in recent_views_qs:
        pid = view.product_id
        if pid not in seen:
            seen.add(pid)
            recent_product_ids.append(pid)
        if len(recent_product_ids) == 3:
            break

    # Maintain original ordering of recently_viewed based on recent_product_ids
    recently_viewed = list(Product.objects.filter(id__in=recent_product_ids))
    recently_viewed.sort(key=lambda p: recent_product_ids.index(p.id))

    print(f"Recently viewed: {recently_viewed}")

    context = {
        "most_viewed": most_viewed,
        "recently_viewed": recently_viewed,
    }
    return render(request, "shelf_life/landing.html", context)


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

# this is called from product_detail to get the client's IP address
def get_client_ip(request):
    """Get the client's IP address from the request object."""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0]
    return request.META.get("REMOTE_ADDR")

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    # --- Track the product view ---
    ip = get_client_ip(request)
    user = request.user if request.user.is_authenticated else None
    ProductView.objects.create(product=product, user=user, ip_address=ip, timestamp=now())
    # print(f"Product viewed: {product.item_name} by {user if user else 'Anonymous'} from IP {ip}")

    # --- Shelf life data logic ---
    def get_category_data(prefix, label):
        shelf_life_str = getattr(product, f"{prefix}_shelf_life", "") or ""
        shelf_life_str = shelf_life_str.strip()

        lower = getattr(product, f"{prefix}_lower", None)
        upper = getattr(product, f"{prefix}_upper", None)
        note = getattr(product, f"{prefix}_note", "") or ""
        note = note.strip()

        if not any([shelf_life_str, lower is not None, upper is not None, note]):
            return None

        same = False
        if lower is not None and upper is not None:
            same = (lower == upper)

        cutoff = None
        if upper is not None:
            cutoff = date.today() - timedelta(days=upper)

        return {
            "label": label,
            "shelf_life_str": shelf_life_str,
            "lower": lower,
            "upper": upper,
            "same": same,
            "cutoff": cutoff,
            "note": note,
        }

    shelf_lives = {}
    for prefix, label in [
        ("baby_food", "Baby Food"),
        ("shelf_stable", "Shelf Stable"),
        ("frig", "Refrigerated"),
        ("frozen", "Frozen"),
    ]:
        data = get_category_data(prefix, label)
        if data:
            shelf_lives[label] = data

    context = {
        "product": product,
        "shelf_lives": shelf_lives,
        "came_from": request.GET.get("from", ""),
        "query": request.GET.get("q", ""),
    }
    return render(request, "shelf_life/product_detail.html", context)


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
