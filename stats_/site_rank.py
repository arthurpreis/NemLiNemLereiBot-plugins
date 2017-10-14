import praw
from urllib.parse import urlparse

reddit = praw.Reddit(client_id='', client_secret="",
                     password='', user_agent='',
                     username='NLNL_aux_bot')

brasil = reddit.subreddit('brasil')
f = open('site_rank.txt', 'w')
url_list = []

for submission in brasil.hot(limit=2560):
    if (submission.link_flair_css_class == 'noticias')
        u = urlparse(submission.url).netloc
        url_list.append(u)

for count, elem in sorted(((url_list.count(e), e) for e in set(url_list)), reverse=True):
    f.write('%s (%d)' % (elem, count))
    print('%s (%d)' % (elem, count))
