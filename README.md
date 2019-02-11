# YoutubeStreamCrawler
a scrapy crawler of youtube live stream

build

```shell
# Docker
docker build -t youtube:latest .
# Docker-compose
docker-compose build
```

usage
1. Pure Docker
```
docker run --rm -v <your-path>/youtube_live_stream:/code youtube sh -c "scrapy crawl getStreamList"
docker run --rm -v <your-path>/youtube_live_stream:/code youtube sh -c "scrapy crawl getLiveStats"
docker run --rm -v <your-path>/youtube_live_stream:/code youtube sh -c "scrapy crawl getChannelDetail"
docker run --rm -v <your-path>/youtube_live_stream:/code youtube sh -c "scrapy crawl getSearchStream"
```
2. Docker-compose
```shell
# build
docker-compose build
# Up & build
docker-compose up (--build)
# Run
docker-compose run --rm crawler getStreamList
docker-compose run --rm crawler getLiveStats
docker-compose run --rm crawler getChannelDetail
docker-compose run --rm crawler getSearchStream
# Down container.
docker-compose down -v
```


cronjob

```
*/5 * * * * /usr/bin/docker run --rm -v <your-path>/youtube_live_stream:/code youtube sh -c "scrapy crawl getStreamList"  1> /dev/null 2> <your-path>/cron.log
*/1 * * * * /usr/bin/docker run --rm -v <your-path>/youtube_live_stream:/code youtube sh -c "scrapy crawl getLiveStats" 1> /dev/null 2> <your-path>/cron.log
*/5 * * * * /usr/bin/docker run --rm -v <your-path>/youtube_live_stream:/code youtube sh -c "scrapy crawl getSearchStream"  1> /dev/null 2> <your-path>/cron.log
0 0 * * * /usr/bin/docker run -v <your-path>/youtube_live_stream:/code youtube sh -c "scrapy crawl getChannelDetail" 1> /dev/null 2> <your-path>/cron.log
```