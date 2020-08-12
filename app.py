import os
from flask import Flask, render_template, request, redirect, jsonify,url_for
from Conv3D_Preprocessing import preprocess
from test import inference
import os
import glob
import shutil
import pandas as pd
from flask_cors import CORS, cross_origin
import json
from cs import shot_similarity

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

df = pd.read_excel("dataset.xlsx")

shot_type=""
batsman=""
destination=""
#for mapping of deliveries
map=dict([(0,3), (1,6), (2, 2), (3, 5), (4, 1), (5, 4)])

app = Flask(__name__)
 
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
target = os.path.join(APP_ROOT, 'uploads')
 
batsmen = ['Vivek', 'Hari', 'Ayush']

stats = {
    'Most Played Shot': 'Cover drive',
    'Ideal Shot': 'Sixer',
    'Average Power': '12 W',
    'Average Reaction Time': '100 ms'
}

def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier
 
@app.route("/")
def index():
    dir_path = 'C:/Users/Administrator/Desktop/Ankita/uploads'
    try:
        shutil.rmtree(dir_path)
    except OSError as e:
        print("Error: %s : %s" % (dir_path, e.strerror))
    try:
        os.makedirs(dir_path)
    except OSError as e:
        pass
    return render_template("index.html", batsmen=batsmen, len=len(batsmen))
 
@app.route("/upload", methods=['POST'])
def upload():
   global shot_type
   global destination
   global batsman
   if request.method == 'POST':
      f = request.files['video-input']
      # This will contain the name of the batsman selected form the dropdown
      action_type = request.form['action-type']
      print("Action type is:", action_type)
      batsman = request.form['batsman']
      # This will contain the path of the file selected
      destination = "\\".join([target, f.filename])
      f.save(destination)
      print(destination)
 
      if action_type == 'analyze':
          # Analyze logic goes here
          preprocess(destination)
          
          bowl_ids=inference()
          #return str(destination)+" "+str(batsman)

           #changing variables
          bm=batsman
          bi=bowl_ids

          print("initial bowling ids predicted by model",bi)
          x=bi[0]#1st bowl id
          y=bi[1]#2nd bowl id

          #after manipulation
          a=map[x]#1st bowl id
          b=map[y]#2nd bowl # IDEA:

          bi[0]=a
          bi[1]=b
          print("final bowling ids after manipulation according to dataset",bi)

          #most played shot
          mps=df.loc[(df['Batsman'] == bm) & ((df['Bowl_Id'] == bi[0]) | (df['Bowl_Id'] == bi[1]))]
          mps=mps.mode()['Shot_Played'][0]

          #ideal shot
          ids=df.loc[ (df['Bowl_Id'] == bi[0]) | (df['Bowl_Id'] == bi[1])]
          ids=ids.groupby('Shot_Played').mean().reset_index()
          ids=ids.iloc[ids["Boundary_Success_Rate"].idxmax()]
          ids=ids["Shot_Played"]

          #avg power
          ap=df.loc[(df['Batsman'] == bm) & ((df['Bowl_Id'] == bi[0]) | (df['Bowl_Id'] == bi[1]))]
          ap=ap["Power_Applied(N)"].mean()


          #avg reaction time
          art=df.loc[(df['Batsman'] == bm) & ((df['Bowl_Id'] == bi[0]) | (df['Bowl_Id'] == bi[1]))]
          art=art["Reaction Time(sec)"].mean()

          #best refrence
          br=df.loc[ (df['Bowl_Id'] == bi[0]) | (df['Bowl_Id'] == bi[1])]
          br=br.groupby('Batsman').mean().reset_index()
          br=br.iloc[br["Boundary_Success_Rate"].idxmax()]
          br=br["Batsman"]
          #return str(destination)+" "+str(batsman)

          stats = {
            'Most Played Shot': mps,
            'Ideal Shot': ids,
            'Average Power': ap,
            'Average Reaction Time': art,
            'Best Refrence': br,
            }
          '''
          stats = {
            'Most Played Shot': 'Cover drive',
            'Ideal Shot': 'Sixer',
            'Average Power': '12 W',
            'Average Reaction Time': '100 ms'
            }
          '''
          dir_path = 'C:/Users/Administrator/Desktop/Ankita/uploads/'
          try:
              shutil.rmtree(dir_path)
          except OSError as e:
              print("Error: %s : %s" % (dir_path, e.strerror))
          return render_template('stats.html', batsman = batsman, stats = stats)
    
      elif action_type == 'coachme':
          print(batsman)
          print(shot_type)
          # Coach me logic goes here
          Cover_drive=[[-0.5, 1.2, -9.1,0,-1,0],[-0.55, 1.2, -8.5,0,-1,0],[-0.58, 1.2, -8.3,0,-1,0],[-0.6, 1.2, -8.0,0,-1,0],[-0.65, 1.2, -7.8,-15,-1,0],[-0.68, 1.2, -7.7,-19,-1,0],[-0.7, 1.2, -7.5,-20,-1,0],[-0.72, 1.2, -7.3,-25,-1,0]]
          Straight_drive=[[-0.5, 1.2, -9.1,0,0,0],[-0.5, 1.2, -8.5,0,0,0],[-0.5, 1.2, -8.3,0,0,0],[-0.5, 1.2, -8.0,0,0,0],[-0.5, 1.2, -7.8,0,0,0],[-0.5, 1.2, -7.7,-20,0,0],[-0.5, 1.2, -7.5,-29,0,0],[-0.5, 1.2, -7.3,-30,0,0]]
          if batsman=="Hari":
            shot_type=Straight_drive
          if batsman=="Vivek":
            shot_type=Cover_drive
          return render_template('coach.html',shot_type=shot_type)
 
      print("Batsman:", batsman)
      print("Filename", destination)
 
      return render_template('index.html', batsmen=batsmen, len=len(batsmen), batsman=batsman, destination=destination)


