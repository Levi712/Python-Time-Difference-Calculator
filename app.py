from flask import Flask, render_template, request
from datetime import datetime
import webbrowser
import threading
import os, sys

# ------------------------------
# Handle paths correctly (works after EXE build)
# ------------------------------
if hasattr(sys, "_MEIPASS"):
    BASE_PATH = sys._MEIPASS
else:
    BASE_PATH = os.path.abspath(".")

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_PATH, "templates")
)


# ------------------------------
# Utility function
# ------------------------------
def parse(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d %H:%M")
    except Exception:
        return None


# ------------------------------
# Routes
# ------------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None

    if request.method == "POST":
        d1 = request.form.get("from", "").strip()
        d2 = request.form.get("to", "").strip()

        date_from = parse(d1)
        date_to = parse(d2)

        if not date_from or not date_to:
            error = "Invalid date format. Please enter values correctly."
        elif date_to < date_from:
            error = "End time must be greater than start time."
        else:
            diff = date_to - date_from
            minutes = diff.total_seconds() / 60
            hours = minutes / 60

            result = {
                "minutes": round(minutes, 2),
                "hours": round(hours, 2),
                "days": round(hours / 24, 2),
            }

    return render_template("index.html", result=result, error=error)


# ------------------------------
# Auto-open browser
# ------------------------------
def open_browser():
    webbrowser.open("http://127.0.0.1:5000")


# ------------------------------
# App entry
# ------------------------------
if __name__ == "__main__":
    threading.Timer(0.8, open_browser).start()
    app.run(host="127.0.0.1", port=5000, debug=False)
