from flask import Flask, request, render_template
import psycopg2
from psycopg2.extras import RealDictCursor
import os

app = Flask(__name__)

# Use PostgreSQL database from Heroku
DATABASE_URL = os.environ.get("DATABASE_URL")

def get_recommendations(symptoms):
    conn = psycopg2.connect(DATABASE_URL, sslmode="require")  
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute("SELECT * FROM recommendations WHERE symptoms ILIKE %s", ('%' + symptoms + '%',))
    result = cursor.fetchone()
    conn.close()

    return result if result else {
        "precautions": "No data available",
        "doctor": "Consult a General Physician",
        "food": "Eat a balanced diet",
        "avoid": "Avoid junk food",
        "exercise": "Try light exercises",
        "prescription": "Consult a doctor"
    }

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/recommend", methods=["POST"])
def recommend():
    symptoms = request.form.get("symptoms", "").lower()
    recommendations = get_recommendations(symptoms)
    return render_template("index.html", recommendations=recommendations, symptoms=symptoms)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