@app.route("/coachme", methods=['POST','GET'])
def coachme():
   global shot_type
   global destination
   global batsman
   
   print(batsman)
   print(shot_type)
   # Coach me logic goes here
   Cover_drive=[[-0.5, 1.2, -9.1,0,-1,0],[-0.55, 1.2, -8.5,0,-1,0],[-0.58, 1.2, -8.3,0,-1,0],[-0.6, 1.2, -8.0,0,-1,0],[-0.65, 1.2, -7.8,-15,-1,0],[-0.68, 1.2, -7.7,-19,-1,0],[-0.7, 1.2, -7.5,-20,-1,0],[-0.72, 1.2, -7.3,-25,-1,0]]
   Straight_drive=[[-0.5, 1.2, -9.1,0,0,0],[-0.5, 1.2, -8.5,0,0,0],[-0.5, 1.2, -8.3,0,0,0],[-0.5, 1.2, -8.0,0,0,0],[-0.5, 1.2, -7.8,0,0,0],[-0.5, 1.2, -7.7,-20,0,0],[-0.5, 1.2, -7.5,-29,0,0],[-0.5, 1.2, -7.3,-30,0,0]]
   if batsman=="Hari":
       shot_type=Straight_drive
   if batsman=="Vivek":
       shot_type=Cover_drive
   return render_template('coach.html',shot_type=shot_type)
   


