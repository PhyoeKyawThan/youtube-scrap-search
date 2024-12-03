from flask import Flask, jsonify, request, render_template
from Generator import URLGenerator

app = Flask(__name__)

@app.route("/search/<string:search_text>")
def search(search_text: str):
    generator = URLGenerator()
    return jsonify(generator.search(search_text=search_text))

@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    search_text = request.form["search-text"]
    generator = URLGenerator()
    generator.search(search_text=search_text)
    return render_template("index.html", videos = generator.get_videos()["search_v_info"])