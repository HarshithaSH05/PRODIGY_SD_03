import streamlit as st
import json
import os
import re

FILE_NAME = "contacts.json"


# ---------- FILE HANDLING ----------

def load_contacts():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    return []


def save_contacts(contacts):
    contacts.sort(key=lambda x: x["name"].lower())
    with open(FILE_NAME, "w") as file:
        json.dump(contacts, file, indent=4)


# ---------- VALIDATION ----------

def validate_name(name):
    return name.strip() if name.strip() else None


def normalize_phone(phone):
    phone = phone.strip().replace(" ", "").replace("-", "")

    if phone.startswith("+"):
        digits = phone[1:]
        if digits.isdigit() and 7 <= len(digits) <= 15:
            return "+" + digits
    else:
        if phone.isdigit() and 7 <= len(phone) <= 15:
            return phone

    return None


def validate_email(email):
    email = email.strip().lower()
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return email if re.match(pattern, email) else None


def duplicate_exists(contacts, name, phone, email):

    for c in contacts:

        if c["name"].lower() == name.lower():
            return "Name already exists"

        if c["phone"] == phone:
            return "Phone already exists"

        if c["email"] == email:
            return "Email already exists"

    return None


# ---------- LOAD CONTACTS ----------

contacts = load_contacts()

st.set_page_config(
    page_title="Contact Manager",
    page_icon="📇",
    layout="wide"
)

st.title("📇 Contact Management System")


# ---------- SIDEBAR ----------

menu = st.sidebar.radio(
    "Menu",
    ["Add Contact", "View Contacts", "Search", "Edit Contact", "Delete Contact"]
)


# ---------- ADD CONTACT ----------

if menu == "Add Contact":

    st.subheader("Add New Contact")

    name = st.text_input("Name")

    phone = st.text_input("Phone (7-15 digits)")

    email = st.text_input("Email")


    col1,col2 = st.columns(2)


    if col1.button("Save Contact"):

        valid_name = validate_name(name)
        valid_phone = normalize_phone(phone)
        valid_email = validate_email(email)


        if not valid_name:
            st.error("Invalid name")

        elif not valid_phone:
            st.error("Phone must be 7–15 digits")

        elif not valid_email:
            st.error("Invalid email")

        else:

            duplicate = duplicate_exists(
                contacts,
                valid_name,
                valid_phone,
                valid_email
            )

            if duplicate:

                st.warning(duplicate)

            else:

                contacts.append({
                    "name":valid_name,
                    "phone":valid_phone,
                    "email":valid_email
                })

                save_contacts(contacts)

                st.success("Contact Added Successfully")


    if col2.button("Add Another Contact"):
        st.rerun()



# ---------- VIEW CONTACT ----------

elif menu == "View Contacts":

    st.subheader("All Contacts")

    if not contacts:

        st.warning("No contacts saved")

    else:

        contacts.sort(key=lambda x: x["name"].lower())

        for c in contacts:

            with st.container():

                col1,col2,col3 = st.columns([2,2,3])

                col1.markdown("### "+c["name"])
                col2.write("📞 "+c["phone"])
                col3.write("📧 "+c["email"])

                st.divider()



# ---------- SEARCH CONTACT ----------

elif menu == "Search":

    st.subheader("Search Contacts")

    keyword = st.text_input("Search by name / phone / email")


    if keyword:

        results = [

            c for c in contacts

            if keyword.lower() in c["name"].lower()
            or keyword in c["phone"]
            or keyword.lower() in c["email"]

        ]


        if results:

            for c in results:

                col1,col2,col3 = st.columns([2,2,3])

                col1.markdown("### "+c["name"])
                col2.write("📞 "+c["phone"])
                col3.write("📧 "+c["email"])

                st.divider()

        else:

            st.error("No matches found")



# ---------- EDIT CONTACT ----------

elif menu == "Edit Contact":

    st.subheader("Edit Contact")

    if not contacts:

        st.warning("No contacts available")

    else:

        search = st.text_input("Search contact")


        filtered = [

            c for c in contacts

            if search.lower() in c["name"].lower()
            or search in c["phone"]
            or search.lower() in c["email"]

        ] if search else contacts


        names = [

            c["name"]+" | "+c["phone"]

            for c in filtered

        ]


        selected = st.selectbox("Select Contact",names)


        index = names.index(selected)

        contact = filtered[index]


        new_name = st.text_input(
            "Name",
            contact["name"]
        )


        new_phone = st.text_input(
            "Phone",
            contact["phone"]
        )


        new_email = st.text_input(
            "Email",
            contact["email"]
        )


        if st.button("Update Contact"):

            valid_name = validate_name(new_name)
            valid_phone = normalize_phone(new_phone)
            valid_email = validate_email(new_email)


            if not valid_name:
                st.error("Invalid name")

            elif not valid_phone:
                st.error("Invalid phone")

            elif not valid_email:
                st.error("Invalid email")

            else:

                contact["name"]=valid_name
                contact["phone"]=valid_phone
                contact["email"]=valid_email

                save_contacts(contacts)

                st.success("Updated Successfully")



# ---------- DELETE CONTACT ----------

elif menu == "Delete Contact":

    st.subheader("Delete Contact")


    if not contacts:

        st.warning("No contacts available")

    else:

        search = st.text_input("Search contact")


        filtered = [

            c for c in contacts

            if search.lower() in c["name"].lower()
            or search in c["phone"]
            or search.lower() in c["email"]

        ] if search else contacts


        names = [

            c["name"]+" | "+c["phone"]

            for c in filtered

        ]


        selected = st.selectbox("Select Contact",names)


        index = names.index(selected)

        contact = filtered[index]


        confirm = st.checkbox("Confirm Delete")


        if st.button("Delete"):

            if confirm:

                contacts.remove(contact)

                save_contacts(contacts)

                st.success("Deleted Successfully")

            else:

                st.warning("Please confirm deletion")
