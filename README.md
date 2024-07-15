## Web-Scraper

web scraper is fun project to scrap data from website.

## How to install?

Its simple have create make file so you dont need to remember all commands

Just run following command to run it locally.

```shell
make install
```

## How to run?

Using following command to run code locally

```shell
make run
```

## How to create docker image?

Using following command to build docker image

```shell
docker build -t web-scraper .
```

## Requirements

- python==3.12
- aiohttp==3.9.5
- aiohttp-retry==2.8.3
- beautifulsoup4==4.12.3
- fastapi==0.111.0
- html5lib==1.1
- pysondb==1.6.7

## Request and response

To scrap data you need to make post request to `http://localhost:8000/scrap_data` with required body parameter

In the response you will get trace id of backgroud task which will run scraping process and and the end user will get notification.

### sample curl

```shell
curl --location 'http://localhost:8000/scrap_data/' \
--header 'X-Access-Token: bWc4eDJ6am1kamwzeTc2ZjdvZWt5bDRuMHVpNmp2Yjlicnc0czBpZm9pOXlzemxrc3pldm43Mmt2Ym12bnFyZnpxeThkdm82d3E5bWZkZWNzMG85YjMzZ3k4enRxYW16eWQyNzk3bmlhN3YwMTcxNnBzM29tOXM4bWdzbjd5cjY=' \
--header 'Content-Type: application/json' \
--data '{
    "after": 1,
    "size": 1
}'
```

### sample response

```json
{
  "success": true,
  "message": "scrapping job scheduled successfully with requestId 'a47f8025-df2b-47e5-affc-773ce152addb'. Notification will be received on 'rahulahir4530@gmail.com' on job completion",
  "trace_id": "a47f8025-df2b-47e5-affc-773ce152addb"
}
```

Notification log

```
NOTIFICATION!! To:3f50b493-e93b-4eb7-bd49-7a32c4652361. Successfully Scraped data!, payload: {'created_count': 0, 'updated_count': 0, 'fetched_count': 24}
```

## Thanks

Made with love by `Rahul Chocha`
