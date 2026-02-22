import streamlit as st
import re
import json
import os
from datetime import datetime

st.set_page_config(
    page_title="Smart Contact Manager",
    page_icon="📇",
    layout="wide"
)

DATA_FILE = "contacts.json"

# ----------------------------
# Load & Save
# ----------------------------
def load_contacts():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_contacts(contacts):
    with open(DATA_FILE, "w") as f:
        json.dump(contacts, f, indent=4)

contacts = load_contacts()

# ----------------------------
# Validation Functions
# ----------------------------
def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)

def is_valid_phone(phone):
    return phone.isdigit() and len(phone) >= 7

# ----------------------------
# Sidebar Navigation
# ----------------------------
st.sidebar.title("📁 Menu")
menu = st.sidebar.radio("Select Option", [
    "🏠 Dashboard",
    "➕ Add Contact",
    "🔍 Search Contact",
    "✏ Edit Contact",
    "🗑 Delete Contact",
    "📊 Sort Contacts"
])

# ----------------------------
# Dashboard
# ----------------------------
if menu == "🏠 Dashboard":
    st.title("📇 Smart Contact Manager")
    st.subheader("Professional Contact Management System")

    col1, col2 = st.columns(2)

    col1.metric("Total Contacts", len(contacts))
    col2.metric("Last Updated", datetime.now().strftime("%d %b %Y"))

    st.markdown("---")

    if contacts:
        st.dataframe(contacts, use_container_width=True)
    else:
        st.info("No contacts available yet.")

# ----------------------------
# Add Contact
# ----------------------------
elif menu == "➕ Add Contact":
    st.title("➕ Add New Contact")

    name = st.text_input("Full Name")
    phone = st.text_input("Phone Number")
    email = st.text_input("Email Address")

    if st.button("Save Contact"):
        if not name.strip():
            st.error("Please enter full name.")
        elif not is_valid_phone(phone):
            st.error("Enter valid phone number.")
        elif not is_valid_email(email):
            st.error("Enter valid email address.")
        else:
            contacts.append({
                "Name": name,
                "Phone": phone,
                "Email": email
            })
            save_contacts(contacts)
            st.success("Contact added successfully!")

# ----------------------------
# Search Contact
# ----------------------------
elif menu == "🔍 Search Contact":
    st.title("🔍 Search Contact")

    search_term = st.text_input("Enter name to search")

    if search_term:
        results = [
            c for c in contacts
            if search_term.lower() in c["Name"].lower()
        ]

        if results:
            st.dataframe(results, use_container_width=True)
        else:
            st.warning("No matching contact found.")

# ----------------------------
# Edit Contact
# ----------------------------
elif menu == "✏ Edit Contact":
    st.title("✏ Edit Contact")

    if not contacts:
        st.warning("No contacts available.")
    else:
        names = [c["Name"] for c in contacts]
        selected_name = st.selectbox("Select Contact", names)

        contact = next(c for c in contacts if c["Name"] == selected_name)

        new_name = st.text_input("Full Name", contact["Name"])
        new_phone = st.text_input("Phone", contact["Phone"])
        new_email = st.text_input("Email", contact["Email"])

        if st.button("Update Contact"):
            if not new_name.strip():
                st.error("Invalid name.")
            elif not is_valid_phone(new_phone):
                st.error("Invalid phone.")
            elif not is_valid_email(new_email):
                st.error("Invalid email.")
            else:
                contact["Name"] = new_name
                contact["Phone"] = new_phone
                contact["Email"] = new_email
                save_contacts(contacts)
                st.success("Contact updated!")

# ----------------------------
# Delete Contact
# ----------------------------
elif menu == "🗑 Delete Contact":
    st.title("🗑 Delete Contact")

    if not contacts:
        st.warning("No contacts available.")
    else:
        names = [c["Name"] for c in contacts]
        selected_name = st.selectbox("Select Contact", names)

        if st.button("Delete"):
            contacts = [c for c in contacts if c["Name"] != selected_name]
            save_contacts(contacts)
            st.success("Contact deleted!")

# ----------------------------
# Sort Contacts
# ----------------------------
elif menu == "📊 Sort Contacts":
    st.title("📊 Sort Contacts")

    if not contacts:
        st.warning("No contacts to be sorted.")
    else:
        sorted_contacts = sorted(contacts, key=lambda x: x["Name"])
        st.dataframe(sorted_contacts, use_container_width=True)
