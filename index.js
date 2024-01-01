const { createConnection, createServer } = require('net');

class Server {
    hostConnecteds = [];
    socketsConnecteds = [];

    constructor() {
        this.Server();
        this.Socket();
        process.stdin.on('data', (buffer) => {
            this.Message(buffer);
        });
    }

    // server for connection with other users
    Server() {
        // config of socket created by server
        const server = createServer((socket) => {
            socket.on('data', (buffer) => {
                try {
                    const data = JSON.parse(buffer.toString());
                    if (data.length) {
                        for (const connection of data) {
                            const isCurrentHost = connection.port === process.env.PORT;
                            const isValidConnection = connection.port !== undefined && connection.host !== undefined;
                            const isNotConnected = !this.hostConnecteds.some(item => item.port === connection.port && item.host === connection.host);

                            if (!isCurrentHost && isValidConnection && isNotConnected) {
                                this.Connected(
                                    connection.host,
                                    connection.port,
                                    data,
                                    { port: process.env.PORT, host: '127.0.0.1' }
                                );
                            }
                        }
                    } else {
                        // connection with user initialized
                        this.Connected(data.host, data.port, data);
                        console.log(`\x1b[32m[+]\x1b[0m ${data.host}:${data.port}`);
                    }
                } catch (error) {
                    // send message
                    const data = buffer.toString();
                    console.log(`\x1b[33m  - \x1b[0m ${data}`);
                }
            });
            // socket connection is disconnected
            socket.on('close', () => {
                console.log(`Socket cerrado: ${socket.remoteAddress}:${socket.remotePort}`);
                // return { port: process.env.PORT, host: '127.0.0.1' };
            });
        });
        // server error 
        server.on('error', (error) => {
            console.error('Error en el servidor:', error.message);
        });
        // running server with port and host for default
        server.listen({ host: '127.0.0.1', port: process.env.PORT }, () => {
            console.log(`Server constructor ${'127.0.0.1'}:${process.env.PORT}`);
        });
    }

    // connect with other peer or user
    Socket() {
        try {
            const connect = process.argv.slice(2)[0].split(':');
            const HIS_HOST = connect[0];
            const HIS_PORT = connect[1];

            this.Connected(HIS_HOST, HIS_PORT, false, { port: process.env.PORT, host: '127.0.0.1' });
            console.log(`\x1b[32m[+]\x1b[0m ${HIS_HOST}:${HIS_PORT}`);
        } catch (error) { }
    }

    // method of conected with socket
    Connected(host, port, data, myCredentials) {
        const _socket = createConnection({ host, port }, () => {
            if (data) {
                this.hostConnecteds.push(data)
            }
            this.socketsConnecteds.push(_socket);
            _socket.write(JSON.stringify(myCredentials || this.hostConnecteds));
        })
    }

    // generatod of message and send info
    Message(buffer) {
        for (const socket of this.socketsConnecteds) {
            socket.write(buffer.toString().trim());
        }
    }
}

new Server()