import streamlit as st
import json
import os
import re

FILE_NAME = "contacts.json"


# ---------- FILE ----------

def load_contacts():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as f:
            return json.load(f)
    return []


def save_contacts(contacts):
    contacts.sort(key=lambda x: x["name"].lower())
    with open(FILE_NAME, "w") as f:
        json.dump(contacts, f, indent=4)


# ---------- VALIDATION ----------

def validate_name(name):
    return name.strip() if name.strip() else None


def normalize_phone(phone):

    phone = phone.strip().replace(" ", "").replace("-", "")

    if phone.startswith("+"):
        digits = phone[1:]
        if digits.isdigit() and 7 <= len(digits) <= 15:
            return "+" + digits

    elif phone.isdigit() and 7 <= len(phone) <= 15:
        return phone

    return None


def validate_email(email):

    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    email=email.strip().lower()

    if re.match(pattern,email):
        return email

    return None


# ---------- LOAD ----------

contacts=load_contacts()

st.set_page_config(
    page_title="Contact Manager",
    layout="wide"
)

st.title("📇 Contact Manager")


menu=st.sidebar.radio(
    "Menu",
    ["Add Contact","View Contacts","Search","Edit Contact","Delete Contact"]
)


# ---------- ADD ----------

if menu=="Add Contact":

    st.subheader("Add Contact")

    if "reset" not in st.session_state:
        st.session_state.reset=False

    if st.session_state.reset:
        st.session_state.reset=False


    name=st.text_input("Name")

    phone=st.text_input("Phone (7-15 digits)")

    email=st.text_input("Email")


    col1,col2=st.columns(2)


    if col1.button("Save"):

        n=validate_name(name)
        p=normalize_phone(phone)
        e=validate_email(email)

        if not n:
            st.error("Invalid Name")

        elif not p:
            st.error("Phone must be 7-15 digits")

        elif not e:
            st.error("Invalid Email")

        else:

            contacts.append({
                "name":n,
                "phone":p,
                "email":e
            })

            save_contacts(contacts)

            st.success("Saved Successfully")


    if col2.button("+ New Contact"):

        st.session_state.reset=True
        st.rerun()


# ---------- VIEW ----------

elif menu=="View Contacts":

    st.subheader("All Contacts")

    if not contacts:

        st.warning("No contacts saved")

    else:

        contacts.sort(key=lambda x:x["name"].lower())

        for c in contacts:

            col1,col2,col3=st.columns([2,2,3])

            col1.write("**"+c["name"]+"**")
            col2.write(c["phone"])
            col3.write(c["email"])

            st.divider()



# ---------- SEARCH ----------

elif menu=="Search":

    st.subheader("Search")

    keyword=st.text_input("Search")

    if keyword:

        results=[

        c for c in contacts

        if keyword.lower() in c["name"].lower()
        or keyword in c["phone"]
        or keyword.lower() in c["email"]

        ]


        for c in results:

            col1,col2,col3=st.columns([2,2,3])

            col1.write("**"+c["name"]+"**")
            col2.write(c["phone"])
            col3.write(c["email"])

            st.divider()



# ---------- EDIT ----------

elif menu=="Edit Contact":

    st.subheader("Edit Contact")

    search=st.text_input("Search contact")

    filtered=[

    c for c in contacts

    if search.lower() in c["name"].lower()
    or search in c["phone"]
    or search.lower() in c["email"]

    ] if search else contacts


    for c in filtered:

        if st.button(c["name"]+" | "+c["phone"]):

            st.session_state.edit=c


    if "edit" in st.session_state:

        c=st.session_state.edit

        st.subheader("Editing")

        new_name=st.text_input("Name",c["name"])

        new_phone=st.text_input("Phone",c["phone"])

        new_email=st.text_input("Email",c["email"])


        if st.button("Update"):

            n=validate_name(new_name)
            p=normalize_phone(new_phone)
            e=validate_email(new_email)

            if n and p and e:

                c["name"]=n
                c["phone"]=p
                c["email"]=e

                save_contacts(contacts)

                st.success("Updated")



# ---------- DELETE ----------

elif menu=="Delete Contact":

    st.subheader("Delete Contact")

    search=st.text_input("Search contact")


    filtered=[

    c for c in contacts

    if search.lower() in c["name"].lower()
    or search in c["phone"]
    or search.lower() in c["email"]

    ] if search else contacts


    for c in filtered:

        if st.button("Delete "+c["name"]):

            st.session_state.delete=c


    if "delete" in st.session_state:

        c=st.session_state.delete

        st.warning(
        "Delete "+c["name"]+" ?"
        )


        if st.button("Confirm Delete"):

            contacts.remove(c)

            save_contacts(contacts)

            st.success("Deleted")
