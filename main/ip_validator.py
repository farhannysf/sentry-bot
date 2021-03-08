import logging
import ipaddress
from functools import wraps
from sanic.response import json

logger = logging.getLogger(__name__)


def validate_ip(devState):
    def vd(f):
        @wraps(f)
        def wrapper(request):
            sentry_ip = [
                ipaddress.ip_network("35.184.238.160/32"),
                ipaddress.ip_network("104.155.159.182/32"),
                ipaddress.ip_network("104.155.149.19/32"),
                ipaddress.ip_network("130.211.230.102/32"),
            ]

            if devState == True:
                sentry_ip.append(ipaddress.ip_address(request.ip))

            for i in sentry_ip:
                if (
                    ipaddress.ip_address(request.ip) == i
                    or ipaddress.ip_address(request.ip) in i
                ):
                    return f(request)

            else:
                logger.error(
                    {
                        "error": {
                            "message": "Unauthorized IP",
                            "ip": request.ip,
                            "body": request.body,
                        }
                    }
                )
                return json({"error": "Unauthorized IP"}, status=401)

        return wrapper

    return vd
