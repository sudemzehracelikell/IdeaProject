from django.views import View
from django.http import JsonResponse, Http404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
import logging
import sys

logger = logging.getLogger(__name__)

from IdeaApp.services import CategoryService, UpdateService
from UserApp.models import User
from .models import Idea, Status, Tag, Media, Category, Team

@method_decorator(csrf_exempt, name='dispatch')
class IdeaView(View):
    def get(self, request):
        ideas = Idea.objects.all()
        data = []
        for idea in ideas:
            data.append({
                "IdeaID": idea.IdeaID,
                "Title": idea.Title,
                "Description": idea.Description,
                "ShortDescription": idea.ShortDescription,
                "VotesCount": idea.VotesCount,
                "CreateDate": idea.CreateDate,
                "CreaterID": {
                    "id": idea.CreaterID.id,
                    "userName": idea.CreaterID.userName
                } if idea.CreaterID else None,
                "StatusID": {
                    "id": idea.StatusID.id,
                    "name": idea.StatusID.name
                } if idea.StatusID else None,
                "CategoryID": {
                    "id": idea.CategoryID.id,
                    "name": idea.CategoryID.name
                } if idea.CategoryID else None,
                "TeamID": {
                    "id": idea.TeamID.id,
                    "teamName": idea.TeamID.teamName
                } if idea.TeamID else None,
                "Tags": [{"TagID": tag.TagID, "TagName": tag.TagName} for tag in idea.Tags.all()],
                "CommentsCount": idea.comments.count()
            })
        return JsonResponse(data, safe=False)

    def post(self, request):
        try:
            body = json.loads(request.body)
            print(f"Received idea data: {body}")  # Debug log
            
            # Get user (CreaterID from frontend)
            user_id = body.get('CreaterID') or body.get('user_id')
            print(f"Looking for user with ID: {user_id}")  # Debug log
            
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                available_users = User.objects.all().values_list('id', 'userName')
                return JsonResponse({
                    "error": f"User with ID {user_id} does not exist. Available users: {list(available_users)}"
                }, status=400)
            
            # Get category (CategoryID from frontend)
            category_id = body.get('CategoryID') or body.get('category_id')
            category = Category.objects.get(id=category_id)
            
            # Get status (StatusID from frontend)
            status_id = body.get('StatusID') or body.get('status_id')
            status = Status.objects.get(id=status_id) if status_id else None
            
            # Get team (optional, TeamID from frontend)
            team_id = body.get('TeamID') or body.get('team_id')
            team = Team.objects.get(id=team_id) if team_id else None

            new_idea = Idea.objects.create(
                Title=body.get('Title') or body.get('title'),
                Description=body.get('Description') or body.get('description'),
                ShortDescription=body.get('ShortDescription') or body.get('short_description', ''),
                CreaterID=user,      
                CategoryID=category, 
                TeamID=team,       
                StatusID=status     
            )

            # Handle tags
            if 'Tags' in body and body['Tags']:
                for tag_data in body['Tags']:
                    tag_name = tag_data.get('TagName') if isinstance(tag_data, dict) else tag_data
                    tag, created = Tag.objects.get_or_create(TagName=tag_name)
                    new_idea.Tags.add(tag)
            elif 'tag_ids' in body:
                tags = Tag.objects.filter(TagID__in=body['tag_ids'])
                new_idea.Tags.set(tags)

            return JsonResponse({"message": "Idea added.", "IdeaID": new_idea.IdeaID}, status=201)
        except Exception as e:
            print(f"Error creating idea: {str(e)}")  # Debug log
            return JsonResponse({"error": str(e)}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class IdeaDetailView(View):
    def get(self, request, idea_id):
        try:
            idea = Idea.objects.get(IdeaID=idea_id)
            data = {
                "IdeaID": idea.IdeaID,
                "Title": idea.Title,
                "Description": idea.Description,
                "ShortDescription": idea.ShortDescription,
                "VotesCount": idea.VotesCount,
                "CreateDate": idea.CreateDate,
                "CreaterID": {
                    "id": idea.CreaterID.id,
                    "userName": idea.CreaterID.userName,
                    "email": idea.CreaterID.email
                } if idea.CreaterID else None,
                "StatusID": {
                    "id": idea.StatusID.id,
                    "name": idea.StatusID.name
                } if idea.StatusID else None,
                "CategoryID": {
                    "id": idea.CategoryID.id,
                    "name": idea.CategoryID.name
                } if idea.CategoryID else None,
                "TeamID": {
                    "id": idea.TeamID.id,
                    "teamName": idea.TeamID.teamName
                } if idea.TeamID else None,
                "Tags": [{"TagID": tag.TagID, "TagName": tag.TagName} for tag in idea.Tags.all()]
            }
            return JsonResponse(data)
        except Idea.DoesNotExist:
            return JsonResponse({"error": "Idea not found"}, status=404)

    def put(self, request, *args, **kwargs):
        idea_id = kwargs.get('idea_id')
        try:
            if not idea_id:
                return JsonResponse({"error": "No idea ID provided"}, status=400)
                
            idea = Idea.objects.get(IdeaID=idea_id)
            try:
                body = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid JSON"}, status=400)
            
            # log body for debug
            print(f"DEBUG PUT BODY: {body}", file=sys.stderr)

            # Update fields
            if 'Title' in body:
                idea.Title = body['Title']
            if 'Description' in body:
                idea.Description = body['Description']
            if 'ShortDescription' in body:
                idea.ShortDescription = body['ShortDescription']
            
            # Robust lookups
            if 'CategoryID' in body and body['CategoryID']:
                try:
                    idea.CategoryID = Category.objects.get(id=body['CategoryID'])
                except Category.DoesNotExist:
                     pass # or error?
            
            if 'StatusID' in body:
                if body['StatusID']:
                    try:
                        idea.StatusID = Status.objects.get(id=body['StatusID'])
                    except Status.DoesNotExist:
                        pass
                else:
                    idea.StatusID = None
            
            if 'TeamID' in body:
                if body['TeamID']:
                     try:
                         idea.TeamID = Team.objects.get(id=body['TeamID'])
                     except Team.DoesNotExist:
                         idea.TeamID = None
                else:
                    idea.TeamID = None
                
            idea.save()
            
            # Update tags
            if 'Tags' in body:
                idea.Tags.clear()
                # Ensure Tags is iterable
                tags_list = body['Tags']
                if tags_list:
                    for tag_data in tags_list:
                        tag_name = tag_data.get('TagName') if isinstance(tag_data, dict) else tag_data
                        if tag_name:
                             # Handle duplicates gracefully
                             existing_tag = Tag.objects.filter(TagName=tag_name).first()
                             if existing_tag:
                                 tag = existing_tag
                             else:
                                 tag = Tag.objects.create(TagName=tag_name)
                             idea.Tags.add(tag)
            
            return JsonResponse({"message": "Idea updated successfully"})
        except Idea.DoesNotExist:
            return JsonResponse({"error": "Idea not found"}, status=404)
        except Exception as e:
            # Log error to file for debugging
            try:
                with open('debug_error.log', 'a', encoding='utf-8') as f:
                    import traceback
                    f.write(f"Update Error: {str(e)}\nTraceback: {traceback.format_exc()}\nBody: {request.body}\n{'-'*20}\n")
            except Exception as log_err:
                print(f"Failed to write log: {log_err}", file=sys.stderr)
            
            logger.error(f"Internal Update Error: {e}", exc_info=True)
            return JsonResponse({"error": str(e)}, status=400)

    def delete(self, request, idea_id):
        try:
            idea = Idea.objects.get(IdeaID=idea_id)
            idea.delete()
            return JsonResponse({"message": "Idea deleted successfully"})
        except Idea.DoesNotExist:
            return JsonResponse({"error": "Idea not found"}, status=404)

@method_decorator(csrf_exempt, name='dispatch')
class StatusView(View):
    def get(self, request):
        statuses = Status.objects.all()
        data = [{"id": s.id, "name": s.name} for s in statuses]
        return JsonResponse(data, safe=False)

    def post(self, request):
        try:
            body = json.loads(request.body)
            new_status = Status.objects.create(name=body['name'])
            return JsonResponse({"message": "Status added.", "id": new_status.id}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
        
@method_decorator(csrf_exempt, name='dispatch')
class TagView(View):
    def get(self, request):
        tags = Tag.objects.all()
        data = [{"id": t.TagID, "name": t.TagName} for t in tags]
        return JsonResponse(data, safe=False)

    def post(self, request):
        try:
            body = json.loads(request.body)
            new_tag = Tag.objects.create(TagName=body['name'])
            return JsonResponse({"message": "Tag added.", "id": new_tag.TagID}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class MediaView(View):
    def get(self, request):
        medias = Media.objects.all()
        data = []
        for m in medias:
            data.append({
                "id": m.MediaID,
                "type": m.MediaType,
                "path": str(m.MediaPath),
                "idea": m.IdeaID.Title if m.IdeaID else "None"
            })
        return JsonResponse(data, safe=False)

    def post(self, request):
        try:
            body = json.loads(request.body)
            idea = Idea.objects.get(IdeaID=body['idea_id'])
            
            new_media = Media.objects.create(
                MediaType=body['type'],
                IdeaID=idea,
                MediaPath=body.get('path', 'default.jpg')
            )
            return JsonResponse({"message": "Media added.", "id": new_media.MediaID}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class CategoryListView(View):
    service = CategoryService()

    def get(self, request):
        categories = self.service.list()
        data = [{"id": c.id, "name": c.name, "description": c.description} for c in categories]
        return JsonResponse(data, safe=False)

    def post(self, request):
        body = json.loads(request.body)
        category = self.service.create(body['name'], body.get('description'))
        return JsonResponse({"id": category.id, "name": category.name})

@method_decorator(csrf_exempt, name='dispatch')
class UpdateView(View):
    service = UpdateService()

    def get(self, request, idea_id):
        idea = Idea.objects.get(IdeaID=idea_id)
        updates = self.service.list(idea)
        data = [{
            "id": u.id, 
            "description": u.description,
            "state": u.state,
            "created_at": u.created_at,
            "user": {"id": u.user.id, "userName": u.user.userName} if u.user else None
        } for u in updates]
        return JsonResponse(data, safe=False)

    def post(self, request, idea_id):
        body = json.loads(request.body)
        idea = Idea.objects.get(IdeaID=idea_id)
        user = User.objects.get(id=body['user_id'])
        update = self.service.add(user, idea, body['description'], body.get('state', 'IN_PROGRESS'))
        return JsonResponse({"id": update.id, "description": update.description})

