from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from apps.accounts.models import UserProfile
from apps.advocates.models import AdvocateProfile
from apps.consultations.models import ConflictCheck, Consultation
from apps.intake.models import IntakeRecord
from apps.matters.models import Matter
from apps.messaging.models import Conversation, Message
from apps.notifications.models import Notification


class Command(BaseCommand):
    help = "Create or refresh local workflow sample data."

    def handle(self, *args, **options):
        if not settings.DEMO_MODE:
            raise CommandError("seed_demo_workspace is disabled when DEMO_MODE=False")
        User = get_user_model()
        user, _ = User.objects.get_or_create(username="demo_user", defaults={"first_name": "IETA Member"})
        UserProfile.objects.update_or_create(user=user, defaults={"role": UserProfile.Roles.USER, "display_name": "IETA Member"})
        advocate_user, _ = User.objects.get_or_create(username="demo_advocate", defaults={"first_name": "Independent Advocate"})
        UserProfile.objects.update_or_create(user=advocate_user, defaults={"role": UserProfile.Roles.ADVOCATE, "display_name": "Independent Advocate"})
        advocate, _ = AdvocateProfile.objects.update_or_create(
            user=advocate_user,
            defaults={
                "display_name": "Independent Advocate",
                "practice_areas": ["Civil information intake", "Consultation preparation"],
                "jurisdictions": ["Jurisdiction to be confirmed"],
                "languages": ["English"],
                "consultation_modes": ["Video", "Audio"],
                "bio": "Professional profile information supplied for advocate discovery.",
                "verified": True,
                "available": True,
            },
        )
        matter, _ = Matter.objects.get_or_create(
            owner=user,
            title="Factual intake — consultation preparation",
            defaults={
                "summary": "Information organised by the account holder for consultation preparation.",
                "status": Matter.Status.CONSULTATION,
                "selected_advocate": advocate,
            },
        )
        matter.selected_advocate = advocate
        matter.status = Matter.Status.CONSULTATION
        matter.save(update_fields=["selected_advocate", "status", "updated_at"])
        IntakeRecord.objects.get_or_create(
            owner=user,
            matter=matter,
            defaults={
                "title": matter.title,
                "facts": "Information recorded by the account holder for consultation preparation.",
                "location": "To be confirmed",
                "status": IntakeRecord.Status.CONFIRMED,
            },
        )
        ConflictCheck.objects.update_or_create(
            matter=matter,
            advocate=advocate,
            defaults={"status": ConflictCheck.Status.CLEAR, "note": "Conflict review completed for this consultation request."},
        )
        consultation, _ = Consultation.objects.get_or_create(matter=matter, user=user, advocate=advocate, defaults={"status": Consultation.Status.CONFIRMED, "mode": "video"})
        consultation.status = Consultation.Status.CONFIRMED
        consultation.save(update_fields=["status", "updated_at"])
        conversation, _ = Conversation.objects.get_or_create(matter=matter, user=user, advocate=advocate)
        Message.objects.get_or_create(conversation=conversation, sender=advocate_user, body="This conversation is ready for authorised communication.")
        Notification.objects.get_or_create(recipient=user, kind="workspace", title="Workspace ready", defaults={"body": "A matter, consultation, message, and advocate profile are ready to review."})
        self.stdout.write(self.style.SUCCESS("Local workflow sample data is ready."))
        self.stdout.write("User: demo_user | Advocate: demo_advocate | Matter: Factual intake — consultation preparation")
