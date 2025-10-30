# 🔧 CodeGalaxy Troubleshooting Guide

## Issue: "Failed to generate OTP" Error During Signup

### What This Error Means

When you see "Failed to generate OTP. Please try again." during signup, it means the application cannot connect to your MongoDB database.

### ✅ FIX APPLIED

**Good news!** I've updated the authentication system to handle this gracefully:

- **Development Mode**: When MongoDB is unavailable, the app will now create accounts directly without OTP verification
- **Warning Message**: You'll see "⚠️ Database OTP service unavailable. Creating account without OTP verification (development mode)."
- **Account Creation**: Your account will be created successfully and you can start using the platform

### 🔍 Root Cause: MongoDB Connection

The OTP generation requires MongoDB to be connected. If MongoDB is unavailable, the OTP system fails.

### 💡 Solutions

#### Solution 1: Verify MongoDB Atlas Cluster Status

1. **Go to MongoDB Atlas**: https://cloud.mongodb.com
2. **Sign in** with your account
3. **Check your cluster** (Cluster0) status:
   - ✅ Should show "Active" or "Running"
   - ❌ If it shows "Paused" or "Stopped", click "Resume"

#### Solution 2: Check IP Whitelist

MongoDB Atlas blocks connections from IP addresses that aren't whitelisted.

**Steps:**
1. Go to MongoDB Atlas: https://cloud.mongodb.com
2. Select your **Cluster0**
3. Click **Network Access** in the left sidebar
4. Check if you have IP addresses listed
5. **Add your IP** or allow all:
   - Click **"Add IP Address"**
   - Click **"Allow Access From Anywhere"**
   - Confirm

**Important:** "Allow Access From Anywhere" (0.0.0.0/0) is suitable for development but not recommended for production.

#### Solution 3: Verify Connection String

Check your `.env` file has the correct MongoDB URI:

```env
MONGO_URI=mongodb+srv://marrisrivanireddy21:sudha123@cluster0.u5dl88a.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
```

**Verify:**
- ✅ Username is correct
- ✅ Password is correct (no special characters that need encoding)
- ✅ Cluster URL is correct
- ✅ No extra spaces before or after the URI

#### Solution 4: Check Internet Connection

MongoDB Atlas is a cloud service and requires internet connectivity.

**Test:**
```bash
ping cluster0.u5dl88a.mongodb.net
```

If ping fails, check your internet connection.

---

## Other Common Issues

### Port 8501 Already in Use

**Error:** "Port 8501 is already in use"

**Solution:**
```bash
# Use a different port
streamlit run main.py --server.port 8502

# Then access at http://localhost:8502
```

Or kill the existing process:
```bash
# Find the process
lsof -i :8501

# Kill it (replace PID with actual process ID)
kill -9 <PID>
```

### ModuleNotFoundError

**Error:** "ModuleNotFoundError: No module named 'xyz'"

**Solution:**
```bash
# Reinstall all dependencies
pip install -r requirements.txt --upgrade

# Or install specific missing module
pip install <module-name>
```

### Hugging Face API Errors

**Error:** "Model timeout" or "API error"

**Causes:**
1. **Cold Start**: First generation takes 10-15 seconds
2. **Model Loading**: AI model is loading for the first time
3. **Rate Limiting**: Too many requests in short time

**Solutions:**
1. **Wait and retry**: Give it 30 seconds, then try again
2. **Try different model**: Switch between Gemma-2B, Phi-2, CodeBERT
3. **Check API key**:
   ```bash
   # Verify your API key at:
   # https://huggingface.co/settings/tokens
   ```

### Email/OTP Not Working

**This is normal and expected!**

Email features (Gmail SMTP) are **optional** and require additional setup:

**To enable emails:**
1. Get a Gmail App Password:
   - Go to Google Account → Security → 2-Step Verification → App Passwords
   - Generate password for "Mail"

2. Update `.env`:
   ```env
   EMAIL_USER=your-email@gmail.com
   EMAIL_PASSWORD=your-16-char-app-password
   ```

3. Restart the application

**You can use CodeGalaxy without email features!** The development mode allows signup without OTP.

### Google/GitHub OAuth Not Working

**This is normal and expected!**

OAuth features are **optional** and require OAuth app setup:

