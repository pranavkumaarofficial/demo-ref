import streamlit as st
from hl7apy import parser
from hl7apy.core import Group, Segment
from hl7apy.exceptions import UnsupportedVersion
import streamlit as st
from hl7apy import parser

import streamlit as st
from hl7apy import parser

def parse_hl7_message(file_path):
    with open(file_path, "r") as file:
        hl7_message = file.read()
    try:
        msg = parser.parse_message(hl7_message.replace('\n', '\r'), find_groups=True, validation_level=1)
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

    uploaded_file = st.file_uploader("Upload HL7 file", type=["txt", "hl7"])

    if uploaded_file is not None:
        st.caption("Parsing HL7 message...")
        msg = parse_hl7_message(uploaded_file.name)
        if msg is not None:
            st.caption("HL7 message parsed successfully!")
            st.write("Writing parsed content to file...")
            output_file_path = "parsed_content.txt"
            showmsg(msg, output_file_path)
            st.success("Parsed content written to file.")
            st.info("Contents of parsed file:")
            with open(output_file_path, "r") as parsed_file:
                parsed_content = parsed_file.read()
                st.code(parsed_content)

if __name__ == "__main__":
    main()
