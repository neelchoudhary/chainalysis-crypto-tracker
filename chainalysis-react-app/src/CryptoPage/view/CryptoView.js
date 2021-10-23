import { ConnectionStatus } from '../../consts';
import CryptoCard from './CryptoCardView';

function CryptoView({ connectionStatus, data }) {
    const isDataEmpty = Object.keys(data).length === 0
    return (
        <div className='crypto-view'>
            {connectionStatus === ConnectionStatus.CONNECTED && !isDataEmpty &&
                Object.keys(data).map((key, index) =>
                    <CryptoCard
                        key={index}
                        name={key.toUpperCase()}
                        buy_exchange={data[key]['best_buy_exchange']}
                        sell_exchange={data[key]['best_sell_exchange']}
                        buy_price={data[key]['best_buy_price']}
                        sell_price={data[key]['best_sell_price']} />
                )
            }
            {connectionStatus === ConnectionStatus.CONNECTED && isDataEmpty && (<h1>Loading Real Time Data</h1>)}
            {connectionStatus === ConnectionStatus.INIT && (<h1>Connecting to server..</h1>)}
            {connectionStatus === ConnectionStatus.DISCONNECTED && (<h1>Disconnected from server. The server is probably down.</h1>)}
        </div>
    )

}

export default CryptoView