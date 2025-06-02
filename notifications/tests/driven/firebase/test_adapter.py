import pytest

try:
    from notifications.driven.firebase.adapter import FirebaseRepositoryAdapter
    from notifications.domain.notification import Notification
    from firebase_admin import messaging
except ImportError:
    pytest.skip("firebase_admin not available, skipping adapter tests", allow_module_level=True)


class DummyUnregisteredError(Exception):
    pass


class DummyQuotaExceededError(Exception):
    pass


@pytest.fixture(autouse=True)
def patch_exceptions(monkeypatch):
    monkeypatch.setattr(messaging, 'UnregisteredError', DummyUnregisteredError)
    monkeypatch.setattr(messaging, 'QuotaExceededError', DummyQuotaExceededError)


class DummyResponse:
    def __init__(self, success, exception=None):
        self.success = success
        self.exception = exception


def test_send_single_success(monkeypatch):
    adapter = FirebaseRepositoryAdapter()
    notification = Notification(title="T", content="C", created_by_user_id=1)
    dummy_message = object()
    monkeypatch.setattr(messaging, 'send', lambda msg: 'msg_id')
    report = adapter._send_single(dummy_message, notification, 'token1')
    assert report.notification == notification
    assert report.sent_to_device_ids == ['token1']
    assert report.invalid_device_ids == []


def test_send_single_with_data(monkeypatch):
    adapter = FirebaseRepositoryAdapter()
    notification = Notification(title="T", content="C", created_by_user_id=1, data={'k': 'v'})
    class DummyMessage:
        pass

    dummy_message = DummyMessage()
    monkeypatch.setattr(messaging, 'send', lambda msg: 'msg_id')
    report = adapter._send_single(dummy_message, notification, 'token2')
    assert report.notification == notification
    assert hasattr(dummy_message, 'data')
    assert dummy_message.data == {'k': 'v'}
    assert report.invalid_device_ids == []


def test_send_single_unregistered(monkeypatch):
    adapter = FirebaseRepositoryAdapter()
    notification = Notification(title="T", content="C", created_by_user_id=1)

    def raise_unregistered(msg):
        raise messaging.UnregisteredError("invalid")

    monkeypatch.setattr(messaging, 'send', raise_unregistered)
    report = adapter._send_single(object(), notification, 'bad_token')
    assert report.notification == notification
    assert report.invalid_device_ids == ['bad_token']


def test_send_bulk(monkeypatch):
    adapter = FirebaseRepositoryAdapter()
    notification = Notification(title="T", content="C", created_by_user_id=1)
    batch_response = type('Batch', (), {'responses': [
        DummyResponse(True),
        DummyResponse(False, messaging.UnregisteredError("uerr")),
        DummyResponse(False, Exception("other"))
    ]})
    monkeypatch.setattr(messaging, 'send_each_for_multicast', lambda msg: batch_response)
    report = adapter._send_bulk(object(), notification, ['t1', 't2', 't3'])
    assert report.notification == notification
    assert report.sent_to_device_ids == ['t1', 't2', 't3']
    assert report.invalid_device_ids == ['t2']


def test_public_send_methods_delegate(monkeypatch):
    adapter = FirebaseRepositoryAdapter()
    notification = Notification(title="T", content="C", created_by_user_id=1)
    calls = []
    # patch internal methods to track calls
    monkeypatch.setattr(FirebaseRepositoryAdapter, '_send_single', lambda self, message, notification, device_id: calls.append((message, device_id)) or 'ok1')
    monkeypatch.setattr(FirebaseRepositoryAdapter, '_send_bulk', lambda self, message, notification, device_ids: calls.append((message, tuple(device_ids))) or 'ok2')
    # visible single
    result1 = adapter.send_single_notification(notification, 'dev1')
    assert result1 == 'ok1'
    # silent single
    result2 = adapter.send_single_silent_notification(notification, 'dev2')
    assert result2 == 'ok1'
    # visible bulk
    result3 = adapter.send_bulk_notification(notification, ['d1', 'd2'])
    assert result3 == 'ok2'
    # silent bulk
    result4 = adapter.send_bulk_silent_notification(notification, ['d3'])
    assert result4 == 'ok2'
    # ensure all methods called
    assert len(calls) == 4