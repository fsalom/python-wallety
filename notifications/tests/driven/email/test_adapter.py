import pytest

try:
    import smtplib
    from email.message import EmailMessage
    from notifications.driven.email.adapter import EmailRepositoryAdapter
    from notifications.domain.notification import Notification
except ImportError:
    pytest.skip(
        "Email libraries not available, skipping adapter tests", allow_module_level=True
    )


class DummySMTP:
    def __init__(self, *args, **kwargs):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        pass

    def send_message(self, msg, *args, **kwargs):
        return {}


@pytest.fixture(autouse=True)
def patch_smtp(monkeypatch):
    monkeypatch.setattr(smtplib, 'SMTP', lambda *args, **kwargs: DummySMTP())


def test_send_single_success():
    adapter = EmailRepositoryAdapter()
    notification = Notification(title="T", content="C", created_by_user_id=1)
    report = adapter._send_single(EmailMessage(), notification, 'a@example.com')
    assert report.notification == notification
    assert report.sent_to_device_ids == ['a@example.com']
    assert report.invalid_device_ids == []


def test_send_single_refused(monkeypatch):
    class RefuseSMTP(DummySMTP):
        def send_message(self, msg, *args, **kwargs):
            raise smtplib.SMTPRecipientsRefused({'a@example.com': (550, b'error')})

    monkeypatch.setattr(smtplib, 'SMTP', lambda *args, **kwargs: RefuseSMTP())
    notification = Notification(title="T", content="C", created_by_user_id=1)
    report = EmailRepositoryAdapter._send_single(EmailMessage(), notification, 'a@example.com')
    assert report.invalid_device_ids == ['a@example.com']


def test_send_single_exception(monkeypatch, capsys):
    class ErrorSMTP(DummySMTP):
        def send_message(self, msg, *args, **kwargs):
            raise Exception('fail')

    monkeypatch.setattr(smtplib, 'SMTP', lambda *args, **kwargs: ErrorSMTP())
    notification = Notification(title="T", content="C", created_by_user_id=1)
    report = EmailRepositoryAdapter._send_single(EmailMessage(), notification, 'b@example.com')
    captured = capsys.readouterr()
    assert 'Failed to send email to b@example.com: fail' in captured.out
    assert report.invalid_device_ids == []


def test_send_bulk_success():
    adapter = EmailRepositoryAdapter()
    notification = Notification(title="T", content="C", created_by_user_id=1)
    report = adapter._send_bulk(EmailMessage(), notification, ['a@example.com', 'b@example.com'])
    assert report.notification == notification
    assert report.sent_to_device_ids == ['a@example.com', 'b@example.com']
    assert report.invalid_device_ids == []


def test_send_bulk_refused(monkeypatch):
    class RefuseSMTP(DummySMTP):
        def send_message(self, msg, *args, **kwargs):
            return {'b@example.com': (550, b'error')}

    monkeypatch.setattr(smtplib, 'SMTP', lambda *args, **kwargs: RefuseSMTP())
    notification = Notification(title="T", content="C", created_by_user_id=1)
    report = EmailRepositoryAdapter._send_bulk(EmailMessage(), notification, ['a@example.com', 'b@example.com'])
    assert report.invalid_device_ids == ['b@example.com']


def test_send_bulk_exception(monkeypatch, capsys):
    class ErrorSMTP(DummySMTP):
        def send_message(self, msg, *args, **kwargs):
            raise Exception('boom')

    monkeypatch.setattr(smtplib, 'SMTP', lambda *args, **kwargs: ErrorSMTP())
    notification = Notification(title="T", content="C", created_by_user_id=1)
    report = EmailRepositoryAdapter._send_bulk(EmailMessage(), notification, ['a@example.com', 'b@example.com'])
    captured = capsys.readouterr()
    assert 'Failed to send email to a@example.com: boom' in captured.out
    assert 'Failed to send email to b@example.com: boom' in captured.out
    assert report.invalid_device_ids == []


def test_public_send_methods_delegate(monkeypatch):
    adapter = EmailRepositoryAdapter()
    notification = Notification(title="T", content="C", created_by_user_id=1)
    calls = []
    monkeypatch.setattr(
        EmailRepositoryAdapter,
        '_send_single',
        lambda self, msg, notification, recipient: calls.append((msg, recipient)) or 'ok1'
    )
    monkeypatch.setattr(
        EmailRepositoryAdapter,
        '_send_bulk',
        lambda self, msg, notification, recipients: calls.append((msg, tuple(recipients))) or 'ok2'
    )
    assert adapter.send(notification, 'x@example.com') == 'ok1'
    assert adapter.send_bulk(notification, ['y@example.com']) == 'ok2'
    assert len(calls) == 2