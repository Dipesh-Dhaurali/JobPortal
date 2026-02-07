from django.db import migrations
from django.db.migrations.operations.special import RunPython
import json


def restore_data(apps, schema_editor):
    """Restore the backed up data into the freshly created tables"""
    try:
        from django.db import connection
        cursor = connection.cursor()
        
        # Try to load backup data
        try:
            with open('/tmp/backup_data.json', 'r') as f:
                data = json.load(f)
                shortlisted_data = data.get('shortlisted', [])
                selected_data = data.get('selected', [])
        except:
            # If no backup file, skip restoration
            return
        
        # Restore shortlisted candidates
        for row in shortlisted_data:
            try:
                cursor.execute("""
                    INSERT INTO hr_shortlistedcandidate 
                    (id, job_id, candidate_id, shortlisted_at, notification_sent)
                    VALUES (?, ?, ?, ?, ?)
                """, row)
            except Exception as e:
                print(f"Error restoring shortlisted candidate: {e}")
        
        # Restore selected candidates
        for row in selected_data:
            try:
                cursor.execute("""
                    INSERT INTO hr_selectedcandidate 
                    (id, job_id, candidate_id, selected_at)
                    VALUES (?, ?, ?, ?)
                """, row)
            except Exception as e:
                print(f"Error restoring selected candidate: {e}")
                
    except Exception as e:
        print(f"Restoration error: {e}")


def reverse_restore(apps, schema_editor):
    """Reverse operation"""
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0003_recreate_candidate_tables'),
    ]

    operations = [
        RunPython(restore_data, reverse_restore),
    ]
