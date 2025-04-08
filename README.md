# obs-template
Create OBS Scene collections


```plantuml
@startuml
component "User" as user
component "API Gateway" as apigw
component "AWS Lambda" as lambda
database "GitHub" as github

user -> apigw : HTTP GET /template
apigw -> lambda : Invoke
lambda -> github : Fetch config.yaml
lambda -> github : Fetch scenes.json
github --> lambda : Files
lambda --> apigw : Templated JSON
apigw --> user : Response
@enduml
```

