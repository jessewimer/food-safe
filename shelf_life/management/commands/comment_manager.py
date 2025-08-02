# shelf_life/management/commands/comment_manager.py

from django.core.management.base import BaseCommand
from shelf_life.models import Comment

class Command(BaseCommand):
    help = "View or delete comments from the Comment table"

    def handle(self, *args, **kwargs):
        while True:
            print("\n📋 Comment Manager:")
            print("1. View recent comments")
            print("2. Delete a comment by ID")
            print("3. Exit")
            choice = input("Choose an option [1–3]: ").strip()

            if choice == "1":
                self.view_comments()
            elif choice == "2":
                self.delete_comment()
            elif choice == "3":
                print("Exiting.")
                break
            else:
                print("Invalid choice. Please enter 1–3.")

    def view_comments(self, limit=10):
        comments = Comment.objects.all()[:limit]
        if not comments:
            print("No comments found.")
            return
        for comment in comments:
            print("-" * 60)
            print(f"ID: {comment.id}")
            print(f"Author: {comment.author_name or '(anonymous)'}")
            print(f"City: {comment.city or '-'}")
            print(f"Email: {comment.email or '-'}")
            print(f"Date: {comment.created_at}")
            print("Content:")
            print(comment.content)
            print("-" * 60)

    def delete_comment(self):
        try:
            comment_id = int(input("Enter comment ID to delete: ").strip())
            comment = Comment.objects.get(id=comment_id)
            print(f"\nAre you sure you want to delete this comment?\n")
            print(f"{comment.created_at} by {comment.author_name}:\n{comment.content}\n")
            confirm = input("Type 'yes' to confirm: ").strip().lower()
            if confirm == 'yes':
                comment.delete()
                print("✅ Comment deleted.")
            else:
                print("Cancelled.")
        except Comment.DoesNotExist:
            print("⚠️ Comment not found.")
        except ValueError:
            print("❌ Invalid input.")
