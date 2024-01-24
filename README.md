## Commands to run

### Docker Build
- docker build -t fetch_flask .  
###  Docker Run 
- docker run -v $(pwd)/:/app/ -p 6000:6000 fetch_flask 


## Testing apis

### As per documentation with the host and port as http://127.0.0.1:6000/

### examples

- http://127.0.0.1:6000/receipts/process with json body.
- http://127.0.0.1:6000/receipts/9c40a074-297e-4c87-adde-b7e251ac48c8/points with appropriate generated id.
