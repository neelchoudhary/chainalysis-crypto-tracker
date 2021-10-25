# chainalysis-crypto-tracker
A full-stack program that tracks real-time prices of cryptocurrencies on several exchanges. Take-home test for Chainalysis. 

## Live Link: 
http://157.230.232.188:3000/


## How to run: 
### Prereqs:
Make sure you have Docker installed. 
Make sure you have ports 8001 and 3000 free.

### Instructions: 
1. Clone this repo. 
2. Run ./build
3. Run ./start_server to start the flask server on port 8001. 
4. In a seperate terminal, run ./start_app to run the react app on port 3000. 
5. Open http://localhost:3000/ in your browser (preferably Chrome). 
6. With the website open, click "Connect" to see live price data. 

## Architecture: 
Backend Server running on Flask-Socket.io. 
- Polls the two crypto APIs (Coinbase & Binance) every 2 seconds to get the latest price data. 
- Broadcasts the current best buy & best sell data on port 8001. 

Frontend React app
- Opens a websocket connecetion to the server when "Connect" is clicked. 
- Receives real-time best buy & best sell data from the backend. 
- Displays the data visually. 
- Closes the websocket connection when "Disconnect" is clicked or the site is closed. 

## Questionnaire:
### 1. Are there any sub-optimal choices( or short cuts taken due to limited time ) in your implementation?


### 2. Is any part of it over-designed? ( It is fine to over-design to showcase your skills as long as you are clear about it)


### 3. If you have to scale your solution to 100 users/second traffic what changes would you make, if any?


### 4. What are some other enhancements you would have made, if you had more time to do this implementation
