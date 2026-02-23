import streamlit as st
import pandas as pd
import os
import re

st.set_page_config(page_title="Contact Manager", layout="wide")

FILE_NAME = "contacts.csv"

# Create file if not exists
if not os.path.exists(FILE_NAME):
    df = pd.DataFrame(columns=["Name", "Phone", "Email"])
    df.to_csv(FILE_NAME, index=False)

def load_contacts():
    return pd.read_csv(FILE_NAME)

def save_contacts(df):
    df.to_csv(FILE_NAME, index=False)

df = load_contacts()

st.title("📇 Contact Management App")

menu = st.sidebar.radio(
    "Navigation",
    ["Add Contact", "View Contacts", "Search", "Edit Contact", "Delete Contact"]
)

# ---------------- ADD CONTACT ----------------
if menu == "Add Contact":
    st.subheader("➕ Add New Contact")

    with st.form("contact_form", clear_on_submit=True):

        name = st.text_input("Name")
        phone = st.text_input("Phone (10 digits only)", max_chars=10)
        email = st.text_input("Email")

        submitted = st.form_submit_button("Save Contact")

        if submitted:

            # Validation
            if not name:
                st.error("Name is required.")
            
            elif not phone.isdigit() or len(phone) != 10:
                st.error("Phone number must be exactly 10 digits.")
            
            elif not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
                st.error("Invalid email format.")
            
            else:
                new_contact = pd.DataFrame(
                    [[name, phone, email]],
                    columns=["Name", "Phone", "Email"]
                )
                df = pd.concat([df, new_contact], ignore_index=True)
                save_contacts(df)

                st.success("Contact added successfully! You can add another.")

# ---------------- VIEW CONTACTS ----------------
elif menu == "View Contacts":
    st.subheader("📋 All Contacts")

    st.write(f"Total Contacts: {len(df)}")
    st.dataframe(df)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Contacts as CSV",
        data=csv,
        file_name="contacts_backup.csv",
        mime="text/csv"
    )

# ---------------- SEARCH ----------------
elif menu == "Search":
    st.subheader("🔍 Search Contact")

    search_term = st.text_input("Enter Name or Phone")

    if search_term:
        result = df[
            df["Name"].str.contains(search_term, case=False, na=False) |
            df["Phone"].str.contains(search_term, case=False, na=False)
        ]

        if not result.empty:
            st.dataframe(result)
        else:
            st.warning("No contact found.")

# ---------------- EDIT CONTACT ----------------
elif menu == "Edit Contact":
    st.subheader("✏️ Edit Contact")

    if not df.empty:
        selected_name = st.selectbox("Select Contact", df["Name"])

        contact_data = df[df["Name"] == selected_name].iloc[0]

        new_name = st.text_input("Name", contact_data["Name"])
        new_phone = st.text_input("Phone", contact_data["Phone"], max_chars=10)
        new_email = st.text_input("Email", contact_data["Email"])

        if st.button("Update Contact"):

            if not new_phone.isdigit() or len(new_phone) != 10:
                st.error("Phone number must be exactly 10 digits.")
            
            elif not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", new_email):
                st.error("Invalid email format.")
            
            else:
                df.loc[df["Name"] == selected_name] = [new_name, new_phone, new_email]
                save_contacts(df)
                st.success("Contact updated successfully!")
    else:
        st.info("No contacts available.")

# ---------------- DELETE CONTACT ----------------
elif menu == "Delete Contact":
    st.subheader("❌ Delete Contact")

    if not df.empty:
        selected_name = st.selectbox("Select Contact to Delete", df["Name"])

        if st.button("Delete"):
            df = df[df["Name"] != selected_name]
            save_contacts(df)
            st.success("Contact deleted successfully!")
    else:
        st.info("No contacts available.")
