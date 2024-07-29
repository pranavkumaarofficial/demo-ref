import streamlit as st
from hl7apy import parser
from hl7apy.core import Group, Segment
from hl7apy.exceptions import UnsupportedVersion
import streamlit as st
from hl7apy import parser
import pandas as pd
import streamlit as st
from hl7apy import parser
import time

def parse_hl7_message(file_path):
    with open(file_path, "r") as file:
        hl7_message = file.read()
    try:
        msg = parser.parse_message(hl7_message.replace('\n', '\r'), find_groups=True, validation_level=2)
        return msg
    except Exception as e:
        st.error(f"Error parsing HL7 message: {e}")
        return None



indent = "    "
indent_seg = "    "
indent_fld = "        "









def subgroup (group, indent,f):
    
    indent = indent + "    "
    print (indent , group)
    f.write(indent  + str(group) + "\n")
    for group_segment in group.children:
        if isinstance(group_segment, Group):
            subgroup (group_segment)
        else: 
            print(indent_seg, indent ,group_segment)
            for attribute in group_segment.children:
                print(indent_fld, indent ,str(attribute), attribute.value)
                f.write(indent_fld + indent + str(attribute) + attribute.value + "\n")


def showmsg (msg,output_file_path):
    with open(output_file_path, "w") as f:
        print(msg.children[1])
        #f.write(indent + segment.name + ": " + segment.value + "\n")
        f.write(str(msg.children[1]) + "\n")
        for segment in msg.children:
            if isinstance(segment, Segment):
                print (indent ,segment)
                f.write(indent + str(segment)  + "\n")
                for attribute in segment.children:
                    print(indent_fld, indent, attribute, attribute.value)
                    f.write(indent_fld + indent + str(attribute) + attribute.value  + "\n")
            if isinstance(segment, Group):
                for group in segment.children:
                    print (indent,group)
                    f.write(indent + str(group)  + "\n")
                    for group_segment in group.children:
                        if isinstance (group_segment, Group): 
                            subgroup (group_segment, indent, f)
                        else:
                            print(indent_seg, indent ,group_segment)
                            f.write(indent_seg + str(indent)  + str(group_segment) + "\n")
                            for attribute in group_segment.children:
                                print(indent_fld, indent, attribute, attribute.value)
                                f.write(indent_fld + indent + str(attribute) + attribute.value + "\n")







import datetime
import hl7
import streamlit as st
import os
import subprocess
from hl7apy.core import Message, Segment, Field, Component, SubComponent

def create_hl7_message_from_input(patient_name, patient_address, visit_number, drug_used,drug_rate_amount, drug_rate_units, pump_emr_id):
    # Create an HL7 message
    msg = Message("RGV_O15")
    st.text(msg)
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
    msh_segment.msh_15 = "AL"
    msh_segment.msh_16 = "AL"
    #msh_segment.msh_22="IHE_PCD_RGV_O15^IHE PCD^1.3.6.1.4.1.19376.1.6.1.3.1^ISO"

    msg.add(msh_segment)

    # PID segment
    pid_segment = Segment("PID")
    pid_segment.pid_1 = "1"
    pid_segment.pid_5 = patient_name
    pid_segment.pid_11 = patient_address
    pid_segment.pid_3 = visit_number #MRN
    msg.add(pid_segment)

    # ORC segment
    orc_segment = Segment("ORC")
    orc_segment.orc_1 = "RE"
    orc_segment.orc_2 = "13"
    orc_segment.orc_9 = "20180308195356"
    # Fill ORC fields accordingly
    msg.add(orc_segment)

    # RXG segment
    rxg_segment = Segment("RXG")
    rxg_segment.rxg_4 = drug_used
    rxg_segment.rxg_5 = "20"
    rxg_segment.rxg_7 = "263762^MDC_DIM_MILLI_L^MDC"
    rxg_segment.rxg_15 = drug_rate_amount
    rxg_segment.rxg_16 = drug_rate_units

    # Fill RXG fields accordingly
    msg.add(rxg_segment)

    # RXR segment
    rxr_segment = Segment("RXR")
    rxr_segment.rxr_1 = "^IV^HL70162"
    #rxr_segment.rxr_3 = "^LVP^HL70164"
    rxr_segment.rxr_3 = "^SYR^HL70164"
    rxr_segment.rxr_4 = "^IV^HL70165"
    # Fill RXR fields accordingly
    msg.add(rxr_segment)

    # OBX segments
    obx_segments = [
        ("1","NM","69986^MDC_DEV_PUMP_INFUS_VMD^MDC", pump_emr_id),
        # Add more OBX segments if needed
    ]
    for obx_data in obx_segments:
        obx_segment = Segment("OBX")
        obx_segment.obx_1 = obx_data[0]
        obx_segment.obx_2 = obx_data[1]
        obx_segment.obx_3 = obx_data[2]
        obx_segment.obx_5 = obx_data[3]
        obx_segment.obx_18 = obx_data[3]
        msg.add(obx_segment)

    return msg.to_er7()




