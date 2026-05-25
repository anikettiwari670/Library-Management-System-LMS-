import streamlit as st

# ------------------------------
# INITIAL SETUP
# ------------------------------
st.set_page_config(
    page_title="BookVerse LMS",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------
# CUSTOM CSS
# ------------------------------
st.markdown("""
<style>
    .main { background-color: #f8f9fa; }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        background-color: #4A90D9;
        color: white;
        font-weight: bold;
        padding: 0.5rem;
        border: none;
    }
    .stButton>button:hover { background-color: #357ABD; }
    .book-card {
        background: white;
        border-radius: 10px;
        padding: 15px;
        margin: 8px 0;
        border-left: 5px solid #4A90D9;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .issued-card {
        border-left: 5px solid #E74C3C;
    }
    .available-badge {
        background: #2ECC71;
        color: white;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 12px;
    }
    .issued-badge {
        background: #E74C3C;
        color: white;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 12px;
    }
    .metric-card {
        background: white;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .login-container {
        max-width: 400px;
        margin: auto;
        padding: 2rem;
        background: white;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# ------------------------------
# SESSION STATE
# ------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "BookVerse" not in st.session_state:
    st.session_state.BookVerse = {
        "Fluent Python":                            {"Author": "Luciano Ramalho",   "Availability": True,  "Issued_to": None, "Genre": "Programming"},
        "Introduction to Machine Learning with Python": {"Author": "Sarah Guido",   "Availability": True,  "Issued_to": None, "Genre": "AI/ML"},
        "Deep Learning with Python":                {"Author": "Francois Chollet",  "Availability": True,  "Issued_to": None, "Genre": "AI/ML"},
        "Natural Language Understanding":           {"Author": "James Allen",       "Availability": True,  "Issued_to": None, "Genre": "AI/ML"},
        "Generative Deep Learning":                 {"Author": "David Foster",      "Availability": True,  "Issued_to": None, "Genre": "AI/ML"},
    }

if "history" not in st.session_state:
    st.session_state.history = []

USERNAME = "LMS_Admin$321"
PASSWORD = "BookVerse@Admin"


# ------------------------------
# LOGIN PAGE
# ------------------------------
def login_page():
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class='login-container'>
            <h2 style='text-align:center; color:#4A90D9;'>📚 BookVerse LMS</h2>
            <p style='text-align:center; color:gray;'>Library Management System</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        username = st.text_input("👤 Username")
        password = st.text_input("🔒 Password", type="password")

        if st.button("🔐 Login"):
            if username == USERNAME and password == PASSWORD:
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("❌ Invalid credentials. Please try again.")

        st.markdown("""
        <p style='text-align:center; color:gray; font-size:12px; margin-top:20px;'>
        Demo: LMS_Admin$321 / BookVerse@Admin
        </p>
        """, unsafe_allow_html=True)


# ------------------------------
# DASHBOARD METRICS
# ------------------------------
def show_metrics():
    BV = st.session_state.BookVerse
    total    = len(BV)
    available = sum(1 for b in BV.values() if b["Availability"])
    issued   = total - available

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📚 Total Books",     total)
    col2.metric("✅ Available",        available)
    col3.metric("📤 Issued",          issued)
    col4.metric("📋 Transactions",    len(st.session_state.history))


# ------------------------------
# MAIN MENU
# ------------------------------
def main_menu():
    BV = st.session_state.BookVerse

    # Sidebar
    with st.sidebar:
        st.markdown("## 📚 BookVerse LMS")
        st.markdown("---")
        menu = st.selectbox("📂 Navigate", [
            "🏠 Dashboard",
            "📖 View Books",
            "➕ Add a Book",
            "🗑️ Remove a Book",
            "📤 Issue a Book",
            "📥 Return a Book",
            "📘 Issued Books",
            "📋 Transaction History",
            "🚪 Logout"
        ])
        st.markdown("---")
        st.markdown(f"👤 **Admin:** LMS_Admin")
        st.markdown(f"📚 **Total Books:** {len(BV)}")

    # ── DASHBOARD ──────────────────────────────────────────
    if menu == "🏠 Dashboard":
        st.title("🏠 Dashboard")
        show_metrics()
        st.markdown("---")
        st.subheader("📚 Quick Book Overview")
        for title, details in BV.items():
            status_badge = "<span class='available-badge'>Available</span>" if details["Availability"] else f"<span class='issued-badge'>Issued to {details['Issued_to']}</span>"
            st.markdown(f"""
            <div class='book-card {"" if details["Availability"] else "issued-card"}'>
                <b>{title}</b> &nbsp;|&nbsp; ✍️ {details['Author']} &nbsp;|&nbsp; 
                🏷️ {details.get('Genre','General')} &nbsp;|&nbsp; {status_badge}
            </div>
            """, unsafe_allow_html=True)

    # ── VIEW BOOKS ─────────────────────────────────────────
    elif menu == "📖 View Books":
        st.title("📖 Book Catalog")
        show_metrics()
        st.markdown("---")

        search = st.text_input("🔍 Search books by title or author")
        genre_filter = st.selectbox("🏷️ Filter by Genre", ["All"] + list(set(b.get("Genre","General") for b in BV.values())))

        for title, details in BV.items():
            if search.lower() not in title.lower() and search.lower() not in details["Author"].lower():
                continue
            if genre_filter != "All" and details.get("Genre") != genre_filter:
                continue
            status_badge = "<span class='available-badge'>Available</span>" if details["Availability"] else f"<span class='issued-badge'>Issued to {details['Issued_to']}</span>"
            st.markdown(f"""
            <div class='book-card {"" if details["Availability"] else "issued-card"}'>
                <b>{title}</b> &nbsp;|&nbsp; ✍️ {details['Author']} &nbsp;|&nbsp;
                🏷️ {details.get('Genre','General')} &nbsp;|&nbsp; {status_badge}
            </div>
            """, unsafe_allow_html=True)

    # ── ADD BOOK ───────────────────────────────────────────
    elif menu == "➕ Add a Book":
        st.title("➕ Add a New Book")
        col1, col2 = st.columns(2)
        with col1:
            title  = st.text_input("📖 Book Title")
            author = st.text_input("✍️ Author Name")
        with col2:
            genre  = st.selectbox("🏷️ Genre", ["Programming", "AI/ML", "Data Science", "Mathematics", "General"])

        if st.button("➕ Add Book"):
            if not title or not author:
                st.warning("⚠️ Please fill in all fields.")
            elif title in BV:
                st.warning("⚠️ This book already exists.")
            else:
                BV[title] = {"Author": author, "Availability": True, "Issued_to": None, "Genre": genre}
                st.session_state.history.append(f"➕ Added: '{title}' by {author}")
                st.success(f"✅ '{title}' added successfully!")

    # ── REMOVE BOOK ────────────────────────────────────────
    elif menu == "🗑️ Remove a Book":
        st.title("🗑️ Remove a Book")
        book_list = list(BV.keys())
        selected  = st.selectbox("Select Book to Remove", book_list)

        if st.button("🗑️ Remove Book"):
            if not BV[selected]["Availability"]:
                st.error(f"❌ Cannot remove — '{selected}' is currently issued to {BV[selected]['Issued_to']}.")
            else:
                del BV[selected]
                st.session_state.history.append(f"🗑️ Removed: '{selected}'")
                st.success(f"✅ '{selected}' removed successfully!")

    # ── ISSUE BOOK ─────────────────────────────────────────
    elif menu == "📤 Issue a Book":
        st.title("📤 Issue a Book")
        available_books = [t for t, d in BV.items() if d["Availability"]]

        if not available_books:
            st.warning("⚠️ No books available to issue.")
        else:
            col1, col2 = st.columns(2)
            with col1:
                selected = st.selectbox("📖 Select Book", available_books)
            with col2:
                person = st.text_input("👤 Issued To (Name)")

            if st.button("📤 Issue Book"):
                if not person:
                    st.warning("⚠️ Please enter the person's name.")
                else:
                    BV[selected]["Availability"] = False
                    BV[selected]["Issued_to"]    = person
                    st.session_state.history.append(f"📤 Issued: '{selected}' → {person}")
                    st.success(f"✅ '{selected}' issued to {person}.")

    # ── RETURN BOOK ────────────────────────────────────────
    elif menu == "📥 Return a Book":
        st.title("📥 Return a Book")
        issued_books = [t for t, d in BV.items() if not d["Availability"]]

        if not issued_books:
            st.info("ℹ️ No books are currently issued.")
        else:
            selected = st.selectbox("📖 Select Book to Return", issued_books)
            st.info(f"📤 Currently issued to: **{BV[selected]['Issued_to']}**")

            if st.button("📥 Return Book"):
                person = BV[selected]["Issued_to"]
                BV[selected]["Availability"] = True
                BV[selected]["Issued_to"]    = None
                st.session_state.history.append(f"📥 Returned: '{selected}' ← {person}")
                st.success(f"✅ '{selected}' returned successfully!")

    # ── ISSUED BOOKS ───────────────────────────────────────
    elif menu == "📘 Issued Books":
        st.title("📘 Currently Issued Books")
        issued = [(t, d["Issued_to"]) for t, d in BV.items() if not d["Availability"]]

        if issued:
            for title, user in issued:
                st.markdown(f"""
                <div class='book-card issued-card'>
                    📖 <b>{title}</b> &nbsp;|&nbsp; 👤 Issued to: <b>{user}</b>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("ℹ️ No books are currently issued.")

    # ── TRANSACTION HISTORY ────────────────────────────────
    elif menu == "📋 Transaction History":
        st.title("📋 Transaction History")
        if st.session_state.history:
            for i, record in enumerate(reversed(st.session_state.history), 1):
                st.markdown(f"`{i}.` {record}")
        else:
            st.info("ℹ️ No transactions yet.")

    # ── LOGOUT ─────────────────────────────────────────────
    elif menu == "🚪 Logout":
        st.session_state.logged_in = False
        st.rerun()


# ------------------------------
# RUN APP
# ------------------------------
if not st.session_state.logged_in:
    login_page()
else:
    main_menu()
