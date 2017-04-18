import requests


def send_wechat_reminder(ak, bk, ck, dk):
    """
        this is my example wechat reminder, you should write your own reminder
    """
    service_url = "xxxx"
    params = {
        'k1': ak, 'k2': bk, 'k3': ck, 'k4': dk
    }
    requests.get(service_url, params=params)
    # should do some error check here
