rpm-uploader
============

rpm-uploader is a small webserver that can take post 



Start server
rpm-uploader --output-dir /var/www/rpms [--port 1234 ] [ --dir release/2.1.3 ] [ --createrepo /usr/bin/createrepo ]


curl -i -F data=@test_post.sh "http://${HOSTNAME}:1234/upload?project=care-reflex&branch=release/1.2.3"