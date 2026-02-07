# Generated migration to clean up orphaned candidate records

from django.db import migrations

def delete_orphaned_records(apps, schema_editor):
    """Delete shortlisted and selected candidates that reference non-existent candidateApplication records"""
    ShortlistedCandidate = apps.get_model('hr', 'ShortlistedCandidate')
    SelectedCandidate = apps.get_model('hr', 'SelectedCandidate')
    
    # Delete orphaned shortlisted candidates
    ShortlistedCandidate.objects.filter(candidate_id__isnull=False).exclude(
        candidate_id__in=apps.get_model('hr', 'candidateApplication').objects.values_list('id', flat=True)
    ).delete()
    
    # Delete orphaned selected candidates
    SelectedCandidate.objects.filter(candidate_id__isnull=False).exclude(
        candidate_id__in=apps.get_model('hr', 'candidateApplication').objects.values_list('id', flat=True)
    ).delete()

def reverse_func(apps, schema_editor):
    """Reverse function - does nothing since we can't restore deleted data"""
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0003_alter_selectedcandidate_candidate_and_more'),
    ]

    operations = [
        migrations.RunPython(delete_orphaned_records, reverse_func),
    ]
