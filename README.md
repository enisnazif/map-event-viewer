# Dependencies
This project requires bower for the management of front-end dependencies

# Installation

`cd map-event-viewer`

First, create a virtualenv environment:

`virtualenv env --clear`

Enter this environment:

`source env/bin/activate`

Next, install all dependencies:

`pip install -r requirements.txt` and then
`bower install` to get all front-end dependencies

Finally, to run the app:

First run `export FLASK_APP=map-event-viewer.py` and then run `flask run` and visit `127.0.0.1:5000`

To leave the virtualenv:

`deactivate`