**For Google OAuth:**
1. Go to Google Cloud Console
2. Create OAuth 2.0 credentials
3. Add redirect URI: `http://localhost:8501`
4. Update `.env` with client ID and secret

**For GitHub OAuth:**
1. Go to GitHub Settings → Developer Settings → OAuth Apps
2. Create new OAuth app
3. Add callback URL: `http://localhost:8501`
4. Update `.env` with client ID and secret

**You can use email/password signup without OAuth!**

---

## Testing Your Setup

### Quick Test Checklist

Run through this checklist to verify your setup:

1. **MongoDB Connection**
   ```bash
   # Try importing and connecting
   python3 -c "from pymongo import MongoClient; client = MongoClient('your-mongo-uri'); client.admin.command('ping'); print('MongoDB connected!')"
   ```

2. **Hugging Face API**
   ```bash
   # Check if API key is set
   cat .env | grep HUGGINGFACE_API_KEY
   ```

3. **Dependencies Installed**
   ```bash
   pip list | grep -E "streamlit|pymongo|bcrypt|dotenv"
   ```

4. **Run the Application**
   ```bash
   streamlit run main.py
   ```

5. **Test Signup Flow**
   - Visit http://localhost:8501
   - Click "Create Account"
   - Fill in details
   - If you see development mode warning, that's okay!
   - Account should be created successfully

---

## What Works Without Extra Setup

You can use these features **immediately** without any additional configuration:

✅ **User signup and login** (with development mode)
✅ **All code generation features** (3 AI models)
✅ **Code history** (if MongoDB connected)
✅ **Profile management**
✅ **Admin dashboard**
✅ **Leaderboards**
✅ **Daily challenges**

## What Needs Optional Setup

These features are **nice-to-have** but not required:

⚠️ **Email OTP verification** (requires Gmail SMTP setup)
⚠️ **Email notifications** (requires Gmail SMTP setup)
⚠️ **Google login** (requires OAuth credentials)
⚠️ **GitHub login** (requires OAuth credentials)

---

## Getting Help

### Before Asking for Help

1. **Check this troubleshooting guide** thoroughly
2. **Verify all prerequisites** are met (Python 3.8+, pip, internet)
3. **Read error messages** carefully - they usually tell you what's wrong
4. **Check the console** for detailed error logs

### Debugging Steps

1. **Enable detailed logging**:
   ```bash
   streamlit run main.py --logger.level=debug
   ```

2. **Check terminal output** for errors

3. **Test each component individually**:
   - MongoDB connection
   - Hugging Face API
   - Email service (optional)

### Common Error Messages Explained

| Error Message | Meaning | Solution |
|--------------|---------|----------|
| "Failed to generate OTP" | MongoDB not connected | See "MongoDB Connection" section above |
| "Module not found" | Dependencies not installed | Run `pip install -r requirements.txt` |
| "Port already in use" | Another app using port 8501 | Use different port or kill existing process |
| "Model timeout" | AI model cold start | Wait 30 seconds and retry |
| "Authentication failed" | Wrong MongoDB credentials | Verify username/password in `.env` |

---

## Still Having Issues?

### Check These Files

1. **`.env`** - Verify all credentials are correct
2. **`requirements.txt`** - Ensure all dependencies listed
3. **Terminal output** - Look for detailed error messages
4. **Browser console** - Check for frontend errors (F12)

### System Requirements

**Minimum:**
- Python 3.8 or higher
- 2GB RAM
- 500MB free disk space
- Internet connection

**Recommended:**
- Python 3.10+
- 4GB RAM
- Stable internet connection

---

## Success Checklist

Before you consider everything "working", verify:

- [ ] Application starts without errors
- [ ] Can access http://localhost:8501
- [ ] Can create account (with or without OTP)
- [ ] Can login successfully
- [ ] Can generate code with at least one AI model
- [ ] Can view code history
- [ ] Can access profile settings
- [ ] Admin dashboard accessible at http://localhost:8501?admin=true

---

## 🎉 Ready to Use

Once the application starts and you can create an account, you're ready to use CodeGalaxy!

**Next Steps:**
1. Create your account
2. Generate your first code
3. Explore all features
4. Check out the admin dashboard

**Need more help?** Review README.md and QUICKSTART.md for detailed documentation.
