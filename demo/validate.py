import streamlit as st
import hl7
from io import BytesIO

def validate_hl7_message(uploaded_file):
    try:
        # Read the content of the uploaded file
        content = uploaded_file.getvalue().decode()

        # Parse the HL7 message using python-hl7 library
        parsed_message = hl7.parse(content)
        st.write(parsed_message.segments)
        # Iterate through segments and validate each line
        for segment in parsed_message.segments:
            # Perform validation checks for each segment
            # For example, you can check segment length, required fields, etc.

            # For demonstration purposes, let's check if the segment has at least 3 fields
            if len(segment) < 3:
                return False, f"Validation failed: Segment {segment[0]} should have at least 3 fields."

        # If all segments pass validation, the message format is correct
        return True, "HL7 message format is correct."

    except Exception as e:
        # If parsing fails, the message format is incorrect
        return False, str(e)

def main():
    st.title("HL7 Message Validation")

    # File Upload
    uploaded_file = st.file_uploader("Choose an HL7 file", type="hl7")

    # Validate button
    if st.button("Validate HL7 Message"):
        if uploaded_file is not None:
            # Validate the uploaded HL7 file
            is_valid, validation_result = validate_hl7_message(uploaded_file)

            # Display the validation result
            if is_valid:
                st.success(validation_result)
            else:
                st.error(validation_result)

if __name__ == "__main__":
    main()
