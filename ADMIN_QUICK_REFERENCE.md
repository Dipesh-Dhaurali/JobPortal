# Admin Panel Quick Reference Guide

## Quick Access Links

```
Dashboard:           /admin/
User Management:     /admin/users/
Job Moderation:      /admin/jobs/
```

---

## Daily Admin Tasks

### Morning Check-In
1. **Visit Dashboard** (`/admin/`)
   - Check total user count
   - Review recent activity log
   - Note any pending moderation

2. **Check User Status**
   - Go to `/admin/users/`
   - Look for suspicious accounts
   - Review recently joined users

3. **Review Job Posts**
   - Go to `/admin/jobs/`
   - Check for spam or inappropriate listings
   - Verify company information accuracy

### When You Need To...

#### Suspend a User Account
1. Navigate to `/admin/users/`
2. Search for username or email
3. Click "Suspend" button
4. Enter reason for suspension
5. Click "Suspend User"
→ User cannot log in but account remains intact

#### Activate a Suspended User
1. Navigate to `/admin/users/`
2. Search for username
3. Click "Activate" button
4. Account is immediately reactivated
→ User can log in normally

#### Edit a Job Post
1. Go to `/admin/jobs/`
2. Search for job title or company
3. Click "Edit" on the job card
4. Modify desired fields:
   - Title
   - Location
   - Salary range
   - Employment type
   - Work mode
5. Click "Save Changes"
→ Changes take effect immediately

#### Delete a Job Post
1. Go to `/admin/jobs/`
2. Search for job
3. Click "Delete" button
4. Review warning about deleted applications
5. Click "Delete Permanently"
→ Job and all applications removed

#### View a Company Profile
1. Find a job posting from that company
2. Click "View HR Profile" button
OR
1. Go to `/admin/users/`
2. Find the HR account
3. Click "View Profile"
→ See company details, all jobs posted, and contact info

#### View a Candidate Profile
1. Go to `/admin/users/`
2. Search for candidate name
3. Click "View Profile"
→ See education, skills, languages, and all job applications

#### Search for Users
1. Go to `/admin/users/`
2. Use the search box (username or email)
3. Filter by type (HR/Candidate)
4. Click "Search"
→ Results displayed with actions

#### Search for Jobs
1. Go to `/admin/jobs/`
2. Use the search box (title or company)
3. Click "Search"
→ Results displayed with full job details

---

## Status Badges & What They Mean

### User Status
| Badge | Meaning | Action |
|-------|---------|--------|
| **Active** (Green) | User can log in and use platform | Monitor for issues |
| **Suspended** (Red) | User cannot log in | Review suspension reason |
| **Pending** (Yellow) | Account under review | Approve or reject |

### User Type
| Badge | Meaning | Profile |
|-------|---------|---------|
| **HR** (Blue) | Company recruiter | View posted jobs |
| **Candidate** (Pink) | Job seeker | View applications |

---

## Common Issues & Solutions

### Issue: Can't find a user
**Solution:**
- Check spelling of username
- Try searching by email instead
- Ensure user actually exists

### Issue: Job won't delete
**Solution:**
- Verify you have admin permissions
- Check if job post still has active applications
- Try refreshing the page and retry

### Issue: Suspended user showing as active
**Solution:**
- Check the UserStatus table
- Verify suspension was saved
- Try suspending again
- Check for database issues

### Issue: Can't edit job salary
**Solution:**
- Enter numbers only (no currency symbols)
- Ensure salary is positive
- Save with "Save Changes" button, not Enter key

---

## Activity Monitoring

### What Gets Logged
✓ User suspensions/activations
✓ Job post edits
✓ Job post deletions
✓ Profile views
✓ Admin actions

### How to View
- Check "Recent Activity" section on dashboard
- View timestamps and descriptions
- Identify which admin performed action

---

## Best Practices

### User Management
1. **Document Suspensions**: Always provide a clear reason
2. **Review First**: Check user profile before suspending
3. **Give Warnings**: Contact user before suspension if possible
4. **Log Everything**: System automatically tracks all actions

### Job Moderation
1. **Check Details**: Verify job information before deletion
2. **Contact HR**: Reach out about questionable posts
3. **Note Patterns**: Track which companies post spam
4. **Maintain Quality**: Delete low-quality or duplicate posts

### Account Security
1. Use strong, unique admin passwords
2. Don't share admin account access
3. Log out when leaving the computer
4. Review activity log regularly for suspicious actions
5. Report security concerns immediately

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `/` | Focus search box |
| `Esc` | Close dropdowns |
| `Enter` | Submit forms |

---

## Statistics Explained

### Dashboard Numbers

**Total Users**
- All registered accounts (HR + Candidates)
- Includes active, suspended, and pending

**HR Accounts**
- Company recruiters only
- Can post jobs and view applications

**Candidates**
- Job seekers
- Apply for jobs and build profiles

**Suspended Users**
- Accounts that cannot log in
- Should review reasons regularly

**Total Jobs**
- All job postings ever made
- Includes deleted jobs

**Total Applications**
- All job applications received
- Across all job posts

**Active Users**
- Users in good standing
- Can access platform normally

**Pending Jobs**
- Jobs awaiting moderation
- Only shows if approval system enabled

---

## Templates & Email

### Suspension Message Template
```
Dear [Username],

Your account has been suspended due to: [Reason]

This means:
- You cannot log in to the platform
- Your jobs/applications are hidden
- Contact support to appeal

Appeal Process:
[Contact information]
```

---

## Monthly Admin Checklist

- [ ] Review user growth statistics
- [ ] Check for inactive HR accounts
- [ ] Audit job post quality
- [ ] Review suspension decisions
- [ ] Check for spam patterns
- [ ] Update admin contact information
- [ ] Backup database
- [ ] Review admin activity log
- [ ] Test disaster recovery procedures

---

## Contact & Support

**Admin Issues?**
- Check ADMIN_SETUP.md for detailed guide
- Review ADMIN_IMPLEMENTATION_SUMMARY.md for full documentation
- Check Django admin interface for more details

**User Issues?**
- Search dashboard for user
- View their full profile
- Review their activity

**Platform Issues?**
- Check error logs
- Review recent admin activity
- Restart Django server
- Check database connection

---

## Tips & Tricks

### Speed Up Your Work
1. Use browser bookmarks for frequent pages
2. Search by partial username (e.g., "john" finds "john.doe")
3. Use Ctrl+F to find text on current page
4. Open profile links in new tab (Ctrl+Click)

### Bulk Operations
- Although not implemented, note candidates for future bulk suspend feature
- Document reasons for future automated filtering
- Track patterns for future reporting feature

### Data Protection
- Never share admin passwords
- Log out fully when done
- Clear browser cache if shared computer
- Use HTTPS only on production
- Enable 2FA when available

---

## Version Info
- Admin Panel Version: 1.0
- Django Version: 5.2.3
- Bootstrap Version: 5.3.3
- Last Updated: 2026-02-04

---

**Questions? Check the main documentation files or contact your development team.**
