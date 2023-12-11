The project goal is to help consumers save money on car fuel. This goal will be achieved with the PFPCS (Predictive Fuel Price Comparison Service) application. The project has been developed in collaboration with IBM, the client. The application will provide personalised insights on fuel prices by geographical area. The application uses structured csv data and unstructured natural language text sourced from a number of API’s and websites. These datasets are processed by the applications algorithms to generate a time series dataset and make multi-step predictions into the future. Predictive statistical and machine learning models have been implemented including an ARIMA model and a Recurral Neural Network. The application selects the best predictive model producing the lowest error value each time a query is processed. Three distinct and complementary interactive web dashboards have been developed. These inform the consumer whether fuel prices are expected to rise or fall in the future based on online news articles; current and predicted fuel prices by petrol station in a particular post code; and personalised fuel price insights for a particular vehicle and journey route. 

A video demo of the PFPCS application can be found at: https://youtu.be/c0W_Lutadu0

Application Features and Technology Stack:

• Built Time Series Predictive models to predict fuel price 6 months into the future. 
Stack: Statistical Predictive Models (StatsModels), Recurral Neural Network (Keras), Pandas, NumPy.

• Built a Natural Language Processing capability to predict the fuel price using text data. 
Stack: Naïve Bayes Classifier, BeautifulSoup (web scraper), IBM Watson Discovery API.

• Analysed Twitter Sentiment of fuel retailers. 
Stack: Tweepy, Twitter API, IBM NLU API.

• Developed geolocational algorithms to map optimal routes between a postcode and petrol station. 
Stack: Geocoding API, Directions API, Places API, Distance Matrix API, Requests.

• Interactive visualisations to provide personalised fuel price insights. 
Stack: Vehicle Data API, Fuel Price API, Bootstrap, Wordcloud, Plotly, Dash, HTML. Persistence provided with MongoDB and GridFS.

<img width="601" alt="Screenshot 2023-12-11 at 11 05 49" src="https://github.com/vs2018/PFPCS_Application_Source_Code/assets/33228620/b43d9838-c17f-43f3-b2bb-9cae429fba04">
