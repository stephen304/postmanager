# PostManager
This project enables easy syndication between subreddits on Reddit and Facebook pages.

It enables the easy maintenance of low effort Facebook pages such as ones whose single purpose is to share memes.

PostManager attempts to capture audiences more effectively than manually administered pages through automation, in an attempt to "beat other pages to the punch" by sharing the latest Reddit posts faster than the human admins of other pages.

## Usage
* Create a Facebook app and get a long lived page token for your page+app using the Graph Explorer (I use 2 months by extending a temporary token using the token debugger)
  * Set `fb_access_token` (`fb_page_id` is unused currently)
* Register a Reddit "script" app
  * Set `praw_id` to the app ID and `praw_secret` to the app secret
* Set `praw_subreddits` to the list of subreddits to pull posts from, in order of descending priority
* Set a cron job similar to below to run the task at a regular interval

This crontab runs the task at every hour at a random minute, and appends all output to `/var/log/postmanager.log`
```
SHELL=/usr/local/bin/bash
0 * * * * sleep $((RANDOM*3600/32768)) && cd /root && /root/postmanager.py >> /var/log/postmanager.log 2>&1
```

The end result is a Facebook page that, once randomly every hour, posts a new top photo and caption from the list of subreddits configured.

## Todo
- [ ] Check size of `.posthistory` file and truncate periodically
- [ ] Support for gifs? Videos?
- [ ] Code cleanup / chores (maybe don't put api creds in the main file)
- [ ] Remove [OC] tags from titles before posting
