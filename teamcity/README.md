# Teamcity Test

**Python version used:** `Python 3.5.2`

**Required Dependencies:**

`apt-get install krb5-config libkrb5-dev libssl-dev libsasl2-dev libsasl2-modules-gssapi-mit python3-dev`

## Virtual environment installations

`apt-get install virtualenv`

OR

`pip install virtualenv`

The above command will install virtual environment

**Create a cirtual environment:** `virtualenv venv`

**Activate virtual environment:** `source venv/bin/activate`

**Execute Python script:** `python <python file>` e.g. `python last_dir_processed.py`


## Git Notifications
1. Copy post-commit to `.git/hooks/post-commit`
2. Make it executable  `chmod a+x .git/hooks/post-commit`

Now for every commit this script will be executed.

**NOTE:** Just adding folder wont help in above script. There has to be at least one
empty file inside the folder created, like `test_2` folder has `test.txt`. Then
only it will be available for `git add` and `git commit` commands.





