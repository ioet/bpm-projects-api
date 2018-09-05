BPM Projects API
================

API for BPM Projects

## Getting started
Follow the following instructions to get the project ready to use ASAP:

### Requirements
Be sure you have installed in your system

- [Python version 3](https://www.python.org/download/releases/3.0/) in your path. It will install
automatically [pip](https://pip.pypa.io/en/stable/) as well.
- A virtual environment, namely [venv](https://docs.python.org/3/library/venv.html).

### Install

Thanks to the `requirements.txt` we can install the dependencies using 

```bash
 pip install -r requirements.txt
```

### Usage

Run the project using 

1. For using Flask's development capabilities as the autoloading set this `FLASK_ENV` environment variable
to `development`, i.e.

```bash
export FLASK_ENV=development
```

1. Run the `run` script corresponding to your OS:

* `source run.sh` for Unix based OS
* `start run.bat` for Windows

What it basically does is to set the `FLASK_APP` env variable to the main package and run the app using `Flask`.
If you are an IDE like PyCharm the process is way easier because they support configurations for running Flask projects.

1. The main page provides a nice client to test the API and even  for you to provide your JWT: 
   Click the lock.
1. To get a token, go to `/login` and authenticate with any username and password `secret` (Just for now of course).
1. In the main page you will also find a *Models* section for you to check the schema of the managed resources:
   projects and its metadata.
1. The swagger schema can be found in `/swagger.json`. You can even generate client code for this API thanks to
   this file.  

The use of an IDE is highly recommended, namely PyCharm.

## Built with
- [Python version 3](https://www.python.org/download/releases/3.0/) as backend programming language
- [Flask](http://flask.pocoo.org/) as backend framework
- [Flask RestPlus](https://flask-restplus.readthedocs.io/en/stable/) for building Restful APIs
- [Swagger](https://swagger.io/) for documentation and standardization 


## License

Copyright 2018 ioet Inc. All Rights Reserved.