import logging


logger = logging.getLogger(__name__)


def send_welcome_email(email: str):
    """
    Simulate sending a welcome email.
    """

    logger.info(
        "Welcome email sent to %s",
        email
    )


def create_audit_log(
    user_id: int,
    action: str
):
    """
    Simulate creating an audit log.
    """

    logger.info(
        "AUDIT: user_id=%s action=%s",
        user_id,
        action
    )