## Server

### Quick start guide

Install dependencies from `requirements.txt` file

```
pip install -r requirements.txt
```

## Running Apache Airflow

Initialize an Airflow database (SQLite)

```
airflow db init
```

Create a user

```
airflow users create     --username {YOUR_USERNAME}     --firstname {YOUR_NAME}     --lastname {YOUR_LAST_NAME}     --role Admin     --email {YOUR_EMAIL}
```

Start an Airflow webserver

```
airflow webserver
```

Start an Airflow scheduler

```
airflow scheduler
```

### Data sources

CoinDesk: https://www.coindesk.com/

Coin Telegraph

Decrypt: https://decrypt.co/

Coinmarketcap: https://coinmarketcap.com/headlines/news/

Developer Tech: https://www.developer-tech.com/
