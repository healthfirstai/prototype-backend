import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="❤️",
)

# TODO: Paramaratize this to get the user name
user_name = "Lawrence"
st.write(f"# Good Afternoon {user_name}")

# st.sidebar.success("Select a demo above.")

st.markdown("HealthFirst AI is a web app that helps you make healthier food choices.")
