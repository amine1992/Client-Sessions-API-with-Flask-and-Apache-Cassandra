# API-user sessions
## Description

This project implements a python based REST API server. It uses Apache Cassandra as db-backend. This is intended for big data queries.

We aim to design and implement a **user session service** which consumes events and provides metrics about users sessions. Each user will generate two events, one start event when the session starts and one end event when session is finished. When both events have been received the session is considered complete. 

## Install
To install python dependencies, please run:
```
pip install -r requirements.txt
```

Make sure you run Cassandra in background.
```
sudo service cassandra start
```
## API Specification

We started with the specification of our APIs using **The RESTful API Modeling Language (RAML)** included in specification/userAPIs.raml folder. It helps defining how the API will look like.

## Usage

### Load the data
Run the following command to load the data
```
python manage.py load
```
This commands load the data presented in data folder into cassandra db. It creates 2 tables. 
The data file should in the current directory (same level as the README) called "assignment_data.jsonl"

### Running the app
Run the following command to load the data
```
python manage.py run
```

#### Viewing the app

 Open the following url on your browser to view swagger documentation
```
http://127.0.0.1:5000/
```
The offered documentation makes it straightforward to understand and test the three offered API:
* **user/batches** : insert batches of events. In order to enable the automatic deletion of events older than 1 year, we added a "time to live" condition to each insertion'
```
curl -X POST "http://127.0.0.1:5000/user/batches" -H "accept: application/json" -H "Content-Type: application/json" -d '[{"user_id": "d6313e1fb7d247a6a034e2aadc30ab30", "country": "TIN", "event": "start", "session_id": "674606b1-2270-4285-928f-eef4a6b90a60", "ts": "2019-04-16T20:40:50"},
{"user_id": "d6313e1fb7d247a6a034e2aadc30ab3f", "event": "end", "session_id": "5f933591-8cd5-4147-8736-d6237bef5891", "ts": "2018-11-18T06:24:50"},
{"user_id": "d6313e1fb7d247a6a034e2aadc30ab3f", "event": "start", "session_id": "5f933591-8cd5-4147-8736-d6237bef5891", "ts": "2018-11-16T18:01:37"},
{"user_id": "29bb390d9b1b4b4b9ec0d6243da34ec4", "event": "end", "session_id": "ef939180-692a-4845-aef7-afb03524c2da", "ts": "2018-11-13T10:38:09"},
{"user_id": "a477ecabc3cc455cb1c6d1dab77d8e5c", "country": "GH", "event": "start", "session_id": "4c55263e-66b2-4814-b431-8ca4c1a9dcc8", "ts": "2018-11-29T19:31:43"},
{"user_id": "1ec36a67785046b3bce1dc432fad9129", "country": "SK", "event": "start", "session_id": "3346a60a-0989-4041-aacc-cf6ff44bd151", "ts": "2018-11-16T05:36:16"},
{"user_id": "9595af0063e94cb8a76cb6628c6b80eb", "country": "DE", "event": "start", "session_id": "06830030-d091-428b-87d6-53914d3d2a18", "ts": "2018-11-07T01:18:09"},
{"user_id": "8d0e3cd4a25d4a0895a6c2e13b5bb26a", "event": "end", "session_id": "a78a4889-4bcf-45a7-a4bd-967cc7adf581", "ts": "2018-11-24T02:12:33"}
]'
```
* **/user/last-events**: fetch session starts for the last X days for each country. The result will be: for each country, we'll get the list of events or empty list.
```
curl -X GET "http://127.0.0.1:5000/user/last-events?days=170" -H "accept: application/json"
```
* **/user/last-sessions-user**: fetch last 20 complete sessions for a given user.
```
curl -X GET "http://127.0.0.1:5000/user/last-sessions-user?user_id=d6313e1fb7d247a6a034e2aadc30ab3f" -H "accept: application/json"
```