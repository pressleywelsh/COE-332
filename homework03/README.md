# **Meteorite Landings Data Analysis and Distance Computation**
This homework took the Meteorite_Landings.json dataset, parsed it into a CSV file, and then analyzed it through a variety of functions. We added the great_circle_distance function that was utilized in the main script to compute summary statistics along with compute_average_mass, check_hemisphere, and count_classes. This assignment had a strong emphasis on using proper software engineering practices such as logging, documenting, and unit testing.

## What the program does
The code generates a CSV version of the Meteorite_Landings.json dataset, prints the average meteorite mass, prints the hemisphere classification for each landing, prints the count of each class, and the great_circle_distances between some of the landings. The DEBUG messages throughout are used to track the code.

### ml_data_analysis.py
This is the main analyzing script for this homework, it is where everything is tied together. It loads and parses the meteorite landing dataset, runs all of the computations, and runs the great_circle_distance function.

### test_ml_data_analysis.py
This is the unit test script for ml_data_analysis.py which is included to ensure the individual functions are working correctly. It checks to make sure the correct values are being returned, as well as checking exceptions.

### gcd_algorithm.py
This script contains the great_circle_distance function which takes five float arguments as input: two latitudes, two longitudes, and the radius. The function converts the coordinates to radians, calculates the spherical law of cosines, and then uses that to calculate and return the distance.

### test_gcd_algorithm.py
This is the unit test script for gcd_algorithm.py which is included to ensure the great_circle_distance function is working correctly. It tests two cases and evaluates them using pytest.approx(), tests if identical coordinates return zero, and checks for an error when entering a string.

### Dockerfile
Dockerfile contains all the steps on how to build the image. It makes sure the code is running in python 3.14. It then runs the installer and makes sure the binary is on the path. It initializes a uv project, sets the working directory, and adds pytest and pydantic. It also copies over all the files needed for the homework.

### Data instructions
This homework requires the Meteorite_Landings.json data which can be obtained from NASA. 

### How to run in a container
To build the docker image you run the command: docker build -t <username>/homework03:1.0 ./ 
In order to test if it built correctly you can run docker images to make sure it ran. 
To download the data, you need to run: wget https://raw.githubusercontent.com/tacc/coe-332-sp26/main/docs/unit05/scripts/Meteorite_Landings.json
This will download the data into the homework03 file. The -v used at run time makes our data accessible by creating a volume mount. 
To start the container you call: docker run --rm \
-it \
-v $PWD/Meteorite_Landings.json:/data/Meteorite_Landings.json \
pressleywelsh/homework03:1.0 \
/bin/bash
To run the code, you call: uv run ml_data_analysis.py /data/Meteorite_Landings.json
To run the tests you call: docker run --rm <username>/homework03:1.0 pytest

### Diagram.png
This diagram shows how the user utilizes the VM to build and run the containerized files. The diagram shows the steps of: accessing the vm, using docker to access the container which results in output printed to the user. It shows how the container accesses the Meteorite_Landings.json data using a volume mount.
<img width="499" height="351" alt="Diagram" src="https://github.com/user-attachments/assets/13f4397f-e8a2-47f6-b7e4-522d2dcd9c75" />
