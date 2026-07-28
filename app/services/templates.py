from urllib.parse import quote


def email_subject(lead) -> str:
    return f"Uma ideia para fortalecer a presença digital da {lead.company_name}"


def email_body(lead) -> str:
    city = f" em {lead.city}" if lead.city else ""
    observation = (
        "Identificamos oportunidades de modernização no site atual."
        if lead.has_website
        else "Percebemos que a empresa ainda não possui um site institucional identificado."
    )
    return f"""Olá! Tudo bem?

Meu nome é Matheus e faço parte da Rabe Soluções Digitais.

Conheci a {lead.company_name}{city} durante uma pesquisa de empresas e gostaria de apresentar nosso trabalho com sites institucionais, sistemas web e soluções digitais personalizadas.

{observation}

Preparamos uma apresentação com projetos já desenvolvidos e modalidades de contratação. Posso encaminhar a proposta para avaliação?

Caso este contato não seja de interesse, basta responder informando e não enviaremos novas mensagens.

Atenciosamente,
Matheus Patryck
Rabe Soluções Digitais
(65) 99245-5040
https://agenciarabe.com.br
"""


def whatsapp_body(lead) -> str:
    city = f" de {lead.city}" if lead.city else ""
    return f"""Olá! Tudo bem? Meu nome é Matheus e faço parte da Rabe Soluções Digitais.

Conheci a {lead.company_name}{city} durante uma pesquisa de empresas e gostaria de apresentar nosso trabalho com criação de sites institucionais, sistemas web e soluções digitais personalizadas.

Posso encaminhar uma breve proposta com exemplos de projetos já desenvolvidos?

Caso este contato não seja de interesse, é só me avisar e não enviarei novas mensagens."""


def whatsapp_link(lead) -> str | None:
    number = lead.whatsapp or lead.phone
    if not number:
        return None
    digits = "".join(ch for ch in number if ch.isdigit())
    if len(digits) in (10, 11):
        digits = "55" + digits
    return f"https://wa.me/{digits}?text={quote(whatsapp_body(lead))}"
