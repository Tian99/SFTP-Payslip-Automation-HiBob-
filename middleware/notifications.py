from observibility.logger import logger

"""
Mock notification module.
Simulates sending Slack and Email alerts by logging the messages instead of actually sending them.
Used for visibility and debugging during local testing.
"""

def slack_notify(text: str, **ctx):
    logger.info("slack_notify", text=text, **ctx)

def email_notify(subject: str, body: str, **ctx):
    logger.info("email_notify", subject=subject, body=body, **ctx)
