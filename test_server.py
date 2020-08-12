import cv2
import numpy as np

import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as hcluster
from flask import Flask,render_template




#matplotlib.rcParams['figure.figsize'] = (20.0, 18.0)

app = Flask(__name__)

	
@app.route('/test', methods=['POST','GET'])    
def init_new():
    print("rendering")
    return render_template("index.html")

@app.route('/', methods=['POST','GET'])    
def new(): 
	return "helololo"
    
        

# start flask app
app.run(host="0.0.0.0", port=5000)


