import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="❤️",
)

# TODO: Paramaratize this to get the user name
user_name = "Lawrence"
st.write(f"# Good Afternoon {user_name}")

st.markdown("HealthFirst AI is here to help you level up your diet and exercise game.")
