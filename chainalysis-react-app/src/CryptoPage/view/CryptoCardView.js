import { ExchangeStyles } from "../../consts";

function CryptoCard({ name, buy_exchange, sell_exchange, buy_price, sell_price }) {
    return (
        <div className='card'>
            <div className='card-header'>
                <h3>{name}</h3>
            </div>
            <div className='card-bottom'>
                <div className='card-side'>
                    <h6>Best Buy: </h6>
                    <DynamicText exchange={buy_exchange} text={buy_exchange}/>
                    <DynamicText exchange={buy_exchange} text={`$${parseFloat(buy_price).toFixed(2)}`}/>
                </div>
                <div className='card-side'>
                    <h6>Best Sell: </h6>
                    <DynamicText exchange={sell_exchange} text={sell_exchange}/>
                    <DynamicText exchange={sell_exchange} text={`$${parseFloat(sell_price).toFixed(2)}`}/>
                </div>
            </div>
        </div>
    )
}

function DynamicText({ exchange, text }) {
    return <p className='dynamic-test' style={ExchangeStyles[exchange]}>{text}</p>;
}

export default CryptoCard