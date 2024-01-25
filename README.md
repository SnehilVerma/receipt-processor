## Commands to run - ( Assuming the env is unix/linux based )

### Docker Build
- docker build -t fetch_flask .  
###  Docker Run 
- docker run -v $(pwd)/:/app/ -p 6000:6000 fetch_flask 

## Testing apis

### As per documentation with the host and port as http://127.0.0.1:6000/

### Endpoint examples

- http://127.0.0.1:6000/receipts/process with json body.
- http://127.0.0.1:6000/receipts/9c40a074-297e-4c87-adde-b7e251ac48c8/points with appropriate generated id.


### Important modifications to retailer regex in validation schema
- Updated retailer name regex from "^\\S+$" to "^[\\S ]+$", to support retailer names with spaces, as provided in the example 
"M&M Corner Market".


### Schema validation
'receipt_schema_2.json' file contains the json schema which is used to validate the input sent in the request, and error is thrown if the input json for the receipt is invalid.

### Yaml configuration
'config.yaml' file has a few config properties for log and schema file. This is to ensure the code is not modified if these files are changed.

### Logging
Logger has been added for console logs and the logs are also pushed onto a file - 'requests.log'. But for ease of log maintenance the log file is flushed at each app run.