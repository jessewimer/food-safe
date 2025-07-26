from django.db import models

class Product(models.Model):
    item_name = models.CharField(max_length=255, unique=True)

    baby_food_shelf_life = models.CharField(max_length=100, blank=True)
    baby_food_subcategory = models.CharField(null=True, max_length=100, blank=True)
    baby_food_lower = models.IntegerField(null=True, blank=True)
    baby_food_upper = models.IntegerField(null=True, blank=True)
    baby_food_note = models.TextField(blank=True)

    shelf_stable_shelf_life = models.CharField(max_length=100, blank=True)
    shelf_stable_subcategory = models.CharField(null=True, max_length=100, blank=True)
    shelf_stable_lower = models.IntegerField(null=True, blank=True)
    shelf_stable_upper = models.IntegerField(null=True, blank=True)
    shelf_stable_note = models.TextField(blank=True)

    frig_shelf_life = models.CharField(max_length=100, blank=True)
    frig_subcategory = models.CharField(null=True, max_length=100, blank=True)
    frig_lower = models.IntegerField(null=True, blank=True)
    frig_upper = models.IntegerField(null=True, blank=True)
    frig_note = models.TextField(blank=True)

    frozen_shelf_life = models.CharField(max_length=100, blank=True)
    frozen_subcategory = models.CharField(null=True, max_length=100, blank=True)
    frozen_lower = models.IntegerField(null=True, blank=True)
    frozen_upper = models.IntegerField(null=True, blank=True)
    frozen_note = models.TextField(blank=True)

    tag = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return self.item_name


class Comment(models.Model):
    author_name = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=100, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']  # Show newest first
    
    def __str__(self):
        return f'Comment by {self.author_name} - {self.created_at}'