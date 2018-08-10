# -*- coding: utf-8 -*-

# Scrapy settings for pybr2018 project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'pybr2018'

SPIDER_MODULES = ['pybr2018.spiders']
NEWSPIDER_MODULE = 'pybr2018.spiders'

LOG_LEVEL = 'INFO'

FEED_EXPORT_INDENT = 4
FEED_EXPORT_ENCODING = 'utf8'

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:62.0) Gecko/20100101 Firefox/62.0'

ROBOTSTXT_OBEY = False

CONCURRENT_REQUESTS = 32
