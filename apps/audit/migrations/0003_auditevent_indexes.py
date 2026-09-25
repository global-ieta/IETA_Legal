from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("audit", "0002_auditevent_request_id"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="auditevent",
            index=models.Index(fields=["-created_at"], name="audit_created_idx"),
        ),
        migrations.AddIndex(
            model_name="auditevent",
            index=models.Index(fields=["action", "-created_at"], name="audit_action_created_idx"),
        ),
        migrations.AddIndex(
            model_name="auditevent",
            index=models.Index(fields=["request_id"], name="audit_request_idx"),
        ),
    ]
