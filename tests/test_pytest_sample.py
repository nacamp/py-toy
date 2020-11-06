import pytest
import smtplib


@pytest.fixture(scope="module")
def smtp_connection():
    return smtplib.SMTP("smtp.gmail.com", 587, timeout=5)

def inc(x):
    return x + 1


def test_answer():
    assert inc(3) == 4

def test_ehlo(smtp_connection):
    response, msg = smtp_connection.ehlo()
    assert response == 250
    assert b"smtp.gmail.com" in msg
    assert 0  # for demo purposes


'''
pycharm
prefereces->Tools->Python Integrated Tools
Testing : select pytest  
https://docs.pytest.org/en/stable/
https://jangseongwoo.github.io/test/pytest_basic/
'''