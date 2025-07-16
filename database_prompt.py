import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "food_safe.settings")
django.setup()

from shelf_life.models import Product

def prompt(msg, cast=str, default=None):
    try:
        val = input(msg).strip()
        if not val:
            return default
        return cast(val)
    except (ValueError, TypeError):
        print("Invalid input.")
        return prompt(msg, cast, default)

def product_has_data(product):
    exclude_fields = {'id', 'item_name'}
    for field in product._meta.get_fields():
        if field.name not in exclude_fields:
            value = getattr(product, field.name)
            if value not in [None, '', 0]:  # Treat 0 as empty if it fits your logic
                return True
    return False

def fill_products():
    products = Product.objects.all().order_by("id")

    for product in products:
        if product_has_data(product):
            continue  # Skip this product if any data exists

        print("\n" + "="*50)
        print(f"[{product.id}] {product.item_name}")
        print("="*50)

        # Baby food
        is_baby = prompt("Is this baby food? (y/n): ", str)
        if is_baby and is_baby.lower().startswith("y"):
            product.baby_food_shelf_life = prompt("  Baby food shelf life: ")
            product.baby_food_subcategory = prompt("  Subcategory: ")
            product.baby_food_lower = prompt("  Lower bound (days): ", int)
            product.baby_food_upper = prompt("  Upper bound (days): ", int)
            product.baby_food_note = prompt("  Notes (optional): ") or ""

        # Shelf Stable
        is_shelf = prompt("Is it shelf stable? (y/n): ", str)
        if is_shelf and is_shelf.lower().startswith("y"):
            product.shelf_stable_shelf_life = prompt("  Shelf-stable shelf life: ")
            product.shelf_stable_subcategory = prompt("  Subcategory: ")
            product.shelf_stable_lower = prompt("  Lower bound (days): ", int)
            product.shelf_stable_upper = prompt("  Upper bound (days): ", int)
            product.shelf_stable_note = prompt("  Notes (optional): ") or ""

        # Refrigerated
        is_frig = prompt("Is it refrigerated? (y/n): ", str)
        if is_frig and is_frig.lower().startswith("y"):
            product.frig_shelf_life = prompt("  Refrigerated shelf life: ")
            product.frig_subcategory = prompt("  Subcategory: ")
            product.frig_lower = prompt("  Lower bound (days): ", int)
            product.frig_upper = prompt("  Upper bound (days): ", int)
            product.frig_note = prompt("  Notes (optional): ") or ""

        # Frozen
        is_frozen = prompt("Is it frozen? (y/n): ", str)
        if is_frozen and is_frozen.lower().startswith("y"):
            product.frozen_shelf_life = prompt("  Frozen shelf life: ")
            product.frozen_subcategory = prompt("  Subcategory: ")
            product.frozen_lower = prompt("  Lower bound (days): ", int)
            product.frozen_upper = prompt("  Upper bound (days): ", int)
            product.frozen_note = prompt("  Notes (optional): ") or ""

        product.save()
        print(f"✅ Saved: {product.item_name}")
def generate_secret_key():
    from django.core.management.utils import get_random_secret_key
    print(get_random_secret_key())

if __name__ == "__main__":
    fill_products()
    # generate_secret_key()