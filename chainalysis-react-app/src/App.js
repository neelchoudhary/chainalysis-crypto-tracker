import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Navbar, Container, Button } from 'react-bootstrap';
import { useState } from 'react';
import CryptoPage from './CryptoPage/CryptoPage';


function App() {
  const [connect, setConnect] = useState(false)

  return (
    <div className="App">
      <Headline />
      <div className="page">
        <InfoText />
        {connect && <CryptoPage />}
        <Button variant="dark" className="btn" onClick={() => setConnect((connect) => !connect)}>{connect ? "Disconnect" : "Connect"}</Button>
      </div>
    </div>
  );
}

function InfoText() {
  return (
    <p className='info-text'>This webapp gets real-time price data for Bitcoin (BTC) and Ethereum (ETH) from Coinbase and Binance.
      {<br />} Made by Neel Choudhary. </p>
  )
}


function Headline() {
  return (<Navbar bg="dark" variant="dark" expand="lg">
    <Container>
      <Navbar.Brand href="#home">Chainalysis Crypto Tracker</Navbar.Brand>
    </Container>
  </Navbar>)
}

export default App;
