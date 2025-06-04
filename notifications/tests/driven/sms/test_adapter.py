import pytest

try:
    import os
    import requests
    from notifications.driven.sms.adapter import SMSRepositoryAdapter
    from notifications.domain.notification import Notification
except ImportError:
    pytest.skip(
        "SMS libraries not available, skipping adapter tests", allow_module_level=True
    )


class DummyResponse:
    def __init__(self, status_code):
        self.status_code = status_code


@pytest.fixture(autouse=True)
def patch_post(monkeypatch):
    monkeypatch.setenv("SMS_API_URL", "http://api.test/sms")
    monkeypatch.setattr(requests, 'post', lambda *args, **kwargs: DummyResponse(200))


def test_send_single_success():
    adapter = SMSRepositoryAdapter()
    notification = Notification(title="T", content="C", created_by_user_id=1)
    report = adapter._send_single({"message": notification.content}, notification, "12345")
    assert report.notification == notification
    assert report.sent_to_device_ids == ["12345"]
    assert report.invalid_device_ids == []


def test_send_single_invalid_number(monkeypatch):
    def post_invalid(url, json, headers=None):
        return DummyResponse(400)

    monkeypatch.setattr(requests, 'post', post_invalid)
    notification = Notification(title="T", content="C", created_by_user_id=1)
    report = SMSRepositoryAdapter._send_single({"message": notification.content}, notification, "bad")
    assert report.invalid_device_ids == ["bad"]


def test_send_single_exception(monkeypatch, capsys):
    def post_error(url, json, headers=None):
        raise Exception("fail")

    monkeypatch.setattr(requests, 'post', post_error)
    notification = Notification(title="T", content="C", created_by_user_id=1)
    report = SMSRepositoryAdapter._send_single({"message": notification.content}, notification, "12345")
    captured = capsys.readouterr()
    assert 'Failed to send SMS to 12345: fail' in captured.out
    assert report.invalid_device_ids == []


def test_send_bulk_success():
    report = SMSRepositoryAdapter._send_bulk({"message": "C"}, Notification(title="T", content="C", created_by_user_id=1), ["123", "456"])
    assert report.sent_to_device_ids == ["123", "456"]
    assert report.invalid_device_ids == []


def test_send_bulk_invalid(monkeypatch):
    def post_resp(url, json, headers=None):
        if json.get("to") == "bad":
            return DummyResponse(400)
        return DummyResponse(200)

    monkeypatch.setattr(requests, 'post', post_resp)
    report = SMSRepositoryAdapter._send_bulk({"message": "C"}, Notification(title="T", content="C", created_by_user_id=1), ["good", "bad"])
    assert report.invalid_device_ids == ["bad"]


def test_send_bulk_exception(monkeypatch, capsys):
    def post_error(url, json, headers=None):
        raise Exception("boom")

    monkeypatch.setattr(requests, 'post', post_error)
    report = SMSRepositoryAdapter._send_bulk({"message": "C"}, Notification(title="T", content="C", created_by_user_id=1), ["123", "456"])
    captured = capsys.readouterr()
    assert 'Failed to send SMS to 123: boom' in captured.out
    assert 'Failed to send SMS to 456: boom' in captured.out
    assert report.invalid_device_ids == []


def test_public_send_methods_delegate(monkeypatch):
    adapter = SMSRepositoryAdapter()
    notification = Notification(title="T", content="C", created_by_user_id=1)
    calls = []
    monkeypatch.setattr(
        SMSRepositoryAdapter,
        '_send_single',
        lambda self, payload, notification, recipient: calls.append(recipient) or 'r1'
    )
    monkeypatch.setattr(
        SMSRepositoryAdapter,
        '_send_bulk',
        lambda self, payload, notification, recipients: calls.append(tuple(recipients)) or 'r2'
    )
    assert adapter.send(notification, '12345') == 'r1'
    assert adapter.send_bulk(notification, ['67890']) == 'r2'
    assert len(calls) == 2