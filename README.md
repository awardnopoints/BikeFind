Hey guys a few pointers about how this one works, with notes on file structures and so forth

You don't have to install anything to run these files. It's actually designed without that in mind. It's set up to be used with the FLASK_APP commands, like so:

navigate to the top of the file structure and input the following command:

$ FLASK_APP=bikefind.py

This will set your flask install to recognise this as the flask app, allowing the following commands to be input (will overwrite itself when you close the terminal, though).

$ flask run

This launches the web app portion of the project to localhost:5000

$ flask db [options]

This gives access to database commands. Most notably this is useful for migrating to the database, a kind of version control for database changes. For instance, to add tables to the database to match the table classes you've made (in app/models.py) you just go 

$ flask db migrate -m "migrate message"

These controls aren't so important, they're just what's used to run the project as it stands, and the reason for current structure.

webscraper.py, on the top level, contains all the code that's being used to run the application. config.py is where the Flask settings are stored, including the URI for the Database. This is called upon every time a file imports app.db. bikefind.py just imports the app package, it's only there to allow for the flask_app commands.

Within the app/ folder: routes.py organises the front end web content. It's currently just using two boiilerplate templates from the /templates folder, with some flash() features to show off some of the more complex features that flask can do. These probably won't be necessary to implement in our project, though. models.py contains the classes for the database tables. forms.py is similar to routes.py, but for form-specific features. These are used on a login page in the current build, but the principles behind them could be useful for designing the user-interface for the app.
