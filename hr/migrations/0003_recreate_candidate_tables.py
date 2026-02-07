from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0002_backup_and_recreate_tables'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShortlistedCandidate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shortlisted_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('notification_sent', models.BooleanField(default=False)),
                ('candidate', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hr.candidateapplication')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hr.jobpost')),
            ],
        ),
        migrations.CreateModel(
            name='SelectedCandidate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('selected_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('candidate', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hr.candidateapplication')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hr.jobpost')),
            ],
        ),
    ]
