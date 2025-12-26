from .models import Comment
from .models import Vote

class CommentService:
    def add(self, user, idea, text):
        # Yeni yorum ekler
        return Comment.objects.create(user=user, idea=idea, text=text)

    def list(self, idea):
        # Belirli bir fikre ait tüm yorumları listeler
        return Comment.objects.filter(idea=idea).order_by('-created_at')

    def delete(self, comment_id):
        # Belirli bir yorumu siler
        comment = Comment.objects.get(id=comment_id)
        comment.delete()
        return True


class VoteService:
    def add(self, user, idea):
        # Kullanıcı aynı fikre ikinci kez oy veremez
        vote, created = Vote.objects.get_or_create(user=user, idea=idea)
        return vote if created else None

    def count(self, idea):
        # Bir fikre ait toplam oy sayısı
        return Vote.objects.filter(idea=idea).count()