build:
<<<<<<< HEAD
	docker build -t cmd2 .
run:
	docker run -it -d -p 8000:80 -v /docker/data:/data -v /docker/nginxsite:/etc/nginx-site-enabled -v /docker/nginxlog:/var/log/nginx cmd2
=======
	docker build -t cmd1 .
run:
	docker run -it -d cmd1
>>>>>>> abaac120221b5f8f2b2ad7aaf1801eb48c64cc68
ps:
	docker ps -a
img:
	docker images
rm:
	docker rm -f $$(docker ps -aq)
rmi:
<<<<<<< HEAD
	docker rmi $$(docker images -q)
=======
	docker rmi $$(docker images -q)

>>>>>>> abaac120221b5f8f2b2ad7aaf1801eb48c64cc68
