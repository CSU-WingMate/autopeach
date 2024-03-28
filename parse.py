import os
import sys

from scapy.all import *
from debug import *


def read_pcap_files(folder_path):
    doing("Reading pcap file")

    if not any(file.endswith('.pcap') for file in os.listdir(folder_path)):
        error(f'No .pcap files found in {folder_path}.')
        sys.exit(-1)

    pcap_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".pcap"):
                pcap_files.append(os.path.join(root, file))

    okf("Reading the pcap files completed. Total number of pcap files: " + str(len(pcap_files)))
    return tuple(pcap_files)
            
    
def extract_pcap_data(pcap_files):
    """
    input: A tuple for storing traffic
    output: The txt file of the parsed data field
    """
    doing("Extract pcap files data")

    for pcap_file in pcap_files:

        output_path = pcap_file[:-5] + '_data.txt'
        input_path = pcap_file

        packets = rdpcap(input_path)
        with open(output_path, 'w') as output_file:
            for packet in packets:
                if Raw in packet:
                    data = str(packet[Raw].load)
                    one_msg = data[2: -1]
                    output_file.write(one_msg + '\n')
    
    okf("Extracting the pcap files completed.")


        



# def main():
#     folder_path = '/home/prk/autoPeach/result'

#     pcap_files = read_pcap_files(folder_path)

#     extract_pcap_data(pcap_files)


# if __name__ == "__main__":
#     main()