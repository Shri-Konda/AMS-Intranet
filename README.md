﻿# AMS-IntraNet

##  1.  Running Local development Server

1.	Go to the path where project is saved, there should be a file named “manage.py”. The path in this case is: <code>C:/inetpub/wwwroot/AMS-Intranet/AMSBIOintranet</code>.
2.	Here, open command prompt by typing “cmd” in the address bar.
3.	Enter the command, <code>python manage.py runserver</code>
4.	The local server will start and could be visited at https://127.0.0.1:8000.
5.  On closing the command prompt the server will stop.

##  2.  Testing Procedures

1.	Go to the path where project is saved, there should be a folder named “functional_tests”. The path in this case is: <code>C:/inetpub/wwwroot/AMS-Intranet/AMSBIOintranet</code>.
2.	Here, open command prompt by typing “cmd” in the address bar.
3.	In the command prompt, enter: <code>C:\ProgramData\Anaconda3\Scripts\activate intranetenv</code> to activate the python environment.
4.	Once activated enter the command, <code>python manage.py test -n functional_tests</code> to run the tests.
5.	The testing should take about 30-35 seconds to finish.

##  3.  Deployment on IIS

###    1.  Required installation 

1.  Install Python(ver=3.7.5) for all users on Windows
2.  Open CMD and install all requirements mentioned in _requirements.txt_ using <code>pip install -r requirements.txt</code>.
3.  After all the libraries are successfully installed, Install _wfastcgi_ and python_dotenv libraries as well, <code>pip install  _wfastcgi_ _python_dotenv_</code><br>
_Note: If error is thrown at the time of installing libraries, try upgrading pip by <code>pip install --upgrade pip</code>, then start from *STEP 2*_
4.  Install *IIS* on Windows

    Enable Internet Information Services (IIS) through the Control Panel:
        Open Control Panel.
        Go to "Programs" and select "Turn Windows features on or off."
        Scroll down and find "Internet Information Services."
        Expand the tree and enable the required features under "Web Management Tools" and "World Wide Web Services."
        Make sure to select "CGI" under "World Wide Web Services."
        Click "OK" to apply the changes.

###    2.  Cloning Project from Git

5.  Navigate to C:/inetpub/wwwroot Open CMD at this location then enter: <code>git clone https://github.com/vaibhavnathj-amsbio/AMS-Intranet.git</code><br>
_Note: Make sure Git is already installed, the above commad will clone/download the project from GitHub_
6.  Navigate to C:/, right-click on Python37, and edit Properties. Under Security, add <code>IIS AppPool\DefaultAppPool</code>. DefaultAppPool is the default app pool.
7.  Repeat *STEP 6* for the Project folder as well, located at *C:/inetpub/wwwroot/AMS-Intranet/AMSBIOintranet*

###    3.  Enabling wfastcgi

7.  Open a CMD terminal as Administrator, and run the command <code>wfastcgi-enable</code><br>
_Note: Before running the command make sure no other wfastcgi app is running in FastCGI module of IIS_

###    4.  Adding web.config
8.  Copy the Python path returned in *STEP 8*, and replace the scriptProcessor="<code>to be filled in</code>" in <code>web.config-template. Or, if using a python virtual enviroment, copy the path from that folder (same for wfastcgi)</code>
9.  If necessary edit the remaining settings in <code>web.config-template</code> then save it as <code>web.config</code> in the _C:/inetpub/wwwroot/_ directory. It should NOT sit inside _AMSBIOintranet/_
    1.  Edit project PYTHONPATH (path to project, should be *C:/inetpub/wwwroot/AMS-Intranet/AMSBIOintranet*)
    2.  Edit WSGI_HANDLER (located in your wsgi.py, should be *AMSBIOintranet.wsgi.application*)
    3.  Edit DJANGO_SETTINGS_MODULE (your settings.py module, should be *AMSBIOintranet.settings*)

###    5.  IIS settings
10. Open Internet Information Services (IIS) Manager. Under connections select the server
11. In the center pane under Management select Configuration Editor
12. Under *Section* select <code>system.webServer/handlers</code>. 
13. Under *Section* select <code> Unlock Section</code>. This is required because the C:/inetpub/wwwroot/web.config creates a route handler for our project.

###    6.  Adding virtual directory for serving static files

14. In order to enable serving static files, create a virtual directory for the site and name it as *static*
15. The Full Path should be: <code>C:/inetpub/wwwroot/AMS-Intranet/AMSBIOintranet/static</code>

###    7.  Bindings

16. Open Bindings for the site and change the port to 81
17. Restart the server and navigate to the website
18. (Optional) If font-awesome/icofont icons are not loading then do the following:
    1.  Open IIS manager
    2.  Navigate to MIME Types
    3.  Actions -> Add
    4.  You will see add MIME Type box and put woff2 extension in the file extension ".woff2" and MIME type as "application/font-woff2" as well.
    5.  Save it and restart the server

###    8.  Configure Database Credentials

1. In the root of your project directory (where `manage.py` is located), create a new file named `.env`.

2. Open the `.env` file in a text editor and add the following lines, replacing the placeholders with your actual database credentials:

    For example:

    ```dotenv
    DB_NAME=mydatabase
    DB_USER=myuser
    DB_PASSWORD=mypassword
    DB_PORT=5432
    ```

3. Security Note:

   Keep the `.env` file in your project's `.gitignore` to avoid accidentally exposing 

###    9.  Find the website at <code>http://localhost:81</code>
