def calculate_score(lead) -> tuple[int, str]:
    score = 0
    reasons: list[str] = []

    if not lead.has_website:
        score += 45
        reasons.append("não possui site")
    else:
        if not lead.has_ssl:
            score += 15
            reasons.append("site sem HTTPS válido")
        if not lead.is_responsive:
            score += 20
            reasons.append("site não responsivo")
        if lead.looks_outdated:
            score += 15
            reasons.append("sinais de site desatualizado")
        if lead.pagespeed_performance is not None:
            if lead.pagespeed_performance < 40:
                score += 15
                reasons.append("performance muito baixa")
            elif lead.pagespeed_performance < 65:
                score += 8
                reasons.append("performance abaixo do ideal")
        if lead.pagespeed_seo is not None and lead.pagespeed_seo < 70:
            score += 8
            reasons.append("SEO técnico abaixo do ideal")

    if lead.phone or lead.whatsapp:
        score += 5
        reasons.append("telefone disponível")
    if lead.email:
        score += 5
        reasons.append("e-mail disponível")
    if lead.instagram:
        score += 4
        reasons.append("Instagram encontrado")
    if lead.has_whatsapp_link:
        score += 3
        reasons.append("WhatsApp identificado no site")

    return min(score, 100), ", ".join(reasons) or "sem sinais suficientes"
