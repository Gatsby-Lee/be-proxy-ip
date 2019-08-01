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

    p = ProxyIP(PROXY_INFO)
    return p


def test_init_object(proxyip_obj):

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
