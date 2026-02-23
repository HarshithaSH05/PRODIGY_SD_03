import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Contact Manager", layout="wide")

FILE_NAME = "contacts.csv"

# Initialize file if not exists
if not os.path.exists(FILE_NAME):
    df = pd.DataFrame(columns=["Name", "Phone", "Email"])
    df.to_csv(FILE_NAME, index=False)

# Load contacts
def load_contacts():
    return pd.read_csv(FILE_NAME)

def save_contacts(df):
    df.to_csv(FILE_NAME, index=False)

st.title("📇 Contact Management App")

menu = st.sidebar.radio(
    "Navigation",
    ["Add Contact", "View Contacts", "Search", "Edit Contact", "Delete Contact"]
)

df = load_contacts()

# ---------------- ADD CONTACT ----------------
if menu == "Add Contact":
    st.subheader("➕ Add New Contact")

    name = st.text_input("Name")
    phone = st.text_input("Phone")
    email = st.text_input("Email")

    if st.button("Save Contact"):
        if name and phone:
            new_contact = pd.DataFrame(
                [[name, phone, email]],
                columns=["Name", "Phone", "Email"]
            )
            df = pd.concat([df, new_contact], ignore_index=True)
            save_contacts(df)
            st.success("Contact added successfully!")
        else:
            st.warning("Name and Phone are required.")

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

    contact_list = df["Name"].tolist()

    if contact_list:
        selected_name = st.selectbox("Select Contact", contact_list)

        contact_data = df[df["Name"] == selected_name].iloc[0]

        new_name = st.text_input("Name", contact_data["Name"])
        new_phone = st.text_input("Phone", contact_data["Phone"])
        new_email = st.text_input("Email", contact_data["Email"])

        if st.button("Update Contact"):
            df.loc[df["Name"] == selected_name] = [new_name, new_phone, new_email]
            save_contacts(df)
            st.success("Contact updated successfully!")
    else:
        st.info("No contacts available to edit.")

# ---------------- DELETE CONTACT ----------------
elif menu == "Delete Contact":
    st.subheader("❌ Delete Contact")

    contact_list = df["Name"].tolist()

    if contact_list:
        selected_name = st.selectbox("Select Contact to Delete", contact_list)

        if st.button("Delete"):
            df = df[df["Name"] != selected_name]
            save_contacts(df)
            st.success("Contact deleted successfully!")
    else:
        st.info("No contacts available to delete.")
