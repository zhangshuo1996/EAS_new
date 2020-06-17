import random
import string
from flask import request, redirect, url_for, current_app
from urllib.parse import urlparse, urljoin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature


def is_safe_url(target):
    """
    确保内部的URL才是安全的
    :param target:
    :return:
    """
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def redirect_back(default='.', **kwargs):
    """
    重定向
    :param default:
    :param kwargs:
    :return:
    """
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))