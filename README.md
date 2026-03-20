<div align="center">

# 🚀 OpenWaitlist

### The open-source waitlist tool with referral system — self-hosted, free forever

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0+-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Stars](https://img.shields.io/github/stars/khaledxbenali92/openwaitlist?style=for-the-badge&color=yellow)](https://github.com/khaledxbenali92/openwaitlist/stargazers)

[Features](#-features) • [Demo](#-demo) • [Installation](#-installation) • [Usage](#-usage) • [Deploy](#-deploy) • [Contributing](#-contributing)

</div>

---

## 🎯 Why OpenWaitlist?

Every startup needs a waitlist. But existing tools charge $29-$99/month.

**OpenWaitlist** is:
- ✅ **Free forever** — self-hosted, no monthly fees
- ✅ **Privacy-first** — you own your data
- ✅ **Full-featured** — referrals, admin dashboard, email confirmations
- ✅ **Easy to deploy** — runs anywhere Python runs

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🎨 **Beautiful Landing Page** | Dark gradient design, mobile responsive |
| 📧 **Email Confirmation** | Double opt-in with HTML emails |
| 🔗 **Referral System** | Each referral moves user up 5 positions |
| 📊 **Admin Dashboard** | Manage subscribers, approve, export |
| 📥 **CSV Export** | Download your entire waitlist |
| 🔌 **REST API** | Embed widget on any website |
| 📍 **Position Tracking** | Real-time queue position display |
| 📨 **Email Blast** | Send announcements to all subscribers |
| 🔒 **Spam Protection** | IP tracking, duplicate prevention |
| 🌐 **UTM Tracking** | Track traffic sources |

---

## 🎬 Demo

**Landing Page:**
```
http://localhost:5000/
```

**Subscriber Status Page:**
```
http://localhost:5000/status/<token>
```

**Admin Dashboard:**
```
http://localhost:5000/admin/
Password: (set in .env)
```

**API:**
```bash
# Get stats
curl http://localhost:5000/api/stats

# Join via API
curl -X POST http://localhost:5000/api/join \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "name": "John"}'
```

---

## 🛠️ Installation

### Prerequisites
- Python 3.9+
- pip

### Step 1 — Clone

```bash
git clone https://github.com/khaledxbenali92/openwaitlist.git
cd openwaitlist
```

### Step 2 — Virtual environment

```bash
python -m venv venv

# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Configure

```bash
cp .env.example .env
```

Edit `.env`:

```env
SECRET_KEY=your-random-secret-key
APP_NAME=My Awesome App
APP_DESCRIPTION=Something amazing is coming. Be the first to know.
ADMIN_PASSWORD=your-secure-password

# Optional: Email (for confirmations)
MAIL_USERNAME=your@gmail.com
MAIL_PASSWORD=your-gmail-app-password
MAIL_DEFAULT_SENDER=noreply@yourapp.com
```

### Step 5 — Run

```bash
python app.py
```

Open: **http://localhost:5000** 🎉

---

## 📧 Email Setup (Optional)

Without email config, the app works in **demo mode** (no emails sent).

To enable emails with Gmail:

1. Enable 2FA on your Google account
2. Go to [App Passwords](https://myaccount.google.com/apppasswords)
3. Generate a password for "Mail"
4. Add to `.env`:

```env
MAIL_USERNAME=your@gmail.com
MAIL_PASSWORD=xxxx-xxxx-xxxx-xxxx
```

---

## 🚀 Deploy

### Deploy to Railway (Recommended — Free)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

Set environment variables in Railway dashboard.

### Deploy to Heroku

```bash
heroku create my-waitlist
heroku config:set SECRET_KEY=xxx APP_NAME="My App"
git push heroku main
```

### Deploy to VPS (Ubuntu)

```bash
# Install
sudo apt update && sudo apt install python3-pip nginx
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 "app:create_app()"
```

### Docker

```bash
docker build -t openwaitlist .
docker run -p 5000:5000 --env-file .env openwaitlist
```

---

## 🔌 Embed Widget

Add to any website:

```html
<form action="https://your-waitlist.com/api/join" method="POST">
  <input type="email" name="email" placeholder="Enter your email" required>
  <button type="submit">Join Waitlist</button>
</form>
```

Or via JavaScript:

```javascript
fetch('https://your-waitlist.com/api/join', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ email: 'user@example.com' })
})
.then(r => r.json())
.then(data => console.log(data));
```

---

## 📁 Project Structure

```
openwaitlist/
├── app.py                        # Flask app factory
├── src/
│   ├── config.py                 # Configuration
│   ├── models/
│   │   └── subscriber.py         # Database models
│   ├── routes/
│   │   ├── public.py             # Landing page & signup
│   │   ├── api.py                # REST API
│   │   └── admin.py              # Admin dashboard
│   └── services/
│       ├── waitlist_service.py   # Core business logic
│       └── email_service.py      # Email sending
├── frontend/
│   └── templates/
│       ├── index.html            # Landing page
│       ├── status.html           # Position page
│       ├── thank_you.html        # Confirmation page
│       ├── admin_dashboard.html  # Admin panel
│       └── admin_login.html      # Admin login
├── tests/
│   └── test_waitlist.py          # Test suite
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🧪 Running Tests

```bash
pip install pytest pytest-cov
pytest tests/ -v
pytest tests/ --cov=src --cov-report=term-missing
```

---

## 🗺️ Roadmap

- [x] Landing page with signup form
- [x] Email confirmation (double opt-in)
- [x] Referral system with position boost
- [x] Admin dashboard with stats
- [x] CSV export
- [x] REST API for embedding
- [x] UTM source tracking
- [ ] Multiple waitlist support
- [ ] Zapier / webhook integration
- [ ] Custom branding per waitlist
- [ ] Slack notifications on signup
- [ ] Analytics dashboard with charts
- [ ] One-click deploy to Vercel/Railway

---

## 🤝 Contributing

```bash
# Fork & clone
git clone https://github.com/YOUR-USERNAME/openwaitlist.git
cd openwaitlist

# Branch
git checkout -b feat/your-feature

# Develop + test
pytest tests/ -v

# Commit
git commit -m "feat: your feature"
git push origin feat/your-feature

# Open Pull Request
```

**Ideas for contributions:**
- 🎨 New landing page themes
- 🌍 i18n / translations
- 📊 Analytics charts
- 🔌 Webhook integrations
- 🐛 Bug fixes

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 👨‍💻 Author

**Khaled Ben Ali**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=flat&logo=linkedin)](https://linkedin.com/in/benalikhaled)
[![Twitter](https://img.shields.io/badge/Twitter-Follow-1DA1F2?style=flat&logo=twitter)](https://twitter.com/khaledbali92)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-333?style=flat&logo=github)](https://github.com/khaledxbenali92)

---

<div align="center">

⭐ **Star this repo if you're using it for your startup!** ⭐

*Built by founders, for founders.*

</div>
