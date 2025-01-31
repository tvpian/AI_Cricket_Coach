import os
from flask import Flask, render_template, request, redirect
from Conv3D_Preprocessing import preprocess
from test import inference
import os
import glob
 
app = Flask(__name__)
 
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
          '''
          preprocess(destination)
          bowl_ids=inference()
          return str(destination)+" "+str(batsman)
          '''
          stats = {
            'Most Played Shot': 'Cover drive',
            'Ideal Shot': 'Sixer',
            'Average Power': '12 W',
            'Average Reaction Time': '100 ms'
            }
          

          files = glob.glob('C:/Users/Administrator/Desktop/Ankita/uploads/*')
          for f in files:
            os.remove(f)
          return render_template('stats.html', batsman = batsman, stats = stats)
    
      elif action_type == 'coachme':
          # Coach me logic goes here
          shot_type=[[-0.5, 1.2, -9.1],[-0.55, 1.2, -8.5],[-0.58, 1.2, -8.3],[-0.6, 1.2, -8.0],[-0.65, 1.2, -7.8],[-0.68, 1.2, -7.7],[-0.7, 1.2, -7.5],[-0.72, 1.2, -7.3]]
          return render_template('coach.html',shot_type=shot_type)
 
      print("Batsman:", batsman)
      print("Filename", destination)
 
      return render_template('index.html', batsmen=batsmen, len=len(batsmen), batsman=batsman, destination=destination)
 
if __name__ == "__main__":
    app.run(port=8080, debug=True)