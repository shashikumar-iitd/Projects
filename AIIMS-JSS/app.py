from flask import Flask, render_template, request
import pickle

app = Flask(__name__)
# load both models
model1 = pickle.load(open('AIIMS_model.sav', 'rb'))
# Assuming you have a second model file
model2 = pickle.load(open('JSS_model.sav', 'rb'))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/model1')
def model1_page():
    result = ''
    return render_template('model1.html', **locals())

@app.route('/model2')
def model2_page():
    result = ''
    return render_template('model2.html', **locals())

@app.route('/predict1', methods=['POST'])
def predict1():
    age = int(request.form['age'])
    cp = float(request.form['cp'])
    thalach = float(request.form['thalach'])
    oldpeak = float(request.form['oldpeak'])
    ca = float(request.form['ca'])
    thal = float(request.form['thal'])
    result = model1.predict([[age, cp, thalach, oldpeak, ca, thal]])[0]
    return render_template('model1.html', **locals())

@app.route('/predict2', methods=['POST'])
def predict2():
    age = int(request.form['Age (in years)'])
    nyha = float(request.form['DOE NYHA Class'])
    rwma = float(request.form['RWMA(seen=1, not seen=0)'])
    syncope = float(request.form['Syncope'])
    orthopnoea = float(request.form['Orthopnoea'])
    presyncope = float(request.form['Pre-Syncope'])
    result = model2.predict([[age, nyha, rwma, syncope, orthopnoea, presyncope]])[0]
    return render_template('model2.html', **locals())

if __name__ == '__main__':
    app.run(debug=True)