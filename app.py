import streamlit as st
import json
import os
import re

FILE_NAME = "contacts.json"


# ---------------- FILE HANDLING ----------------

def load_contacts():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            contacts = json.load(file)

            # Fix old format automatically
            fixed = []
            for c in contacts:
                fixed.append({
                    "Name": c.get("Name", c.get("name", "")),
                    "Phone": c.get("Phone", c.get("phone", "")),
                    "Email": c.get("Email", c.get("email", ""))
                })
            return fixed

    return []


def save_contacts(contacts):
    contacts.sort(key=lambda x: x["Name"].lower())

    with open(FILE_NAME, "w") as file:
        json.dump(contacts, file, indent=4)


# ---------------- VALIDATION ----------------

def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)


def validate_phone(phone):
    phone = phone.replace(" ", "").replace("-", "")

    if phone.isdigit() and 7 <= len(phone) <= 15:
        return True
    return False


# ---------------- LOAD DATA ----------------

contacts = load_contacts()

if "page" not in st.session_state:
    st.session_state.page = "home"


# ---------------- HOME PAGE ----------------

if st.session_state.page == "home":

    st.title("📒 Contact Management App")

    st.button("+ New Contact", on_click=lambda:
              st.session_state.update(page="add"))

    st.subheader("All Contacts")

    if contacts:

        for c in contacts:
            st.write(
                f"**{c['Name']}** | {c['Phone']} | {c['Email']}")

    else:
        st.info("No contacts available")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Edit Contact"):
            st.session_state.page = "edit"

    with col2:
        if st.button("Delete Contact"):
            st.session_state.page = "delete"


# ---------------- ADD CONTACT ----------------

elif st.session_state.page == "add":

    st.title("➕ Add Contact")

    name = st.text_input("Name")
    phone = st.text_input("Phone")
    email = st.text_input("Email")

    duplicate = False

    if st.button("Save Contact"):

        if name == "" or phone == "" or email == "":
            st.warning("All fields required")

        elif not validate_phone(phone):
            st.warning("Invalid phone number")

        elif not validate_email(email):
            st.warning("Invalid email")

        else:

            for c in contacts:
                if c["Name"].lower() == name.lower():
                    st.warning("Name already exists")
                    duplicate = True
                    break

                if c["Phone"] == phone:
                    st.warning("Phone already exists")
                    duplicate = True
                    break

                if c["Email"].lower() == email.lower():
                    st.warning("Email already exists")
                    duplicate = True
                    break

            if duplicate == False:

                contacts.append({
                    "Name": name,
                    "Phone": phone,
                    "Email": email
                })

                save_contacts(contacts)

                st.success("Contact Added Successfully")


    col1, col2 = st.columns(2)

    with col1:
        if st.button("+ New Contact"):
            st.rerun()

    with col2:
        if st.button("⬅ Back"):
            st.session_state.page = "home"
            st.rerun()


# ---------------- EDIT CONTACT ----------------

elif st.session_state.page == "edit":

    st.title("✏ Edit Contact")

    if contacts:

        names = [c["Name"] for c in contacts]

        selected = st.selectbox(
            "Select Contact",
            names
        )

        contact = next(
            c for c in contacts if c["Name"] == selected)

        name = st.text_input("Name", contact["Name"])
        phone = st.text_input("Phone", contact["Phone"])
        email = st.text_input("Email", contact["Email"])

        if st.button("Update"):

            if name == "" or phone == "" or email == "":
                st.warning("All fields required")

            elif not validate_phone(phone):
                st.warning("Invalid phone")

            elif not validate_email(email):
                st.warning("Invalid email")

            else:

                contact["Name"] = name
                contact["Phone"] = phone
                contact["Email"] = email

                save_contacts(contacts)

                st.success("Contact Updated")

    else:
        st.info("No contacts available")

    if st.button("⬅ Back"):
        st.session_state.page = "home"
        st.rerun()


# ---------------- DELETE CONTACT ----------------

elif st.session_state.page == "delete":

    st.title("🗑 Delete Contact")

    if contacts:

        names = [c["Name"] for c in contacts]

        selected = st.selectbox(
            "Select Contact",
            names
        )

        if st.button("Delete"):

            contacts[:] = [
                c for c in contacts
                if c["Name"] != selected
            ]

            save_contacts(contacts)

            st.success("Contact Deleted")

    else:
        st.info("No contacts available")

    if st.button("⬅ Back"):
        st.session_state.page = "home"
        st.rerun()
