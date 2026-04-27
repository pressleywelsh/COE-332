NAME ?= pressleywelsh524

all: clean run check

im-me:
	docker images | grep ${NAME}

ps-me:
	docker ps -a | grep ${NAME}


clean:
	docker compose down

run:
	docker compose up --build -d

check:
	sleep 8
	curl localhost:5000/help
