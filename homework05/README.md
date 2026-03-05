# International Space Station Trajectory Data Analysis
This project utilizes a FastAPI application to access ISS state vector data from NASA. It allows the user to retrieve epochs, use query parameters to retrieve parts of the dataset, and compute instantaneous speed. The application is containerized using docker to ensure reproducibility.

### Structure
Dockerfile: Has everything necessary to build and run docker image which runs the FastAPI application
diagram.png: diagram showing how user interacts with API
iss_tracker.py: FastAPI application that requests and processes ISS trajectory data
test_iss_tracker.py: unit tests for iss_tracker.py functions

### Data
The dataset is sourced from the NASA International Space Station Trajectory Data page: https://www.nasa.gov/spot-the-station/#TRAJECTORY 
The project uses the XML Orbit Ephemeris Message which contains ISS state vectors at 4 minute intervals over 15 days. The iss_tracker.py retrieves the xml at runtime using the requests library.

### How to build and run a container
To build the container you need to run: ``` docker build -t username/homework05:1.0 ./ ```
In order to test if it built correctly you can run ``` docker images ``` to make sure it ran. 
After this to run the container you should run: ``` docker run --name "homework05" -d -p 8000:8000 username/homework05:1.0 ```
To get full list of epochs, you run: ``` curl localhost:8000/epochs ```
To get a specific epoch, you run: ``` curl localhost:8000/epochs/<epoch> ```
To retrieve speed for a specific epoch, you run: ``` curl localhost:8000/epochs/<epoch>/speed ```
To retrieve epoch closest to now and its instantaneous speed, you run: ``` curl localhost:8000/now ```

### Outputs
``` /epochs ```
Returns full list of state vectors.
``` /epochs?limit=int&offset=int ```
Returns a part of dataset according to query parameters.
``` /epochs/<epoch> ```
Returns the state vector of the specified epoch.
``` /epochs/<epoch>/speed ```
Returns the instantaneous speed of the specified epoch.
``` /now ```
Returns the state vector closest to the current time along with its instantaneous speed.
