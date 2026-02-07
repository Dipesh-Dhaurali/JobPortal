from django.db import migrations

def fix_orphaned_fks(apps, schema_editor):
    """Set orphaned foreign keys to NULL instead of deleting records"""
    ShortlistedCandidate = apps.get_model('hr', 'ShortlistedCandidate')
    SelectedCandidate = apps.get_model('hr', 'SelectedCandidate')
    CandidateApplication = apps.get_model('hr', 'candidateApplication')
    
    # Get all valid candidate application IDs
    valid_ids = set(CandidateApplication.objects.values_list('id', flat=True))
    
    # Fix ShortlistedCandidate orphaned references
    for obj in ShortlistedCandidate.objects.all():
        if obj.candidate_id and obj.candidate_id not in valid_ids:
            obj.candidate_id = None
            obj.save()
    
    # Fix SelectedCandidate orphaned references
    for obj in SelectedCandidate.objects.all():
        if obj.candidate_id and obj.candidate_id not in valid_ids:
            obj.candidate_id = None
            obj.save()

def reverse_fix(apps, schema_editor):
    """Reverse operation - no action needed"""
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0002_alter_hrprofile_options_candidateapplication_and_more'),
    ]

    operations = [
        migrations.RunPython(fix_orphaned_fks, reverse_fix),
    ]
