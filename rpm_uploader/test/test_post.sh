#!/bin/sh
curl -i -F data=@test_post.sh data=@test_server.sh "http://$(hostname):1234/upload?dir=care-reflex/release/1.2.3"
