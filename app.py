import streamlit as st
import json
import os
import re
from datetime import datetime

st.set_page_config(page_title="Smart Contact Manager", layout="wide")

DATA_FILE = "contacts.json"

# =========================
# Load & Save
# =========================
def load_contacts():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_contacts(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

contacts = load_contacts()

# =========================
# Validation
# =========================
def valid_email(email):
    return re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email)

def valid_phone(phone):
    return re.match(r'^\+?[0-9]{7,15}$', phone)

def is_duplicate(name, phone, email, exclude=None):
    for c in contacts:
        if exclude and c == exclude:
            continue
        if c["Name"].lower() == name.lower() or \
           c["Phone"] == phone or \
           c["Email"].lower() == email.lower():
            return True
    return False

# =========================
# Header
# =========================
st.title("📇 Smart Contact Manager")
st.caption("Clean & Professional Contact Management System")

tab1, tab2 = st.tabs(["➕ Add Contact", "👥 Contacts"])

# =====================================================
# ADD CONTACT
# =====================================================
with tab1:
    st.subheader("Add New Contact")

    name = st.text_input("Full Name")
    phone = st.text_input("Phone Number (+ optional)")
    email = st.text_input("Email")

    if st.button("Save Contact"):
        if not name.strip():
            st.warning("Full name is required.")
        elif not valid_phone(phone):
            st.warning("Phone must be 7–15 digits (optional +).")
        elif not valid_email(email):
            st.warning("Enter valid email.")
        elif is_duplicate(name, phone, email):
            st.warning("This contact already exists.")
        else:
            contacts.append({
                "Name": name.strip(),
                "Phone": phone,
                "Email": email,
                "Added": str(datetime.now())
            })
            save_contacts(contacts)
            st.success("Contact Added Successfully ✅")

            if st.button("Add Another Contact"):
                st.experimental_rerun()

# =====================================================
# CONTACT LIST
# =====================================================
with tab2:

    search = st.text_input("🔍 Search by name, phone, or email")

    sort_option = st.selectbox("Sort By", [
        "Name (A–Z)",
        "Name (Recently Added)",
        "Phone (Ascending)",
        "Phone (Descending)",
        "Email (Alphabetical)",
        "Email (By Domain)"
    ])

    filtered = contacts.copy()

    # Ranking search results to top
    if search:
        search_lower = search.lower()
        filtered.sort(
            key=lambda x: (
                search_lower not in x["Name"].lower() and
                search_lower not in x["Phone"] and
                search_lower not in x["Email"].lower()
            )
        )

    # Sorting logic
    if sort_option == "Name (A–Z)":
        filtered.sort(key=lambda x: x["Name"].lower())
    elif sort_option == "Name (Recently Added)":
        filtered.sort(key=lambda x: x["Added"], reverse=True)
    elif sort_option == "Phone (Ascending)":
        filtered.sort(key=lambda x: x["Phone"])
    elif sort_option == "Phone (Descending)":
        filtered.sort(key=lambda x: x["Phone"], reverse=True)
    elif sort_option == "Email (Alphabetical)":
        filtered.sort(key=lambda x: x["Email"].lower())
    elif sort_option == "Email (By Domain)":
        filtered.sort(key=lambda x: x["Email"].split("@")[-1])

    if not filtered:
        st.info("No contacts available.")
    else:
        st.subheader("Contact List")
        names = [c["Name"] for c in filtered]
        selected_name = st.selectbox("Select Contact", names)

        selected_contact = next(c for c in filtered if c["Name"] == selected_name)

        st.markdown("---")
        st.subheader("Edit / Delete Contact")

        new_name = st.text_input("Name", selected_contact["Name"])
        new_phone = st.text_input("Phone", selected_contact["Phone"])
        new_email = st.text_input("Email", selected_contact["Email"])

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Update Contact"):
                if not valid_phone(new_phone):
                    st.warning("Invalid phone.")
                elif not valid_email(new_email):
                    st.warning("Invalid email.")
                elif is_duplicate(new_name, new_phone, new_email, exclude=selected_contact):
                    st.warning("Duplicate contact exists.")
                else:
                    selected_contact["Name"] = new_name
                    selected_contact["Phone"] = new_phone
                    selected_contact["Email"] = new_email
                    save_contacts(contacts)
                    st.success("Contact Updated ✅")

        with col2:
            confirm = st.checkbox("Confirm Delete")
            if st.button("Delete Contact"):
                if confirm:
                    contacts.remove(selected_contact)
                    save_contacts(contacts)
                    st.success("Contact Deleted ✅")
                    st.experimental_rerun()
                else:
                    st.warning("Please confirm deletion.")
