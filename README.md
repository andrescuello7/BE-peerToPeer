# Peer-to-Peer Network


<p align="center">
  <img align="center" width="200" src="https://i.ibb.co/PcRw7Kg/Captura-de-pantalla-2024-01-01-a-la-s-18-51-06.png" />
</p>

This project implements a peer-to-peer network to facilitate connection and communication between different nodes in a decentralized network architecture. Peer-to-peer networking allows nodes to communicate directly with each other without depending on a central server.

## Characteristics

- **Direct Connection:** Nodes can establish direct connections with each other, allowing efficient communication without intermediaries.

- **Decentralization:** There is no central server that manages all communications. Each node is equal and can communicate directly with other nodes on the network.

- **Scalability:** The peer network is scalable, since each node can connect to new nodes without affecting the overall performance of the system.

## Facility

Clone this repository:

    ```bash
    git clone https://github.com/andrescuello7/BE-peerToPeer
   
    cd BE-peerToPeer/
    ````

#### Genesis

    ```bash
    PORT=3000 node index.js
    ````

#### Peer or Node

    ```
    # Connection is IP:PORT

    PORT=3000 node index.js 127.0.0.1:3000
    ```