# bracs-api

bracs-api is a necessary backend component of [bracs](https://github.com/henryjeff/bracs). The respective endpoints within the API are responsible for persisting user and team data along with grabbing existing data in the DB.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install virtualenv.

```bash
pip install virtualenv
```

Once virtualenv is installed, create a bracs-api environment and activate it.
```bash
virtualenv <env-directory>
source <env-directory>/bin/activate
```

Now that the environment is activated, navigate to the cloned bracs-api repository and install the requirements in `requirements.txt`.
```bash
pip install -r requirements.txt
```

The dependencies for bracs-api should now be included in your local environment.

To run the application,
```bash
flask run
```

## Secrets configuration  

As much as we would like to release the production database credentials, we feel that our users would not appreciate that - so, as an alternative, you can set
environment variables that the application will use to configure the API appropriately. We are using [python-dotenv](https://pypi.org/project/python-dotenv/) to manage environment variables. The application looks for the following env variables using `os.environ[<var>]`:
| Variable | Description |
| --- | --- |
| `DB_URI` | The database URI that should be used for the DB connection |
| `DB_USER` | The user accessing the DB |
| `DB_PASS` | The password for the user accessing the DB |
| `DB_NAME` | The name of the database | 

python-dotenv looks for a file called `.env` in the root directory of the project. The values should be given as key-pairs within the `.env` file. Follow the python-dotenv documentation for a full setup walkthrough.

## Usage

By default the API runs on port 5000. The current API endpoints are outlined below.

| HTTP Action | Endpoint |
| --- | --- |
| POST | `/api/post-user` |
| GET | `/api/get-user` |
| POST | `/api/login` |
| POST | `/api/create-team` |
| GET | `/api/get-team` |
| POST | `/api/create-bracket` |
| GET | `/api/get-bracket` |
| GET | `/api/get-user-brackets` |

We recommend installing Postman to test these endpoints out. As we develop the API, the documentation will be updated outlining things like POST data, etc.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
