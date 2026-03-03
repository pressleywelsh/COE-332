# International Space Station Trajectory Data Analysis
This project downloads an XML of ISS state vector data from NASA using the requests library, and represents it through a Pydantic model. It then analyzes it through various functions such as time range, velocity calculation, and instantaneous and average speed across the dataset. We used software engineering and design practices such as containerizing, logging, documenting, and unit testing.

### Data
The dataset is sourced from the NASA International Space Station Trajectory Data page: https://www.nasa.gov/spot-the-station/#TRAJECTORY 
The project uses the XML Orbit Ephemeris Message which contains ISS state vectors at 4 minute intervals over 15 days. The iss_tracker.py downloads the xml through requests at runtime, so the data isn't in this repository.

### How to build and run a container
To build the container you need to run: ``` docker build -t username/homework04:1.0 ./ ```
In order to test if it built correctly you can run ``` docker images ``` to make sure it ran. 
After this to run the container you should run: ``` docker run --rm -it username/homework04:1.0 /bin/bash ```
To run the code, you run: ``` uv run iss_tracker.py ```
To run the tests, you run: ``` uv run pytest ```

### Outputs
When the code is executed, it outputs information summarizing the ISS data. Example output: 
```
The data spans from 2026-054T12:00:00.000Z to 2026-069T12:00:00.000Z
Closest epoch to now is: EPOCH='2026-055T06:32:00.000Z' X=-321.921914099372 Y=5077.30191532368 Z=-4527.13075764741 X_DOT=-6.50548267615531 Y_DOT=2.43242609490043 Z_DOT=3.19173698613554
Average speed over data is: 7.657057078994583
Instantaneous speed closest to now: 7.643636997239926
```
The first line is showing the time range of the dataset.
The second line is printing out the full vector of the epoch closest to now (when the code is executed). 
The third line is the average speed which is the average magnitude of ISS velocity components over the entire dataset.
The last line is the instantaneous speed which is the magnitude of the ISS velocity components taken from the closest to now row.
