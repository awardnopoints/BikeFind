### BikeFind

**Basic instructions for use:**

After installing the application using pip install, the following commands can be used to control the application.

*bf_display* will run the app.py module loading the web page.

*bf_scrape* will run the webscraper.py module, updating the DB with information from the APIs.


**Basic structure for this project:**

*/*

.gitignore --> List of files not to be pushed to GitHub.

MANIFEST.in --> Instructions for installing non-python module files

requirements.txt --> Necessary packages to run the app

scriptTests.zip --> Archive of redundant modules

setup.py --> Installs the app

sqlScripts.txt --> Basic sql command for viewing bike data by day/time, 

.travis.yml --> Config file for Travis CI

webscraper.log --> Log of errors encountered by webscraper.py

*/backups/*

all --> CSV backups of databases

*/bikefind/*

appendToDynamic.py --> Module for updating dynamicData from CSV

app.py --> Central application, reads data from DB and runs web page from the static/ and template/ files. Handles POST and GET requests from front end.

dbClasses.py --> Classes for all tables in the DB, including staticData, currentData, dynamicData, weatherData, and chartData. Used by webscraper.py when writing to DB.

__init__.py --> Makes bikefind/ a package.

linearRegression.py --> Module for loading the linear model from objects/ and applying it to forecast data

saveData.py --> Records DB table as CSV

webscraper.log --> Same as webscraper.log from upper level

webscraper.py --> Main module for updating DB. Runs continuously on AWS Instance, checking APIs at regular intervals and updating all dynamically updated tables (dynamicData, currentData, weatherData, forecastData)

*/bikefind/objects/*

features.p --> Pickle object containing a list of features from the linear regression model.

model.p --> Pickle object containing the linear regression model.

*/bikefind/static/*

script.js --> JavaScript for the web page.

*/bikefind/templates/*

index.html --> HTML for the web page.

*/docs/*

Linear Regression Model.ipynb --> Jupyter Notebook for building linear regression model and saving it to a pickle file.

Making Predictions.ipynb --> Jupyter Notebook demo-ing the linear regression model.

Predictive Table Charts.ipynb --> Jupyter Notebook that uses the Random Forest Model to generate data for chartData table.

Random_Forest_Model.ipynb --> Jupyter Notebook for building Random Forest Classification Model.

*/tests/*

__init__.py --> Makes the test folder a package for pytest

test_basic.py --> Module containing a set of tests to be run by pytest, either manually with >>>pytest test_basic.py or automatically by Travis CI whenever a push is made to GitHub.



Version control policy:

Please don't directly add new features to the master branch.
When adding features, please create a new branch (with a relevant name)
and add/test out the new feature there. Then, when the feature is working
properly on the new branch, merge it with the master branch.