#DATABASE CONNECTION DETAILS
import hl7
import streamlit as st
import os
import subprocess
import sqlite3
from hl7apy.core import Message, Segment
conn = sqlite3.connect('hl7_data.db')
c = conn.cursor()

# Create tables if they don't exist
# c.execute('''CREATE TABLE IF NOT EXISTS Patient (
#              id INTEGER PRIMARY KEY,
#              mrn TEXT,
#              name TEXT,
#              address TEXT,
#              visit_timestamp TEXT)''')

# c.execute('''CREATE TABLE IF NOT EXISTS Drug (
#              id INTEGER PRIMARY KEY,
#              mrn TEXT,
#              drug_used TEXT,
#              rate_amount INTEGER,
#              rate_units TEXT,
#              visit_timestamp TEXT)''')

# c.execute('''CREATE TABLE IF NOT EXISTS Pump (
#              id INTEGER PRIMARY KEY,
#              mrn TEXT,
#              emr_id TEXT,
#              visit_timestamp TEXT)''')

# c.execute('''CREATE TABLE IF NOT EXISTS MRN_Timestamp (
#              id INTEGER PRIMARY KEY,
#              mrn TEXT,
#              visit_timestamp TEXT)''')



c.execute('''CREATE TABLE IF NOT EXISTS Patient (
             MRN INTEGER,
             PATIENT_NAME TEXT,
             PATIENT_ADDRESS TEXT,
             VISIT_ID VARCHAR PRIMARY KEY)''')

c.execute('''CREATE TABLE IF NOT EXISTS Drug (
             MRN INTEGER,
             DRUG_USED TEXT,
             RATE_AMOUNT INTEGER,
             RATE_UNITS TEXT,
             VISIT_ID VARCHAR PRIMARY KEY)''')

c.execute('''CREATE TABLE IF NOT EXISTS Pump (
             MRN INTEGER,
             PUMP_EMR TEXT,
             VISIT_ID VARCHAR PRIMARY KEY)''')

c.execute('''CREATE TABLE IF NOT EXISTS MRN_Timestamp (
             MRN VARCHAR,
             VISIT_ID VARCHAR PRIMARY KEY)''')
c.execute('''CREATE TABLE IF NOT EXISTS Full_Database (
            MRN VARCHAR,
            VISIT_ID VARCHAR PRIMARY KEY,
            DATE_TIME_OF_ORDER TEXT,
            PUMP_EMR TEXT,
            PATIENT_NAME TEXT,
            PATIENT_ADDRESS TEXT,
            DRUG_USED TEXT,
            RATE_AMOUNT INTEGER,
            RATE_UNITS TEXT
          
          )''')


conn.commit()









conn = sqlite3.connect('hl7_data.db')
c = conn.cursor()











