# **Meteorite Landings Data Analysis and Distance Computation**
This homework took the Meteorite_Landings.json dataset, parsed it into a CSV file, and then analyzed it through a variety of functions. We added the great_circle_distance function that was utilized in the main script to compute summary statistics along with compute_average_mass, check_hemisphere, and count_classes. This assignment had a strong emphasis on using proper software engineering practices such as logging, documenting, and unit testing.

### ml_data_analysis.py
This is the main analyzing script for this homework, it is where everything is tied together. It loads and parses the meteorite landing dataset, runs all of the computations, and runs the great_circle_distance function.

### test_ml_data_analysis.py
This is the unit test script for ml_data_analysis.py which is included to ensure the individual functions are working correctly. It checks to make sure the correct values are being returned, as well as checking exceptions.

### gcd_algorithm.py
This script contains the great_circle_distance function which takes five float arguments as input: two latitudes, two longitudes, and the radius. The function converts the coordinates to radians, calculates the spherical law of cosines, and then uses that to calculate and return the distance.

### test_gcd_algorithm.py
This is the unit test script for gcd_algorithm.py which is included to ensure the great_circle_distance function is working correctly. It tests two cases and evaluates them using pytest.approx(), tests if identical coordinates return zero, and checks for an error when entering a string.

### Data instructions
This homework requires the Meteorite_Landings.json data which can be obtained from NASA. It should be in the directory of the homework02 folder for the script to locate it accurately.

### Obtaining and understanding results
To run the analysis, go to the homework02 folder and enter: "uv run python ml_data_analysis.py". The code generates a CSV version of the Meteorite_Landings.json dataset, prints the average meteorite mass, prints the hemisphere classification for each landing, prints the count of each class, and the great_circle_distances between some of the landings. The DEBUG messages throughout are used to track the code.
