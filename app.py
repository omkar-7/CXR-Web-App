from flask import Flask, render_template,request
import pickle                                           #Initialize the flask App
app = Flask(__name__)
# model = pickle.load(open('model.pkl', 'rb'))

#default page of our web-app
@app.route('/')
def home():
    return render_template('login.html')

@app.route('/registration')
def registration():
    return render_template('registration.html')

@app.route('/upload_image')
def upload_image():
    return render_template('upload_image.html')

if __name__ == "__main__":
    app.run(debug=True)