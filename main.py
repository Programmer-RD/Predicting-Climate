from flask import *
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import json
import pickle

app = Flask(__name__)
app.debug = True
app.secret_key = "Ranuga D 2008"


@app.route("/", methods=["POST", "GET"])
def index():
    try:
        if request.method == "POST":
            date = request.form["D"]
            country = request.form["C"]
            countries = json.load(open("./country.json", "r"))
            country = str(country)
            date = date.replace("-", "")
            array = np.array([countries[country], date])
            df = pd.DataFrame(array)
            model = pickle.load(open("model.pkl", "rb"))
            try:
                result = model.predict(df)
            except:
                result = model.predict(df.T)
            print(result)
            flash(f"AverageTemperature : {result[0]} *Prediction may change", "success")
            return redirect("/")
        else:
            countries = json.load(open("./country.json", "r"))
            return render_template("index.html", infos=countries)
    except:
        return abort(505)


if __name__ == "__main__":
    app.run(host="192.168.1.9")
