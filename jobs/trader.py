import os, sys
from datetime import datetime, timedelta, timezone
from time import sleep

if __name__ == '__main__':

    trade_frequency = timedelta(days=FREQUENCY).total_seconds()

    prev_time = datetime(2019, 2, 1, tzinfo=timezone.utc)
    while 1:
        current_time = datetime.now()
        if current_time - prev_time >= trade_frequency:
            prev_time = current_time

            # for h in heuristics:
            #   if h is true:
            #     trade
        else:
            sleep(trade_frequency - current_time + prev_time)
