# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name: Philip Nguyen
# Collaborators: Duncan Calder
# Time: Few Hours to a Day, throughout the week

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1 -PHILIP

# TODO: NewsStory
class NewsStory:
    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate
    def get_guid(self):
        return self.guid
    def get_title(self):
        return self.title
    def get_description(self):
        return self.description
    def get_link(self):
        return self.link
    def get_pubdate(self):
        return self.pubdate
    
## Problem 1 - Duncan
#class NewsStory(object):
#    def __init__(self, guid, title, description, link, pubdate):
#        self.guid = guid
#        self.title = title
#        self.description = description
#        self.link = link
#        self.pubdate = pubdate
#        
#    def get_guid(self):
#        return self.guid
#    def get_title(self):
#        return self.title
#    def get_description(self):
#        return self.description
#    def get_link(self):
#        return self.link
#    def get_pubdate(self):
#        return self.pubdate
    


#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS
# Return True if phrase is in NewsStory
# Problem 2 -PHILIP
# TODO: PhraseTrigger
class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        self.phrase = phrase.lower() # make the input phrase lowercase
    def is_phrase_in(self, text):
        wordIndex = []
        result = True
        phraseWords = self.phrase.split() # split the phrase into words
        text = text.lower() # lowercase the text
        for letter in string.punctuation:
            text = text.replace(letter, " ") # replace punctuation with space
        textWords = text.split() # split the text into words
        for word in phraseWords:
            if word in textWords: # if word phrases in text
                wordIndex.append(textWords.index(word)) # add the index to a list
            else:
                result = False # if not set result false
        for i in range(len(wordIndex)-1): # if each word is consecutive, if not set result false
            if wordIndex[i+1] - wordIndex[i] != 1:
                result = False
        return result

#PhraseTrigger - Duncan
#Problem 2
#charachterised by words containing one space between them
#can assume that there is no punctuation
#need to figure out how to detect multiple spaces in a row
#convert to lowercase to search
#take out all punctuation and spaces to search - string.punctuation
#also use split, replace, and join methods
#takes in string phrase
#is_phrase_in
#'''
    
#class PhraseTrigger(Trigger):
#    def __init__(self, phrase):
#        self.phrase = phrase.lower()
#    
#    def is_phrase_in(self, text):
#        '''
#        >>> text = "purple!!!cow"
#        >>> punctuation = string.punctuation
#        >>> text_removed = text
#        >>> for punct in punctuation:
#        ...     text_removed = text_removed.replace(punct, '')
#        >>> print(text_removed)
#        purplecow
#        >>>
#        # need to figure out how to remove extra spaces but leave one between two words in the phrase
#        # if punctuation found replace with space then go through process below
#        # if space found and there is a space after, remove the spaces after
#        # also need to stop it from finding when it is contained in another word
#        # for loop looking through string, when it finds a space or a punctuation
#            # turn into a space
#                # look for more spaces or punctuation but just remove it, if something not space or punctuation is found update iteration and keep looking
#        # if there isn't a space at the end then add one
#        '''
#        text = text.lower()
#        punctuation = string.punctuation
#        text_removed = ""
#        i = 0
#        text_length = len(text)
#        while i < text_length:
#            if text[i] == " " or text[i] in punctuation:
#                text_removed = text_removed + " "
#                if i < text_length - 1:
#                    i+=1
#                else:
#                    break
#                while i < text_length and text[i] == " " or text[i] in punctuation:
#                    if i < text_length - 1:
#                        i+=1
#                    else:
#                        break
#            else:
#                text_removed = text_removed + text[i]
#                if i < text_length - 1:
#                    i+=1
#                else:
#                    break
#        if len(text_removed) > 0 and text_removed[len(text_removed)-1] != " ":
#            text_removed = text_removed + " "
#        if len(text_removed) > 0 and self.phrase[len(self.phrase)-1] != " ":
#            self.phrase = self.phrase + " "
#        if text_removed.find(self.phrase) > -1:
#            return True
#        else:
#            return False
        
# Problem 3 -PHILIP
# TODO: TitleTrigger
class TitleTrigger(PhraseTrigger):
    def evaluate(self, story):
        return PhraseTrigger.is_phrase_in(self, story.get_title())

# Problem 4 -PHILIP
# TODO: DescriptionTrigger
class DescriptionTrigger(PhraseTrigger):
    def evaluate(self, story):
        return PhraseTrigger.is_phrase_in(self, story.get_description())
    
