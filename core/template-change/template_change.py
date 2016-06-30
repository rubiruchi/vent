import sys
import time

from redis import Redis
from rq import Queue
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

class GZHandler(PatternMatchingEventHandler):

    patterns = ["*"]

    def process(self, event):
        """
        event.event_type
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        """
        q = Queue(connection=Redis(host="redis"), default_timeout=86400)
        if event.event_type == "created":
            print event.event_type, event.src_path
            # let jobs run for up to one day
            # let jobs be queued for up to 30 days
            if event.src_path.endswith(".template"):
                result = q.enqueue('template_change.template_queue', event.event_type+":"+event.src_path, ttl=2592000)
        elif event.event_type == "modified":
            print event.event_type, event.src_path
            # let jobs run for up to one day
            # let jobs be queued for up to 30 days
            if event.src_path.endswith(".template"):
                result = q.enqueue('template_change.template_queue', event.event_type+":"+event.src_path, ttl=2592000)
        elif event.event_type == "deleted":
            print event.event_type, event.src_path
            # let jobs run for up to one day
            # let jobs be queued for up to 30 days
            if event.src_path.endswith(".template"):
                result = q.enqueue('template_change.template_queue', event.event_type+":"+event.src_path, ttl=2592000)

    def on_created(self, event):
        self.process(event)

    def on_deleted(self, event):
        self.process(event)

    def on_modified(self, event):
        self.process(event)

if __name__ == '__main__':
    args = None
    if len(sys.argv) > 1:
        args = sys.argv[1:]

    observer = Observer()
    observer.schedule(GZHandler(), path=args[0] if args else '/templates')
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()