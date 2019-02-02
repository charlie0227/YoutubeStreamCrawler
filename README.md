# YoutubeStreamCrawler
a scrapy crawler of youtube live stream

build

```
docker build -t youtube:latest .
```

usage

```
docker run --rm -v <your-path>/youtube_live_stream:/code youtube sh -c "scrapy crawl getStreamList"
docker run --rm -v <your-path>/youtube_live_stream:/code youtube sh -c "scrapy crawl getLiveStats"
docker run --rm -v <your-path>/youtube_live_stream:/code youtube sh -c "scrapy crawl getChannelDetail"
docker run --rm -v <your-path>/youtube_live_stream:/code youtube sh -c "scrapy crawl getSearchStream"
```

cronjob

```
*/5 * * * * /usr/bin/docker run --rm -v <your-path>/youtube_live_stream:/code youtube sh -c "scrapy crawl getStreamList"  1> /dev/null 2> <your-path>/cron.log
*/1 * * * * /usr/bin/docker run --rm -v <your-path>/youtube_live_stream:/code youtube sh -c "scrapy crawl getLiveStats" 1> /dev/null 2> <your-path>/cron.log
*/5 * * * * /usr/bin/docker run --rm -v <your-path>/youtube_live_stream:/code youtube sh -c "scrapy crawl getSearchStream"  1> /dev/null 2> <your-path>/cron.log
0 0 * * * /usr/bin/docker run -v <your-path>/youtube_live_stream:/code youtube sh -c "scrapy crawl getChannelDetail" 1> /dev/null 2> <your-path>/cron.log
```