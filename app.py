import streamlit as st

# ------------------------------
# INITIAL SETUP
# ------------------------------

st.set_page_config(page_title="Library Management System", page_icon="📚")

# Session state to store login status and BookVerse
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "BookVerse" not in st.session_state:
    st.session_state.BookVerse = {
        "Fluent Python": {"Author": "Luciano Ramalho", "Availability": True, "Issued_to": None},
        "Introduction to Machine Learning with Python": {"Author": "Sarah Guido", "Availability": True, "Issued_to": None},
        "Deep Learning with Python": {"Author": "Francois Chollet", "Availability": True, "Issued_to": None},
        "Natural Language Understanding": {"Author": "James Allen", "Availability": True, "Issued_to": None},
        "Generative Deep Learning": {"Author": "David Foster", "Availability": True, "Issued_to": None}
    }

# Default credentials
USERNAME = "LMS_Admin$321"
PASSWORD = "BookVerse@Admin"


# ------------------------------
# LOGIN PAGE
# ------------------------------
def login_page():
    st.title("📚 Library Management System (LMS)")

    st.subheader("🔐 Admin Login")
    username = st.text_input("Enter Username")
    password = st.text_input("Enter Password", type="password")

    if st.button("Login"):
        if username == USERNAME and password == PASSWORD:
            st.session_state.logged_in = True
            st.success("Access Granted!")
        else:
            st.error("Access Denied! Incorrect Username or Password.")


# ------------------------------
# MAIN MENU (AFTER LOGIN)
# ------------------------------
def main_menu():

    st.title("📖 LMS Dashboard")

    menu = st.sidebar.selectbox(
        "Menu Options",
        ["View Books", "Add a Book", "Issue a Book", "Return a Book", "View Issued Books", "Logout"]
    )

    BookVerse = st.session_state.BookVerse

    # ---------------- VIEW BOOKS ----------------
    if menu == "View Books":
        st.header("📚 Available Books")
        for title, details in BookVerse.items():
            status = "Available" if details["Availability"] else f"Issued to {details['Issued_to']}"
            st.write(f"**{title}** — {details['Author']} | `{status}`")

    # ---------------- ADD BOOK ----------------
    elif menu == "Add a Book":
        st.header("➕ Add a New Book")
        title = st.text_input("Enter Book Title")
        author = st.text_input("Enter Author Name")

        if st.button("Add Book"):
            if title in BookVerse:
                st.warning("This book already exists in BookVerse.")
            else:
                BookVerse[title] = {"Author": author, "Availability": True, "Issued_to": None}
                st.success(f"{title} has been added successfully!")

    # ---------------- ISSUE BOOK ----------------
    elif menu == "Issue a Book":
        st.header("📤 Issue a Book")
        book_list = list(BookVerse.keys())
        selected_book = st.selectbox("Select a Book", book_list)
        username = st.text_input("Enter the name of the person issuing the book")

        if st.button("Issue Book"):
            if BookVerse[selected_book]["Availability"]:
                BookVerse[selected_book]["Availability"] = False
                BookVerse[selected_book]["Issued_to"] = username
                st.success(f"{selected_book} has been issued to {username}.")
            else:
                st.error(f"{selected_book} is already issued to {BookVerse[selected_book]['Issued_to']}.")

    # ---------------- RETURN BOOK ----------------
    elif menu == "Return a Book":
        st.header("📥 Return a Book")
        book_list = list(BookVerse.keys())
        selected_book = st.selectbox("Select a Book", book_list)

        if st.button("Return Book"):
            if BookVerse[selected_book]["Availability"] == False:
                BookVerse[selected_book]["Availability"] = True
                BookVerse[selected_book]["Issued_to"] = None
                st.success(f"{selected_book} has been returned successfully!")
            else:
                st.warning("This book was not issued.")

    # ---------------- VIEW ISSUED BOOKS ----------------
    elif menu == "View Issued Books":
        st.header("📘 Issued Books")

        issued_books = [
            (title, details["Issued_to"])
            for title, details in BookVerse.items()
            if details["Availability"] == False
        ]

        if issued_books:
            for title, user in issued_books:
                st.write(f"**{title}** — issued to **{user}**")
        else:
            st.info("No books are currently issued.")

    # ---------------- LOGOUT ----------------
    elif menu == "Logout":
        st.session_state.logged_in = False
        st.success("Logged out successfully!")


# ------------------------------
# RUN THE APP
# ------------------------------
if not st.session_state.logged_in:
    login_page()
else:
    main_menu()
