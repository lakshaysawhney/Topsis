import streamlit as st
import subprocess
import re

EMAIL_REGEX = r'^[\w\.-]+@[\w\.-]+\.\w+$'

st.set_page_config(page_title="TOPSIS App", layout="centered")

st.title("TOPSIS Decision Making Tool")
st.write("Upload a CSV file and provide weights and impacts.")

uploaded_file = st.file_uploader(
    "Upload CSV file",
    type=["csv"],
    key="file_uploader_1"
)

weights = st.text_input(
    "Weights (comma separated)",
    placeholder="1,1,1,1",
    key="weights_input"
)

impacts = st.text_input(
    "Impacts (+ or -, comma separated)",
    placeholder="+,+,-,+",
    key="impacts_input"
)

email = st.text_input(
    "Email (optional)",
    key="email_input"
)

if st.button("Run TOPSIS", key="run_button"):
    if not uploaded_file or not weights or not impacts:
        st.error("Please fill all required fields")
        st.stop()

    if email and not re.match(EMAIL_REGEX, email):
        st.error("Invalid email format")
        st.stop()

    with open("input.csv", "wb") as f:
        f.write(uploaded_file.getbuffer())

    try:
        subprocess.run(
            ["topsis", "input.csv", weights, impacts, "result.csv"],
            check=True
        )
        st.success("TOPSIS executed successfully")

        with open("result.csv", "rb") as f:
            st.download_button(
                "Download Result CSV",
                f,
                file_name="topsis_result.csv",
                mime="text/csv",
                key="download_button"
            )

    except Exception as e:
        st.error("Error while running TOPSIS")