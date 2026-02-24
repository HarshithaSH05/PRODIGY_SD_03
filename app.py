import streamlit as st
import json
import os
import re
import pandas as pd

FILE = "contacts.json"

# ---------- Load Contacts ----------
def load_contacts():
    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            return json.load(f)
    return []

# ---------- Save Contacts ----------
def save_contacts(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

contacts = load_contacts()

st.title("📇 Contact Management App")

# ---------- Session State ----------
if "page" not in st.session_state:
    st.session_state.page = "View"

# ---------- Navigation Buttons ----------
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("📋 View Contacts"):
        st.session_state.page = "View"

with col2:
    if st.button("+ New Contact"):
        st.session_state.page = "Add"
        st.session_state.name = ""
        st.session_state.phone = ""
        st.session_state.email = ""

with col3:
    if st.button("✏ Edit Contact"):
        st.session_state.page = "Edit"

with col4:
    if st.button("🗑 Delete Contact"):
        st.session_state.page = "Delete"


# ---------- VIEW CONTACTS ----------
if st.session_state.page == "View":

    st.subheader("All Contacts")

    if contacts:
        df = pd.DataFrame(contacts)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No contacts available")


# ---------- ADD CONTACT ----------
elif st.session_state.page == "Add":

    st.subheader("Add Contact")

    name = st.text_input("Name", key="name")
    phone = st.text_input("Phone Number", key="phone")
    email = st.text_input("Email", key="email")

    error = ""

    # ---------- ADD BUTTON ----------
    if st.button("Save Contact"):

        if not name or not phone or not email:
            error = "All fields required"

        elif not phone.isdigit() or len(phone) != 10:
            error = "Phone must be 10 digits"

        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            error = "Invalid Email"

        else:

            # Duplicate Check
            for c in contacts:

                if c["Name"].lower() == name.lower():
                    error = "Name already exists"

                if c["Phone"] == phone:
                    error = "Phone already exists"

                if c["Email"].lower() == email.lower():
                    error = "Email already exists"

            if error == "":
                contacts.append({
                    "Name": name,
                    "Phone": phone,
                    "Email": email
                })

                save_contacts(contacts)

                st.success("Contact Saved")

    if error:
        st.warning(error)


    # ---------- ADD ANOTHER CONTACT ----------
    if st.button("Add Another Contact"):

        st.session_state.name = ""
        st.session_state.phone = ""
        st.session_state.email = ""

        st.rerun()



# ---------- EDIT CONTACT ----------
elif st.session_state.page == "Edit":

    st.subheader("Edit Contact")

    if contacts:

        names = [c["Name"] for c in contacts]

        selected = st.selectbox(
            "Select Contact",
            names
        )

        contact = next(c for c in contacts if c["Name"] == selected)

        name = st.text_input("Name", contact["Name"])
        phone = st.text_input("Phone", contact["Phone"])
        email = st.text_input("Email", contact["Email"])

        if st.button("Update"):

            contact["Name"] = name
            contact["Phone"] = phone
            contact["Email"] = email

            save_contacts(contacts)

            st.success("Updated Successfully")

    else:
        st.info("No contacts available")


# ---------- DELETE CONTACT ----------
elif st.session_state.page == "Delete":

    st.subheader("Delete Contact")

    if contacts:

        names = [c["Name"] for c in contacts]

        selected = st.selectbox(
            "Select Contact",
            names
        )

        if st.button("Delete"):

            contacts = [c for c in contacts if c["Name"] != selected]

            save_contacts(contacts)

            st.success("Deleted Successfully")

    else:
        st.info("No contacts available")
