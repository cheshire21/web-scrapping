import logging
logging.basicConfig(level=logging.INFO)
import subprocess
import shutil
import os

logger = logging.getLogger(__name__)
news_sites_uids = ['larepublica','elcorreo']
def main():
    _extract()
    _transform()
    _load()

def _extract():
    logger.info('Starting extract process')
    for news_sites_uid in news_sites_uids:
        subprocess.run(['C:\\Users\\Coren\\anaconda3\\python.exe', 'main.py', news_sites_uid], cwd='./extract')
        #subprocess.Popen('mv .\\'+news_sites_uid+'_.csv .\\transform', shell=True)
        shutil.move(".\\extract\\{}_.csv".format(news_sites_uid), ".\\transform")

def _transform():
    logger.info('Starting transform process')
    for news_sites_uid in news_sites_uids:
        dirty_data_filename= '{}_.csv'.format(news_sites_uid)
        clean_data_filename = 'clean_{}'.format(dirty_data_filename)
        logger.info('Starting transform {}'.format(dirty_data_filename))
        subprocess.run(['C:\\Users\\Coren\\anaconda3\\python.exe', 'main.py',dirty_data_filename],cwd='./transform')
        os.remove(".\\transform\\{}".format(dirty_data_filename))
        shutil.move(".\\transform\\{}".format(clean_data_filename), ".\\load")
        

def _load():
    logger.info('Starting load process')
    for news_sites_uid in news_sites_uids:
        clean_data_filename = 'clean_{}_.csv'.format(news_sites_uid)
        logger.info('Starting load {}'.format(clean_data_filename))
        subprocess.run(['C:\\Users\\Coren\\anaconda3\\python.exe','main.py',clean_data_filename],cwd='./load')
        os.remove(".\\load\\{}".format(clean_data_filename))
        
if __name__ == "__main__":
    main()