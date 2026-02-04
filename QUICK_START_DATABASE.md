# Quick Start - Database Setup (2 Minutes)

## The Problem
Your database is empty - no users, companies, or jobs exist.

## The Solution
Run 3 commands to populate the database with realistic test data.

## Step-by-Step

### Step 1: Create New Model Migrations
```bash
python manage.py makemigrations authuser
python manage.py makemigrations admin_portal
```

### Step 2: Apply Migrations
```bash
python manage.py migrate
```

### Step 3: Populate Database
```bash
python manage_db.py
```

That's it! Your database now has:
- 1 Admin user
- 3 HR/Company accounts
- 5 Candidate accounts
- 4 Job postings
- 12+ Job applications

## Test Immediately

### Admin Login
```
URL: http://localhost:8000/admin_panel/
Username: admin_user
Password: admin123
```

### HR Login
```
URL: http://localhost:8000/hrdash/
Username: tech_company_hr
Password: hr@123456
```

### Candidate Login
```
URL: http://localhost:8000/candidate_dashboard/
Username: john_candidate
Password: candidate@123456
```

## What You'll See

✅ Admin Dashboard - Full platform statistics
✅ 3 Companies with their HR profiles
✅ 4 Job postings across companies
✅ 5 Candidates with complete profiles
✅ 12+ Job applications to manage
✅ Shortlist notifications
✅ Activity logs

## Detailed Credentials

| Role | Username | Password | Company/Position |
|------|----------|----------|-----------------|
| Admin | admin_user | admin123 | Admin |
| HR | tech_company_hr | hr@123456 | TechCorp Solutions |
| HR | finance_company_hr | hr@123456 | FinancePro Services |
| HR | health_company_hr | hr@123456 | HealthSystem Ltd |
| Candidate | john_candidate | candidate@123456 | Software Engineer |
| Candidate | sarah_designer | candidate@123456 | UI/UX Designer |
| Candidate | alex_marketer | candidate@123456 | Marketing Manager |
| Candidate | emma_developer | candidate@123456 | Full Stack Developer |
| Candidate | michael_analyst | candidate@123456 | Data Analyst |

## Troubleshooting

### Error: "django.core.exceptions.ImproperlyConfigured"
→ Run: `python manage.py migrate`

### Error: "No such table"
→ Run all 3 steps in order (makemigrations → migrate → populate)

### Error: "Duplicate key"
→ Run: `rm db.sqlite3` then redo all 3 steps

### No data appears in views
→ Verify Step 3 completed successfully (should show ✓ symbols)

## What's Inside the Database

### Companies
1. **TechCorp Solutions** - Technology/Startup (51-200 employees)
2. **FinancePro Services** - Finance/Private (201-500 employees)
3. **HealthSystem Ltd** - Healthcare/Private (501-1000 employees)

### Jobs
1. Senior Python Developer (Remote, $80k-$120k)
2. React Frontend Developer (Hybrid, $60k-$90k)
3. Financial Analyst (On-site, $55k-$80k)
4. Healthcare Administrator (On-site, $40k-$60k)

### Candidates
1. John Doe - 3 years software experience
2. Sarah Williams - 5 years design experience
3. Alex Brown - 2 years marketing experience
4. Emma Davis - Junior developer (currently studying)
5. Michael Garcia - 4 years data analysis experience

## Next Steps

1. ✅ Run the 3 setup commands above
2. ✅ Log in with admin credentials
3. ✅ View the admin dashboard
4. ✅ Check user management
5. ✅ View job moderation
6. ✅ Review candidate/HR profiles

## Files Involved

- `manage_db.py` - Does all the population work
- `init_database.sh` - Optional automated script
- `DATABASE_SETUP_INSTRUCTIONS.md` - Detailed guide
- `DATABASE_COMPLETE.md` - Technical overview

---

**Total Setup Time: 2-3 minutes**
**Database Size: ~1MB SQLite file**
**Status: Ready to use immediately after setup**
