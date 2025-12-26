from .models import Category
from .models import Update

class CategoryService:

    def create(self, name, description=None):
        return Category.objects.create(name=name, description=description)

    def list(self):
        return Category.objects.all()

    def get(self, category_id):
        return Category.objects.get(id=category_id)

    def update(self, category_id, **kwargs):
        category = Category.objects.get(id=category_id)
        for key, value in kwargs.items():
            setattr(category, key, value)
        category.save()
        return category

    def delete(self, category_id):
        category = Category.objects.get(id=category_id)
        category.delete()
        return True


class UpdateService:
    def add(self, user, idea, text):
        # Yeni güncelleme ekler
        return Update.objects.create(user=user, idea=idea, update_text=text)

    def list(self, idea):
        # Belirli bir fikre ait tüm güncellemeleri listeler
        return Update.objects.filter(idea=idea).order_by('-created_at')