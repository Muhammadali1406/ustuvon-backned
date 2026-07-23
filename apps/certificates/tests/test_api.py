import uuid
from datetime import datetime, timezone
from types import SimpleNamespace

import pytest
from django.urls import reverse
from rest_framework.test import APIClient


pytestmark = pytest.mark.django_db


def _build_user_stub(user_id=None):
    return SimpleNamespace(
        id=user_id or uuid.uuid4(),
        username="tester",
        is_authenticated=True,
    )


def _build_certificate_stub(user_id, certificate_number="UST-1234"):
    user = _build_user_stub(user_id)
    return SimpleNamespace(
        id=uuid.uuid4(),
        user=user,
        user_id=user.id,
        result=SimpleNamespace(id=uuid.uuid4()),
        certificate_number=certificate_number,
        pdf_file=None,
        status="generated",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
        is_deleted=False,
        deleted_at=None,
    )


@pytest.fixture
def api_client():
    return APIClient()


def test_certificate_list_requires_authentication(api_client):
    response = api_client.get(reverse("certificates:list"))

    assert response.status_code == 401


def test_certificate_list_returns_current_user_certificates(api_client, monkeypatch):
    owner = _build_user_stub()
    certificate = _build_certificate_stub(owner.id)

    def fake_get_user_certificates(user):
        assert user.id == owner.id
        return [certificate]

    monkeypatch.setattr("apps.certificates.views.get_user_certificates", fake_get_user_certificates)
    api_client.force_authenticate(user=owner)

    response = api_client.get(reverse("certificates:list"))

    assert response.status_code == 200
    assert response.json()["results"][0]["certificate_number"] == certificate.certificate_number


def test_certificate_detail_allows_owner(api_client, monkeypatch):
    owner = _build_user_stub()
    certificate = _build_certificate_stub(owner.id)

    monkeypatch.setattr(
        "apps.certificates.views.get_user_certificates",
        lambda user: [certificate] if user.id == owner.id else [],
    )
    api_client.force_authenticate(user=owner)

    response = api_client.get(reverse("certificates:detail", kwargs={"pk": str(certificate.id)}))

    assert response.status_code == 200
    assert response.json()["certificate_number"] == certificate.certificate_number


def test_certificate_detail_denies_non_owner(api_client, monkeypatch):
    owner = _build_user_stub()
    other_user = _build_user_stub()
    certificate = _build_certificate_stub(owner.id)

    monkeypatch.setattr(
        "apps.certificates.views.get_user_certificates",
        lambda user: [certificate],
    )
    api_client.force_authenticate(user=other_user)

    response = api_client.get(reverse("certificates:detail", kwargs={"pk": str(certificate.id)}))

    assert response.status_code == 403


def test_certificate_validation_is_public_and_returns_data(api_client, monkeypatch):
    certificate = _build_certificate_stub(uuid.uuid4(), certificate_number="UST-VALID-1")

    monkeypatch.setattr(
        "apps.certificates.views.get_certificate_by_number",
        lambda certificate_number: certificate if certificate_number == "UST-VALID-1" else None,
    )

    response = api_client.get(
        reverse("certificates:validate", kwargs={"certificate_number": "UST-VALID-1"})
    )

    assert response.status_code == 200
    assert response.json()["valid"] is True
    assert response.json()["data"]["certificate_number"] == certificate.certificate_number


def test_certificate_validation_returns_not_found_for_unknown_number(api_client, monkeypatch):
    monkeypatch.setattr("apps.certificates.views.get_certificate_by_number", lambda certificate_number: None)

    response = api_client.get(
        reverse("certificates:validate", kwargs={"certificate_number": "UNKNOWN"})
    )

    assert response.status_code == 404
    assert response.json() == {"valid": False}
