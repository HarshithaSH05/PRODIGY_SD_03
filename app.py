import streamlit as st
import json
import os
import re

FILE_NAME = "contacts.json"


# ---------- FILE HANDLING ----------

def load_contacts():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            contacts = json.load(file)

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


# ---------- VALIDATION ----------

def validate_phone(phone):

    phone = phone.replace(" ", "").replace("-", "")

    if phone.startswith("+"):
        digits = phone[1:]
    else:
        digits = phone

    return digits.isdigit() and 7 <= len(digits) <= 15


def validate_email(email):

    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)



# ---------- LOAD DATA ----------

contacts = load_contacts()


# ---------- SIDEBAR ----------

st.sidebar.title("📒 Contact Manager")

menu = st.sidebar.radio(
    "Menu",
    [
        "View Contacts",
        "Add Contact",
        "Edit Contact",
        "Delete Contact",
        "Sort Contacts"
    ]
)



# ---------- VIEW CONTACT ----------

if menu == "View Contacts":

    st.title("📋 Contact List")

    if not contacts:
        st.info("No contacts saved yet")

    else:

        for c in contacts:

            st.write(
                c["Name"],
                "|",
                c["Phone"],
                "|",
                c["Email"]
            )



# ---------- ADD CONTACT ----------

elif menu == "Add Contact":

    st.title("➕ Add Contact")

    name = st.text_input("Name")

    phone = st.text_input("Phone")

    email = st.text_input("Email")


    # duplicate warnings

    name_dup = any(
        c["Name"].lower() == name.lower()
        for c in contacts
    ) if name else False

    phone_dup = any(
        c["Phone"] == phone
        for c in contacts
    ) if phone else False

    email_dup = any(
        c["Email"].lower() == email.lower()
        for c in contacts
    ) if email else False


    if name_dup:
        st.warning("Name already exists")

    if phone_dup:
        st.warning("Phone already exists")

    if email_dup:
        st.warning("Email already exists")



    if st.button("Save Contact"):

        if name == "" or phone == "" or email == "":
            st.warning("Fill all fields")

        elif not validate_phone(phone):
            st.warning("Invalid phone number")

        elif not validate_email(email):
            st.warning("Invalid email")

        else:

            contacts.append({

                "Name": name,
                "Phone": phone,
                "Email": email

            })

            save_contacts(contacts)

            st.success("Contact Saved")


    if st.button("+ New Contact"):
        st.rerun()



# ---------- EDIT CONTACT ----------

elif menu == "Edit Contact":

    st.title("✏ Edit Contact")


    if not contacts:
        st.info("No contacts available")

    else:

        search = st.text_input("Search contact")

        filtered = [

            c for c in contacts

            if search.lower() in c["Name"].lower()
            or search in c["Phone"]
            or search.lower() in c["Email"].lower()

        ] if search else contacts


        names = [

            f'{c["Name"]} | {c["Phone"]} | {c["Email"]}'

            for c in filtered

        ]


        selected = st.selectbox(
            "Select Contact",
            names
        )


        if selected:

            index = names.index(selected)

            contact = filtered[index]


            new_name = st.text_input(
                "Name",
                contact["Name"]
            )

            new_phone = st.text_input(
                "Phone",
                contact["Phone"]
            )

            new_email = st.text_input(
                "Email",
                contact["Email"]
            )


            if st.button("Save Changes"):

                if not validate_phone(new_phone):

                    st.warning("Invalid phone")

                elif not validate_email(new_email):

                    st.warning("Invalid email")

                else:

                    contact["Name"] = new_name
                    contact["Phone"] = new_phone
                    contact["Email"] = new_email

                    save_contacts(contacts)

                    st.success("Updated")



# ---------- DELETE CONTACT ----------

# ---------- DELETE CONTACT ----------

elif menu == "Delete Contact":

    st.title("🗑 Delete Contact")

    if not contacts:
        st.info("No contacts available")

    else:

        # Search Bar
        search = st.text_input("Search Contact (Name / Phone / Email)")

        filtered = [

            c for c in contacts

            if search.lower() in c["Name"].lower()
            or search in c["Phone"]
            or search.lower() in c["Email"].lower()

        ] if search else contacts


        if not filtered:
            st.warning("No matching contacts")

        else:

            options = [

                f'{c["Name"]} | {c["Phone"]} | {c["Email"]}'

                for c in filtered

            ]


            selected = st.selectbox(
                "Select Contact to Delete",
                options
            )


            index = options.index(selected)

            contact = filtered[index]


            # Confirmation Checkbox
            confirm = st.checkbox("Confirm Delete")


            # Delete Button ONLY after checking box
            if confirm:

                if st.button("Delete Contact"):

                    contacts.remove(contact)

                    save_contacts(contacts)

                    st.success("✅ Successfully Deleted")

                    st.rerun()

# ---------- SORT CONTACT ----------

elif menu == "Sort Contacts":

    st.title("🔽 Sort Contacts")


    if not contacts:

        st.info("No contacts to sort")

    else:

        field = st.selectbox(

            "Sort By",

            ["Name","Phone","Email"]

        )


        order = st.selectbox(

            "Order",

            ["Ascending","Descending"]

        )


        reverse = order == "Descending"


        sorted_contacts = sorted(

            contacts,

            key=lambda x: x[field].lower(),

            reverse=reverse

        )


        for c in sorted_contacts:

            st.write(

                c["Name"],
                "|",
                c["Phone"],
                "|",
                c["Email"]

            )
