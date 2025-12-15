# Tic-Tac-Toe Client–Server Application

## Overview
This project implements a Client–Server based Tic-Tac-Toe application using Python and C.
It is designed to demonstrate fundamental concepts of Computer Networks and Data Communication,
including socket programming, packet-based communication, and error detection mechanisms.

## Objectives
The main objectives of this project are:
- To implement a Client–Server communication model using TCP sockets
- To design a structured packet format for reliable data transmission
- To apply error detection techniques using control information
- To support clients implemented in different programming languages

## System Description
The server application is implemented in Python and is responsible for managing the game logic
and coordinating communication between connected clients. Two clients connect to the server
to participate in the game. Client applications are implemented in both Python and C to
demonstrate interoperability between different programming languages over a network.

## Packet Format
All data exchanged between the server and the clients follows the format:
DATA | METHOD | CONTROL_INFORMATION
The METHOD field specifies the error detection technique used, while the CONTROL_INFORMATION
field contains the generated control value.

The project uses CRC-16 (Cyclic Redundancy Check) as the primary error detection method.

Example packet:
HELLO | CRC16 | 87AF

## Project Structure
Server.py        – Python server application  
Client.py        – Python client application  
Main.c           – C client application  
control_info.py  – Control information generation (CRC-16)  
README.md        – Project documentation  

## Execution Instructions
To run the project, follow the steps below:
1. Start the server by running: python Server.py
2. Start the first client using: python Client.py
3. Start the second client using either Python or C:
   - Python client: python Client.py
   - C client: first compile using gcc Main.c -o client -lws2_32, then run client

## Academic Relevance
This project provides practical experience with Client–Server communication, TCP socket
programming, and error detection using CRC-16. It also demonstrates how applications written
in different programming languages can communicate using a common protocol.

## Technologies Used
Python 3, C (Winsock API), TCP/IP

## Author
Computer Engineering Students – 3rd Year

## License
This project is developed for educational purposes only.
