import streamlit as st
from typing import List, Dict, Tuple
import hashlib
import re
import os
import smtplib
import ssl
import random
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

def send_verification_code(email: str, code: str) -> bool:
    subject = "LIU ChatBot - Email Verification Code"
    body = f"Your verification code is: {code}"

    sender_email = os.getenv("EMAIL_HOST_USER")
    sender_password = os.getenv("EMAIL_HOST_PASSWORD")

    # Debug log
    print("Using email:", sender_email)

    if not sender_email or not sender_password:
        print("❌ Missing email or password in environment variables.")
        return False

    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = email

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        print("✅ Email sent successfully")
        return True
    except smtplib.SMTPAuthenticationError as e:
        print("❌ Authentication failed:", e.smtp_error.decode())
        return False
    except Exception as e:
        print("❌ Other error:", str(e))
        return False

# Configure page
st.set_page_config(
    page_title="LIU ChatBot",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
def load_custom_css():
    """Load custom CSS for better UI styling"""
    st.markdown("""
        <style>
        
        
        /* Hide fullscreen button */
        div.stElementToolbar {
            display: none !important;
        }
        
        /* Improve chat message styling */
        .stChatMessage {
            border-radius: 10px;
            margin-bottom: 10px;
        }
        
        /* Style the main title */
        .main-title {
            text-align: center;
            color: #1f4e79;
            font-size: 2.5rem;
            margin-bottom: 20px;
        }
        
        /* Perfect Auth UI Styling - Compact Size */
        .auth-page {
            min-height: 100vh;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px 10px;
            display: block;
        }
        
        .auth-container {
            max-width: 320px;  /* Reduced from 420px */
            width: 100%;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            border-radius: 20px;  /* Slightly reduced from 24px */
            padding: 2rem 1.8rem;  /* Reduced from 3rem 2.5rem */
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1), 
                        0 0 0 1px rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            animation: slideUp 0.6s ease-out;
            margin-top: 10px;  /* Reduced from 20px */
            margin-bottom: 20px;  /* Reduced from 40px */
        }
        
        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .auth-logo {
            text-align: center;
            margin-bottom: 1.5rem;  /* Reduced from 2rem */
        }
        
        .auth-logo-circle {
            width: 60px;  /* Reduced from 80px */
            height: 60px;  /* Reduced from 80px */
            background: linear-gradient(135deg, #1f4e79 0%, #3a7bd5 100%);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 0.8rem;  /* Reduced from 1rem */
            box-shadow: 0 8px 20px rgba(31, 78, 121, 0.3);
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }
        
        .auth-logo-text {
            font-size: 2.2rem;  /* Reduced from 3rem */
            color: white;
            font-weight: bold;
        }
        
        .auth-title {
            text-align: center;
            color: #1f4e79;
            font-size: 1.5rem;  /* Reduced from 1.8rem */
            font-weight: 700;
            margin-bottom: 0.4rem;  /* Reduced from 0.5rem */
            background: linear-gradient(135deg, #1f4e79, #3a7bd5);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .auth-subtitle {
            text-align: center;
            color: #6c757d;
            font-size: 0.85rem;  /* Reduced from 0.95rem */
            margin-bottom: 1.5rem;  /* Reduced from 2rem */
            font-weight: 400;
        }
        
        /* Perfect Form Styling - Compact */
        .stTextInput > div > div > input {
            border: 2px solid #e9ecef !important;
            border-radius: 12px !important;  /* Reduced from 16px */
            padding: 12px 16px !important;  /* Reduced from 16px 20px */
            font-size: 14px !important;  /* Reduced from 16px */
            background: #f8f9fa !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05) !important;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #1f4e79 !important;
            background: white !important;
            box-shadow: 0 0 0 3px rgba(31, 78, 121, 0.1), 
                        0 4px 20px rgba(0, 0, 0, 0.1) !important;
            transform: translateY(-2px) !important;
        }
        
        .stTextInput > label {
            color: #495057 !important;
            font-weight: 600 !important;
            font-size: 13px !important;  /* Reduced from 14px */
            margin-bottom: 6px !important;  /* Reduced from 8px */
        }
        
        /* Perfect Button Styling for all buttons - Compact */
        .stButton > button, .stFormSubmitButton > button {
            background: linear-gradient(135deg, #1f4e79 0%, #3a7bd5 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 12px !important;  /* Reduced from 16px */
            padding: 12px 20px !important;  /* Reduced from 16px 24px */
            font-size: 14px !important;  /* Reduced from 16px */
            font-weight: 600 !important;
            width: 100% !important;
            margin: 6px 0 !important;  /* Reduced from 8px 0 */
            transition: all 0.3s ease !important;
            box-shadow: 0 8px 20px rgba(31, 78, 121, 0.3) !important;
            cursor: pointer !important;
            height: 48px !important;  /* Reduced from 60px */
        }
        
        .stButton > button:hover, .stFormSubmitButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 12px 25px rgba(31, 78, 121, 0.4) !important;
            background: linear-gradient(135deg, #1a4269 0%, #3571c4 100%) !important;
        }
        
        /* Secondary button styling for specific buttons */
        .stButton > button[kind="secondary"] {
            background: transparent !important;
            color: #6c757d !important;
            border: 2px solid #e9ecef !important;
        }
        
        .stButton > button[kind="secondary"]:hover {
            border-color: #1f4e79 !important;
            color: #1f4e79 !important;
            background: rgba(31, 78, 121, 0.05) !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 8px 20px rgba(31, 78, 121, 0.1) !important;
        }
        
        /* Form spacing - Compact */
        .auth-form-spacing {
            margin-bottom: 1rem;  /* Reduced from 1.5rem */
        }
        
        /* Divider - Compact */
        .auth-divider {
            text-align: center;
            margin: 1.2rem 0;  /* Reduced from 2rem 0 */
            position: relative;
            color: #6c757d;
            font-size: 13px;  /* Reduced from 14px */
        }
        
        .auth-divider::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 0;
            right: 0;
            height: 1px;
            background: linear-gradient(90deg, transparent, #e9ecef, transparent);
        }
        
        .auth-divider span {
            background: white;
            padding: 0 15px;  /* Reduced from 20px */
        }
        
        /* Success/Error messages */
        .stAlert {
            border-radius: 10px !important;  /* Reduced from 12px */
            border: none !important;
            margin: 0.8rem 0 !important;  /* Reduced from 1rem 0 */
        }
        
        .stSuccess {
            background: linear-gradient(90deg, #d4edda, #c3e6cb) !important;
            color: #155724 !important;
        }
        
        .stError {
            background: linear-gradient(90deg, #f8d7da, #f5c6cb) !important;
            color: #721c24 !important;
        }
        
        /* Demo info styling */
        .demo-info {
            background: linear-gradient(135deg, #e3f2fd, #bbdefb);
            border: none;
            border-radius: 12px;  /* Reduced from 16px */
            padding: 15px;  /* Reduced from 20px */
            margin-top: 1.5rem;  /* Reduced from 2rem */
            border-left: 4px solid #2196f3;
        }
        
        /* Style footer icons */
        .footer-icons a {
            margin: 0 5px;
            text-decoration: none;
        }
        
        .footer-icons img {
            transition: opacity 0.3s ease;
        }
        
        .footer-icons img:hover {
            opacity: 0.7;
        }
        
        /* Button styling */
        .stButton > button {
            border-radius: 20px;
            border: 2px solid #1f4e79;
            background-color: #1f4e79;
            color: white;
            font-weight: bold;
            transition: all 0.3s ease;
            width: 100%;
        }
        
        .stButton > button:hover {
            background-color: white;
            color: #1f4e79;
        }
        
        /* Welcome message styling */
        .welcome-user {
            background-color: #e8f4fd;
            padding: 10px;
            border-radius: 10px;
            border-left: 4px solid #1f4e79;
            margin-bottom: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

def initialize_session_state():
    """Initialize all session state variables"""
    session_vars = {
        "messages": [],
        "chat_history": [],
        "chat_history1": [],
        "chat_initialized": False,
        "authenticated": False,
        "username": "",
        "users": {},  # In production, use a proper database
        "current_page": "login"
    }
    
    for var, default_value in session_vars.items():
        if var not in st.session_state:
            st.session_state[var] = default_value

def hash_password(password: str) -> str:
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password: str) -> Tuple[bool, str]:
    """Validate password strength"""
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    if not re.search(r'[A-Za-z]', password):
        return False, "Password must contain at least one letter"
    if not re.search(r'\d', password):
        return False, "Password must contain at least one digit"
    return True, "Password is valid"

def register_user(username: str, email: str, password: str) -> Tuple[bool, str]:
    """Register a new user"""
    # Check if username already exists
    if username in st.session_state.users:
        return False, "Username already exists"
    
    # Check if email already exists
    for user_data in st.session_state.users.values():
        if user_data.get("email") == email:
            return False, "Email already registered"
    
    # Validate email
    if not validate_email(email):
        return False, "Invalid email format"
    
    # Validate password
    is_valid, message = validate_password(password)
    if not is_valid:
        return False, message
    
    # Register user
    st.session_state.users[username] = {
        "email": email,
        "password": hash_password(password),
        "created_at": st.session_state.get("current_time", "now")
    }
    
    return True, "Registration successful!"

def authenticate_user(username: str, password: str) -> Tuple[bool, str]:
    """Authenticate user login"""
    if username not in st.session_state.users:
        return False, "Username not found"
    
    stored_password = st.session_state.users[username]["password"]
    if hash_password(password) != stored_password:
        return False, "Incorrect password"
    
    return True, "Login successful!"

def login_page():
    """Display perfect login page"""
   
    
    # Logo and branding
    st.markdown('''
    <div class="auth-logo">
        <div class="auth-logo-circle">
            <div class="auth-logo-text">🎓</div>
        </div>
        <h1 class="auth-title">Welcome Back</h1>
        <p class="auth-subtitle">Sign in to your LIU ChatBot account</p>
    </div>
    ''', unsafe_allow_html=True)
    
    with st.form("login_form", clear_on_submit=False):
        st.markdown('<div class="auth-form-spacing">', unsafe_allow_html=True)
        username = st.text_input("Username", placeholder="Enter your username", key="login_username")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="auth-form-spacing">', unsafe_allow_html=True)
        password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_password")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Login button
        login_btn = st.form_submit_button("Sign In", use_container_width=True)
        
        if login_btn:
            if username and password:
                success, message = authenticate_user(username, password)
                if success:
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.session_state.current_page = "chat"
                    st.success("🎉 " + message)
                    st.balloons()
                    st.rerun()
                else:
                    st.error("❌ " + message)
            else:
                st.error("❌ Please fill in all fields")
    
    # Divider
    st.markdown('<div class="auth-divider"><span>or</span></div>', unsafe_allow_html=True)
    
    # Sign up button
    if st.button("Create New Account", key="goto_signup", use_container_width=True):
        st.session_state.current_page = "signup"
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    
    
    st.markdown('</div>', unsafe_allow_html=True)

def signup_page():
    """Display perfect signup page"""
   
    
    # Logo and branding
    st.markdown('''
    <div class="auth-logo">
        <div class="auth-logo-circle">
            <div class="auth-logo-text">🎓</div>
        </div>
        <h1 class="auth-title">Join LIU ChatBot</h1>
        <p class="auth-subtitle">Create your account to get started</p>
    </div>
    ''', unsafe_allow_html=True)
    
    with st.form("signup_form", clear_on_submit=False):
        st.markdown('<div class="auth-form-spacing">', unsafe_allow_html=True)
        username = st.text_input("Username", placeholder="Choose a unique username", key="signup_username")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="auth-form-spacing">', unsafe_allow_html=True)
        email = st.text_input("Email Address", placeholder="Enter your email address", key="signup_email")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="auth-form-spacing">', unsafe_allow_html=True)
        password = st.text_input("Password", type="password", placeholder="Create a strong password", key="signup_password")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="auth-form-spacing">', unsafe_allow_html=True)
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password", key="signup_confirm")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Create account button
        signup_btn = st.form_submit_button("Create Account", use_container_width=True)
        
        if signup_btn:
            if username and email and password and confirm_password:
                if password != confirm_password:
                    st.error("❌ Passwords do not match")
                else:
                    code = str(random.randint(100000, 999999))
                    st.session_state["pending_user"] = {
                        "username": username,
                        "email": email,
                        "password": password,
                        "code": code
                    }
                    if send_verification_code(email, code):
                        st.success("✅ Verification code sent to your email.")
                        st.session_state.current_page = "verify_email"
                        st.rerun()
                    else:
                        st.error("❌ Failed to send verification email.")


    
    # Divider
    st.markdown('<div class="auth-divider"><span>or</span></div>', unsafe_allow_html=True)
    
    # Back to login button
    if st.button("Already have an account? Sign In", key="goto_login", use_container_width=True):
        st.session_state.current_page = "login"
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

    
    st.markdown('</div>', unsafe_allow_html=True)


def email_verification_page():
    st.title("📧 Email Verification")

    code_input = st.text_input("Enter the verification code sent to your email")

    if st.button("Verify"):
        pending = st.session_state.get("pending_user", {})
        if code_input == pending.get("code"):
            success, msg = register_user(
                pending["username"],
                pending["email"],
                pending["password"]
            )
            if success:
                st.success("🎉 Email verified! You can now sign in.")
                st.session_state.current_page = "login"
                del st.session_state["pending_user"]
                st.rerun()
            else:
                st.error(msg)
        else:
            st.error("❌ Invalid code. Please try again.")

def logout():
    """Logout user and clear session"""
    st.session_state.authenticated = False
    st.session_state.username = ""
    st.session_state.messages = []
    st.session_state.chat_history = []
    st.session_state.chat_history1 = []
    st.session_state.current_page = "login"
    st.rerun()

def clear_chat_history():
    """Clear all chat-related session state"""
    st.session_state.messages = []
    st.session_state.chat_history = []
    st.session_state.chat_history1 = []
    st.rerun()

def display_chat_messages():
    """Display all chat messages from history"""
    for message_data in st.session_state.messages:
        with st.chat_message(message_data["role"]):
            st.markdown(message_data["content"])

def process_user_input(prompt: str) -> str:
    """Process user input and generate response"""
    try:
        # Import here to avoid issues if module is not available
        from Backend.rag2 import run_llm2
        
        # Add user message to session state
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.chat_history.append(("human", prompt))
        
        # Generate response
        with st.spinner("🤔 Thinking..."):
            generated_response = run_llm2(query=prompt)
        
        # Add assistant response to session state
        st.session_state.messages.append({"role": "assistant", "content": generated_response})
        st.session_state.chat_history.append(("ai", generated_response))
        
        return generated_response
        
    except ImportError:
        error_msg = "❌ Backend service is currently unavailable. Please try again later."
        st.session_state.messages.append({"role": "assistant", "content": error_msg})
        return error_msg
    except Exception as e:
        error_msg = f"❌ An error occurred: {str(e)}"
        st.session_state.messages.append({"role": "assistant", "content": error_msg})
        return error_msg

def create_sidebar():
    """Create and populate the sidebar for authenticated users"""
    with st.sidebar:
        # User info and logout
        st.markdown(f'<div class="welcome-user">👋 Welcome, <strong>{st.session_state.username}</strong>!</div>', 
                   unsafe_allow_html=True)
        
        if st.button("🚪 Logout", use_container_width=True):
            logout()
        
        st.markdown("---")
        
        # LIU Logo
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            try:
                st.image("img/LIU_Logo.png", width=150)
            except:
                st.write("🎓 LIU ChatBot")  # Fallback if image not found
        
        # Description
        st.markdown("---")
        st.write("**Confused about majors, fees, or admissions?**")
        st.write("LIU Chatbot has your back! 🚀")
        
        # Spacing
        st.markdown("<br>", unsafe_allow_html=True)
        
        # New Chat button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 New Chat", use_container_width=True, key="new_chat_btn"):
                clear_chat_history()
        
        # Chat statistics
        if st.session_state.messages:
            st.markdown("---")
            st.write("**Chat Stats:**")
            user_messages = len([msg for msg in st.session_state.messages if msg["role"] == "user"])
            st.write(f"Messages exchanged: {user_messages}")
        
        # Footer
        st.markdown("---")
        st.markdown("<br>" * 2, unsafe_allow_html=True)
        
        st.write("© 2025 LIU ChatBot. All rights reserved.")
        
        # Social media links
        st.markdown(
            """
            <div class="footer-icons">
            <p>
            <a href="#" target="_blank" title="GitHub">
                <img src="https://img.icons8.com/ios-glyphs/30/000000/github.png" alt="GitHub"/>
            </a>
            <a href="#" target="_blank" title="Telegram">
                <img src="https://img.icons8.com/ios-glyphs/30/000000/telegram-app.png" alt="Telegram"/>
            </a>
            <a href="#" target="_blank" title="Email">
                <img src="https://img.icons8.com/ios-glyphs/30/000000/email.png" alt="Email"/>
            </a>
            </p>
            </div>
            """,
            unsafe_allow_html=True
        )

def main_chat_interface():
    """Main chat interface for authenticated users"""
    # Title
    st.markdown('<h1 class="main-title">🎓 LIU ChatBot</h1>', unsafe_allow_html=True)
    
    # Welcome message for new users
    if not st.session_state.messages and not st.session_state.chat_initialized:
        st.info(f"👋 Welcome {st.session_state.username}! Ask me anything about LIU - majors, admissions, fees, campus life, and more!")
        st.session_state.chat_initialized = True
    
    # Display chat history
    display_chat_messages()
    
    # Chat input
    if prompt := st.chat_input("Ask anything about LIU...", key="chat_input"):
        # Display user message immediately
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Process and display response
        response = process_user_input(prompt)
        
        with st.chat_message("assistant"):
            st.markdown(response)

def main():
    """Main application function"""
    # Load custom CSS
    load_custom_css()
    
    # Initialize session state
    initialize_session_state()
    
    # Route to appropriate page based on authentication status
    if not st.session_state.authenticated:
        if st.session_state.current_page == "signup":
            signup_page()
        elif st.session_state.current_page == "verify_email":
            email_verification_page()
        else:
            login_page()

    else:
        # Create sidebar for authenticated users
        create_sidebar()
        
        # Main chat interface
        main_chat_interface()

if __name__ == "__main__":
    main()