python -m venv virtualenv
virtualenv\Scripts\Activate.ps1
pip install --upgrade setuptools, pip
pip install --upgrade boto3
pip install --upgrade flask
pip install --upgrade aws-flask-swagger-ui
pip install --upgrade black
pip freeze > requirements.txt
deactivate
Remove-Item virtualenv -Recurse
