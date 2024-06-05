Video Object Tracker

The application monitors objects in the video, records their tracks, and creates a visualization of the track.


## Gitlab
https://github.com/AiwenorAnga/lxns


## Requirements:
- `Python 3.12+`, `pip`, `venv`, `pipenv`


## Setup
```bash
# Virtual env creation and activation
python3.8 -m venv .venv
cd .venv
.\Scripts\activate  # activate venv - win
. bin/activate      # activate venv - linux

# Dependencies installation
.venv/bin/pip install -U pip
.venv/bin/pip install -U pipenv
.venv/bin/pipenv install

## Launching the whole app
Components:
```bash
.venv/bin/python -m app.tracker
# tracks circles and rectangles in a video `luxonis_task_video.mp4` using OpenCV.
# the processed data are stored in .venv/data/ dir.
# if the object is tracked, it has a highlighted outline
.venv/bin/python -m app.presenter
# Presenter class for loading, preparing, and visualizing trajectory data from JSON files.
# Select the data you want to view from dir .venv/data/
# The record of the programs run is in logile.log 
```

## Testing 
- `python -m pytest ./app/tests -v`
- `pytest ./app/tests -k circle_test -v`
- `pytest ./app/tests -k rectangle_test -v`
- `pytest ./app/tests -k presenter_test -v`
- `pytest ./app/tests -k tracker_test -v`