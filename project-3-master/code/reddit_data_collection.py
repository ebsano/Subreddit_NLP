#!/usr/bin/env python


# This code is inteded for automatization of subreddits requests


#imports
import pandas as pd
import numpy as np
import requests
import time
import datetime
import warnings
import sys


def get_posts(subreddit, n_iter, epoch_right_now): 
    '''takes in subreddit name, the number requests, and current time in epoch
    and returns subreddits in a dataframe. It will make a request every 30 seconds.'''
    # subreddit name and number of times function should run
    # store base url variable
    base_url = 'https://api.pushshift.io/reddit/search/submission/?subreddit='
    # instantiate empty list    
    df_list = []
    # save current epoch, used to iterate in reverse through time
    current_time = epoch_right_now
    # set up for loop
    for post in range(n_iter):
        # instantiate get request
        res = requests.get(
            # requests.get takes base_url and params
            base_url,
            
            # parameters for get request
            params = {
                # specify subreddit
                'subreddit' : subreddit,
                # specify number of posts to pull
                'size' : 100,
                # ???
                'lang' : True,
                # pull everything from current time backward
                'before' : current_time }
        )
        # take data from most recent request, store as df
        df = pd.DataFrame(res.json()['data'])
        
        # pull specific columns from dataframe for analysis
#         df = df.loc[:, ['title',
#                         'created_utc', 
#                         'selftext',
#                         'subreddit',
#                         'author',
#                         'permalink']]
        
        # append to empty dataframe list
        df_list.append(df)
        
        # add wait time
        time.sleep(30)
        
        # set current time counter back to last epoch in recently grabbed df
        current_time = df['created_utc'].min()
        
    # return one dataframe for all requests
    return pd.concat(df_list, axis=0)



# Get The Onion Posts
onion = get_posts('TheOnion', 150, 1601596265)

# Get the news posts
news = get_posts('news', 150, 1601596265)

# concatanate both subreddits
both = pd.concat([onion, news])

# write to file
both.to_csv('onion_news.csv')