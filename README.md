# Dating app

The project contains 6 tasks with the functionality of the dating app.

## Technical stack, technologies

- Python 3.10
- Django
- Django Rest Framework
- PostgreSQL


## Application API

### 1. Client registration
Creates  new client.
```
POST /api/clients/create
```

**Body**

| Name      | Type    | Description                                 | Required field |
|-----------|---------|---------------------------------------------|----------------|
| email     | Email   | mail                                        | +              |
| name      | Char    | first name                                  | +              |
| surname   | Char    | second name                                 | +              |
| password  | Char    | password                                    | +              |
| gender    | Char    | sex: m(male) or f(female)                   | +              |
| avatar    | Image   | image file                                  | +              |
| longitude | Decimal | coordinate by longitude (min=-180, max=180) | -              |
| latitude  | Decimal | coordinate by latitude (min=-90, max=90)    | -              |

**Response**

| Name    | Description          |
|---------|----------------------|
| success | Successful execution |
| token   | Authorization token  |

### 2. Client matching (Authorization is required)
Clients evaluation. If there is mutual sympathy, then messages are sent to the mail of the clients.
```
POST /api/clients/{id}/match
```
{id} - Another client id

**Response**

Not mutual sympathy

| Name    | Description                                       |
|---------|---------------------------------------------------|
| success | Successful execution                              |
| message | Message about showing sympathy  to another client |

Mutual sympathy with sending emails to the clients email

| Name    | Description                             |
|---------|-----------------------------------------|
| success | Successful execution                    |
| message | Text about sending a letter to an email |


### 3.List of clients
Returns list of clients.
Filtering by gender, name, surname and distance from each other is available.
Only an authorized user can receive lists.
Filtering by distance is offered only to the client with latitude and longitude coordinates.
```
GET /api/list
```

**Query parameters**

| Name     | Description                                                   |
|----------|---------------------------------------------------------------|
| gender   | gender: m(male) or f(female)                                  |
| name     | first name                                                    |
| surname  | second name                                                   |
| distance | maximum distance between clients in miles (for example, 1000) |

**Response**

List os Client. Client model:

| Name      | Type    | Description               |
|-----------|---------|---------------------------|
| email     | Email   | mail                      |
| name      | Char    | first name                |
| surname   | Char    | second name               |
| gender    | Char    | sex: m(male) or f(female) |
| avatar    | Image   | link to the image         |
| longitude | Decimal | coordinate by longitude   |
| latitude  | Decimal | coordinate by latitude    |