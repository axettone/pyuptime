# pyuptime
Uptime checker for paranoid webmasters. This programs just check for
HTTP status code and/or exceptions to determine if the website is up
or down. This tool should be paired with another application that
uses the data to display a dashboard.
All the probes are inserted into "checks" table.

## TODO
Implement email notifications.

## Setup
Copy config.yml.example to config.yml and setup your SMTP parameters.
You can add some sites using add_site.py script, doing something like
```shell
./add_site.py http://www.myurl.com alarms@mywebagency.com
```

## Requirements
PyYAML is required.