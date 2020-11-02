# Fedora

The purpose of this document is to outline steps required to run and develop ProjectQuay on Fedora.

## Local Development

Note: The following steps were tested on Fedora 33.

First, grab a copy of Quay and install all Python dependencies.

```
# Install System Packages
sudo dnf install libpq-devel python3-devel libffi-devel openldap-devel zlib-devel libjpeg-turbo-devel

# Fetch Quay's Source Code
git clone quay
cd quay

# Create and Activate a Python Virtual Environment for Quay
python -m venv ./venv
source ./venv/bin/activate

# Install Quay's Python Dependencies
pip install --upgrade pip
pip install setuptools==45  # work-around for 'https://github.com/pypa/setuptools/issues/2017'
pip install -r requirements.txt  # Run-time Dependencies
pip install -r requirements-dev.txt
```

Then, install all front-end (JavaScript) dependencies.

```
sudo dnf install npm
npm install --ignore-engines
mkdir -p static/ldn static/fonts static/webfonts
python external_libraries.py
npm run watch
```

Finally, open two separate terminal windows and run the following processes in each:
```
python -m application  # backend
npm run watch  # front-end code
```

The application should be available at [localhost:5000](http://localhost:5000)
