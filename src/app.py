import json

from flask import Flask
from flask import request, render_template

from .tasks import retrieve_data_from_playlist


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dashboard/<playlist_id>")
def dashboard(playlist_id):
    # Get parameters
    cache_option = request.args.get("cache", default=True, type=json.loads)
    if cache_option == 0:
        cache_option = False
    # Fetch data
    playlist_url = f"https://www.youtube.com/playlist?list={playlist_id}"
    df, stats = retrieve_data_from_playlist(
        playlist_id,
        save_as_files=cache_option,
        insert_to_db=cache_option,
    )
    # Normalize data
    df["Daily View Count"] = df["Daily View Count"].map("{:,.2f}".format)
    df["Estimated Daily View Count"] = df["Estimated Daily View Count"].map("{:,.2f}".format)
    # df["Like Rate"] = df["Like Rate"].map("{:,.2f}%".format)
    # Render web page
    return render_template(
        "dashboard.html",
        playlist_title=stats["playlist_title"],
        playlist_url=playlist_url,
        stats=stats,
        data=df.to_dict(orient='records'),
    )
