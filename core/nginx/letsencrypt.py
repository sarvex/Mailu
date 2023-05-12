#!/usr/bin/python3

import os
import time
import subprocess

command = [
    "certbot",
    "-n",
    "--agree-tos",
    "-d",
    os.environ["HOSTNAMES"],
    "-m",
    f'{os.environ["POSTMASTER"]}@{os.environ["DOMAIN"]}',
    "certonly",
    "--standalone",
    "--cert-name",
    "mailu",
    "--preferred-challenges",
    "http",
    "--http-01-port",
    "8008",
    "--keep-until-expiring",
    "--renew-with-new-domains",
    "--config-dir",
    "/certs/letsencrypt",
    "--post-hook",
    "/config.py",
]
command2 = [
    "certbot",
    "-n",
    "--agree-tos",
    "-d",
    os.environ["HOSTNAMES"],
    "-m",
    f'{os.environ["POSTMASTER"]}@{os.environ["DOMAIN"]}',
    "certonly",
    "--standalone",
    "--cert-name",
    "mailu-ecdsa",
    "--preferred-challenges",
    "http",
    "--http-01-port",
    "8008",
    "--keep-until-expiring",
    "--key-type",
    "ecdsa",
    "--renew-with-new-domains",
    "--config-dir",
    "/certs/letsencrypt",
    "--post-hook",
    "/config.py",
]

def format_for_nginx(fullchain, output):
    """ We may want to strip ISRG Root X1 out
    """
    certs = []
    with open(fullchain, 'r') as pem:
        cert = ''
        for line in pem:
            cert += line
            if '-----END CERTIFICATE-----' in line:
                certs += [cert]
                cert = ''
    with open(output, 'w') as pem:
        for cert in certs[:-1] if len(certs)>2 and os.getenv('LETSENCRYPT_SHORTCHAIN', default="False") else certs:
            pem.write(cert)

# Wait for nginx to start
time.sleep(5)

# Run certbot every day
while True:
    subprocess.call(command)
    format_for_nginx('/certs/letsencrypt/live/mailu/fullchain.pem', '/certs/letsencrypt/live/mailu/nginx-chain.pem')
    subprocess.call(command2)
    format_for_nginx('/certs/letsencrypt/live/mailu-ecdsa/fullchain.pem', '/certs/letsencrypt/live/mailu-ecdsa/nginx-chain.pem')
    time.sleep(86400)
