# Receipt Processor Challenge

A Python/Flask-based web service for processing receipts and returning point values based on the following set of rules:
1. One point for every alphanumeric character in the retailer name.
2. 50 points if the total is a round dollar amount with no cents.
3. 25 points if the total is a multiple of 0.25.
4. 5 points for every two items on the receipt.
5. If the trimmed length of the item description is a multiple of 3, multiply the price by 0.2 and round up to the nearest integer. The result is the number of points earned.
6. 6 points if the day in the purchase date is odd.
7. 10 points if the time of purchase is after 2:00pm and before 4:00pm.

## Features

1. **POST** `/receipts/process`  
   Submits a receipt for processing and returns a JSON object containing an `id`.

2. **GET** `/receipts/{id}/points`  
   Retrieves the number of points awarded to the given receipt ID.


## Prerequisites

- Docker (tested with Docker version 20.x or later).

- Python 3.9+ if running locally without Docker (Optional)


## Quick Start (Docker)

1. **Clone this repository (or download the contents)**.

2. **Build the Docker image. In the repository’s root directory (where the `Dockerfile` lives), run**:
   
   ```bash
   docker build -t receipt-processor .
   ```
   
   This will create a Docker image named `receipt-processor`.

3. **Run a container from that image**:
   
   ```bash
   docker run -p 8080:8080 --name receipt-processor-container receipt-processor
   ```
   
   - `-p 8080:8080` maps the container’s port **8080** to **8080** on your host machine.  
   - The service will now be accessible at `http://localhost:8080`.

4. **Test the endpoints**:

   - **Check** that the service is running:
     
     ```bash
     curl http://localhost:8080
     ```
     
     You will likely see a 404 or similar default message, since the root path `/` is not defined.

   - **POST a sample receipt**:
     
     ```bash
     curl -X POST -H "Content-Type: application/json" \
     -d '{
           "retailer": "M&M Corner Market",
           "purchaseDate": "2022-03-20",
           "purchaseTime": "14:33",
           "items": [
             { "shortDescription": "Gatorade", "price": "2.25" },
             { "shortDescription": "Gatorade", "price": "2.25" },
             { "shortDescription": "Gatorade", "price": "2.25" },
             { "shortDescription": "Gatorade", "price": "2.25" }
           ],
           "total": "9.00"
         }' \
     http://localhost:8080/receipts/process
     ```
     
     This will return an ID:
     
     ```json
     { "id": "generated-uuid" }
     ```

   - **GET the points for the returned ID**:
     
     ```bash
     curl http://localhost:8080/receipts/<generated-uuid>/points
     ```
     
     This returns a JSON with the points value, for example:
     
     ```json
     { "points": 109 }
     ```

## Endpoints

1. **POST** `/receipts/process`
   - **Body** (JSON):
     
     ```json
     {
       "retailer": "string",
       "purchaseDate": "YYYY-MM-DD",
       "purchaseTime": "HH:MM",
       "items": [
         { "shortDescription": "string", "price": "string" }
       ],
       "total": "string"
     }
     ```
   
   - **Response** (JSON):
     
     ```json
     { "id": "<receipt-id>" }
     ```

2. **GET** `/receipts/{id}/points`
   - **Response** (JSON):
     
     ```json
     { "points": "<integer>" }
     ```


## Optional: Run Locally (Without Docker)

1. **Install dependencies**:
   
   ```bash
   pip install -r requirements.txt
   ```

2. **Run** the Flask app:
   
   ```bash
   python app.py
   ```
   
   The service starts by default on port **8080**. You can access it at `http://localhost:8080`.


