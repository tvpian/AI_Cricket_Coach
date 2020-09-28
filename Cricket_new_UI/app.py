import os
from flask import Flask, render_template, request, redirect, jsonify
from flask_cors import CORS, cross_origin
import json

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
target = os.path.join(APP_ROOT, 'uploads')

batsmen = ['Sehwag', 'Sachin', 'Sourav']


@app.route("/")
def index():
    return render_template("index.html", batsmen=batsmen, len=len(batsmen))


@app.route("/upload", methods=['POST'])
def upload():
   if request.method == 'POST':
      f = request.files['video-input']
      # This will contain the name of the batsman selected form the dropdown
      action_type = request.form['action-type']
      print("Action type is:", action_type)
      batsman = request.form['batsman']
      # This will contain the path of the file selected
      destination = "\\".join([target, f.filename])
      f.save(destination)

      if action_type == 'analyze':
        # Analyze logic goes here

        stats = {
            'Most Played Shot': 'Cover drive',
            'Ideal Shot': 'Sixer',
            'Average Power': '12 W',
            'Average Reaction Time': '100 ms'
        }

        return render_template('stats.html', batsman = batsman, stats = stats)
      elif action_type == 'coachme':
          # Coach me logic goes here
          pass

      print("Batsman:", batsman)
      print("Filename", destination)

      return render_template('index2.html', batsmen=batsmen, len=len(batsmen), batsman=batsman, destination=destination)

@app.route("/analyse", methods=['POST'])
@cross_origin()
def analyse():
    print(request.json)
    player = request.json['player']
    delivery = request.json['delivery']
    print("Player details: ", player['id'], player['name'], player['imageUrl'], player['isCaptain'])
    print("Delivery details: ", delivery['id'], delivery['name'], delivery['videoUrl'])

    # Player and delivery details are available in the variable above, as described

    resp = jsonify(success=True)
    return resp

@app.route("/coach", methods=['POST'])
def coach():
    #bat_coord = request.form.getlist('bat_coord[]') 
    '''
    bat_coord = request.form.get('bat_coord') 
    print(bat_coord)
    return jsonify(otstr="bat_coord")
    '''
    result = []
    data = request.get_json()
    a = data['a'] #will give you array a
    b = data['b'] #will give you array b
    c = data['c'] #will give you array c
    d = data['d'] #will give you array d
    e = data['e'] #will give you array e
    newArray = [a, b, c, d, e]
    #To test you got the data do a print statement

    print(newArray)
    # Player and delivery details are available in the variable above, as described
    return "hello"

if __name__ == "__main__":
    app.run(port=8080, debug=True)