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


## Usage

By default the application runs on port 5000. The current API endpoints are outlined below.

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
