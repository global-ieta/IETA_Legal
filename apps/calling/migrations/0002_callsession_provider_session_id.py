from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("calling", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="callsession",
            name="provider_session_id",
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