#TitleTrigger - Duncan
#Problem 3
#triggers when a NewsStory's title contains the phrase
#inherits from PhraseTrigger
#uses is_phrase_in from PraseTrigger to evaluate the title
#'''
#
#class TitleTrigger(PhraseTrigger):
#    def __init__(self, phrase):
#        self.phrase = phrase.lower()
#    
#    def evaluate(self, story):
#        return self.is_phrase_in(story.get_title())
#
#'''
#Description Trigger - Duncan
#Problem 4
#triggers when a NewsStory's description contains the phrase
#inherits from PhraseTrigger
#uses is_phrase_in from PraseTrigger to evaluate the description
#'''
#class DescriptionTrigger(PhraseTrigger):
#    def __init__(self, phrase):
#        self.phrase = phrase.lower()
#
#    def evaluate(self, story):
#        return self.is_phrase_in(story.get_description())
## TODO: DescriptionTrigger


# TIME TRIGGERS

# Problem 5 -PHILIP
# TODO: TimeTrigger
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.
class TimeTrigger(Trigger):
    def __init__(self, pubtime):
        #EST = pytz.timezone("US/Eastern") #create est time zone
        pubtime = datetime.strptime(pubtime, "%d %b %Y %H:%M:%S") # Parse the time of the string
        pubtime = pubtime.replace(tzinfo=pytz.timezone("EST")) #Replace est timezone
        self.pubtime = pubtime
        
#TimeTrigger - Duncan
#Problem 5
#Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.
#'''
#class TimeTrigger(Trigger):
#    def __init__(self, time):
#        time = datetime.strptime(time, "%d %b %Y %H:%M:%S")
#        time = time.replace(tzinfo=pytz.timezone('EST'))
#        self.time = time

# Problem 6 -PHILIP
# TODO: BeforeTrigger and AfterTrigger
class BeforeTrigger(TimeTrigger):
    def evaluate(self, story):
        return self.pubtime.replace(tzinfo=pytz.timezone("EST")) > story.get_pubdate().replace(tzinfo=pytz.timezone("EST"))
    
class AfterTrigger(TimeTrigger):
    def evaluate(self, story):
        return self.pubtime.replace(tzinfo=pytz.timezone("EST")) < story.get_pubdate().replace(tzinfo=pytz.timezone("EST"))
    
    
#BeforeTrigger - Duncan
#Problem 6
#is an instance of TimeTrigger and triggers when 
#the time is strictly after the given time
#'''
#class BeforeTrigger(TimeTrigger):
#    def __init__(self, time):
#        TimeTrigger.__init__(self, time)
#    def evaluate(self, story):
#        story_time = story.get_pubdate().replace(tzinfo=None)
#        search_time = self.time.replace(tzinfo=None)
#        if story_time < search_time:
#            return True
#        else:
#            return False
#
#'''
#AfterTrigger - Duncan
#is an instance of TimeTrigger and triggers when
#the time is strictly after the given time
#'''
#class AfterTrigger(TimeTrigger):
#    def __init__(self, time):
#        TimeTrigger.__init__(self, time)
#
#    def evaluate(self, story):
#        story_time = story.get_pubdate().replace(tzinfo=None)
#        search_time = self.time.replace(tzinfo=None)
#        if story_time > search_time:
#            return True
#        else:
#            return False
## TODO: BeforeTrigger and AfterTrigger

# COMPOSITE TRIGGERS

# Problem 7 -DUNCAN
# TODO: NotTrigger
# returns the NOT of the trigger given
class NotTrigger(Trigger):
    def __init__(self, trigger):
        self.trigger = trigger
    def evaluate(self, story):
        return not self.trigger.evaluate(story)
# Problem 8 -DUNCAN
# TODO: AndTrigger
# returns the AND of the triggers given
class AndTrigger(Trigger):
    def __init__(self, trigger_1, trigger_2):
        self.trigger_1 = trigger_1
        self.trigger_2 = trigger_2

    def evaluate(self, story):
        return self.trigger_1.evaluate(story) and self.trigger_2.evaluate(story)
# Problem 9 -DUNCAN
# TODO: OrTrigger
# returns the OR of the triggers given
class OrTrigger(Trigger):
    def __init__(self, trigger_1, trigger_2):
        self.trigger_1 = trigger_1
        self.trigger_2 = trigger_2

    def evaluate(self, story):
        return self.trigger_1.evaluate(story) or self.trigger_2.evaluate(story)

#======================
# Filtering
#======================

# Problem 10 -PHILIP
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    stories_firedOn = []
    for newsstory in stories: # for each story
        for trigger in triggerlist: # for each trigger
            if trigger.evaluate(newsstory): # if trigger fires, add it to the list
                stories_firedOn.append(newsstory)
    return stories_firedOn



