# Ref: https://github.com/bhavaniravi/rasa-site-bot
from flask import Flask
from flask import render_template,jsonify,request
import requests
# from models import *
from engine import *
import random


app = Flask(__name__)
app.secret_key = '12345'

@app.route('/')
def hello_world():
    return render_template('home.html')

get_random_response = lambda intent:random.choice(intent_response_dict[intent])


@app.route('/chat',methods=["POST"])
def chat():
    try:
        user_message = request.form["text"]
        response = requests.get("http://localhost:5000/parse",params={"q":user_message})
        response = response.json()
        entities = response.get("entities")
        topresponse = response["topScoringIntent"]
        intent = topresponse.get("intent")
        print("Intent {}, Entities {}".format(intent,entities))
        if intent == "info":
            response_text = govt_info(entities)# "Sorry will get answer soon" #get_event(entities["day"],entities["time"],entities["place"])
        elif intent == "Greet":
            response_text = "Hello!! How can I help you?"
        elif intent == "bye":
            response_text = "Goodbye! It was nice talking to you."
        return jsonify({"status":"success","response":response_text})
    except Exception as e:
        print(e)
        return jsonify({"status":"success","response":"Sorry I am not trained to do that yet..."})


app.config["DEBUG"] = True
if __name__ == "__main__":
    app.run(port=8080)
'''
response = {
  "query": "what about males of mgnrega",
  "topScoringIntent": {
    "intent": "info",
    "score": 0.9929875764345676
  },
  "intents": [
    {
      "intent": "info",
      "score": 0.9929875764345676
    },
    {
      "intent": "bye",
      "score": 0.004822894988674407
    },
    {
      "intent": "Greet",
      "score": 0.002189528576757897
    }
  ],
  "entities": [
    {
      "entity": "males",
      "type": "scheme",
      "startIndex": 11,
      "endIndex": 15,
      "score": 0.9949152319304928
    },
    {
      "entity": "mgnrega",
      "type": "department",
      "startIndex": 20,
      "endIndex": 26,
      "score": 0.9702521068739876
    }
  ]
}
  '''