# Options

The option request describes the upcomming requests for an endpoint:

seqdiag {
  Client -> Server [label = "OPTIONS /model/"];
  Client <- Server [label = "List Metadata"];

  Client -> Server [label = "GET /model/"];
  Client <- Server [label = "List Response"];
}


<!-- seqdiag {
  browser  -> webserver [label = "GET /index.html"];
  browser <-- webserver;
  browser  -> webserver [label = "POST /blog/comment"];
              webserver  -> database [label = "INSERT comment"];
              webserver <-- database;
  browser <-- webserver;
} -->