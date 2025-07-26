import os
import django
import sys

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_safe.settings')  # adjust if needed
django.setup()

from shelf_life.models import Comment, Product
from django.db import models


def view_comments():
    comments = Comment.objects.all()
    if not comments:
        print("\nNo comments found.\n")
        return

    while True:
        print("\n--- Comments ---")
        for idx, c in enumerate(comments, start=1):
            summary = c.content[:60].replace('\n', ' ') + ('...' if len(c.content) > 60 else '')
            print(f"{idx}) [{c.created_at.strftime('%Y-%m-%d')}] {c.author_name or 'Anonymous'} - {summary}")
        print("0) Back to main menu")

        try:
            choice = int(input("\nEnter comment number to view/delete, or 0 to go back: "))
        except ValueError:
            print("Invalid input.\n")
            continue

        if choice == 0:
            return
        if 1 <= choice <= len(comments):
            selected = comments[choice - 1]
            print("\n--- Full Comment ---")
            print(f"Author: {selected.author_name or 'Anonymous'}")
            print(f"City: {selected.city}")
            print(f"Email: {selected.email}")
            print(f"Date: {selected.created_at.strftime('%Y-%m-%d %H:%M')}")
            print(f"\n{selected.content}")
            print("-" * 40)
            confirm = input("Type 'delete' to delete this comment, or press Enter to go back: ").strip().lower()
            if confirm == 'delete':
                selected.delete()
                print("✅ Comment deleted.")
                comments = Comment.objects.all()  # Refresh the list
        else:
            print("Invalid selection.")



def view_or_edit_products():
    search = input("\nEnter product name or keyword to search: ").strip()
    if not search:
        print("No input provided.\n")
        return

    products = Product.objects.filter(item_name__icontains=search)
    if not products.exists():
        print(f"No products found for: '{search}'\n")
        return

    for idx, p in enumerate(products, start=1):
        print(f"{idx}) {p.item_name}")
    print("0) Cancel")

    try:
        choice = int(input("\nSelect product to view/edit (number): "))
    except ValueError:
        print("Invalid input.\n")
        return

    if choice == 0 or choice > len(products):
        return

    product = products[choice - 1]
    print(f"\nEditing: {product.item_name}")
    print("Press Enter to leave a field unchanged.\n")

    # Loop through all editable fields
    for field in Product._meta.get_fields():
        if isinstance(field, models.Field) and not field.auto_created:
            field_name = field.name
            old_val = getattr(product, field_name)
            new_val = input(f"{field_name} [{old_val}]: ").strip()

            if new_val != "":
                try:
                    if isinstance(field, models.IntegerField):
                        new_val = int(new_val)
                    setattr(product, field_name, new_val)
                except ValueError:
                    print(f"⚠️ Invalid value for {field_name}, keeping original.")

    product.save()
    print("✅ Product updated.\n")


def main_menu():
    while True:
        print("\n--- Admin Menu ---")
        print("1) View comments")
        print("2) View/edit products")
        print("0) Exit")

        choice = input("Select an option: ").strip()

        if choice == '1':
            view_comments()
        elif choice == '2':
            view_or_edit_products()
        elif choice == '0':
            print("Goodbye!")
            sys.exit()
        else:
            print("Invalid option.\n")


if __name__ == "__main__":
    main_menu()
