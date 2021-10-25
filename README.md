# chainalysis-crypto-tracker
A full-stack program that tracks real-time prices of cryptocurrencies on several exchanges. Take-home test for Chainalysis. 

## Live Link: 
http://157.230.232.188:3000/


## How to run: 
#### Prereqs:
Make sure you have Docker installed. 
Make sure you have ports 8001 and 3000 free.

#### Instructions: 
1. Clone this repo. 
2. Run ./build
3. Run ./start_server to start the flask server on port 8001. 
4. In a separate terminal, run ./start_app to run the react app on port 3000. 
5. Open http://localhost:3000/ in your browser (preferably Chrome). 
6. With the website open, click "Connect" to see live price data. 

Please reach out at choudhary.ne@northeastern.edu if you have any issues getting it to run. 

## Architecture: 
Backend Server running on Flask-Socket.io. 
- Polls the two crypto APIs (Coinbase & Binance) every 2 seconds to get the latest price data. 
- Broadcasts the current best buy & best sell data on port 8001. 

Frontend React app
- Opens a websocket connection to the server when "Connect" is clicked. 
- Receives real-time best buy & best sell data from the backend. 
- Displays the data visually. 
- Closes the websocket connection when "Disconnect" is clicked or the site is closed. 

## Questionnaire:
##### 1. Are there any sub-optimal choices( or short cuts taken due to limited time ) in your implementation?
I would split the flask server into two separate services. One two handle getting crypto data from the exchange APIs, and the other to handle processing and the data & sending the best buy / best sell data to the frontend. 
Also, I would prefer to use websockets to stream data from Coinbase & Binance instead of polling them every 2 seconds. 
Lastly, if I had more time, I would have used Go for its performance & low latency benefits.  

##### 2. Is any part of it over-designed? ( It is fine to over-design to showcase your skills as long as you are clear about it)
I designed the server to make it easy to add additional cryptocurrencies & additional exchanges by using object oriented design. 
I would've liked to have a more sophisticated, scalable architecture, but given the time constraints (I needed to finish by Sun Oct. 24), I opted to go with a more simple architecture. 

##### 3. If you have to scale your solution to 100 users/second traffic what changes would you make, if any?
I would first make the change I mentioned in Question 1. Then I would have a redis instance as an intermediary between the two services. The benefit to having the two services separated would be if the service that sends data to the frontend gets overloaded from too many users, the price-retrieval service would be unaffected. 
I would also place a load balancer in front of the price-retrieval service to keep it highly available. 
Lastly, I would use a reverse proxy like nginx to serve & load balance the react app. 

##### 4. What are some other enhancements you would have made, if you had more time to do this implementation
For deployment, I would use TLS to encrypt the network traffic via HTTPS. 
I would build on the error handling to log any error and maybe display error messages on the front end. 