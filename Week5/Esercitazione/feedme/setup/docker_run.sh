#!/bin/sh

# port 2000 is internal listening port of the container
# change port 8198 with external host listening port

docker run -i -d -p "8198:2000" -t "feed_me"