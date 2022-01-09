from searchtweets import ResultStream, gen_rule_payload, load_credentials, collect_results
from datetime import timedelta, date, datetime
from pathlib import Path
import time
import os
import errno
import sys
import requests
import urllib3


class TwitterArchiver(object):

    def __init__(self, account, start_date, end_date, keys):
        self.query = "from:" + account
        self.start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        self.end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        self.results_per_call = 100
        self.days_per_request = 2

        # sleep times 
        self.request_frequency = 53568  # 14.88 hours
        self.connection_error_sleep_time = 3600  # 1 hour
        self.maximum_tweet_sleep_time = 86400  # 1 day

        self.keys = None

        # while loop in case of no internet connection
        while self.keys is None:
            try:
                self.keys = load_credentials(keys, yaml_key="search_tweets_api", env_overwrite=False)
            except urllib3.exceptions.NewConnectionError as e:
                print("NewConnectionError 1")

                # sleep 1 hour
                time.sleep(self.connection_error_sleep_time)

            except urllib3.exceptions.MaxRetryError as e:
                print("MaxRetryError 1")

                # sleep 1 hour
                time.sleep(self.connection_error_sleep_time)

            except requests.exceptions.ConnectionError as e:
                print("ConnectionError 1")

                # sleep 1 hour
                time.sleep(self.connection_error_sleep_time)

    def dateRange(self, start_date, end_date):
        for n in range(int((end_date - start_date).days / self.days_per_request)):
            yield start_date + timedelta(self.days_per_request * n)

    def dateIterator(self):
        return self.dateRange(self.start_date, self.end_date)

    def getTweets(self, date):

        # get to date
        to_date = date + timedelta(self.days_per_request)

        # build rule
        rule = gen_rule_payload(self.query, from_date=str(date), to_date=str(to_date),
                                results_per_call=self.results_per_call)

        # get tweets
        tweets = collect_results(rule, max_results=self.results_per_call, result_stream_args=self.keys)

        return tweets

    def writeResults(self, date, tweets):

        print("Date range:", date, "-", date + timedelta(self.days_per_request - 1))

        currentDir = "./data/"

        # create dates for both days OLD: currentDir = "/home/pi/data/" + str(date.year) + "/" + str(date.month) + "/"
        date2 = date + timedelta(1)
        file1 = currentDir + str(date.year) + "/" + str(date.month) + "/" + str(
            date) + ".txt"  # currentDir + str(tweet.created_at_datetime.date()) + ".txt"
        file2 = currentDir + str(date2.year) + "/" + str(date2.month) + "/" + str(
            date2) + ".txt"  # currentDir + str(tweet.created_at_datetime.date()) + ".txt"

        # create directory if not exists already
        Path(currentDir + str(date.year) + "/" + str(date.month)).mkdir(parents=True, exist_ok=True)
        Path(currentDir + str(date2.year) + "/" + str(date2.month)).mkdir(parents=True, exist_ok=True)

        # create files first (file remains empty if no tweets on that day)
        with open(file1, "a+") as f:
            f.close()
        with open(file2, "a+") as f:
            f.close()

        # check if tweets size is over 100!
        if len(tweets) >= 100:
            # if over 100 then append date to tooManyTweets textfile
            with open("./tooManyTweets.txt", "a+") as f:
                f.write(str(date) + '\n')
                f.close()

        # write tweet to file
        for tweet in tweets:

            # get year month and day as a list
            filedate = str(tweet.created_at_datetime.date()).split("-")
            fileyear = filedate[0]
            filemonth = filedate[1]

            # remove 0 prefix from month string
            if filemonth[0] == "0":
                filemonth = filemonth[1:]

            file = currentDir + fileyear + "/" + filemonth + "/" + str(
                tweet.created_at_datetime.date()) + ".txt"  # currentDir + str(tweet.created_at_datetime.date()) + ".txt"

            # if filepath has not yet been created, create it
            # if not os.path.exists(os.path.dirname(file)):
            #    try:
            #        os.makedirs(os.path.dirname(file))
            #    except OSError as exc:  # Guard against race condition
            #        if exc.errno != errno.EEXIST:
            #            raise

            # write to file
            with open(file, "a+") as f:
                print("Writing:", tweet)
                print("To file:", file)
                f.write(str(tweet) + "\n")
                f.close()

    def archiveTweets(self):

        for date in self.dateIterator():

            date2 = date + timedelta(1)

            currentDir = "./data/"  # + str(date.year) + "/" + str(date.month) + "/"
            file1 = currentDir + str(date.year) + "/" + str(date.month) + "/" + str(
                date) + ".txt"  # currentDir + str(date) + ".txt"
            file2 = currentDir + str(date2.year) + "/" + str(date2.month) + "/" + str(
                date2) + ".txt"  # currentDir + str(date + timedelta(1)) + ".txt"

            # print("Checking:", date, "and", date + timedelta(1))

            # check that date has not already been archived
            if not os.path.isfile(file1) or not os.path.isfile(file2):

                tweets = None
                attempts = 0

                # while loop in case of no internet connection
                while tweets is None:

                    attempts += 1
                    print("Attempts:", attempts)

                    try:
                        # get Tweets
                        tweets = self.getTweets(date)

                        # save tweets
                        self.writeResults(date, tweets)

                        # sleep 14.88 hours
                        time.sleep(self.request_frequency)

                    except urllib3.exceptions.NewConnectionError as e:
                        print("NewConnectionError 2")

                        # sleep 1 hour
                        time.sleep(self.connection_error_sleep_time)

                    except urllib3.exceptions.MaxRetryError as e:
                        print("MaxRetryError 2")

                        # sleep 1 hour
                        time.sleep(self.connection_error_sleep_time)

                    except requests.exceptions.ConnectionError as e:
                        print("ConnectionError 2")

                        # sleep 1 hour
                        time.sleep(self.connection_error_sleep_time)

                    except KeyError as e:
                        print("KeyError - Maximum Tweets Reached")

                        # sleep 1 day
                        time.sleep(self.maximum_tweet_sleep_time)


if __name__ == "__main__":
    twitterArchiver = TwitterArchiver(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    twitterArchiver.archiveTweets()
