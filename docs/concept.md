The main concept of django bridger is to leverage preflight OPTION requests and automatically assemble a frontend, based on the model, the serializer and the viewset.

### Frontend

The frontend is a react based desktop like application that populates itself with OPTION requests. Each OPTION requests describes the upcoming request:

* Is it a list or an instance?
* What fields are available?
* What filters are available?
* Can something be searched?
* Can something be ordered?
* Are there buttons that should open something?
