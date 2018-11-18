# flapi
A bootstrap for App Engine projects with Flask

See it running on App Engine:

Web App: https://gae-flapi.appspot.com/

API: https://api-dot-gae-flapi.appspot.com/

Running the app on local. From the src/ directory execute:

```$ dev_appserver.py api-service/app.yaml web-service/app.yaml```

Clearing the local Datastore

```$ dev_appserver.py --clear_datastore=yes app.yaml```

Deploying to App Engine

```$ gcloud app deploy --project [project] --version [version]```