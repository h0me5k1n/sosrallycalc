# MANUAL RUNNING
Clone the project

Create a virtual environment
python3 -m venv env;source env/bin/activate

Install the dependencies
pip install -r requirements.txt

Run the app
python3 app.py

# DOCKER
## Build a docker container
docker build --tag sosrallycalc .

## Run the container
docker run -p 3000:3000 sosrallycalc