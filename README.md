steps to start the services
1. cd <path/to/streaming_pipeline>
2. start rabbitmq and elasticsearch first by using command `docker-compose up -d` and wait until it starts
On Terminal One:
3. cd ./ingester
4. run `bash build.sh` if linux/macos else run `docker build -t ingester .`
5. run `docker run -it --name ingester --network streaming_pipeline_default ingester:latest`
On Termial Two:
6. cd ../produce_tweets
7. run `bash build.sh` if linux/macos else run `docker build -t produce_tweets .`
8. run `docker run -it --name produce_tweets --network streaming_pipeline_default produce_tweets:latest`

To get Counts:

1. python get_counts.py - this is in the root folder
