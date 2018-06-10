# Jenkins Test

**Python version used:** `Python 3.5.2`

**Required Dependencies:**

`apt-get install krb5-config libkrb5-dev libssl-dev libsasl2-dev libsasl2-modules-gssapi-mit python3-dev`


## Generate Jenkins Crumb using following command [OPTIONAL]:

`wget -q --auth-no-challenge --user <USER> --password <PASSWORD> --output-document - 'http://<Jenkins_URL>/crumbIssuer/api/xml?xpath=concat(//crumbRequestField,":",//crumb)'`

*The above command will generate Crumb in the following format:*

`Jenkins-Crumb:<Hash>`

E.g.:

`Jenkins-Crumb:4f538ebe9d8f08d1c3e1a8f72198475f`


## Git Notifications
1. Copy post-commit to `.git/hooks/post-commit`
2. Make it executable  `chmod a+x .git/hooks/post-commit`

Now for every commit this script will be executed.




