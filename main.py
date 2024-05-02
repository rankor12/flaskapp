from flask import Flask,render_template, request,redirect
from db import Database
import pickle
import pandas as pd

data = pd.read_csv('cleaned data (1).csv')
pipeline = pickle.load(open('pipeline (2).pkl', 'rb'))
X = pickle.load(open('df (1).pkl', 'rb'))

app = Flask(__name__)

dbo = Database()

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/register')
def about():
    return render_template('register.html')

@app.route('/perform_registration',methods=['POST'])
def perform_registration():
    name = request.form.get('name')
    telephone = request.form.get('telephone')
    email = request.form.get('email')
    password = request.form.get('password')

    response = dbo.insert(name, telephone, email, password)

    if response:
        return render_template('login.html', message="register successfully kindly login to proceed")
    else:
        return render_template('register.html', message="email already exist")

@app.route('/perform_login',methods=['POST'])
def perform_login():
    email = request.form.get('email')
    password = request.form.get('password')
    response = dbo.search(email, password)

    if response:
        return redirect('/profile')
    else:
        return render_template('login.html',message1='incorrect email/password')


@app.route('/profile')
def profile():
    sex = sorted(data['sex'].unique())
    education = sorted(data['education'].unique())
    occupation = sorted(data['occupation'].unique())
    diabetes = sorted(data['diabetes'].unique())
    hypertension = sorted(data['hypertension'].unique())
    asthma = sorted(data['asthma'].unique())
    tb = sorted(data['tb'].unique())
    cancer = sorted(data['cancer'].unique())
    covid_severity = sorted(data['covid_severity'].unique())
    lc_fatigue_four = sorted(data['lc_fatigue_four'].unique())
    lc_cough_four = sorted(data['lc_cough_four'].unique())
    lc_headache_four = sorted(data['lc_headache_four'].unique())
    lc_breathing_four = sorted(data['lc_breathing_four'].unique())
    lc_taste_four = sorted(data['lc_taste_four'].unique())
    lc_smell_four = sorted(data['lc_smell_four'].unique())
    lc_brainfog_four = sorted(data['lc_brainfog_four'].unique())
    lc_chestpain_four = sorted(data['lc_chestpain_four'].unique())
    lc_fever_four = sorted(data['lc_fever_four'].unique())
    return render_template('profile.html', sex=sex, education=education, occupation=occupation, diabetes=diabetes,
                           hypertension=hypertension, asthma=asthma, tb=tb, cancer=cancer,
                           covid_severity=covid_severity, lc_fatigue_four=lc_fatigue_four,
                           lc_cough_four=lc_cough_four, lc_headache_four=lc_headache_four,
                           lc_breathing_four=lc_breathing_four, lc_taste_four=lc_taste_four,
                           lc_smell_four=lc_smell_four, lc_brainfog_four=lc_brainfog_four,
                           lc_chestpain_four=lc_chestpain_four, lc_fever_four=lc_fever_four
                           )


@app.route('/predict', methods=['POST'])
def predict():
    age = request.form.get('age')
    sex = request.form.get('sex')
    education = request.form.get('education')
    occupation = request.form.get('occupation')
    height = request.form.get('height')
    weight = request.form.get('weight')
    diabetes = request.form.get('diabetes')
    hypertension = request.form.get('hypertension')
    asthma = request.form.get('asthma')
    tb = request.form.get('tb')
    cancer = request.form.get('cancer')
    covid_severity = request.form.get('covid_severity')
    lc_fatigue_four = request.form.get('lc_fatigue_four')
    lc_cough_four = request.form.get('lc_cough_four')
    lc_headache_four = request.form.get('lc_headache_four')
    lc_breathing_four = request.form.get('lc_breathing_four')
    lc_taste_four = request.form.get('lc_taste_four')
    lc_smell_four = request.form.get('lc_smell_four')
    lc_brainfog_four = request.form.get('lc_brainfog_four')
    lc_chestpain_four = request.form.get('lc_chestpain_four')
    lc_fever_four = request.form.get('lc_fever_four')
    print(age, sex, education, occupation, height, weight, diabetes, hypertension, asthma, tb, cancer, covid_severity,
          lc_fatigue_four,
          lc_cough_four, lc_headache_four, lc_breathing_four, lc_taste_four, lc_smell_four, lc_brainfog_four,
          lc_chestpain_four, lc_fever_four)

    data = [
        [age, sex, education, occupation, height, weight, diabetes, hypertension, asthma, tb, cancer, covid_severity,
         lc_fatigue_four,
         lc_cough_four, lc_headache_four, lc_breathing_four, lc_taste_four, lc_smell_four, lc_brainfog_four,
         lc_chestpain_four, lc_fever_four]]

    columns = ['age', 'sex', 'education', 'occupation', 'height', 'weight', 'diabetes',
               'hypertension', 'asthma', 'tb', 'cancer', 'covid_severity',
               'lc_fatigue_four', 'lc_cough_four', 'lc_headache_four',
               'lc_breathing_four', 'lc_taste_four', 'lc_smell_four',
               'lc_brainfog_four', 'lc_chestpain_four', 'lc_fever_four']

    # Convert to DataFrame
    one_df = pd.DataFrame(data, columns=columns)
    prediction = pipeline.predict(one_df)

    covid = ""
    if prediction == 0:
        covid = "NO (End of Data Collection)"
    elif prediction == 1:
        covid = "YES - Not severe"
    elif prediction == 2:
        covid = "YES - Severe"

    return covid


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))