
from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import Comment, Vote
from IdeaApp.models import Idea
from UserApp.models import User
import json

@method_decorator(csrf_exempt, name='dispatch')
class CommentView(View):
    def get(self, request, idea_id):
        try:
            idea = Idea.objects.get(IdeaID=idea_id)
            comments = Comment.objects.filter(idea=idea).order_by('-comment_date')
            data = [{
                "id": c.id, 
                "user": {"id": c.user.id, "userName": c.user.userName}, 
                "text": c.text, 
                "comment_date": c.comment_date
            } for c in comments]
            return JsonResponse(data, safe=False)
        except Idea.DoesNotExist:
            return JsonResponse({"error": "Idea not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    def post(self, request, idea_id):
        try:
            body = json.loads(request.body)
            idea = Idea.objects.get(IdeaID=idea_id)
            user = User.objects.get(id=body['user_id'])
            
            comment = Comment.objects.create(
                idea=idea,
                user=user,
                text=body['text']
            )
            return JsonResponse({
                "id": comment.id, 
                "text": comment.text,
                "user": {"id": user.id, "userName": user.userName},
                "comment_date": comment.comment_date
            })
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class VoteView(View):
    def post(self, request, idea_id):
        try:
            body = json.loads(request.body)
            idea = Idea.objects.get(IdeaID=idea_id)
            user = User.objects.get(id=body['user_id'])
            
            # Check if already voted
            existing_vote = Vote.objects.filter(idea=idea, user=user).first()
            if existing_vote:
                return JsonResponse({"status": "failed", "message": "Already voted"})
            
            vote = Vote.objects.create(idea=idea, user=user, value=1)
            
            # Update idea votes count
            idea.VotesCount = Vote.objects.filter(idea=idea).count()
            idea.save()
            
            return JsonResponse({"status": "success", "total_votes": idea.VotesCount})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)