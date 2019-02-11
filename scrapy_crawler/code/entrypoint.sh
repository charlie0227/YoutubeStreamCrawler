#!bin/bash
scrapy_exe=$(which scrapy)
echo $scrapy_exe, $1
if [ "$1" == "getStreamList" ]; then
    $scrapy_exe crawl getStreamList
elif [ "$1" == "getLiveStats" ]; then
    $scrapy_exe crawl getLiveStats
elif [ "$1" == "getChannelDetail" ]; then
    $scrapy_exe crawl getChannelDetail
elif [ "$1" == "getSearchStream" ]; then
    $scrapy_exe crawl getSearchStream
else
    echo "Not match any condition."
fi