@app.route("/analyse", methods=['POST','GET'])
@cross_origin()
def analyse():
    global selected_player
    global selected_delivery
    global destination
    global batsman

    if request.method == 'POST':
        print(request.json)
        selected_player = request.json['player']
        selected_delivery = request.json['delivery']
        print("Selected player in POST is: ", selected_player)
        print("Player details: ", selected_player['id'], selected_player['name'], selected_player['imageUrl'], selected_player['isCaptain'])
        print("Delivery details: ", selected_delivery['id'], selected_delivery['name'], selected_delivery['videoUrl'])
        
        # Player and delivery details are available in the variable above, as described
        resp = jsonify(success=True)
        return resp

    if request.method == 'GET':
        batsman=selected_player['name']
        original="C:/Users/Administrator/Desktop/Cricket_new_UI/" + selected_delivery['videoUrl']
        shutil.copyfile(original, 'C:/Users/Administrator/Desktop/Ankita/uploads/test.webm')

        print("Selected player in GET is: ", selected_player)
        print("Selected delivery in GET is: ", selected_delivery['videoUrl'])
        destination = "C:\\Users\\Administrator\\Desktop\\Ankita\\uploads\\test.webm"

        # Analyze logic goes here
        preprocess(destination)
          
        bowl_ids=inference()
        #return str(destination)+" "+str(batsman)

        #changing variables
        bm=batsman
        bi=bowl_ids

        print("initial bowling ids predicted by model",bi)
        x=bi[0]#1st bowl id
        y=bi[1]#2nd bowl id

        #after manipulation
        a=map[x]#1st bowl id
        b=map[y]#2nd bowl # IDEA:

        bi[0]=a
        bi[1]=b
        print("final bowling ids after manipulation according to dataset",bi)

        #most played shot
        mps=df.loc[(df['Batsman'] == bm) & ((df['Bowl_Id'] == bi[0]) | (df['Bowl_Id'] == bi[1]))]
        mps=mps.mode()['Shot_Played'][0]

        #ideal shot
        ids=df.loc[ (df['Bowl_Id'] == bi[0]) | (df['Bowl_Id'] == bi[1])]
        ids=ids.groupby('Shot_Played').mean().reset_index()
        ids=ids.iloc[ids["Boundary_Success_Rate"].idxmax()]
        ids=ids["Shot_Played"]

        #avg power
        ap=df.loc[(df['Batsman'] == bm) & ((df['Bowl_Id'] == bi[0]) | (df['Bowl_Id'] == bi[1]))]
        ap=ap["Power_Applied(N)"].mean()


        #avg reaction time
        art=df.loc[(df['Batsman'] == bm) & ((df['Bowl_Id'] == bi[0]) | (df['Bowl_Id'] == bi[1]))]
        art=art["Reaction Time(sec)"].mean()

        #best refrence
        br=df.loc[ (df['Bowl_Id'] == bi[0]) | (df['Bowl_Id'] == bi[1])]
        br=br.groupby('Batsman').mean().reset_index()
        br=br.iloc[br["Boundary_Success_Rate"].idxmax()]
        br=br["Batsman"]
        #return str(destination)+" "+str(batsman)

        stats = {
            'Most Played Shot': mps,
            'Ideal Shot': ids,
            'Average Power': ap,
            'Average Reaction Time': art,
            'Best Refrence': br,
        }
        '''
        stats = {
        'Most Played Shot': 'Cover drive',
        'Ideal Shot': 'Sixer',
        'Average Power': '12 W',
        'Average Reaction Time': '100 ms'
        }
        '''
        dir_path = 'C:/Users/Administrator/Desktop/Ankita/uploads/'
        try:
            shutil.rmtree(dir_path)
        except OSError as e:
            print("Error: %s : %s" % (dir_path, e.strerror))
        try:
            os.makedirs(dir_path)
        except OSError as e:
            pass
        return render_template('stats.html', batsman = batsman, stats = stats)

        ##return render_template('stats.html', batsman = selected_player['name'], stats = stats)

@app.route("/coach", methods=['POST'])
@cross_origin()
def coach():
    #bat_coord = request.form.getlist('bat_coord[]') 
    '''
    bat_coord = request.form.get('bat_coord') 
    print(bat_coord)
    return jsonify(otstr="bat_coord")
    '''
    result = []
    data = request.get_json()
    player_shot = data['player_shot'] #will give you array a
    reference_shot = data['reference_shot'] #will give you array b
    newArray = [player_shot, reference_shot]
    #To test you got the data do a print statement
    print(len(player_shot))
    print(len(reference_shot))
    #print(player_shot.type)
    #print(reference_shot.type)
    score=shot_similarity(player_shot,reference_shot)
    score=score*100
    score=truncate(score,2)
    print(player_shot)
    print(reference_shot)
    print(score)
    # Player and delivery details are available in the variable above, as described
    return json.dumps(score)
 
if __name__ == "__main__":
    app.run(port=8080, debug=False,threaded=False)