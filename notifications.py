from logger import logger

def slack_notify(text: str, **ctx):
    logger.info("slack_notify", text=text, **ctx)

def email_notify(subject: str, body: str, **ctx):
    logger.info("email_notify", subject=subject, body=body, **ctx)
