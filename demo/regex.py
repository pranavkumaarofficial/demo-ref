import re

def validate_hl7_message(hl7_message):
    # Define regular expressions for MSH, EVN, PID, and PV1 segments
    msh_pattern = re.compile(r'^MSH\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*$')
    evn_pattern = re.compile(r'^EVN\|.*\|.*\|.*\|.*$')
    pid_pattern = re.compile(r'^PID\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*$')
    pv1_pattern = re.compile(r'^PV1\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*$')

    # Validate MSH segment
    if not msh_pattern.match(hl7_message.split('\r')[0]):
        return False

    # Validate EVN segment
    if not evn_pattern.match(hl7_message.split('\r')[1]):
        return False

    # Validate PID segment
    if not pid_pattern.match(hl7_message.split('\r')[2]):
        return False

    # Validate PV1 segment
    if not pv1_pattern.match(hl7_message.split('\r')[3]):
        return False

    return True

# Example usage
hl7_message_example = """MSH|^~\&|SendingApp|SendingFacility|ReceivingApp|ReceivingFacility|20240226120000||ADT^A04|123456|P|2.5.1|
EVN|A04|20240226120000|||
PID|1|123456789|1011121314|John^Doe||19700101|M|123 Main St^^Anytown^CA^12345^USA||(555)555-5555|(555)555-5556||S||123456789|987654321|
PV1|1|I|^Room123|||||||||||||||||12345678||||||||||||||||||"""

if validate_hl7_message(hl7_message_example):
    print("HL7 message is valid.")
else:
    print("HL7 message is not valid.")
