python -m venv virtualenv
virtualenv\Scripts\Activate.ps1
python.exe -m pip install --upgrade pip
pip install --upgrade setuptools
pip install --upgrade boto3
pip install --upgrade flask
pip install --upgrade aws-flask-swagger-ui
pip install --upgrade black
pip freeze > requirements.txt
deactivate
Remove-Item virtualenv -Recurse
