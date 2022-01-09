import re
import sys
from datetime import timedelta, date, datetime
import ast
import json
import requests
import time

class ImageRetriever(object):
    
    def __init__(self, start_date, end_date):
        self.start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        self.end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        self.days_per_request = 2
        
    def dateRange(self, start_date, end_date):
        for n in range(int((end_date - start_date).days / self.days_per_request)):
            yield start_date + timedelta(self.days_per_request*n)

    def dateIterator(self):
        return self.dateRange(self.start_date, self.end_date)
        
    def getImageURL(self, text):
        '''finds image urls'''
        return re.finditer(r'(http|https):\/\/([a-zA-Z0-9-._~:/?#\[\]@!$&\'()*+,;%=])+.(png|gif|jpg)', text) 

    def retrieveImages(self):
        
        #set data filepath
        data_dir = "../data/"
        
        #parse files
        for date in self.dateIterator():
            
            tweet_file = data_dir + str(date.year) + "/" + str(date.month) + "/" + str(date) + ".txt"
            print("opening:",tweet_file)
            

            #open file
            with open (tweet_file, "r") as data:
                file_text=data.read()

            #search for images
            results = self.getImageURL(file_text)

            #download images
            for result in results:
                image_url = str(result.group(0))
                print(image_url)
                image_data = requests.get(image_url).content
                image_filename = image_url.split("/")
                image_filepath = "../image/" + image_filename[-1]
                with open(image_filepath, 'wb') as handler:
                    handler.write(image_data)
                time.sleep(0.5)
            
            print("DONE\n\n")
            
            
            
if __name__ == "__main__":
    imageRetriever = ImageRetriever(sys.argv[1], sys.argv[2])
    imageRetriever.retrieveImages()
