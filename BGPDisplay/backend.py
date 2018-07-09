from datetime import datetime, timezone
import thread
import time

from classes import BGPDataAggregator
from classes.helper.functions import get_push_timestamp

collector = BGPDataAggregator()

start_time = get_push_timestamp(datetime.now(timezone.utc))

try:
    thread.start_new_thread(collector.start, (start_time))
except Exception as e:
    raise e

time.sleep(600)  # Hardcoded inittime of 10 Minutes to gater data

while True:
    print(collector.)
    time.sleep(30)  # Delay for 5 minutes.
