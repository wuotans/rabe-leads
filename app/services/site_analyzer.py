from __future__ import annotations
import re
import ssl
import socket
import time
from urllib.parse import urlparse, urljoin
import requests
from bs4 import BeautifulSoup
from app.config import get_settings

settings = get_settings()

OLD_MARKERS = [
    "jquery-1.", "jquery/1.", "bootstrap/3.", "table layout",
    "flash player", "microsoft frontpage", "generator\" content=\"wordpress 4",
]


def normalize_url(url: str) -> str:
    if not url:
        return ""
    url = url.strip()
    if not url.startswith(("http://", "https://")):
        return "https://" + url
    return url


def check_ssl(url: str) -> bool:
    parsed = urlparse(url)
    if parsed.scheme != "https" or not parsed.hostname:
        return False
    try:
        context = ssl.create_default_context()
        with socket.create_connection((parsed.hostname, parsed.port or 443), timeout=8) as sock:
            with context.wrap_socket(sock, server_hostname=parsed.hostname):
                return True
    except OSError:
        return False


def analyze_html(url: str) -> dict:
    normalized = normalize_url(url)
    started = time.perf_counter()
    result = {
        "has_website": bool(normalized),
        "has_ssl": False,
        "is_responsive": False,
        "looks_outdated": False,
        "has_whatsapp_link": False,
        "has_contact_form": False,
        "response_ms": None,
        "email": None,
        "instagram": None,
        "facebook": None,
        "linkedin": None,
        "error": None,
    }
    if not normalized:
        return result

    result["has_ssl"] = check_ssl(normalized)

    try:
        response = requests.get(
            normalized,
            headers={"User-Agent": settings.user_agent},
            timeout=settings.request_timeout,
            allow_redirects=True,
        )
        result["response_ms"] = int((time.perf_counter() - started) * 1000)
        response.raise_for_status()
        html = response.text[:2_000_000]
        lower = html.lower()
        soup = BeautifulSoup(html, "lxml")

        viewport = soup.find("meta", attrs={"name": re.compile("^viewport$", re.I)})
        result["is_responsive"] = bool(viewport and "width=device-width" in viewport.get("content", "").lower())
        result["has_whatsapp_link"] = bool(re.search(r"(wa\.me|api\.whatsapp\.com|whatsapp://)", lower))
        result["has_contact_form"] = soup.find("form") is not None
        result["looks_outdated"] = (
            any(marker in lower for marker in OLD_MARKERS)
            or not result["is_responsive"]
            or result["response_ms"] > 4000
        )

        email_match = re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", html)
        if email_match:
            result["email"] = email_match.group(0).lower()

        for link in soup.find_all("a", href=True):
            href = urljoin(response.url, link["href"])
            low = href.lower()
            if "instagram.com/" in low and not result["instagram"]:
                result["instagram"] = href
            elif "facebook.com/" in low and not result["facebook"]:
                result["facebook"] = href
            elif "linkedin.com/" in low and not result["linkedin"]:
                result["linkedin"] = href

    except requests.RequestException as exc:
        result["error"] = str(exc)

    return result


def pagespeed(url: str) -> dict:
    normalized = normalize_url(url)
    if not normalized:
        return {}
    params = {
        "url": normalized,
        "strategy": "mobile",
        "category": ["performance", "accessibility", "seo"],
    }
    if settings.google_pagespeed_api_key:
        params["key"] = settings.google_pagespeed_api_key

    response = requests.get(
        "https://www.googleapis.com/pagespeedonline/v5/runPagespeed",
        params=params,
        timeout=max(settings.request_timeout, 60),
    )
    response.raise_for_status()
    categories = response.json().get("lighthouseResult", {}).get("categories", {})

    def score(name: str):
        value = categories.get(name, {}).get("score")
        return round(value * 100) if isinstance(value, (int, float)) else None

    return {
        "pagespeed_performance": score("performance"),
        "pagespeed_accessibility": score("accessibility"),
        "pagespeed_seo": score("seo"),
    }
