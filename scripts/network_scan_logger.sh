#!/bin/bash

# Comprobamos que se pasen los argumentos necesarios
if [ $# -ne 2 ]; then
    echo "Usage: $0 <HostFile> <ScanType>"
    echo "-> ScanType values: tcp-1000, tcp-full, udp-common, udp-1000, udp-full"
    exit 1
fi

# Asignamos los argumentos a variables
HostFile=$1
ScanType=$2

# Definimos los comandos de escaneo predefinidos y sus correspondientes comandos Nmap
tcp_1000="sudo nmap -v -T4 -Pn -open -sS --script=default,vuln -A --host-timeout 10m"
tcp_full="nmap -v -T4 -Pn -open -sS --script=default,vuln -A --host-timeout 10m -p-"
udp_common="nmap -v -T4 -Pn -sU -sV -A --host-timeout 10m -p '53,69,11,123,137,161,500,514,520,563'"
udp_1000="nmap -v -T4 -Pn -sU -sV -A --host-timeout 10m"
udp_full="nmap -v -T4 -Pn -sU -sV -A --host-timeout 10m -p-"

# Comprobamos si el tipo de escaneo proporcionado es válido
case $ScanType in
    tcp-1000) NmapScanCommand=$tcp_1000 ;;
    tcp-full) NmapScanCommand=$tcp_full ;;
    udp-common) NmapScanCommand=$udp_common ;;
    udp-1000) NmapScanCommand=$udp_1000 ;;
    udp-full) NmapScanCommand=$udp_full ;;
    *) echo "Invalid ScanType. Please choose one of: tcp-1000, tcp-full, udp-common, udp-1000, udp-full"; exit 1 ;;
esac

# Iteramos sobre cada host en el archivo proporcionado y realizamos el escaneo
while IFS= read -r IP || [ -n "$IP" ]; do
    # Creamos una carpeta para cada host para guardar los resultados del escaneo
    WorkFolder="nmap/hosts"
    HostFolder="$WorkFolder/$IP"
    FileName="$IP\_$ScanType"

    # Intentamos crear la carpeta
    mkdir -p "$HostFolder"
    echo "|+| Folder created: $HostFolder"

    # Registramos información sobre el escaneo
    ScanLogInfo="[$(date)] | $HostFolder | $FileName"
    ScanInfoStart="$ScanLogInfo | started"
    ScanInfoFinish="$ScanLogInfo | finished"

    # Construimos el comando Nmap basado en el tipo de escaneo elegido
    NmapScanCommand="$NmapScanCommand -oA $HostFolder/$FileName $IP"

    # Iniciamos el escaneo y registramos información en un archivo
    echo "$ScanInfoStart"
    echo "$ScanInfoStart" >> "$WorkFolder/scan.logs"
    eval "$NmapScanCommand"
    echo "$ScanInfoFinish"
    echo "$ScanInfoFinish" >> "$WorkFolder/scan.logs"
done < "$HostFile"