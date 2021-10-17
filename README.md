# Youtube Playlist Dashboard

This is a dashboard that displays the information of videos in a Youtube playlist.

Demo site: https://youtube-playlist-dashboard.herokuapp.com/

It is useful to browse the video statistics when you are not the owner of the videos in the playlist. Just enter the playlist url or the playlist id, you will see the dashboard of the videos.

For example, the following shows the playlist dashboard of "Top 50 This Week & Top 100 Songs 2021 (Best New Music Hits Playlist)".

![Example](https://github.com/elvisyjlin/youtube-playlist-dashboard/blob/main/images/example.png)

https://youtube-playlist-dashboard.herokuapp.com/dashboard/PLx0sYbCqOb8TBPRdmBHs5Iftvv9TPboYG

## Requirements

This project is developed in Python 3.8.10. [pyenv](https://github.com/pyenv/pyenv) is recommended for setting up a virtual Python environment.

```bash
pip install -r requirements.txt
```

You will need a Youtube API Key in order to get Youtube video data. Please follow the instructions in [Youtube Data API](https://developers.google.com/youtube/v3/getting-started) to get one. `YouTube Data API v3` is used in this project.

## Usage

### Start the Local Server

Replace `[YOUR_YOUTUBE_API_KEY]` with your Youtube API key in `run.sh` first.

```bash
./run.sh
```

The server is listening on `http://127.0.0.1:5001/`.

### Deploy the Server to Heroku

You can host the service on [Heroku](https://www.heroku.com) easily with a few steps.

1. Create an App in Heroku.
2. Go to `Settings -> Config Vars -> Reveal Config Vars` and set the Youtube API key you created as `YOUTUBE_API_KEY`.
3. Push the repository to your Heroku App with git.
4. The deployment will be done automatically. Enjoy it!
