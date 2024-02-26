
import streamlit as st
import os
import subprocess

def main():
    st.title("HL7 Sender Application 🩺🏥")

    # Radio button for choosing input method
    input_method = st.sidebar.radio("Choose Input Method:", ("Upload HL7 File", "Enter Text"))

    # Conditional rendering based on user's choice
    if input_method == "Upload HL7 File":
        # File Upload
        uploaded_file = st.file_uploader("Choose an HL7 file", type="hl7")

        # Save the uploaded file to the same directory
        if uploaded_file is not None:
            file_path = os.path.join(os.getcwd(), uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getvalue())
    elif input_method == "Enter Text":
        # Textbox for entering HL7 text
        entered_text = st.text_area("Enter HL7 Text")

        # Save the entered text to a temporary file
        if entered_text:
            file_path = os.path.join(os.getcwd(), "entered_text.hl7")
            with open(file_path, "w") as f:
                f.write(entered_text)

    # Server IP and Port
    server_ip = st.text_input("Enter Server IP:")
    server_port = st.text_input("Enter Server Port:")

    # Execute mllp_send command
    if st.button("Send Message"):
        if (input_method == "Upload HL7 File" and uploaded_file) or (input_method == "Enter Text" and entered_text):
            # Construct and execute the mllp_send command
            command = f"mllp_send --file {file_path} --port {server_port} --loose {server_ip}"
            result = subprocess.run(command, shell=True, capture_output=True, text=True)

            # Display the result
            st.text(f"Command executed:\n {command}")
            st.code(f"Result:\n {result.stdout}")

if __name__ == "__main__":
    main()
