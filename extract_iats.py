import pyshark
import numpy as np
import csv
import os
from tqdm import tqdm

def extract_iats_to_csv(pcap_file, output_csv, label, num_packets=256):
    """
    Extract inter-arrival times from pcap and save to CSV
    Format: label,iat1,iat2,...,iat256
    """
    cap = pyshark.FileCapture(pcap_file)
    packets = []
    iats = []
    
    print(f"Processing {pcap_file}...")
    
    # Get packet timestamps
    for pkt in tqdm(cap, desc="Reading packets"):
        if hasattr(pkt, 'sniff_time'):
            packets.append(pkt)
    
    # Write to CSV
    with open(output_csv, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # Calculate inter-arrival times
        for i in tqdm(range(1, len(packets)), desc="Calculating IATs"):
            iat = packets[i].sniff_time.timestamp() - packets[i-1].sniff_time.timestamp()
            iats.append(iat)
            
            # When we have enough for one sample
            if len(iats) == num_packets:
                # Write to CSV: label followed by 256 IAT values
                writer.writerow([label] + iats)
                iats = []  # Reset for next sample

def main():
    # Clear existing output file
    output_csv = r'C:\Users\okore\OneDrive\Desktop\Inno_Courses\PROJECTS\OT\ML\iat_data.csv'
    if os.path.exists(output_csv):
        os.remove(output_csv)
    
    # Add header to CSV
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        header = ['label'] + [f'iat_{i}' for i in range(1, 257)]
        writer.writerow(header)
    
    # Process each pcap file
    datasets = [
        (r'packet_captures\covert_traffic.pcap', 1),  # 1 for covert
        (r'packet_captures\overt_traffic.pcap', 0),  # 0 for overt
    ]
    
    for pcap_file, label in datasets:
        if os.path.exists(pcap_file):
            extract_iats_to_csv(pcap_file, output_csv, label)
        else:
            print(f"Warning: File {pcap_file} not found")

if __name__ == "__main__":
    main()