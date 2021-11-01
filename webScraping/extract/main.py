import argparse
import datetime
import csv
import logging
import news_page_objects as news
from common import config
import re
from requests.exceptions import HTTPError
from urllib3.exceptions import MaxRetryError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

is_well_formed_link = re.compile(r'^https?://.+/.+$') #
is_root_path = re.compile(r'^/.+$') 

def _news_scrapper(news_site_uid):
    host = config()['news_sites'][news_site_uid]['url']
    logging.info('Begining scraper for {}'.format(host))

    homepage = news.HomePage(news_site_uid,host) 
    articles = []
    for link in homepage.article_links:
        article = _fecth_article(news_site_uid,host,link) 

        if article:
            logger.info('Article fetched')
            articles.append(article)
            
    _save_articcles(news_site_uid, articles)

def _save_articcles(news_site_uid, articles):
    #now = datetime.datetime.now().strftime('%Y_%m_%d') # fecha  %Y_%m_%d => "2020_08_21"
    out_file_name = '{news_site_uid}_.csv'.format(news_site_uid=news_site_uid)#, datetime=now) # xigua_2020_08_21
    csv_headers = list(
        filter(#function, arreglos 
            lambda property: not property.startswith('_'), # def property(property):    if not property.startwith('_'): return property
            dir(articles[0]) # __init__,  _select, _visit, body, title 
        )# body, title 
    ) #[body, title]
    with open(out_file_name, mode='w+',encoding='utf-8') as f: # open the file 
        writer = csv.writer(f) # writer 
        writer.writerow(csv_headers) # body , title <- cabecera  
        for article in articles: 
            row = [str(getattr(article,prop)) for prop in csv_headers]
            #row = []
            # for prop in csv_headers: # [body, title ]
            #   var = str(getattr(article, prop)) -> objeto article devuelve la propiedad prop(body)
            #   row.append(var)
            # row = ['西瓜','【00，00，00】鱼']
            writer.writerow(row)

def _fecth_article(news_site_uid,host,link):
    logging.info('Start fetching article at {}'.format(link))
    article = None
    try:
        article = news.ArticlePage(news_site_uid,_build_link(host, link))
    except (HTTPError,MaxRetryError) as e:
        logger.warning('Error while fechting the artcle', exc_info=False)
    if article and not article.body:
        logger.warning('Invalid article. There is no body')
        return None
    return article

def _build_link(host, link):
    if is_well_formed_link.match(link):
        return link
    elif is_root_path.match(link):
        return '{}{}'.format(host, link)
    else:
        return '{host}/{uri}'.format(host=host,uri=link)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    news_site_choices = list(config()['news_sites'].keys())

    parser.add_argument('new_site',
                        help='The news site that you want to scrape',
                        type=str,
                        choices=news_site_choices)

    args = parser.parse_args()
    _news_scrapper(args.new_site)
