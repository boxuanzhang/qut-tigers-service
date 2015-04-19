# Qut-Tigers Web Service Demo

## Currently Implemented Components

* Flask based structure
* Flask-RESTful based routing and arguments parsing
* mongoengine based models
* JSON Web Token(JWT) based authentication
* redis based request rate limiting(unfinished)
* qiniu based photo uploading(unfinished)

## Currently Implemented Features

* Auth(User) System
* Status(Feed) System

# Feature: Parameters Checking

```
$ curl -X POST "http://0.0.0.0:8000/auth"
{
    "message": "[username]: Missing required parameter in the JSON body or the post body or the query string"
}
```

# Feature: Auth(User) System

## Register (Unfinished, just for testing now)

```
$ curl -X POST -d username=root -d password=root -d name=root "http://0.0.0.0:8000/auth"
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub25jZSI6IjRjOWQ4Yjk3ZGFhNDhjODIxOWZmIiwidWlkIjoiNTUzMzVkMTgxNWRkZDYwYTBmNTRiMGIwIiwiZXhwIjoxNDMyMDIxNTI4fQ.350EHnUoPQtkuxrnC8x3q_HlHN6YvLfJ9vl1pRkbXPg",
    "expire": 1432021528,
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJoYXNoIjoiYmY3ZjAyYjY1YWUwNTc1NzE3MWU2MmFkNWIwODc2MjkwY2FmZTg2OSIsImlkIjoiNTUzMzVkMTgxNWRkZDYwYTBmNTRiMGIxIn0.qwjxFqLdqS7kK2beV4vr1NcxaI8BWRvdLiVuR6pSchk",
    "user": {
        "join_time": 1429429528,
        "name": "root",
        "username": "root"
    }
}
```

## Login

```
$ curl -X GET -d username=root -d password=root "http://0.0.0.0:8000/auth"{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub25jZSI6IjEzNzE4ZjVlMWU1NDIxZmExMzU4IiwidWlkIjoiNTUzMzVkMTgxNWRkZDYwYTBmNTRiMGIwIiwiZXhwIjoxNDMyMDIyNzU1fQ.IkoaORHcJhrl7-EDp-y9_iclGkfpTc7yk9XwWHImmOA",
    "expire": 1432022755,
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJoYXNoIjoiNmY0NTRiMmRmYmMzOTJmZmM4MjcyYzg5NjI5MzVjZGU1NTg5NzllYyIsImlkIjoiNTUzMzYxZTMxNWRkZDYwYTUwYzE3NzkyIn0.DsZeBvDOvVUoqwB-vl88cBkxcvDTbjos1CGysSCenTs",
    "user": {
        "join_time": 1429429528,
        "name": "root",
        "username": "root"
    }
}
```

## Authorization Checking

```
$ curl -X POST -d "title=First Status" -d "subtitle=This is my first post" -d "content=Hello World" "http://0.0.0.0:8000/status"
"Authorization header required”
```

# Feature: Statuses

## Post Status (Photo uploading unfinished)

```
$ curl -X POST -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub25jZSI6IjRjOWQ4Yjk3ZGFhNDhjODIxOWZmIiwidWlkIjoiNTUzMzVkMTgxNWRkZDYwYTBmNTRiMGIwIiwiZXhwIjoxNDMyMDIxNTI4fQ.350EHnUoPQtkuxrnC8x3q_HlHN6YvLfJ9vl1pRkbXPg" -d "title=First Status" -d "subtitle=This is my first post" -d "content=Hello World" -d "photos=" "http://0.0.0.0:8000/status"
{
    "status": {
        "content": "Hello World",
        "id": "55335ea815ddd60a3a972a76",
        "photos": [
            ""
        ],
        "subtitle": "This is my first post",
        "timestamp": 1429429928,
        "title": "First Status",
        "user": "55335d1815ddd60a0f54b0b0"
    }
}
```

## Status List with Full Functional Pagination

```
$ curl -X GET -d _per_page=2 "http://0.0.0.0:8000/status"
{
    "_paging": {
        "after": "MjAxNS0wNC0xOSAwODoxMTo0OC42ODUwMDA=:NTUzMzYzNDQxNWRkZDYwYTUwYzE3Nzkz"
    },
    "statuses": [
        {
            "content": "Hello World",
            "id": "5533634815ddd60a50c17794",
            "photos": [
                ""
            ],
            "subtitle": "This is my first post",
            "timestamp": 1429431112,
            "title": "First Status",
            "user": "55335d1815ddd60a0f54b0b0"
        },
        {
            "content": "Hello World",
            "id": "5533634415ddd60a50c17793",
            "photos": [
                ""
            ],
            "subtitle": "This is my first post",
            "timestamp": 1429431108,
            "title": "First Status",
            "user": "55335d1815ddd60a0f54b0b0"
        }
    ]
}
```

```
$ curl -X GET -d _per_page=2 -d "_after=MjAxNS0wNC0xOSAwODoxMTo0OC42ODUwMDA=:NTUzMzYzNDQxNWRkZDYwYTUwYzE3Nzkz" "http://0.0.0.0:8000/status"
{
    "_paging": {},
    "statuses": [
        {
            "content": "Hello World",
            "id": "55335ea815ddd60a3a972a76",
            "photos": [
                ""
            ],
            "subtitle": "This is my first post",
            "timestamp": 1429429928,
            "title": "First Status",
            "user": "55335d1815ddd60a0f54b0b0"
        }
    ]
}
```

## Get Single Status

```
$ curl -X GET "http://0.0.0.0:8000/status/55335dfb15ddd60a2403fcb1"
{
    "status": {
        "content": "Hello World",
        "id": "55335dfb15ddd60a2403fcb1",
        "photos": [
            ""
        ],
        "subtitle": "This is my first post",
        "timestamp": 1429429755,
        "title": "First Status",
        "user": "55335d1815ddd60a0f54b0b0"
    }
}
```

## Delete Status

```
$ curl -X DELETE "http://0.0.0.0:8000/status/55335dfb15ddd60a2403fcb1"
"Authorization header required”
```

```
$ curl -X DELETE -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub25jZSI6IjRjOWQ4Yjk3ZGFhNDhjODIxOWZmIiwidWlkIjoiNTUzMzVkMTgxNWRkZDYwYTBmNTRiMGIwIiwiZXhwIjoxNDMyMDIxNTI4fQ.350EHnUoPQtkuxrnC8x3q_HlHN6YvLfJ9vl1pRkbXPg" “http://0.0.0.0:8000/status/55335dfb15ddd60a2403fcb1"
```

```
$ curl -X GET "http://0.0.0.0:8000/status/55335dfb15ddd60a2403fcb1"{
    "message": "Not Found",
    "status": 404
}
```
