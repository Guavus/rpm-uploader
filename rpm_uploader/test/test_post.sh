#!/bin/sh
curl -i -F data=@test_post.sh "http://$(hostname):1234/upload?project=care-reflex&branch=release/1.2.3"
