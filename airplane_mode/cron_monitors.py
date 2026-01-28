monitor_config = {
    "schedule": {"type": "crontab", "value": "*/10 * * * *"},  # every 10 minutes
    "timezone": "Europe/Vienna",
    "checkin_margin": 5,
    "max_runtime": 10,
    "failure_issue_threshold": 3,
    "recovery_threshold": 1,
}