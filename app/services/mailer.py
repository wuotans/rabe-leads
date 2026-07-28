from __future__ import annotations

import smtplib
from email.message import EmailMessage
from pathlib import Path

from app.config import get_settings

settings = get_settings()


class MailerError(RuntimeError):
    pass


def send_proposal_email(
    recipient: str,
    subject: str,
    body: str,
    attachment_path: str,
) -> None:
    if not settings.smtp_host:
        raise MailerError("SMTP_HOST não configurado no arquivo .env.")
    if not settings.smtp_from_email:
        raise MailerError("SMTP_FROM_EMAIL não configurado no arquivo .env.")

    pdf_path = Path(attachment_path).expanduser().resolve()
    if not pdf_path.exists() or not pdf_path.is_file():
        raise MailerError(f"Arquivo da proposta não encontrado: {pdf_path}")
    if pdf_path.suffix.lower() != ".pdf":
        raise MailerError("O anexo da proposta deve ser um arquivo PDF.")

    message = EmailMessage()
    message["From"] = f"{settings.smtp_from_name} <{settings.smtp_from_email}>"
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(body)

    message.add_attachment(
        pdf_path.read_bytes(),
        maintype="application",
        subtype="pdf",
        filename=pdf_path.name,
    )

    try:
        if settings.smtp_use_ssl:
            client = smtplib.SMTP_SSL(
                settings.smtp_host,
                settings.smtp_port,
                timeout=30,
            )
        else:
            client = smtplib.SMTP(
                settings.smtp_host,
                settings.smtp_port,
                timeout=30,
            )

        with client:
            client.ehlo()
            if settings.smtp_use_tls and not settings.smtp_use_ssl:
                client.starttls()
                client.ehlo()
            if settings.smtp_user:
                client.login(settings.smtp_user, settings.smtp_password)
            client.send_message(message)
    except (OSError, smtplib.SMTPException) as exc:
        raise MailerError(f"Falha ao enviar o e-mail: {exc}") from exc
