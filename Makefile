start:
	sudo docker-compose up
close:
	sudo docker-compose disown
clean:
	sudo docker system prune -af