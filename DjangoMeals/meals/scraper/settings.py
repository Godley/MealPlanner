import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "example_project.settings") #Changed in DDS v.0.3

BOT_NAME = 'open_news'

SPIDER_MODULES = ['dynamic_scraper.spiders', 'open_news.scraper',]
USER_AGENT = '%s/%s' % (BOT_NAME, '1.0')

#Scrapy 0.20+
ITEM_PIPELINES = {
    'dynamic_scraper.pipelines.ValidationPipeline': 400,
    'open_news.scraper.pipelines.DjangoWriterPipeline': 800,
}
