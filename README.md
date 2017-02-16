# NodeConfig
Tool to configure multiple HSMM-Pi nodes at once

Is able to update SSID and channel settings that would potentially disconnect nodes when changed, by calculating the order to access nodes so that they are only cutoff when they have already been updated.

## Docker Image
A docker image is available at: https://hub.docker.com/r/colinzeidler/nodeconfig/ and can be run with ```docker run -p=5000:5000 colinzeidler/nodeconfig```

## Usage
 1. python app.py
 1. connect to node at port 5000
 1. select nodes to configure, provide login details, and choose new config options

## Libraries in use
 * requests version 2.4.3
  * used to interact with the HSMM-Pi web interface to update a nodes settings
 * flask
  * provides the REST API backend
