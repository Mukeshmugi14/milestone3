# CodeGalaxy 🚀🌌

**AI-Powered Code Generation Platform built with Streamlit**

CodeGalaxy is a visually stunning, feature-rich web application for AI-powered code generation, collaboration, and management. Built with Streamlit, it provides an intuitive interface inspired by modern platforms like Replit, Vercel, and Hugging Face Spaces.

## ✨ Features

### 🔐 Multi-Provider Authentication
- **Email/Password** with OTP verification
- **Google OAuth** integration
- **GitHub OAuth** integration
- Secure password hashing with bcrypt
- Session management and timeout

### ✨ AI Code Generation
- **3 AI Models** powered by Hugging Face:
  - **Gemma-2B**: General-purpose code generation
  - **Phi-2**: Fast and efficient for quick tasks
  - **CodeBERT**: Specialized in code analysis

- **Multiple Capabilities**:
  - Generate code from natural language descriptions
  - Explain existing code
  - Improve code for performance, readability, or security
  - Support for 8+ programming languages

### 📊 User Dashboard
Six comprehensive pages:
1. **Home**: Welcome dashboard with statistics and recent activity
2. **Generate Code**: AI-powered code generation with model selection
3. **History**: Search, filter, and manage generated code
4. **Profile**: User account management and settings
5. **Reviews**: Submit feedback and view community reviews
6. **Support**: FAQ and help documentation

### ⚙️ Admin Dashboard
Complete administrative control:
- **Analytics**: Platform statistics with interactive Plotly charts
- **User Management**: View, edit, suspend, and manage users
- **Review Moderation**: Approve, reject, or respond to user feedback
- **Model Monitoring**: Track AI model usage and performance
- **Activity Logs**: Audit trail of all system actions
- **Settings**: Platform configuration and management

### 🎯 Additional Features
- **Leaderboards**: Rank users by code generation, contributions, and model diversity
- **Daily Challenges**: AI-generated coding challenges with hints and solutions
- **Search**: Fuzzy search across code history and reviews
- **Email Notifications**: OTPs, welcome emails, weekly reports
- **Modern UI**: Glassmorphism design with dark/light theme support

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- MongoDB Atlas account (free tier available)
- Hugging Face API key
- Gmail account for SMTP (optional for email features)
- Google OAuth credentials (optional)
- GitHub OAuth credentials (optional)

### Setup

1. **Clone the repository**:
   ```bash
   cd milestone3
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**:
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your credentials:
   ```env
   # MongoDB
   MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/codegalaxy

   # Email (Gmail SMTP)
   EMAIL_USER=your-email@gmail.com
   EMAIL_PASSWORD=your-app-password

   # Hugging Face API
   HUGGINGFACE_API_KEY=hf_your_api_key_here

   # Admin
   ADMIN_PASSWORD=Infosys
   ADMIN_EMAIL=admin@codegalaxy.com

   # Optional: OAuth
   GOOGLE_CLIENT_ID=your-client-id
   GOOGLE_CLIENT_SECRET=your-client-secret
   GITHUB_CLIENT_ID=your-github-client-id
   GITHUB_CLIENT_SECRET=your-github-client-secret

   # App Settings
   APP_URL=http://localhost:8501
   SESSION_TIMEOUT=60
   ```

4. **Run the application**:
   ```bash
   streamlit run main.py
   ```

5. **Access the app**:
   - User Interface: `http://localhost:8501`
   - Admin Portal: `http://localhost:8501?admin=true`

## 📋 Configuration Guide

