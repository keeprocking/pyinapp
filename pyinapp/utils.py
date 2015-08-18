import base64


def decode_base64_url(url):
    """ Aligns given base64 encoded url and then decodes it """

    url += '=' * (4 - len(url) % 4)
    return base64.urlsafe_b64decode(url)
