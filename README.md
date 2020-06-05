# Re Structure API KonfHub

## Running the Project

### Requirements 
- python >= 3.6

```bash
# Clone the repo
git clone git@github.com:ramanaditya/restructure-api-konfhub.git

# Move inside the Project
cd restructure-api-konfhub

# Create Virtual Env and Activating Virtual Env
python3 -m venv venv
source venv/bin/activate

# Installing Dependencies
python -m pip install -r requirements.txt

# Running Application
flask run --host=localhost

# Open Browser using the link http://localhost:5000/
```

## Documentation

### `app.py` File
This file is used for the flask creating backend services and displaying the events on the HTML page


### `api_wrapper.py` File
This file contains `APIWrapper` class contains all the different functions used for the backend services and the tasks.

#### Task 1
To create human readable list of events
Output is saved in `human_readable.txt`

#### Task 2
To bring out the events which are complete duplicates
Output is saved in `exact_duplicates.txt`

#### Task 3
To bring out events semantically similar
Output is saved in `semantic_duplicates.txt`