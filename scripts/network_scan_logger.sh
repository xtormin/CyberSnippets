#!/bin/bash

# Check if necessary arguments are provided
if [ $# -ne 2 ]; then
    echo "Usage: $0 <HostFile> <ScanType>"
    echo "-> ScanType values: tcp-1000, tcp-full, udp-common, udp-1000, udp-full"
    exit 1
fi

# Assign arguments to variables
HostFile=$1
ScanType=$2

# Define predefined scanning commands and their corresponding Nmap commands
tcp_1000="sudo nmap -v -T4 -Pn -open -sS --script=default,vuln -A --host-timeout 10m"
tcp_full="sudo nmap -v -T4 -Pn -open -sS --script=default,vuln -A --host-timeout 10m -p-"
udp_common="sudo nmap -v -T4 -Pn -sU -sV -A --host-timeout 10m -p '53,69,11,123,137,161,500,514,520,563'"
udp_1000="sudo nmap -v -T4 -Pn -sU -sV -A --host-timeout 10m"
udp_full="sudo nmap -v -T4 -Pn -sU -sV -A --host-timeout 10m -p-"

# Check if the provided scan type is valid
case $ScanType in
    tcp-1000) NmapScanCommand=$tcp_1000 ;;
    tcp-full) NmapScanCommand=$tcp_full ;;
    udp-common) NmapScanCommand=$udp_common ;;
    udp-1000) NmapScanCommand=$udp_1000 ;;
    udp-full) NmapScanCommand=$udp_full ;;
    *) echo "Invalid ScanType. Please choose one of: tcp-1000, tcp-full, udp-common, udp-1000, udp-full"; exit 1 ;;
esac

# Iterate over each host in the provided file and perform the scan
while IFS= read -r IP || [ -n "$IP" ]; do
    # Create a folder for each host to save the scan results
    WorkFolder="nmap/hosts"
    HostFolder="$WorkFolder/$IP"
    FileName="$IP\_$ScanType"

    # Attempt to create the folder
    mkdir -p "$HostFolder"
    echo "|+| Folder created: $HostFolder"

    # Log scan information
    ScanLogInfo="$HostFolder | $FileName"
    ScanInfoStart="$ScanLogInfo | started"
    ScanInfoFinish="$ScanLogInfo | finished"

    TargetOutput="-oA $HostFolder/$FileName $IP"
    # Build the Nmap command based on the chosen scan type
    NmapScan="$NmapScanCommand $TargetOutput"

    # Start the scan and log information to a file
    echo "[$(date)] | $ScanInfoStart"
    echo "$ScanInfoStart" >> "$WorkFolder/scan.logs"
    eval "$NmapScan"
    echo "[$(date)] | $ScanInfoFinish"
    echo "$ScanInfoFinish" >> "$WorkFolder/scan.logs"
    TargetOutput=""
done < "$HostFile"