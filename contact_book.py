import streamlit as st
import pandas as pd


if "contacts" not in st.session_state:
    st.session_state.contacts = pd.DataFrame(columns=['Name', 'Phone', 'Email', 'Address'])

st.sidebar.title("🔮 Contact Book")
menu = st.sidebar.radio("Select an option:", ["Add", "View", "Search", "Update", "Delete"], label_visibility="collapsed")
st.title("✨ Contact Book")
st.caption("Your futuristic contact manager")

if menu == "Add":
    with st.form("add_form"):
        name = st.text_input("Name")
        phone = st.text_input("Phone")
        email = st.text_input("Email")
        address = st.text_input("Address")
        submitted = st.form_submit_button("🚀 Add Contact")
        
        if submitted:
            if name and phone.isdigit():
                new_entry = pd.DataFrame([[name, phone, email, address]], columns=['Name', 'Phone', 'Email', 'Address'])
                st.session_state.contacts = pd.concat([st.session_state.contacts, new_entry], ignore_index=True)
                st.success("✅ Contact added successfully!")
                st.stop()  # Ensures the message is shown before rerunning
            else:
                st.error("❌ Invalid input! Ensure name is entered and phone contains only numbers.")

elif menu == "View":
    st.dataframe(st.session_state.contacts, use_container_width=True)

elif menu == "Search":
    search_term = st.text_input("Search by name...")
    if search_term:
        results = st.session_state.contacts[st.session_state.contacts['Name'].str.contains(search_term, case=False, na=False)]
        if not results.empty:
            st.dataframe(results)
        else:
            st.warning("⚠️ No contacts found")

elif menu == "Update":
    if not st.session_state.contacts.empty:
        selected = st.selectbox("Select contact", st.session_state.contacts['Name'])
        if selected:
            idx = st.session_state.contacts[st.session_state.contacts['Name'] == selected].index[0]
            with st.form("update_form"):
                new_name = st.text_input("Name", value=st.session_state.contacts.at[idx, 'Name'])
                new_phone = st.text_input("Phone", value=st.session_state.contacts.at[idx, 'Phone'])
                new_email = st.text_input("Email", value=st.session_state.contacts.at[idx, 'Email'])
                new_address = st.text_input("Address", value=st.session_state.contacts.at[idx, 'Address'])
                if st.form_submit_button("🌌 Update"):
                    st.session_state.contacts.loc[idx] = [new_name, new_phone, new_email, new_address]
                    st.success("✅ Contact updated successfully!")
                    st.stop()
    else:
        st.warning("⚠️ No contacts available to update.")


elif menu == "Delete":
    if not st.session_state.contacts.empty:
        selected = st.selectbox("Select contact", st.session_state.contacts['Name'])
        if st.button("💣 Delete Contact"):
            st.session_state.contacts = st.session_state.contacts[st.session_state.contacts['Name'] != selected]
            st.warning("❌ Contact deleted!")
            st.stop()
    else:
        st.warning("⚠️ No contacts available to delete.")
