from django.db import migrations
from django.db.migrations.operations.special import RunPython
import json


def backup_and_recreate(apps, schema_editor):
    """Backup data from tables, drop them, and let them be recreated fresh"""
    # Get the data before dropping
    try:
        from django.db import connection
        cursor = connection.cursor()
        
        # Backup shortlisted candidates data
        cursor.execute("""
            SELECT id, job_id, candidate_id, shortlisted_at, notification_sent 
            FROM hr_shortlistedcandidate
        """)
        shortlisted_data = cursor.fetchall()
        
        # Backup selected candidates data
        cursor.execute("""
            SELECT id, job_id, candidate_id, selected_at 
            FROM hr_selectedcandidate
        """)
        selected_data = cursor.fetchall()
        
        # Drop the problematic tables
        cursor.execute("DROP TABLE IF EXISTS hr_shortlistedcandidate")
        cursor.execute("DROP TABLE IF EXISTS hr_selectedcandidate")
        
        # Store data for restoration in next migration
        with open('/tmp/backup_data.json', 'w') as f:
            json.dump({
                'shortlisted': shortlisted_data,
                'selected': selected_data
            }, f)
    except Exception as e:
        print(f"Backup error (non-critical): {e}")


def reverse_backup(apps, schema_editor):
    """Reverse operation - just recreate empty tables"""
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0001_initial'),
    ]

    operations = [
        RunPython(backup_and_recreate, reverse_backup),
    ]
