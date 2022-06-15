from flask import Flask, render_template, url_for, flash, redirect
from flask import request
from flask import send_from_directory
from flask_socketio import SocketIO

import numpy as np
import tensorflow
from tensorflow import keras
import tensorflow as tf
import os
from PIL import Image


app=Flask(__name__,template_folder='template')
#app = Flask(__name__, template_folder='template')
#socketio = SocketIO(app)

# RELATED TO THE SQL DATABASE
app.config['SECRET_KEY'] = "UddA58IkCqP5nZkwEzA7YA"
#app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"



dir_path = os.path.dirname(os.path.realpath(__file__))

UPLOAD_FOLDER = 'uploads'
STATIC_FOLDER = 'static'


# global graph
# graph = tf.get_default_graph()
model = tensorflow.keras.models.load_model('./model/model.h5')
model1 = tensorflow.keras.models.load_model("./model/pneumonia.h5")
model2 = tensorflow.keras.models.load_model("./model/Covid_model.h5")

#tuberculosis
def api(full_path):
    #with graph.as_default():
    pp_img = keras.preprocessing.image.load_img(full_path, target_size=(
        500, 500), color_mode='grayscale')
   # pp_img = image.img_to_array(img)
    pp_img = np.expand_dims(pp_img, axis=0)
    pp_img = pp_img * 1.0/ 255
    # with graph.as_default():
    predicted = model.predict(pp_img)        #vấn đề ở dòng này
    return predicted

#pneumonia
def api1(full_path):
    #with graph.as_default():
    data = keras.preprocessing.image.load_img(full_path, target_size=(224, 224, 3))
    data = np.expand_dims(data, axis=0)
    data = data * 1.0/ 255
    # with graph.as_default():
    predicted = model1.predict(data)
    return predicted

#Covid-19
def api111(full_path):
    #with graph.as_default():
    data = keras.preprocessing.image.load_img(full_path, target_size=(224, 224, 3))
    data = np.expand_dims(data, axis=0)
    data = data * 1.0/ 255

    # with graph.as_default():
    predicted = model2.predict(data)
    return predicted

# tuberculosis
@app.route('/upload', methods=['POST', 'GET'])
def upload_file():
    #with graph.as_default():

    if request.method == 'GET':
        return render_template('tuberculosis.html')
    else:
        try:
            file = request.files['image']
            full_name = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(full_name)
           # indices = {0: 'Tuberculosis_Infected', 1: 'Healthy'}
            result = api(full_name)
            print(result)
            predicted_class = np.asscalar(np.argmax(result, axis=1))
            accuracy = round(100 - result[0][predicted_class] * 100, 2)
            if result >= 0.5:
                out = ('Đây là 1 trường hợp bị lao phổi')
            else:                                                                                                                
                out = ('Đây là trường hợp khỏe mạnh')
            if accuracy<85:
                prediction = "Hãy kiểm tra lại với bác sĩ"
            else:
                prediction = "Kết quả là chính xác"
            return render_template('tuberculosispredict.html', image_file_name=file.filename, label=out, accuracy=accuracy, prediction=prediction)
        except:
            flash("Làm ơn hãy chọn ảnh trước", "danger")
            return redirect(url_for("tuberculosis"))
#Pneumonia
@app.route('/upload11', methods=['POST', 'GET'])
def upload11_file():
    #with graph.as_default():

    if request.method == 'GET':
        return render_template('pneumonia.html')
    else:
        try:
            file = request.files['image']
            full_name = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(full_name)

            indices = {1: 'Khỏe mạnh', 0: 'Bị ảnh hưởng bởi viêm phổi'}
            result = api1(full_name)

            predicted_class = np.asscalar(np.argmax(result, axis=1))
            accuracy = round(result[0][predicted_class] * 100, 2)
            label = indices[predicted_class]
            if accuracy < 85:
                prediction = "Hãy kiểm tra lại với bác sĩ"
            else:
                prediction = "Kết quả là chính xác"

            return render_template('pneumoniapredict.html', image_file_name=file.filename, label=label, accuracy=accuracy,
                                   prediction=prediction)
        except:
            flash("Làm ơn hãy chọn ảnh trước", "danger")
            return redirect(url_for("Pneumonia"))


#Covid-19
@app.route('/upload111', methods=['POST', 'GET'])
def upload111_file():
    #with graph.as_default():

    if request.method == 'GET':
        return render_template('corona.html')
    else:
        try:
            file = request.files['image']
            full_name = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(full_name)

            indices = {1: 'Khỏe mạnh', 0: 'Bệnh nhân đã bị nhiễm covid 19'}
            result = api111(full_name)

            predicted_class = np.asscalar(np.argmax(result, axis=1))
            accuracy = round(result[0][predicted_class] * 100, 2)
            label = indices[predicted_class]
            if accuracy<85:
                prediction = "Hãy kiểm tra lại với bác sĩ"
            else:
                prediction = "Kết quả là chính xác"

            return render_template('coronapredict.html', image_file_name = file.filename, label = label, accuracy = accuracy, prediction=prediction)
        except:
            flash("Làm ơn hãy chọn ảnh trước", "danger")
            return redirect(url_for("covid_19")) 
'''@app.route('/upload111', methods=['POST', 'GET'])
def upload111_file():
    #with graph.as_default():

    if request.method == 'GET':
        return render_template('corona.html')
    else:
        try:
            file = request.files['image']
            full_name = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(full_name)

            indices = {1: 'Khỏe mạnh', 0: 'Bệnh nhân đã bị nhiễm covid 19'}
            result = api111(full_name)

            predicted_class = np.asscalar(np.argmax(result, axis=1))
            accuracy = round(esult[0][predicted_class] * 100, 2)
            label = indices[predicted_class]
            if accuracy<85:
                prediction = "Hãy kiểm tra lại với bác sĩ"
            else:
                prediction = "Kết quả là chính xác"

            return render_template('coronapredict.html', image_file_name = file.filename, label = label, accuracy = accuracy, prediction=prediction)
        except:
            flash("Làm ơn hãy chọn ảnh trước", "danger")
            return redirect(url_for("covid_19"))     '''


@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

#Initial Home Page

@app.route("/signup")
def signup():
    return render_template("home.html")

@app.route("/")
@app.route("/login")
def login():
    return render_template("home.html") 


@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/covid_19")
def covid_19():
    # if form.validate_on_submit():
    return render_template("corona.html")

@app.route("/tuberculosis")
def tuberculosis():
    return render_template("tuberculosis.html")

@app.route("/Pneumonia")
def Pneumonia():
    return render_template("pneumonia.html")


if __name__ == "__main__":
    app.run(debug=True)
