import logging

from scrapy.core.scheduler import Scheduler
from scrapy import signals


class SequentialScheduler(Scheduler):
    """
    Schedule one request at a time.

    Optionally, use in combination with FIFO disk/memory
    queues to preserve the order of the requests:
        SCHEDULER_DISK_QUEUE = 'scrapy.squeues.PickleFifoDiskQueue'
        SCHEDULER_MEMORY_QUEUE = 'scrapy.squeues.FifoMemoryQueue'
    """

    in_progress = False

    @classmethod
    def from_crawler(cls, crawler):
        scheduler = super().from_crawler(crawler)
        scheduler.logger = logging.getLogger(__name__)
        crawler.signals.connect(scheduler.response_downloaded, signal=signals.response_downloaded)
        return scheduler

    def response_downloaded(self):
        self.in_progress = False

    def next_request(self):
        if not self.in_progress:
            request = super().next_request()
            if request:
                self.in_progress = True
            return request
        self.logger.debug('A request is in progress, could not get a request from the Scheduler')
