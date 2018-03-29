#!/usr/bin/env python2

from datetime import datetime
import praw
import facebook
import urllib2
import os.path

def main():
  cfg = {
    "fb_page_id"      : "",
    "fb_access_token" : "",
    "praw_id"         : "",
    "praw_secret"     : "",
    "praw_agent"      : "script:com.stephen304.PostManager:v1.0 (by /u/Stephen304)",
    "praw_subreddits" : ["funny", "memes", "me_irl"],
    "acceptable_domains" : ["i.imgur.com", "i.redd.it"],
    "acceptable_mime" : ["image/png", "image/jpeg"]
  }

  print "#########################"
  print "## " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " ##"
  print "#########################\n"

  # Initialize Reddit API
  reddit = praw.Reddit(client_id=cfg['praw_id'],
                     client_secret=cfg['praw_secret'],
                     user_agent=cfg['praw_agent'])

  candidates = []

  # Read historyfile and prepare for appending
  historyfile = open(".posthistory", "r")
  posthistory = historyfile.read().splitlines()
  historyfile = open(".posthistory", "a")

  # Gather candidates
  for subreddit in cfg['praw_subreddits']:
    candidate = get_candidate(cfg, reddit, subreddit)
    if candidate is not None:
      print "Top in Hot: " + subreddit
      print u' '.join(("Post:", candidate.title)).encode('utf-8')
      print "URL:  " + candidate.url + "\n"
      candidates.append(candidate)

  # Remove already posted and unacceptable posts
  for candidate in candidates:
    try:
      imagedata = urllib2.urlopen(candidate.url)
    except Exception:
      print "ERROR! Requesting: " + candidate.url
      import traceback
      print('generic exception: ' + traceback.format_exc())
      continue
    if is_posted(posthistory, candidate) or is_unacceptable(cfg, imagedata, candidate):
      continue
    else:
      # Add to history
      posthistory_add(historyfile, candidate)
      print "POSTING: " + candidate.url
      # Post to FB
      do_post(cfg, imagedata, u''.join((candidate.title, "\n\nBy /u/", candidate.author.name)).encode('utf-8'))
      break
  print ""
  return

# Get candidates that are sfw and not stickied
def get_candidate(cfg, reddit, subreddit):
  candidate = None
  for submission in reddit.subreddit(subreddit).hot(limit=10):
    if submission.stickied or submission.over_18:
      continue
    else:
      candidate = submission
      break
  return candidate

# Return if post exists in posthistory file
def is_posted(posthistory, candidate):
  if candidate.url in posthistory:
    print "ISPOSTED: " + candidate.url
    return True
  else:
    return False

# Return if post is unacceptable
def is_unacceptable(cfg, imagedata, candidate):
  mime = imagedata.headers.getheader('content-type')
  if candidate.post_hint != "image" or candidate.domain not in cfg['acceptable_domains'] or mime not in cfg['acceptable_mime']:
    print "ISUNACC: " + candidate.url
    return True
  else:
    return False

def posthistory_add(historyfile, candidate):
  historyfile.write(candidate.url + "\n")

def do_post(cfg, imagedata, title):
  api = get_api(cfg)
  status = api.put_photo(image=imagedata, message=title)

def get_api(cfg):
  graph = facebook.GraphAPI(cfg['fb_access_token'])
  # Get page token to post as the page. You can skip
  # the following if you want to post as yourself.

  #resp = graph.get_object('me/accounts')
  #page_access_token = None
  #for page in resp['data']:
  #  if page['id'] == cfg['page_id']:
  #    page_access_token = page['access_token']
  #graph = facebook.GraphAPI(page_access_token)

  return graph
  # You can also skip the above if you get a page token:
  # http://stackoverflow.com/questions/8231877/facebook-access-token-for-pages
  # and make that long-lived token as in Step 3

if __name__ == "__main__":
  main()
