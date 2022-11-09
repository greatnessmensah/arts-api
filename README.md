# Arts-API

## Getting Started

### Prerequisites

Kindly ensure you have the following installed:
- [ ] [Python 3.6](https://www.python.org/downloads/release/python-365/)
- [ ] [Pip](https://pip.pypa.io/en/stable/installing/)
- [ ] [Virtualenv](https://virtualenv.pypa.io/en/stable/installation/)

### Setting up + Running

1. Clone the repo:

    ```
    $ git clone https://github.com/greatnessmensah/arts-api.git
    $ cd arts-api
    ```

2. With Python 3.6 and Pip installed:

    ```
    $ virtualenv --python=python3 env --no-site-packages
    $ source env/bin/activate
    $ pip install -r requirements.txt
    ```


4. Export the required environment variables:

    ```
    $ export FLASK_APP=app.py
    ```

6. Run the Flask API:

    ```
    $ flask run
    ```

7. Navigate to `http://localhost:5000/{any of the endpoints}` to view the artifact or museum data.

## Contribution

Please feel free to raise issues and I'll get back to you.

You can also fork the repository, make changes and submit a Pull Request
