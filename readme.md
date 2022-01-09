# Twitter Archiver Readme

The code in this repository allows archiving of data from Twitter. The user account, date range, and API keys can be specified from the command line like so: 

`python3 TwitterArchiver.py Tyson_Fury 2011-01-01 2021-01-01 keys/twitter_keys_1.yaml`

The Twitter full-archive API allows 50 free requests a month, therefore Twitter Archiver makes a request every 14.88 hours in order to stay below this limit. However, multiple accounts can be created to circumvent this restriction.

## Prerequisites 

A Twitter developer account needs to be created (https://developer.twitter.com/en/apply-for-access) and a development environment needs to be set up (https://developer.twitter.com/en/account/environments).

Enter the access information into a `.yaml` file in the `/keys` folder. In the folder you will find an example showing how this should be done.

## How to Start

To begin archiving data, you need to run the following command with options:

`python3 TwitterArchiver.py [TWITTER ACCOUNT] [FROM DATE] [TO DATE] [API KEY FILE]`

For example, if I wanted to archive the tweets of Tyson Fury's twitter account (@Tyson_Fury), between the 1st January 2011 and the 1st January 2021, I would run:

`python3 TwitterArchiver.py Tyson_Fury 2011-01-01 2021-01-01 keys/twitter_keys_1.yaml`

Tweet data is stored in the following format:

```
{
   "created_at":"Sun Nov 03 15:37:28 +0000 2013",
   "id":397024737408606208,
   "id_str":"397024737408606208",
   "text":"4 down 6 to go. Then I'm off home to break the wife's jaw. http://t.co/LEX5a6IzuR",
   "source":"<a href=\"http://twitter.com/download/iphone\" rel=\"nofollow\">Twitter for iPhone</a>",
   "truncated":false,
   "in_reply_to_status_id":"None",
   "in_reply_to_status_id_str":"None",
   "in_reply_to_user_id":"None",
   "in_reply_to_user_id_str":"None",
   "in_reply_to_screen_name":"None",
   "user":{...},
   "geo":"None",
   "coordinates":"None",
   "place":"None",
   "contributors":"None",
   "is_quote_status":false,
   "quote_count":569,
   "reply_count":530,
   "retweet_count":12580,
   "favorite_count":15821,
   "entities":{...},
   "extended_entities":{...},
   "favorited":false,
   "retweeted":false,
   "possibly_sensitive":false,
   "filter_level":"low",
   "lang":"en",
   "matching_rules":[...]
}
```

The data will be saved in a text file for each day, in the `/data` folder. Once data has been collected, image data can be downloaded by running the `helper-scripts/image_retriver.py` script with the following command:

`python3 image_retriever.py 2021-11-14 2021-12-16`

If the user created more than 100 tweets for one of the days in the date range you specified, the date in question will be appended to the tooManyTweets.txt file.

## Cronjobs

The startup.sh script was created for the execution of multiple Twitter Archiver instances on start up for an embedded device such as a raspberry pi. See https://www.tomshardware.com/how-to/run-script-at-boot-raspberry-pi for more info.