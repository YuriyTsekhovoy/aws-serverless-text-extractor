# Text Extractor API 


## Use Cases

Exteracts text from files in ```pdf```, ```png```, ```jpeg```, ```tiff``` formats using AWS Textract. 

Client makes a ```POST``` request containing a ```callback_url``` as a request body parameter to ```/files``` API Endpoint. AWS Lambda function generates file uuid and stores it together with ```callback_url``` in a DynamoDB table. The function returns response with an ```upload_url``` to an S3 Bucket. 

Once Client uploads the file using ```upload_url```, Lambda function is called. File is processed by AWS Textract and DynamoDB file record is updated with text info. 

Once DynamoDB file record is updated, a function to make callback is triggered. It sends the text information to the callback_url specified by Client. 

Client can also make a GET request containing ```file_id``` to the ```/files/{file_id}``` endpoint to receive the information extracted from the uploaded file. 

## API Endpoints: 

```
POST /files
```
Accepts callback_url for receiving callback when extracting will be ended, and returns upload_url for uploading files

**Request Parameters:**
```callback_url```

**Response Parameters:** 
```upload_url```

---
```
GET /files/{file_id}
``` 
Returns information about text extraction results for specified file 

**Request Parameters:**
```file_id```

**Response Parameters:** 
```file_id```
```text```

## Deploy to AWS

```
$ sls deploy --org your-org --app your-app
```

### Example POST Request

```
curl -X POST https://xxxxxxxxxxxx.amazonaws.com/dev/files -d '{"callback_url": "example.com"}' -H "Content-Type: application/json"
```

### Example GET Request
```
curl -X GET https://xxxxxxxxxxxx.amazonaws.com/dev/files/file_id 
```
