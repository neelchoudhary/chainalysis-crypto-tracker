import { useState, useEffect } from "react";
import socketio from "socket.io-client";
import { ConnectionStatus } from "../consts";
import CryptoView from "./view/CryptoView";

const HOST = 'localhost:8001'

function CryptoPage() {

    const [data, setData] = useState({})
    const [connectionStatus, setConnectionStatus] = useState(ConnectionStatus.INIT)

    useEffect(() => {
        const socket = socketio(HOST)

        socket.on("connect", () => {
            setConnectionStatus(ConnectionStatus.CONNECTED)
        })

        socket.on("connect_error", () => {
            socket.disconnect();
            setConnectionStatus(ConnectionStatus.DISCONNECTED)
          });

        socket.on("disconnect", () => {
            setConnectionStatus(ConnectionStatus.DISCONNECTED)
        })

        socket.on("crypto-price-data-stream", (data) => {
            setData(data['crypto-price-data'])
        })

        return () => socket.disconnect();
      }, []);
    
      return <CryptoView data={data} connectionStatus={connectionStatus}/>;
}

export default CryptoPage