#======================
# User-Specified Triggers
#======================
# Problem 11 -DUNCAN
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # make list for triggers
    triggers = []
    # make dictionary to store trigger names and triggers
    trigger_names = {}
    # process lines
    for line in lines:
        # split up the line to process
        split_line = line.split(',')
        # if ADD
        if line.startswith('ADD'):
            # remove ADD from line
            split_line.pop(0)
            # for each trigger name in list
            # look up name and add trigger to list
            # if not in list then print error for now, change to a real error
            for trigger_name in split_line:
                trigger = trigger_names.get(trigger_name)
                if trigger != None:
                    triggers.append(trigger)
                else:
                    raise Exception("trigger name: %s does not exist in dictionary" % trigger_name)
        # for each filter title associate the name with the trigger
        elif(split_line[1] == 'TITLE'):
            trigger_names[split_line[0]] = TitleTrigger(split_line[2])
        elif(split_line[1] == 'DESCRIPTION'):
            trigger_names[split_line[0]] = DescriptionTrigger(split_line[2])
        elif(split_line[1] == 'AFTER'):
            trigger_names[split_line[0]] = AfterTrigger(split_line[2])
        elif(split_line[1] == 'BEFORE'):
            trigger_names[split_line[0]] = BeforeTrigger(split_line[2])
        # for the filters that you need to look up the trigger name
        # look it up and add the trigger to the dict
        elif(split_line[1] == 'NOT'):
            trigger = trigger_names.get(split_line[2])
            if trigger != None:
                trigger_names[split_line[0]] = NotTrigger(trigger)
            else:
                raise Exception("trigger name: %s does not exist in dictionary" % trigger_name)
        elif(split_line[1] == 'AND'):
            trigger_1 = trigger_names.get(split_line[2])
            trigger_2 = trigger_names.get(split_line[3])
            if (trigger_1 != None) or (trigger_2 != None):
                trigger_names[split_line[0]] = AndTrigger(trigger_1, trigger_2)
            else:
                raise Exception("trigger name: %s does not exist in dictionary" % trigger_name)
        elif(split_line[1] == 'OR'):
            trigger_1 = trigger_names.get(split_line[2])
            trigger_2 = trigger_names.get(split_line[3])
            if (trigger_1 != None) or (trigger_2 != None):
                trigger_names[split_line[0]] = OrTrigger(trigger_1, trigger_2)
            else:
                raise Exception("trigger name: %s does not exist in dictionary" % trigger_name)
    return triggers
    # TITLE​: one phrase
    # DESCRIPTION​: one phrase
    # AFTER​: one correctly formatted time string
    # BEFORE​: one correctly formatted time string
    # NOT​: the name of the trigger that will be NOT'd
    # AND​: the names of the two triggers that will be AND'd.
    # OR​: the names of the two triggers that will be OR'd.
    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers
    # use dictionary to match trigger names to values
    # switch statement?
    # parse each line by storing the trigger name in a dictionary
    # and evaluating the given trigger and storing it into the value
    # Use a switch or an if else group to match the trigger in the link
    # to the trigger and evaluates it on the current story with the given arguments
    # for title and description there will be one string parameter
    # for not, and, or triggers there will be one two and two respectfully
    # if ADD is seen then create a list of triggers into filter stories function

SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        #t1 = TitleTrigger("school")
        #t2 = DescriptionTrigger("New York")
        #t3 = DescriptionTrigger("Iran")
        #t4 = AndTrigger(t2, t3)
        #triggerlist = [t1,t2,t3,t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        #triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__': # added test code in main because the code did not run
    
    import doctest
    doctest.testmod()
    # # Get stories from Google's Top Stories RSS news feed
    stories = process("http://news.google.com/news?output=rss")

    # # Get stories from Yahoo's Top Stories RSS news feed
    stories.extend(process("http://news.yahoo.com/rss/topstories"))

    triggerlist = read_trigger_config('triggers.txt')
    filtered_stories = filter_stories(stories, triggerlist)

    for news_story in filtered_stories:
        print("Title: %s" % news_story.get_title())
        print("%s" % news_story.get_description())
        print("Date: %s" % news_story.get_pubdate())
        print("Link: %s" % news_story.get_link())
        print("---------------------------------------------------------------")
    #root = Tk()
    #root.title("Some RSS parser")
    #t = threading.Thread(target=main_thread, args=(root,))
    #t.start()
    #root.mainloop()

