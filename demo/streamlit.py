"""import streamlit as st
import os
import subprocess

def main():
    st.title("HL7 Client")

    # File Upload
    uploaded_file = st.file_uploader("Choose an HL7 file", type="hl7")

    # Server IP and Port
    server_ip = st.text_input("Enter Server IP:")
    server_port = st.text_input("Enter Server Port:")

    # Execute mllp_send command
    if st.button("Send Message"):
        if uploaded_file is not None and server_ip and server_port:
            # Save the uploaded file to a temporary location
            file_path = os.path.join("/tmp", "uploaded.hl7")
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getvalue())

            # Construct and execute the mllp_send command
            command = f"mllp_send --file {file_path} --port {server_port} {server_ip}"
            result = subprocess.run(command, shell=True, capture_output=True, text=True)

            # Display the result
            st.text(f"Command executed:\n {command}")
            st.text(f"Result:\n {result.stdout}")

if __name__ == "__main__":
    main()
"""




import streamlit as st
import os
import subprocess

def main():
    st.title("HL7 Client")

    # File Upload
    uploaded_file = st.file_uploader("Choose an HL7 file", type="hl7")

    # Server IP and Port
    server_ip = st.text_input("Enter Server IP:")
    server_port = st.text_input("Enter Server Port:")

    # Execute mllp_send command
    if st.button("Send Message"):
        if uploaded_file is not None and server_ip and server_port:
            # Save the uploaded file to the same directory
            file_path = os.path.join(os.getcwd(), uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getvalue())

            # Construct and execute the mllp_send command
            command = f"mllp_send --file {file_path} --port {server_port} --loose {server_ip}"
            result = subprocess.run(command, shell=True, capture_output=True, text=True)

            # Display the result
            st.text(f"Command executed:\n {command}")
            st.text(f"Result:\n {result.stdout}")

if __name__ == "__main__":
    main()
