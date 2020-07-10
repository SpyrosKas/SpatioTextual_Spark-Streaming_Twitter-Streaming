#!/usr/bin/env python

import tweepy
from tweepy.auth import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import socket
import json
import pickle
import struct

# request to get credentials at http://developer.twitter.com
consumer_key    = ''
consumer_secret = ''
access_token    = ''
access_secret   = ''

# we create this class that inherits from the StreamListener in tweepy StreamListener
class TweetsListener(StreamListener):

    def __init__(self, csocket):
        self.client_socket = csocket
    # we override the on_data() function in StreamListener
    def on_data(self, data):
        try:
            message = json.loads( data )
            if message['geo']:
                latitude, longitude = message['geo']['coordinates']
                print( message['text'] )
                data_all = "fadsljhklasdghjlksadfjhglsadhjg||||"
                print(latitude, longitude)
                # cords = { "latitude": str(latitude), "longitude": str(longitude)}
                self.client_socket.send( data.encode('utf-8') )
            return True
            
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True
        

    def if_error(self, status):
        print(status)
        return True


def send_tweets(c_socket):
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    
    twitter_stream = Stream(auth, TweetsListener(c_socket))
    twitter_stream.filter(locations=[-180,-90,180,90]) # this is the topic we are interested in



if __name__ == "__main__":
    new_skt = socket.socket()         # initiate a socket object
    host = "127.0.0.1"     # local machine address
    port = 5555                 # specific port for your service.
    new_skt.bind((host, port))        # Binding host and port

    print("Now listening on port: %s" % str(port))

    new_skt.listen(5)                 #  waiting for client connection.
    c, addr = new_skt.accept()        # Establish connection with client. it returns first a socket object,c, and the address bound to the socket

    print("Received request from: " + str(addr))
    # and after accepting the connection, we can send the tweets through the socket
    send_tweets(c)

