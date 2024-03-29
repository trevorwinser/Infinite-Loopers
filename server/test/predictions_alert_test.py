import pytest
from unittest.mock import patch
from app import send_alert

@pytest.mark.parametrize("kind", ['email', 'phone'])
def test_send_alert(kind):
    user = {'email': 'test@example.com', 'phone': '1234567890'} 
    month = 6
    risk = 'High'

    with patch('app.Client') as MockClient:
        send_alert(user, month, risk, kind)

        if kind == 'email':
            MockClient().messages.create.assert_called_once_with(
                from_='+19163024424',
                body='Alert Hurricane Risk: High\nMonth: 6',
                to='test@example.com'
            )
        elif kind == 'phone':
            MockClient().messages.create.assert_called_once_with(
                from_='+19163024424',
                body='Alert Hurricane Risk: High\nMonth: 6',
                to='1234567890'
            )
