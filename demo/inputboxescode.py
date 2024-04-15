# import streamlit as st
# from hl7apy import parser
# from hl7apy.core import Message, Segment
# import socket

# def create_hl7_message(data):
#     # Create an HL7 message
#     msg = Message("ADT_A01")
    
#     # Add segments based on user input
#     # For demonstration purposes, let's assume we're adding PID and PV1 segments
#     pid = Segment("PID")
#     pid.pid_3 = data.get('patient_id', '')
#     pid.pid_5 = data.get('patient_name', '')
#     msg.add(pid)
    
#     pv1 = Segment("PV1")
#     pv1.pv1_7 = data.get('visit_number', '')
#     msg.add(pv1)
    
#     return msg.to_er7()

# def main():
#     st.title("HL7 Message Generator")

#     # Collect user input
#     patient_id = st.text_input("Patient ID:")
#     patient_name = st.text_input("Patient Name:")
#     visit_number = st.text_input("Visit Number:")

#     if st.button("Generate HL7 Message"):
#         # Collect user input data
#         input_data = {
#             'patient_id': patient_id,
#             'patient_name': patient_name,
#             'visit_number': visit_number
#         }

#         # Create HL7 message
#         hl7_message = create_hl7_message(input_data)
        
#         # Display generated HL7 message
#         st.header("Generated HL7 Message:")
#         st.code(hl7_message)

#         # Optionally, you can send the HL7 message to an IP
#         # Assuming you have an IP and port defined
#         ip = '127.0.0.1'
#         port = 12345
#         try:
#             with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#                 s.connect((ip, port))
#                 s.sendall(hl7_message.encode())
#             st.success("HL7 message sent successfully!")
#         except Exception as e:
#             st.error(f"Error sending HL7 message: {e}")

# if __name__ == "__main__":
#     main()











import streamlit as st
import os
import subprocess
from hl7apy.core import Message, Segment, Field, Component, SubComponent

def create_hl7_message_from_input(patient_name, patient_address, visit_number, drug_used, pump_emr_id):
    # Create an HL7 message
    msg = Message("RGV_O15")

    # MSH segment
    msh_segment = Segment("MSH")
    msh_segment.msh_1 = "|"
    msh_segment.msh_2 = "^~\&"
    msh_segment.msh_3 = "EHR"
    msh_segment.msh_4 = "EHR"
    msh_segment.msh_5 = "PAT_DEVICE_BAX_NPP"
    msh_segment.msh_6 = "BAX"
    msh_segment.msh_7 = "20180402165937"
    msh_segment.msh_8 = "201142"
    msh_segment.msh_9 = "RGV^O15^RGV_O15"
    msh_segment.msh_10 = "3888"
    msh_segment.msh_11 = "T"
    msh_segment.msh_12 = "2.6"
    msh_segment.msh_16 = "AL"
    msg.add(msh_segment)

    # PID segment
    pid_segment = Segment("PID")
    pid_segment.pid_5 = patient_name
    pid_segment.pid_11 = patient_address
    pid_segment.pid_3 = visit_number
    msg.add(pid_segment)

    # ORC segment
    orc_segment = Segment("ORC")
    # Fill ORC fields accordingly
    msg.add(orc_segment)

    # RXG segment
    rxg_segment = Segment("RXG")
    rxg_segment.rxg_1 = drug_used
    # Fill RXG fields accordingly
    msg.add(rxg_segment)

    # RXR segment
    rxr_segment = Segment("RXR")
    # Fill RXR fields accordingly
    msg.add(rxr_segment)

    # OBX segments
    obx_segments = [
        ("69986^MDC_DEV_PUMP_INFUS_VMD^MDC", pump_emr_id),
        # Add more OBX segments if needed
    ]
    for obx_data in obx_segments:
        obx_segment = Segment("OBX")
        obx_segment.obx_3 = obx_data[0]
        obx_segment.obx_5 = obx_data[1]
        msg.add(obx_segment)

    return msg.to_er7()

def main():
    st.title("HL7 Sender Application 🩺🏥")

    # Radio button for choosing input method
    input_method = st.sidebar.radio("Choose Input Method:", ("Upload HL7 File", "Enter HL7 Text","Input Details"))

    # Conditional rendering based on user's choice
    if input_method == "Upload HL7 File":
        # File Upload
        uploaded_file = st.file_uploader("Choose an HL7 file", type="hl7")

        # Save the uploaded file to the same directory
        if uploaded_file is not None:
            file_path = os.path.join(os.getcwd(), uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getvalue())

    elif input_method == "Enter HL7 Text":
        # Textbox for entering HL7 text
        entered_text = st.text_area("Enter HL7 Text")

        # Save the entered text to a temporary file
        if entered_text:
            # Create HL7 message from entered text
            hl7_message = create_hl7_message(entered_text)
            
            # Save the HL7 message to a temporary file
            file_path = os.path.join(os.getcwd(), "entered_text.hl7")
            with open(file_path, "w") as f:
                f.write(hl7_message)



    elif input_method == "Input Details":
        # Textbox for entering HL7 text
        # Collect user input
        patient_name = st.text_input("Patient Name:")
        patient_address = st.text_input("Patient Address:")
        visit_number = st.text_input("Visit Number:")
        drug = st.text_input("Drug value:")
        pump_emr = st.text_input("Pump_emr_id")

        if st.button("Generate HL7 Message"):
            # Collect user input data
            input_data = {
                'patient_name': patient_name,
                'patient_address': patient_address,
                'visit_number': visit_number,
                "drug_used" : drug,
                "pump_emr" : pump_emr
            }

            # Create HL7 message
            hl7_message = create_hl7_message_from_input(patient_name,patient_address,visit_number,drug,pump_emr)
            
            # Display generated HL7 message
            st.header("Generated HL7 Message:")
            st.text(hl7_message)



    # st.markdown("""
    #     <style>
    #         div.stButton > button:first-child  {
    #             background-color: red;
    #             color: white;
    #         }
    #     </style>
    # """, unsafe_allow_html=True)

    




    # Server IP and Port
    server_ip = st.sidebar.text_input("Enter Server IP:")
    server_port = st.sidebar.text_input("Enter Server Port:")

    # Execute mllp_send command
    if st.sidebar.button("Send Message"):
        if (input_method == "Upload HL7 File" and uploaded_file) or (input_method == "Enter Text" and entered_text):
            # Construct and execute the mllp_send command
            command = f"mllp_send --file {file_path} --port {server_port} --loose {server_ip}"
            result = subprocess.run(command, shell=True, capture_output=True, text=True)

            # Display the result
            st.text(f"Command executed:\n {command}")
            st.code(f"Result:\n {result.stdout}")

if __name__ == "__main__":
    main()