def resend_order():
    st.subheader("Resend Previous Order")
    
    c.execute("SELECT VISIT_ID, MRN, DATE_TIME_OF_ORDER FROM Full_Database")
    orders = c.fetchall()
    if orders:
        df_orders = pd.DataFrame(orders, columns=["Order ID", "MRN", "Date Time of Order"])
        selected_order = st.selectbox("Select Order to Resend:",  df_orders["Order ID"])
        
        if st.button("Resend Selected Order"):
            c.execute(f"SELECT * FROM Full_Database WHERE VISIT_ID={selected_order}")
            order_data = c.fetchone()
            if order_data:
                visit_number = order_data[1]
                visit_timestamp = int(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
                patient_name = order_data[4]
                patient_address = order_data[5]
                drug_used = order_data[6]
                drug_rate_amount = order_data[7]
                drug_rate_units = order_data[8]
                pump_emr = order_data[3]
                
                # Insert new order with new timestamp
                c.execute("INSERT INTO Patient (MRN, PATIENT_NAME, PATIENT_ADDRESS, VISIT_ID) VALUES (?, ?, ?, ?)",
                          (visit_number, patient_name, patient_address, visit_timestamp))
                c.execute("INSERT INTO Drug (MRN, DRUG_USED, RATE_AMOUNT, RATE_UNITS, VISIT_ID) VALUES (?, ?, ?, ?, ?)",
                          (visit_number, drug_used, drug_rate_amount, drug_rate_units, visit_timestamp))
                c.execute("INSERT INTO Pump (MRN, PUMP_EMR, VISIT_ID) VALUES (?, ?, ?)",
                          (visit_number, pump_emr, visit_timestamp))
                c.execute("INSERT INTO MRN_Timestamp (MRN, VISIT_ID) VALUES (?, ?)",
                          (visit_number, visit_timestamp))
                now = datetime.datetime.now()
                dose_date_time = now.strftime("%Y/%m/%d %H:%M:%S")
                c.execute("INSERT INTO Full_Database (MRN, VISIT_ID, DATE_TIME_OF_ORDER, PUMP_EMR, PATIENT_NAME, PATIENT_ADDRESS, DRUG_USED, RATE_AMOUNT, RATE_UNITS) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                          (visit_number, visit_timestamp, dose_date_time, pump_emr, patient_name, patient_address, drug_used, drug_rate_amount, drug_rate_units))
                
                conn.commit()
                st.success(f"Order with new timestamp {visit_timestamp} has been resent.")
    else:
        st.write("No orders available to resend.")







#MAIN FUNCTION DEFINITION 
def main():

    st.set_page_config(
        page_title="BAX HL7 tool",
        page_icon="📟",
        layout="wide", #wide #centered
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://www.baxter.com/',
            'About': "Made with 🍵 by Team Interop"
        }
        )

        
    st.header("HL7 Sender Application 📟", divider='rainbow')
    st.caption("""<div style='position: fixed; bottom: 0px; right: 10px;'><p>Made with 🧋 by Pranav K</p></div>""", unsafe_allow_html=True)
    st.caption("""<div style='position: fixed; bottom: 18px; right: 10px;'><p>Version v1.0.3</p></div>""", unsafe_allow_html=True)
   
   
   
   
   
    # Radio button for choosing input method
    #input_method = st.sidebar.selectbox("Pick option", ("Upload HL7 File", "Enter HL7 Text","Input Details","View Database"))
    input_method = st.sidebar.selectbox("Choose Input Method:", ("Upload HL7 File", "Enter HL7 Text", "Input Details", "View Database", "Resend Previous Order"))









    # Conditional rendering based on user's choice
    if input_method == "Upload HL7 File":
        try:
            # File Upload
            uploaded_file = st.file_uploader("Choose an HL7 file", type="hl7")

            # Save the uploaded file to the same directory
            if uploaded_file is not None:
                file_path = os.path.join(os.getcwd(), uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getvalue())
                msg = parse_hl7_message(file_path)
                if msg is not None:
                    st.caption("HL7 message parsed successfully!")
                    #st.write("Writing parsed content to file...")
                    #output_file_path = "parsed_content.txt"
                    output_file_path = uploaded_file.name + ".txt"
                    showmsg(msg, output_file_path)
                    #st.success("Parsed content written to file.")
                    st.info("Contents of parsed file:")
                    with open(output_file_path, "r") as parsed_file:
                        parsed_content = parsed_file.read()
                        st.code(parsed_content)
        except Exception as e:
            st.warning("Error occured", icon="⚠️")
            st.warning(f"Reason is: {e}")




    elif input_method == "Enter HL7 Text":
        try:
            entered_text = st.text_area("Enter HL7 Text")
            if entered_text:    
                file_path = os.path.join(os.getcwd(), "entered_text.hl7")
                with open(file_path, "w") as f:
                    f.write(entered_text)
                msg = parse_hl7_message(file_path)
                if msg is not None:
                    st.caption("HL7 message parsed successfully!")
                    #st.write("Writing parsed content to file...")
                    #output_file_path = "parsed_content.txt"
                    output_file_path = "enteredHL7text" + ".txt"
                    showmsg(msg, output_file_path)
                    #st.success("Parsed content written to file.")
                    st.info("Contents of parsed file:")
                    with open(output_file_path, "r") as parsed_file:
                        parsed_content = parsed_file.read()
                        st.code(parsed_content)
        except Exception as e:
            st.warning("Error occured", icon="⚠️")
            st.warning(f"Reason is: {e}")

















    elif input_method == "Input Details":
        # Textbox for entering HL7 text
        # Collect user input
        st.markdown("Enter Patient, Drug, and Pump details")

    # Create three columns layout
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("Enter Patient details")
            visit_number = st.text_input("Patient ID")
            patient_name = st.text_input("Patient Name")
            patient_address = st.text_input("Patient Address")

        # Column 2: Drug Details
        with col2:
            st.markdown("Enter Drug details")
            drug = st.selectbox("Drug value", ["0.9% NaCl"])
            if drug == "0.9% NaCl":
                drug = "NaCl 0.9%1^NaCl 0.9%^erx"
            drug_rate_amount = st.selectbox("Drug rate amount", ["20", "30", "40"])
            drug_rate_units = st.selectbox("Drug rate units", ["mL per Hour", "cL per Hour"])
            if drug_rate_units == "mL per Hour":
                drug_rate_units = "265266^MDC_DIM_MILLI_L_PER_HR^MDC"

        # Column 3: Pump Details
        with col3:
            st.markdown("Enter Pump details")
            pump_emr = st.selectbox("Pump EMR ID", ["EMR_02T190700151", "EMR_01A210900029"])


        if st.button("Generate HL7 Message"):
            # Collect user input data
            input_data = {
                'patient_name': patient_name,
                'patient_address': patient_address,
                'visit_number': visit_number,
                "drug_used" : drug,
                "pump_emr" : pump_emr
            }



            #INPUT DETAILS ONTO DATABASE
            conn = sqlite3.connect('hl7_data.db')
            c = conn.cursor()

            #visit_timestamp = str(time.time())  # Generate unique timestamp

            now = datetime.datetime.now()
            date_string = now.strftime("%Y%m%d%H%M%S")

            visit_timestamp = int(date_string)
            print(visit_timestamp)
            date_string_date=now.strftime("%Y/%m/%d")
            date_string_time=now.strftime("%H:%M:%S")
            dose_date_time=date_string_date + " " + date_string_time
            print(dose_date_time)



            c.execute("INSERT INTO Patient (MRN, PATIENT_NAME, PATIENT_ADDRESS, VISIT_ID) VALUES (?, ?, ?, ?)",
                      (visit_number, patient_name, patient_address, visit_timestamp))
            c.execute("INSERT INTO Drug (MRN, DRUG_USED, RATE_AMOUNT, RATE_UNITS, VISIT_ID) VALUES (?, ?, ?, ?, ?)",
                      (visit_number, drug, drug_rate_amount, drug_rate_units, visit_timestamp))
            c.execute("INSERT INTO Pump (MRN, PUMP_EMR, VISIT_ID) VALUES (?, ?, ?)",
                      (visit_number, pump_emr, visit_timestamp))
            c.execute("INSERT INTO MRN_Timestamp (MRN, VISIT_ID) VALUES (?, ?)",
                      (visit_number, visit_timestamp))
            c.execute("INSERT INTO Full_Database (MRN, VISIT_ID,DATE_TIME_OF_ORDER,PUMP_EMR,PATIENT_NAME,PATIENT_ADDRESS,DRUG_USED,RATE_AMOUNT, RATE_UNITS) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                      (visit_number, visit_timestamp,dose_date_time,pump_emr,patient_name,patient_address,drug,drug_rate_amount,drug_rate_units))
            
            conn.commit()












            # Create HL7 message
            hl7_message = create_hl7_message_from_input(patient_name,patient_address,visit_number,drug,drug_rate_amount, drug_rate_units,pump_emr)
            hl7.ishl7(hl7_message)
            h = hl7.parse(hl7_message)
            # Display generated HL7 message
            st.subheader("Generated HL7 Message")
            #st.text(hl7_message)
            
            file_path = os.path.join(os.getcwd(), "entered_text.hl7")
            with open(file_path, "w") as f:
                f.write(hl7_message)
            with open(file_path, 'r') as f:
                f.seek(36)
                data = f.read()
            with open(file_path, 'w') as f:
                f.write(data)
            with open(file_path, "r") as parsed_file:
                parsed_content = parsed_file.read()
                st.code(parsed_content)

    #Red button 

    # st.markdown("""
    #     <style>
    #         div.stButton > button:first-child  {
    #             background-color: red;
    #             color: white;
    #         }
    #     </style>
    # """, unsafe_allow_html=True)

    




    elif input_method == "View Database":
        import pandas as pd
        import plotly.express as px
        import plotly.graph_objects as go

        import plotly.io as pio
        pio.templates.default="plotly"


        conn = sqlite3.connect('hl7_data.db')
        c = conn.cursor()

        st.subheader("View Database Tables")
        table_names = ["Patient", "Drug", "Pump", "MRN_Timestamp","Full_Database"]

        
        selected_table = st.selectbox("Select Table:", table_names,index=4)
        
        if selected_table:
            c.execute(f"SELECT * FROM {selected_table}")
            data = c.fetchall()
            if data:
                # Convert data to DataFrame
                df = pd.DataFrame(data, columns=[description[0] for description in c.description])
                # Display DataFrame
                st.dataframe(df)

        
            else:
                st.error("Table is empty.")


        

        # Sample DataFrame based on the provided schema
        c.execute(f"SELECT * FROM Full_Database")
        data = c.fetchall()
        if data:
            # Convert data to DataFrame
            df = pd.DataFrame(data, columns=[description[0] for description in c.description])

        #df = pd.DataFrame(data)

        # Preprocess the data
        df['DATE_TIME_OF_ORDER'] = pd.to_datetime(df['DATE_TIME_OF_ORDER'], format='%Y/%m/%d %H:%M:%S')
        df['DRUG_USED'] = df['DRUG_USED'].str.split('^').str[0]
        #df['RATE_UNITS'] = df['RATE_UNITS'].str.split('^').str[1]

        # Plot 1: Distribution of Drug Usage
        fig1 = px.bar(df, x='DRUG_USED', y='RATE_AMOUNT', title='Distribution of Drug Usage')

        # Plot 2: Rate Amount Over Time
        fig2 = px.line(df, x='DATE_TIME_OF_ORDER', y='RATE_AMOUNT', title='Rate Amount Over Time')

        # Plot 3: Rate Units Distribution
        fig3 = px.pie(df, names='RATE_UNITS', title='Rate Units Distribution')

        # Plot 4: Count of Drug Usage
        fig4 = px.histogram(df, x='DRUG_USED', title='Count of Drug Usage')

        # Show the plots
        # fig1.show()
        # fig2.show()
        # fig3.show()
        # fig4.show()
        
        fig1.write_html("fig1.html")
        fig2.write_html("fig2.html")
        fig3.write_html("fig3.html")
        fig4.write_html("fig4.html")

        st.subheader('Drug Record Insights')

        col1, col2 = st.columns(2)

        with col1:
            st.components.v1.html(open("fig1.html", 'r' , encoding='utf-8').read(), height=500)

        with col2:
            st.components.v1.html(open("fig2.html", 'r' , encoding='utf-8').read(), height=500)

        col3, col4 = st.columns(2)

        with col3:
            st.components.v1.html(open("fig3.html", 'r' , encoding='utf-8').read(), height=500)

        with col4:
            st.components.v1.html(open("fig4.html", 'r' , encoding='utf-8').read(), height=500)












    elif  (input_method == "Input Details"):
            # Construct and execute the mllp_send command
            progress_text = "Sending message to pump..."
            my_bar = st.sidebar.progress(0, text=progress_text)

            for percent_complete in range(95,100):
                time.sleep(0.01)
                my_bar.progress(percent_complete + 1, text=progress_text)
            time.sleep(1)
            my_bar.empty()
            file_path = os.path.join(os.getcwd(), "entered_text.hl7")
            command = f"mllp_send --file {file_path} --port {server_port} --loose {server_ip}"
            result = subprocess.run(command, shell=True, capture_output=True, text=True)

            if("Accepted" in result.stdout):
                st.sidebar.success(f"Order accepted by IQE server",icon="✅")
                st.sidebar.code(f"Result from IQE server:\n {result.stdout}")
            elif("Rejected" in result.stdout):
                st.sidebar.error(f"Order rejected by IQE server",icon="🚨")
                st.sidebar.code(f"Result from IQE server:\n {result.stdout}")




    elif (input_method == "Resend Previous Order"):
            st.subheader("Resend Previous Order")
            resend_order()
            # c.execute("SELECT id, MRN, DATE_TIME_OF_ORDER FROM Full_Database")
            # orders = c.fetchall()
            # if orders:
            #     df_orders = pd.DataFrame(orders, columns=["Order ID", "MRN", "Date Time of Order"])
            #     selected_order = st.selectbox("Select Order to Resend:", df_orders["Order ID"])
                
            #     if st.button("Resend Selected Order"):
            #         c.execute(f"SELECT * FROM Full_Database WHERE id={selected_order}")
            #         order_data = c.fetchone()
            #         if order_data:
            #             visit_number = order_data[1]
            #             visit_timestamp = int(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
            #             patient_name = order_data[4]
            #             patient_address = order_data[5]
            #             drug_used = order_data[6]
            #             drug_rate_amount = order_data[7]
            #             drug_rate_units = order_data[8]
            #             pump_emr = order_data[3]
                        
            #             # Insert new order with new timestamp
            #             c.execute("INSERT INTO Patient (MRN, PATIENT_NAME, PATIENT_ADDRESS, VISIT_ID) VALUES (?, ?, ?, ?)",
            #                     (visit_number, patient_name, patient_address, visit_timestamp))
            #             c.execute("INSERT INTO Drug (MRN, DRUG_USED, RATE_AMOUNT, RATE_UNITS, VISIT_ID) VALUES (?, ?, ?, ?, ?)",
            #                     (visit_number, drug_used, drug_rate_amount, drug_rate_units, visit_timestamp))
            #             c.execute("INSERT INTO Pump (MRN, PUMP_EMR, VISIT_ID) VALUES (?, ?, ?)",
            #                     (visit_number, pump_emr, visit_timestamp))
            #             c.execute("INSERT INTO MRN_Timestamp (MRN, VISIT_ID) VALUES (?, ?)",
            #                     (visit_number, visit_timestamp))
            #             now = datetime.datetime.now()
            #             dose_date_time = now.strftime("%Y/%m/%d %H:%M:%S")
            #             c.execute("INSERT INTO Full_Database (MRN, VISIT_ID, DATE_TIME_OF_ORDER, PUMP_EMR, PATIENT_NAME, PATIENT_ADDRESS, DRUG_USED, RATE_AMOUNT, RATE_UNITS) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            #                     (visit_number, visit_timestamp, dose_date_time, pump_emr, patient_name, patient_address, drug_used, drug_rate_amount, drug_rate_units))
                        
            #             conn.commit()
            #             st.success(f"Order with new timestamp {visit_timestamp} has been resent.")
            # else:
            #     st.write("No orders available to resend.")













    # Server IP and Port
    server_ip = st.sidebar.text_input("IQE Server IP","10.40.128.250")
    server_port = st.sidebar.text_input("IQE Server Port","3005")

    # Execute mllp_send command
    if st.sidebar.button("Send Message"):
        if (input_method == "Upload HL7 File" and uploaded_file) or (input_method == "Enter HL7 Text" and entered_text):
            # Construct and execute the mllp_send command
            #file_path = os.path.join(os.getcwd(), "entered_text.hl7")
            progress_text = "Sending message to pump..."
            my_bar = st.sidebar.progress(0, text=progress_text)

            for percent_complete in range(100):
                time.sleep(0.01)
                my_bar.progress(percent_complete + 1, text=progress_text)
            time.sleep(1)
            my_bar.empty()
            command = f"mllp_send --file {file_path} --port {server_port} --loose {server_ip}"
            result = subprocess.run(command, shell=True, capture_output=True, text=True)

            # Display the result
            #st.sidebar.text(f"Command executed:\n {command}")
            #result_list=list(result.stdout)
            #st.write(result_list,split='|')
            if("Accepted" in result.stdout):
                st.sidebar.success(f"Order accepted by IQE server",icon="✅")
                st.sidebar.code(f"Result from IQE server:\n {result.stdout}")
            elif("Rejected" in result.stdout):
                st.sidebar.error(f"Order rejected by IQE server",icon="🚨")
                st.sidebar.code(f"Result from IQE server:\n {result.stdout}")
                

        









if __name__ == "__main__":
    main()
