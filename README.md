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

1. Run the app from your terminal, i.e.

```
python bpm-projects-api/app.py
```

The use of an IDE is highly recommended, namely PyCharm.

## Built with
- [Python version 3](https://www.python.org/download/releases/3.0/) as backend programming language
- [Flask](http://flask.pocoo.org/) as backend framework
- [Flask RestPlus](https://flask-restplus.readthedocs.io/en/stable/) for building Restful APIs
- [Swagger](https://swagger.io/) for documentation and standardization 


## License

IOET Inc. all rights reserved.