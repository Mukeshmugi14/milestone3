# 🚀 CodeGalaxy Quick Start Guide

Your credentials are already configured! Follow these simple steps to run the application.

## ✅ What's Already Set Up

- ✅ MongoDB Connection: Configured with your cluster
- ✅ Hugging Face API: Your API key is set
- ✅ All 18 Python modules: Complete and ready
- ✅ Admin Password: `Infosys` (you can change in .env)

## 📋 Prerequisites

Make sure you have:
- **Python 3.8+** installed ([Download here](https://www.python.org/downloads/))
- **pip** (comes with Python)
- Internet connection (for MongoDB Atlas and Hugging Face API)

## 🎯 Steps to Run

### Option 1: Automated Start (Recommended)

```bash
# Navigate to the project
cd milestone3

# Run the startup script
./start.sh
```

### Option 2: Manual Start

```bash
# Navigate to the project
cd milestone3

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run main.py
```

### Option 3: With Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # On Mac/Linux
# or
venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run main.py
```

## 🌐 Access Your Application

Once the app starts, you'll see:

```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

### Your Access Links:

- **👥 User Portal**: http://localhost:8501
- **👑 Admin Portal**: http://localhost:8501?admin=true

## 🔐 Login Credentials

### For Users (First Time):
1. Click "Create Account"
2. Fill in your details
3. Verify with OTP (Note: Email features require Gmail SMTP setup - optional)
4. Start generating code!

### For Admin:
1. Go to http://localhost:8501?admin=true
2. Enter password: `Infosys`
3. Access full admin dashboard

## 🎨 What You Can Do

### As a User:
- ✨ **Generate Code** with 3 AI models (Gemma-2B, Phi-2, CodeBERT)
- 📝 **Explain Code** - Paste code and get explanations
- ⚡ **Improve Code** - Get optimized versions
- 🕒 **View History** - Search and manage generated code
- 💬 **Submit Reviews** - Share feedback
- 🏆 **Check Leaderboard** - See rankings
- ⚡ **Daily Challenges** - Solve coding challenges

### As Admin:
- 📊 **Analytics Dashboard** - Platform statistics
- 👥 **User Management** - Manage all users
- 💬 **Review Moderation** - Approve/reject feedback
- 🤖 **Model Monitoring** - Track AI usage
- 📋 **Activity Logs** - Audit trail
- ⚙️ **Settings** - Configure platform

## 🔥 Quick Test

After starting the app:

1. **Create an account**:
   - Go to http://localhost:8501
   - Click "Create Account"
   - Enter details (OTP will be skipped if email not configured)

2. **Generate your first code**:
   - Navigate to "Generate Code"
   - Select "Gemma-2B" model
   - Choose "Python"
   - Enter: "Create a function to calculate fibonacci numbers"
   - Click "Generate Code"
   - Wait 5-10 seconds for AI response

3. **Try admin portal**:
   - Go to http://localhost:8501?admin=true
   - Password: `Infosys`
   - Explore analytics and user management

## ⚠️ Important Notes

### Email Features (Optional)
To enable OTP emails and notifications, update `.env`:
```env
EMAIL_USER=your-gmail@gmail.com
EMAIL_PASSWORD=your-gmail-app-password
```
Get Gmail app password: Google Account → Security → 2-Step Verification → App Passwords

### OAuth (Optional)
Google/GitHub login requires OAuth credentials. For now, use email signup.

### First Run
- First code generation may take 10-15 seconds (cold start)
- Database indexes are created automatically
- All collections are created on first use

## 🆘 Troubleshooting

### Port 8501 Already in Use
```bash
streamlit run main.py --server.port 8502
# Then access at http://localhost:8502
```

### Module Not Found
```bash
pip install -r requirements.txt --upgrade
```

### MongoDB Connection Error
- Check your internet connection
- Verify MongoDB Atlas cluster is running
- Confirm IP whitelist includes 0.0.0.0/0 or your IP

### Hugging Face API Error
- First generation might fail (cold start)
- Try again after 30 seconds
- Check API key is valid at https://huggingface.co/settings/tokens

## 📊 System Requirements

- **RAM**: 2GB minimum (4GB recommended)
- **Storage**: 500MB for dependencies
- **Internet**: Required (MongoDB Atlas + Hugging Face API)

## 🎉 You're All Set!

Run `./start.sh` or `streamlit run main.py` and start exploring CodeGalaxy! 🚀🌌

---

**Need Help?**
- Check README.md for detailed documentation
- Review error messages carefully
- Ensure all credentials in .env are correct

**Your Configuration:**
- ✅ MongoDB: Connected to Cluster0
- ✅ Hugging Face API: Key configured
- ✅ Admin Access: Password set to "Infosys"
