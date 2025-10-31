build:
	 docker build -t syntheticimage .

run:
	 docker run -d -p 8000:8000 --name syntheticproducer syntheticimage

start:
	 docker start syntheticproducer

stop:
	 docker stop syntheticproducer

rm:
	 docker rm syntheticproducer

clean:
	 docker rmi syntheticimage
