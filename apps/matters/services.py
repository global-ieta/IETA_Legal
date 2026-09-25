from .models import Matter, MatterAccess

def user_can_access_matter(user_id, matter):
    return matter.owner_id == user_id or MatterAccess.objects.filter(matter=matter, user_id=user_id).exists()
