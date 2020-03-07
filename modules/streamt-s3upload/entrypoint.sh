#!/bin/sh
if [[ -z "$CRON_SCHEDULE" ]]; then
    # Else run once
    python /app/upload_videos.py
else
    # Install crontab if scheduled variable set.
    echo "$CRON_SCHEDULE python /app/upload_videos.py" > /app/crontab.txt
    /usr/bin/crontab /app/crontab.txt
    # Run crond in foreground with most verbose output
    /usr/sbin/crond -f -l 0
fi

