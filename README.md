# Chatbot
Chatbot which gives information about the schemes of Government.
# Training Data
Data used for extracting intent and entities is present in training_data.json. Rasa-NLU is used for intent and entity extraction. Training data is built using online tool chatito. 
# Data Collection
This Chatbot can answer details about the various schemes of the government. In Data_colletion.py data about the government schemes is scrapped using BeautifulSoup and Requests.  
# Chatbot
The chatbot.py files gets the intents, entities from the server and based on the them required output is given. If the chatbot gets Welcome, Bye intent then it just outputs message. But if the user tries to get information about schemes then it uses the data collected using data_collection.py and provides required information.
