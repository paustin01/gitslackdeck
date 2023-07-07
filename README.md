# GitSlackDeck
A Docker image to be used in a GitHub Actions workflow which includes the
`pipelines_notifier.py` script. This script can post a message to Slack with
details about the build and offer options in the form of buttons for what to do
with it (deploy it, view the build etc...).

# How it works
See the Github Actions workflow file below for an example. We're
hard coding some variables which tell the script things like which Slack channel
to post to, which Rundeck project and job ID should be referenced, and what
options on that job we want to set (in the form of the `QUERY_STRING_PARAMS`
variable). Additionally we're parsing the last commit to find the committer's
name for posting in the message as well.

```yml
TBD
```

# Building
```bash
docker build -t burstbucker/gitslackdeck:latest .
```