### MongoDB Atlas Setup
1. Create account at [mongodb.com](https://www.mongodb.com/)
2. Create a free M0 cluster
3. Create database named `codegalaxy`
4. Get connection string and add to `MONGO_URI`
5. Whitelist your IP address or use 0.0.0.0/0 for development

### Hugging Face API Setup
1. Create account at [huggingface.co](https://huggingface.co/)
2. Go to Settings → Access Tokens
3. Generate new token with read permissions
4. Add to `HUGGINGFACE_API_KEY` in .env

### Gmail SMTP Setup (for OTP emails)
1. Enable 2-factor authentication on your Gmail account
2. Generate an App Password:
   - Google Account → Security → 2-Step Verification → App Passwords
3. Select "Mail" and "Other (Custom name)"
4. Copy the 16-character password
5. Add your email and app password to .env

### Google OAuth Setup (Optional)
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create new project or select existing
3. Enable Google+ API
4. Go to Credentials → Create Credentials → OAuth 2.0 Client ID
5. Add authorized redirect URI: `http://localhost:8501`
6. Copy Client ID and Secret to .env

### GitHub OAuth Setup (Optional)
1. Go to GitHub Settings → Developer Settings → OAuth Apps
2. Click "New OAuth App"
3. Add authorization callback URL: `http://localhost:8501/oauth/github/callback`
4. Copy Client ID and Secret to .env

## 🎨 Project Structure

```
milestone3/
├── main.py                 # Streamlit entry point and routing
├── auth.py                 # Authentication (Email/OTP, OAuth)
├── user_dashboard.py       # User interface (6 pages)
├── admin_dashboard.py      # Admin portal (6 tabs)
├── ai_models.py            # AI model integration
├── database.py             # MongoDB operations
├── review_system.py        # Review submission and moderation
├── leaderboard.py          # Rankings and leaderboards
├── challenges.py           # Daily challenges
├── search.py               # Search functionality
├── ui_components.py        # Reusable UI components
├── utils.py                # Helper functions
├── email_service.py        # Email sending
├── requirements.txt        # Python dependencies
├── .env.example            # Example environment variables
├── .gitignore              # Git ignore rules
├── README.md               # This file
└── assets/
    ├── styles.css          # Custom CSS styles
    └── icons/              # Platform icons
```

## 🎯 Usage

### For Users

1. **Sign Up**: Create an account with email/OTP, Google, or GitHub
2. **Generate Code**:
   - Navigate to "Generate Code"
   - Select AI model (Gemma-2B, Phi-2, or CodeBERT)
   - Choose programming language
   - Describe what you want to build
   - Click "Generate Code"
3. **Manage History**: View, search, filter, and export your code history
4. **Submit Reviews**: Share feedback to help improve the platform
5. **Complete Challenges**: Try daily coding challenges to improve skills
6. **View Leaderboard**: See how you rank against other users

### For Admins

1. **Access Admin Portal**: Navigate to `http://localhost:8501?admin=true`
2. **Login**: Enter admin password (default: "Infosys" from .env)
3. **Analytics**: View platform statistics and charts
4. **User Management**: Manage users, suspend accounts, reset passwords
5. **Review Moderation**: Approve, reject, or respond to user reviews
6. **Monitor Models**: Track AI model usage and performance
7. **View Logs**: Audit trail of all platform activities
8. **Configure Settings**: Manage platform settings

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python 3.8+
- **Database**: MongoDB (Atlas)
- **AI Models**: Hugging Face Inference API
  - google/gemma-2b-it
  - microsoft/phi-2
  - microsoft/codebert-base
- **Authentication**: bcrypt, Google OAuth, GitHub OAuth
- **Email**: Gmail SMTP
- **Charts**: Plotly
- **Data Processing**: Pandas

## 📦 Dependencies

```
streamlit==1.30.0
pymongo==4.6.0
bcrypt==4.1.2
python-dotenv==1.0.0
google-auth==2.26.0
google-auth-oauthlib==1.2.0
PyGithub==2.1.1
huggingface-hub==0.20.0
plotly==5.18.0
pandas==2.1.4
streamlit-extras==0.3.6
```

## 🎨 Design Features

- **Glassmorphism UI**: Modern glass-effect cards with backdrop blur
- **Gradient Accents**: Purple-blue gradient theme throughout
- **Responsive Layout**: Works on desktop and mobile devices
- **Dark/Light Themes**: Toggle between theme modes
- **Smooth Animations**: CSS transitions and loading states
- **Custom Icons**: Emoji and icon-based navigation

## 🔒 Security Features

- **Password Hashing**: bcrypt with 12 salt rounds
- **OTP Verification**: 6-digit codes with 10-minute expiration
- **Session Management**: Secure session handling with timeouts
- **Input Sanitization**: Protection against injection attacks
- **Rate Limiting**: Prevent abuse of API endpoints
- **Audit Logging**: Track all administrative actions

## 📈 Performance

- **Model Response Times**: 2-10 seconds depending on complexity
- **Database Queries**: Indexed for fast lookups
- **Caching**: Session state caching for improved UX
- **Pagination**: Efficient loading of large datasets

## 🤝 Contributing

This is a demonstration project. For production use:
1. Add proper error handling
2. Implement rate limiting
3. Add comprehensive testing
4. Set up CI/CD pipeline
5. Configure production MongoDB
6. Add monitoring and logging
7. Implement proper OAuth callbacks

## 📝 License

MIT License - Feel free to use this project for learning and development.

## 🐛 Known Limitations

- **OAuth Integration**: Requires proper redirect URI configuration
- **Email Reports**: Weekly reports need external scheduler (cron)
- **Mobile UI**: Streamlit has limited mobile optimization
- **Real-time Updates**: No WebSocket support for live updates
- **CodeArena**: Marked as "Coming Soon" (collaborative feature)

## 🆘 Support

For issues, questions, or feature requests:
- Check the Support page within the app
- Review FAQ section
- Contact: support@codegalaxy.com (demo email)

## 🎉 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- AI models by [Hugging Face](https://huggingface.co/)
- Icons and emojis by Unicode Consortium
- Inspired by Replit, Vercel, and Hugging Face Spaces

---

**Made with ❤️ and AI - CodeGalaxy 🚀🌌**

*"Where code meets the cosmos!"*
