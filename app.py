import matplotlib
matplotlib.use("Agg")

from flask import Flask, render_template
from log_analyzer import analyze_log
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route("/")
def index():
    summary, df = analyze_log("logs/server.log")

    if summary["error_frequency"]:
        plt.figure(figsize=(6,4))
        plt.bar(
            summary["error_frequency"].keys(),
            summary["error_frequency"].values()
        )
        plt.xlabel("HTTP Error Code")
        plt.ylabel("Frequency")
        plt.title("HTTP Error Distribution")
        plt.tight_layout()
        plt.savefig("static/error_chart.png")
        plt.close()

    return render_template("index.html", summary=summary)

if __name__ == "__main__":
    app.run(debug=True)
