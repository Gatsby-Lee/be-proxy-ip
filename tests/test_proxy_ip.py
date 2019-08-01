import time

import pytest

from be_proxy_ip import ProxyIP

MOCK_TIME = 1564683072.3187723


PROXY_INFO = [
    1,  # proxy_id
    '1.2.3.4',  # proxy_ip
    3999,  # proxy_port
    'hello-proxy',  # proxy_username
    'hellop-proxy-pwd',  # proxy_pwd
    -1,  # last_request_time
    11,  # num_ok_requests
    22,  # num_banned_requests
    33,  # num_timedout_requests
    44,  # counted
    '4.5.6.7',  # request_ip
]


@pytest.fixture
def proxyip_obj():

    p = ProxyIP.create_from_tuple(PROXY_INFO)
    return p


def test_create_from_tuple(proxyip_obj):

    assert proxyip_obj.proxy_id == PROXY_INFO[0]
    assert proxyip_obj.proxy_ip == PROXY_INFO[1]
    assert proxyip_obj.proxy_port == PROXY_INFO[2]
    assert proxyip_obj.proxy_username == PROXY_INFO[3]
    assert proxyip_obj.proxy_pwd == PROXY_INFO[4]
    assert proxyip_obj.last_request_time == PROXY_INFO[5]
    assert proxyip_obj.num_ok_requests == PROXY_INFO[6]
    assert proxyip_obj.num_banned_requests == PROXY_INFO[7]
    assert proxyip_obj.num_timedout_requests == PROXY_INFO[8]
    assert proxyip_obj.counted == PROXY_INFO[9]
    assert proxyip_obj.request_ip == PROXY_INFO[10]


def test_init_object():

    proxy_id = 1
    proxy_ip = '1.2.3.4'
    proxy_port = '8888'
    proxy_username = 'hello-world-proxy'
    proxy_pwd = 'doyouknow?'
    last_request_time = 1212
    num_ok_requests = 22
    num_banned_requests = 33
    num_timedout_requests = 44
    counted = 1
    request_ip = '4.4.6.7'

    proxyip_obj = ProxyIP(
        proxy_id=proxy_id,
        proxy_ip=proxy_ip,
        proxy_port=proxy_port,
        proxy_username=proxy_username,
        proxy_pwd=proxy_pwd,
        last_request_time=last_request_time,
        num_ok_requests=num_ok_requests,
        num_banned_requests=num_banned_requests,
        num_timedout_requests=num_timedout_requests,
        counted=counted,
        request_ip=request_ip,
    )

    assert proxyip_obj.proxy_id == proxy_id
    assert proxyip_obj.proxy_ip == proxy_ip
    assert proxyip_obj.proxy_port == proxy_port
    assert proxyip_obj.proxy_username == proxy_username
    assert proxyip_obj.proxy_pwd == proxy_pwd
    assert proxyip_obj.last_request_time == last_request_time
    assert proxyip_obj.num_ok_requests == num_ok_requests
    assert proxyip_obj.num_banned_requests == num_banned_requests
    assert proxyip_obj.num_timedout_requests == num_timedout_requests
    assert proxyip_obj.counted == counted
    assert proxyip_obj.request_ip == request_ip


def test_reset_stats(proxyip_obj):

    proxyip_obj.reset_stats()

    assert proxyip_obj.proxy_id == PROXY_INFO[0]
    assert proxyip_obj.proxy_ip == PROXY_INFO[1]
    assert proxyip_obj.proxy_port == PROXY_INFO[2]
    assert proxyip_obj.proxy_username == PROXY_INFO[3]
    assert proxyip_obj.proxy_pwd == PROXY_INFO[4]
    assert proxyip_obj.last_request_time == -1
    assert proxyip_obj.num_ok_requests == 0
    assert proxyip_obj.num_banned_requests == 0
    assert proxyip_obj.num_timedout_requests == 0
    assert proxyip_obj.counted == 0
    assert proxyip_obj.request_ip == PROXY_INFO[10]


def test_set_banned(proxyip_obj, mocker):

    mocker.patch('time.time', return_value=MOCK_TIME)
    proxyip_obj.set_banned()

    assert proxyip_obj.proxy_id == PROXY_INFO[0]
    assert proxyip_obj.proxy_ip == PROXY_INFO[1]
    assert proxyip_obj.proxy_port == PROXY_INFO[2]
    assert proxyip_obj.proxy_username == PROXY_INFO[3]
    assert proxyip_obj.proxy_pwd == PROXY_INFO[4]
    assert proxyip_obj.last_request_time == int(MOCK_TIME)
    assert proxyip_obj.num_ok_requests == 0
    assert proxyip_obj.num_banned_requests == 1
    assert proxyip_obj.num_timedout_requests == 0
    assert proxyip_obj.counted == 0
    assert proxyip_obj.request_ip == PROXY_INFO[10]


def test_is_partially_used(proxyip_obj):

    threshold = 10
    assert proxyip_obj.is_partially_used(threshold) is False

    proxyip_obj.num_ok_requests = 2
    proxyip_obj.num_banned_requests = 0
    proxyip_obj.num_timedout_requests = 0
    assert proxyip_obj.is_partially_used(threshold) is True
