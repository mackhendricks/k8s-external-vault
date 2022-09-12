#HelloVault Sample App

## Build Image
```
docker build  -t hellovault .
```

## Test Image
Test with Docker
```
docker run -p 5000:5000 --env APP_SERVICE1_API_KEY=afe24243dad --env APP_SERVICE2_API_KEY=fafaw44fff hellovault
```

TODO: Sample Yaml for Deploying -  will build together
