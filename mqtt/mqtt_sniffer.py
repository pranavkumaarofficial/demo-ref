import pyshark

def mqtt_packet_handler(packet):
    try:
        if 'MQTT' in packet:
            topic = packet.mqtt.topic
            payload = bytes.fromhex(packet.mqtt.msg).decode('utf-8')
            print(f"Topic: {topic}, Payload: {payload}")
    except AttributeError as e:
        # Handle the case where the packet does not contain MQTT data
        pass

# Replace 'your_interface' with your network interface, e.g., 'eth0', 'wlan0'
#capture = pyshark.LiveCapture(interface='your_interface', display_filter='mqtt')
capture = pyshark.LiveCapture(interface='wlan0', display_filter='mqtt')


print("Sniffing MQTT packets. Press CTRL+C to stop...")
try:
    for packet in capture.sniff_continuously():
        mqtt_packet_handler(packet)
except KeyboardInterrupt:
    print("Stopped sniffing.")
