from django.core.management.base import BaseCommand
from analytics.models import Visit
from datetime import datetime

# moscow ip: 50.52.111.94

class Command(BaseCommand):
    help = "Interactive menu to explore analytics data"

    def handle(self, *args, **kwargs):
        while True:
            print("\n📊 Analytics Menu:")
            print("1. View recent visits")
            print("2. Count total visits")
            print("3. Show today's visits")
            print("4. Exit")
            choice = input("Choose an option [1-4]: ").strip()

            if choice == "1":
                self.show_recent()
            elif choice == "2":
                self.count_visits()
            elif choice == "3":
                self.show_today()
            elif choice == "4":
                print("Exiting.")
                break
            else:
                print("Invalid choice. Please enter 1–4.")

    def show_recent(self, limit=100):
        visits = Visit.objects.order_by('-timestamp')[:limit]
        if not visits:
            print("No recent visits found.")
            return
        for visit in visits:
            print(f"{visit.timestamp} — {visit.ip_address} (session: {visit.session_key})")

    def count_visits(self):
        count = Visit.objects.count()
        print(f"Total visits recorded: {count}")

    def show_today(self):
        today = datetime.now().date()
        visits = Visit.objects.filter(timestamp__date=today)
        if not visits:
            print("No visits today.")
            return
        for visit in visits:
            print(f"{visit.timestamp} — {visit.ip_address}")
