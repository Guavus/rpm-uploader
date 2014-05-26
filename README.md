rpm-uploader
============

rpm-uploader is a small webserver that handles rpm upload to a directory and running createrepo on it.

Start server
-----
rpm-uploader --output-dir /var/www/rpms [--port 1234 ] [ --createrepo /usr/bin/createrepo ]

Send to server
------
curl -i -F data=@test_post.sh "http://${HOSTNAME}:1234/upload?dir=care-reflex/release/1.2.3"