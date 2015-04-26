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

# Installation

```
pip install -r requirements.txt
```

# Running

## Development

```
python ./run.py
```

## Production

```
uwsgi --ini uwsgi.ini
```

Example of `uwsgi.ini`:

```
[uwsgi]
chdir=/opt/qut-tigers-service/
module=simplrapi:app
master=true
pidfile=/var/run/qut-tigers.pid
vacuum=true
max-requests=5000
daemonize=/var/log/uwsgi/qut-tigers.log
socket=/var/run/qut-tigers.sock
processes=2
buffer-size=65535
lazy-app=true
gevent=64
gevent-monkey-patch=true
```

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

## Upload Photo

```
curl -X GET -d "description=Test" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub25jZSI6IjhmN2RhNjc2ZjM4NGI0YmQ0ZWQ3IiwidWlkIjoiNTUzY2FiMjgyMmUxMmUzMGY2MGYwOWZkIiwiZXhwIjoxNDMyNjMxMzM2fQ.e7tPj7l-HZvF6O9Od6dZiwRh7SA6oVDfKpRkdxq1w60" "http://104.236.171.181/0.1/photo_token"
{
    "upload": {
        "token": "OP5dyOhOKgg2H4ozu_8e0iuPl5FV1jvDuQYMIcGa:iiDe_oo_9O4QljZcBmL_Re_MgwQ=:eyJtaW1lTGltaXQiOiJpbWFnZS9wbmc7aW1hZ2UvanBlZyIsImRldGVjdE1pbWUiOjAsImRlYWRsaW5lIjoxNDMwMDQ1MjY0LCJzY29wZSI6InF1dC10aWdlcnMiLCJjYWxsYmFja0JvZHkiOiJoYXNoPSQoaGFzaCkma2V5PSQoa2V5KSZleHRyYT1leUoxYVdRaU9pQWlOVFV6WTJGaU1qZ3lNbVV4TW1Vek1HWTJNR1l3T1daa0lpd2dJbVJsYzJNaU9pQWlWR1Z6ZENKOSIsImNhbGxiYWNrVXJsIjoiaHR0cDovLzEwNC4yMzYuMTcxLjE4MS8wLjEvcGhvdG9fdG9rZW4ifQ==",
        "type": "qiniu_form",
        "url": "http://upload.qiniu.com/"
    }
}
```

```
curl -X POST -F "file=_82574793_davidhowell_getty-624.jpg" -F "token=OP5dyOhOKgg2H4ozu_8e0iuPl5FV1jvDuQYMIcGa:iiDe_oo_9O4QljZcBmL_Re_MgwQ=:eyJtaW1lTGltaXQiOiJpbWFnZS9wbmc7aW1hZ2UvanBlZyIsImRldGVjdE1pbWUiOjAsImRlYWRsaW5lIjoxNDMwMDQ1MjY0LCJzY29wZSI6InF1dC10aWdlcnMiLCJjYWxsYmFja0JvZHkiOiJoYXNoPSQoaGFzaCkma2V5PSQoa2V5KSZleHRyYT1leUoxYVdRaU9pQWlOVFV6WTJGaU1qZ3lNbVV4TW1Vek1HWTJNR1l3T1daa0lpd2dJbVJsYzJNaU9pQWlWR1Z6ZENKOSIsImNhbGxiYWNrVXJsIjoiaHR0cDovLzEwNC4yMzYuMTcxLjE4MS8wLjEvcGhvdG9fdG9rZW4ifQ==" -H "Content-Type:multipart/form-data" "http://upload.qiniu.com"
{
    "status": {
        "description": "Test",
        "id": "553cc19822e12e32e20441ae",
        "timestamp": 1430045080,
        "url": "http://7xis0d.com1.z0.glb.clouddn.com/FnyPxNJdaEonCJP7YRlhiKWwZl7d?imageView2/4/w/320/h/320&e=1430110800&token=OP5dyOhOKgg2H4ozu_8e0iuPl5FV1jvDuQYMIcGa:SaZZK2q0ckItkesCpgHKKguT1Lg=",
        "url_hd": "http://7xis0d.com1.z0.glb.clouddn.com/FnyPxNJdaEonCJP7YRlhiKWwZl7d?e=1430110800&token=OP5dyOhOKgg2H4ozu_8e0iuPl5FV1jvDuQYMIcGa:CAJu7ZIGnuBX3wweHvbYJWvw6CE=",
        "url_large": "http://7xis0d.com1.z0.glb.clouddn.com/FnyPxNJdaEonCJP7YRlhiKWwZl7d?imageView2/4/w/640/h/640&e=1430110800&token=OP5dyOhOKgg2H4ozu_8e0iuPl5FV1jvDuQYMIcGa:1sl-y0ryci-zjZHwMbXwNm6r-C0=",
        "user": "553cab2822e12e30f60f09fd"
    }
}
```

## Get Photo

```
curl -X GET "http://104.236.171.181/0.1/photo/553cc19822e12e32e20441ae"
{
    "status": {
        "description": "Test",
        "id": "553cc19822e12e32e20441ae",
        "timestamp": 1430045080,
        "url": "http://7xis0d.com1.z0.glb.clouddn.com/FnyPxNJdaEonCJP7YRlhiKWwZl7d?imageView2/4/w/320/h/320&e=1430110800&token=OP5dyOhOKgg2H4ozu_8e0iuPl5FV1jvDuQYMIcGa:SaZZK2q0ckItkesCpgHKKguT1Lg=",
        "url_hd": "http://7xis0d.com1.z0.glb.clouddn.com/FnyPxNJdaEonCJP7YRlhiKWwZl7d?e=1430110800&token=OP5dyOhOKgg2H4ozu_8e0iuPl5FV1jvDuQYMIcGa:CAJu7ZIGnuBX3wweHvbYJWvw6CE=",
        "url_large": "http://7xis0d.com1.z0.glb.clouddn.com/FnyPxNJdaEonCJP7YRlhiKWwZl7d?imageView2/4/w/640/h/640&e=1430110800&token=OP5dyOhOKgg2H4ozu_8e0iuPl5FV1jvDuQYMIcGa:1sl-y0ryci-zjZHwMbXwNm6r-C0=",
        "user": "553cab2822e12e30f60f09fd"
    }
}
```

## Post Status

```
$ curl -X POST -d "title=Our First Status~ Hello World~" -d "subtitle=This is my first post" -d "content=Hello World~ Hello World~ Hello World~" -d "photos=553cc19822e12e32e20441ae" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub25jZSI6IjhmN2RhNjc2ZjM4NGI0YmQ0ZWQ3IiwidWlkIjoiNTUzY2FiMjgyMmUxMmUzMGY2MGYwOWZkIiwiZXhwIjoxNDMyNjMxMzM2fQ.e7tPj7l-HZvF6O9Od6dZiwRh7SA6oVDfKpRkdxq1w60" "http://104.236.171.181/0.1/status"
{
    "status": {
        "content": "Hello World~ Hello World~ Hello World~",
        "id": "553d08d022e12e32ef3ceec9",
        "photos": [
            "553cc19822e12e32e20441ae"
        ],
        "subtitle": "This is my first post",
        "timestamp": 1430063312,
        "title": "Our First Status~ Hello World~",
        "user": "553cab2822e12e30f60f09fd"
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
