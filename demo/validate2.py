import streamlit as st
from hl7apy import parser
from hl7apy.core import Group, Segment
from hl7apy.exceptions import UnsupportedVersion
import streamlit as st
from hl7apy import parser

import streamlit as st
from hl7apy import parser

def parse_hl7_message(hl7_message):
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
 






def main():
    st.title("HL7 Message Parser")

    uploaded_files = st.file_uploader("Upload HL7 file", type=["hl7"],accept_multiple_files=True)
    st.write(uploaded_files)
    if uploaded_files is not None:
        
        for uploaded_file in uploaded_files:
            hl7_messages = uploaded_file.read().decode("utf-8").split("\n\n")  # Split messages by double newline
            st.caption("Parsing HL7 messages...")
            for idx, hl7_message in enumerate(hl7_messages, start=1):
                st.caption(f"Parsing HL7 message {idx}...")
                msg = parse_hl7_message(hl7_message)
                if msg is not None:
                    st.caption(f"HL7 message {idx} parsed successfully!")
                    st.write(f"Parsed content of HL7 message {idx}:")
                    st.json(msg.as_dict())  # Display parsed content as JSON

if __name__ == "__main__":
    main()