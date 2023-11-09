# Image Server - A production level http/https server for testing image downloading

## Code Layout
- `conf/**` nginx configurations per instance
- `nginx/**` the rest of the nginx configuration stuff
- `ca/*` created at runtime, CA for https.
- `images/**` created at runtime, images that are served
- `start_http.sh` starts the server in http
- `start_https.sh` starts the server in https
