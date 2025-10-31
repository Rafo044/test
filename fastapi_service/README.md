# Synthetic Supermarket Data Producer

This project provides a synthetic supermarket data generator using SDV (Single Table Gaussian Copula) and exposes a FastAPI endpoint to retrieve the latest generated record. Data is stored in a local SQLite database.

----

### Features

- Generates synthetic supermarket sales data based on `supermarket.csv`  
- Continuously appends new rows to `synthetic.db`  
- Provides a FastAPI endpoint `/latest` to fetch the most recent record  
- Runs in a Docker container for easy deployment 

### Project structure 

```
.
├── Makefile          # Docker build, run, start, stop, remove commands
├── syntheticproducer.py       # Main Python script for data generation and API
├── supermarket.csv   # Raw data used to train SDV synthesizer
```
### How to use :

Build image : 

```
make build
```
Run container :
```
make run
```

### All command :

```
| Command      | Description                                                                   |
| ------------ | ----------------------------------------------------------------------------- |
| `make build` | Build the Docker image (`syntheticimage`)                                     |
| `make run`   | Run the container in detached mode (`syntheticproducer`) and expose port 8000 |
| `make start` | Start the container if it is stopped                                          |
| `make stop`  | Stop the running container                                                    |
| `make rm`    | Remove the container                                                          |
| `make clean` | Remove the Docker image                                                       |

```


### Access control

```
curl http://localhost:8000/latest

```

Response example 
```
[
  {
    "Invoice_ID": 101,
    "Branch": "A",
    "City": "New York",
    "Customer_type": "Member",
    "Gender": "Male",
    "Product_line": "Electronics",
    "Unit_price": 15.5,
    "Quantity": 2,
    "Payment": "Cash"
  }
]
```


### Extending the API

The project currently provides the `/latest` endpoint to fetch the most recent synthetic record.  
You can extend the API by adding new endpoints in `producer.py`. 




