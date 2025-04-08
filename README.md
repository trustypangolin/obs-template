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

```dot
digraph architecture {
    rankdir=LR;
    node [shape=box];
    
    User -> API_Gateway [label="HTTP Request"];
    API_Gateway -> Lambda [label="Invoke"];
    Lambda -> GitHub [label="Read Files"];
    GitHub -> Lambda [label="JSON/YAML"];
    Lambda -> API_Gateway [label="Templated JSON"];
    API_Gateway -> User [label="Response"];
    
    {rank=same; API_Gateway Lambda}
}
```

