import streamlit as st
import json
import os
import re
from datetime import datetime

st.set_page_config(page_title="Smart Contact Manager", layout="wide")

DATA_FILE = "contacts.json"

# ==============================
# Styling (Purple → Blue SaaS)
# ==============================
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #6C63FF, #3A8DFF);
}

.header {
    background: linear-gradient(90deg, #6C63FF, #3A8DFF);
    padding: 25px;
    border-radius: 18px;
    color: white;
    text-align: center;
    margin-bottom: 30px;
}

.card {
    background: rgba(255,255,255,0.15);
    backdrop-filter: blur(12px);
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 15px;
    color: white;
}

.stButton>button {
    border-radius: 10px;
    font-weight: 600;
}

.stTextInput>div>div>input {
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# Utility Functions
# ==============================
def load_contacts():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_contacts(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def valid_email(email):
    return re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email)

def valid_phone(phone):
    return re.match(r'^\+?[0-9]{7,15}$', phone)

contacts = load_contacts()

# ==============================
# Header
# ==============================
st.markdown("""
<div class="header">
    <h1>📇 Smart Contact Manager</h1>
    <p>Modern SaaS Style Contact Management System</p>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "👥 Contacts", "➕ Add Contact"])

# ==============================
# Dashboard
# ==============================
with tab1:
    st.metric("Total Contacts", len(contacts))
    if contacts:
        st.write("Recently Added:")
        st.success(contacts[-1]["Name"])

# ==============================
# Add Contact
# ==============================
with tab3:
    st.subheader("Add New Contact")

    name = st.text_input("Full Name")
    phone = st.text_input("Phone Number (+Country Code)")
    email = st.text_input("Email Address")

    if st.button("Save Contact"):
        if not name.strip():
            st.warning("Please enter full name.")
        elif not valid_phone(phone):
            st.warning("Enter valid phone (7–15 digits, optional +).")
        elif not valid_email(email):
            st.warning("Enter valid email.")
        elif any(c["Phone"] == phone or c["Email"] == email for c in contacts):
            st.warning("Contact already exists.")
        else:
            contacts.append({
                "Name": name,
                "Phone": phone,
                "Email": email,
                "Added": str(datetime.now())
            })
            save_contacts(contacts)
            st.success("Contact Added Successfully ✅")
            st.button("Add Another Contact")

# ==============================
# Contacts (Search + Sort + Edit + Delete)
# ==============================
with tab2:
    st.subheader("Your Contacts")

    search = st.text_input("🔍 Search by name, phone, or email")

    sort_option = st.selectbox("Sort By", [
        "Name (A-Z)",
        "Name (Recently Added)",
        "Phone (Ascending)",
        "Phone (Descending)",
        "Email (Alphabetical)"
    ])

    filtered = contacts.copy()

    if search:
        filtered = [
            c for c in contacts
            if search.lower() in c["Name"].lower()
            or search in c["Phone"]
            or search.lower() in c["Email"].lower()
        ]

    if sort_option == "Name (A-Z)":
        filtered.sort(key=lambda x: x["Name"])
    elif sort_option == "Name (Recently Added)":
        filtered.sort(key=lambda x: x["Added"], reverse=True)
    elif sort_option == "Phone (Ascending)":
        filtered.sort(key=lambda x: x["Phone"])
    elif sort_option == "Phone (Descending)":
        filtered.sort(key=lambda x: x["Phone"], reverse=True)
    elif sort_option == "Email (Alphabetical)":
        filtered.sort(key=lambda x: x["Email"])

    if not filtered:
        st.info("No contacts found.")
    else:
        for idx, c in enumerate(filtered):
            st.markdown(f"""
            <div class="card">
                <b>{c['Name']}</b><br>
                📞 {c['Phone']}<br>
                📧 {c['Email']}
            </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns(2)

            # Edit
            if col1.button(f"Edit {idx}"):
                new_name = st.text_input("Edit Name", c["Name"], key=f"name{idx}")
                new_phone = st.text_input("Edit Phone", c["Phone"], key=f"phone{idx}")
                new_email = st.text_input("Edit Email", c["Email"], key=f"email{idx}")

                if st.button(f"Update {idx}"):
                    if valid_phone(new_phone) and valid_email(new_email):
                        c["Name"] = new_name
                        c["Phone"] = new_phone
                        c["Email"] = new_email
                        save_contacts(contacts)
                        st.success("Updated Successfully")
                    else:
                        st.warning("Invalid data.")

            # Delete with confirmation
            if col2.button(f"Delete {idx}"):
                confirm = st.checkbox("Confirm Delete", key=f"confirm{idx}")
                if confirm:
                    contacts.remove(c)
                    save_contacts(contacts)
                    st.success("Deleted Successfully")
