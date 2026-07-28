import requests
from app.config import get_settings

settings = get_settings()

FIELDS = ",".join([
    "places.id",
    "places.displayName",
    "places.formattedAddress",
    "places.nationalPhoneNumber",
    "places.internationalPhoneNumber",
    "places.websiteUri",
    "places.googleMapsUri",
    "places.primaryTypeDisplayName",
    "places.businessStatus",
    "nextPageToken",
])


class GooglePlacesError(RuntimeError):
    pass


def search_places(text_query: str, page_token: str | None = None) -> dict:
    if not settings.google_places_api_key:
        raise GooglePlacesError("GOOGLE_PLACES_API_KEY não configurada.")

    body = {
        "textQuery": text_query,
        "languageCode": "pt-BR",
        "regionCode": "BR",
        "pageSize": 20,
        "includePureServiceAreaBusinesses": True,
    }
    if page_token:
        body["pageToken"] = page_token

    response = requests.post(
        "https://places.googleapis.com/v1/places:searchText",
        headers={
            "Content-Type": "application/json",
            "X-Goog-Api-Key": settings.google_places_api_key,
            "X-Goog-FieldMask": FIELDS,
        },
        json=body,
        timeout=settings.request_timeout,
    )
    if not response.ok:
        raise GooglePlacesError(
            f"Google Places retornou {response.status_code}: {response.text[:500]}"
        )
    return response.json()


def normalize_place(place: dict, query_category: str, city: str, state: str) -> dict:
    display_name = place.get("displayName") or {}
    category_name = place.get("primaryTypeDisplayName") or {}
    phone = place.get("internationalPhoneNumber") or place.get("nationalPhoneNumber")

    return {
        "source": "google_places",
        "external_id": place.get("id"),
        "company_name": display_name.get("text", "Empresa sem nome"),
        "category": category_name.get("text") or query_category,
        "city": city,
        "state": state,
        "address": place.get("formattedAddress"),
        "phone": phone,
        "whatsapp": phone,
        "website": place.get("websiteUri"),
        "google_maps_url": place.get("googleMapsUri"),
        "has_website": bool(place.get("websiteUri")),
    }
