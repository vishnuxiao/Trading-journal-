from flask import Flask, render_template, request, redirect
import pandas as pd
from datetime import datetime
import os

app = Flask(name)
data_file = "journal.csv"

# Initialize CSV if it doesn't exist
if not os.path.exists(data_file):
    df = pd.DataFrame(columns=["date", "outcome"])
    df.to_csv(data_file, index=False)

@app.route("/", methods=["GET", "POST"])
def index():
    df = pd.read_csv(data_file)
    if request.method == "POST":
        date = request.form["date"]
        outcome = float(request.form["outcome"])
        df = pd.concat([df, pd.DataFrame({"date": [date], "outcome": [outcome]})])
        df.to_csv(data_file, index=False)
        return redirect("/")

    # Prepare monthly totals
    df['month'] = pd.to_datetime(df['date']).dt.to_period('M')
    monthly_totals = df.groupby('month')['outcome'].sum().to_dict()

    return render_template("index.html", entries=df.to_dict(orient="records"), monthly_totals=monthly_totals)

if name == "main":
    app.run(host="0.0.0.0", port=5000, debug=True)
