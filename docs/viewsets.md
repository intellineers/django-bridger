# OPTION

The option request describes the upcomming requests for an endpoint:

seqdiag {
  Client -> Server [label = "OPTIONS /model/", leftnote = "Widget Start"];
  Client <- Server [label = "List Metadata"];

  Client -> Server [label = "GET /model/"];
  Client <- Server [label = "List Response", leftnote = "Widget Rendered"];
}

seqdiag {
  Client -> Server [label = "OPTIONS /model/<id:int>", leftnote = "Widget Start"];
  Client <- Server [label = "Instance Metadata"];

  Client -> Server [label = "GET /model/<id:int>"];
  Client <- Server [label = "Instance Response", leftnote = "Widget Rendered"];
}

!!! note "Naming Convention"
    Basically, there are two different Viewsets, the `ModelViewSet` and `RepresentationViewSet`.
    By convention, all classes that inherit from `ModelViewSet` are named `someModelModelViewset` and those that inherit from `RepresentationViewSet` are named `someModelRepresentationViewSet`

    e.g. the viewsets of model `User` will be `UserModelViewSet` and `UserRepresentationViewSet`
