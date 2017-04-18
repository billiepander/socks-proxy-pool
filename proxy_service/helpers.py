import requests

host = "http://m.niucodata.com/sendwxms.php"

def send_wechat_reminder(ak, bk, ck, dk):
    params = {
        'k1': ak, 'k2': bk, 'k3': ck, 'k4': dk
    }
    requests.get(host, params=params)
