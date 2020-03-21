#!/usr/bin/env python3

from datetime import datetime, timedelta, timezone
from base64 import b64encode
import hashlib
import click

def forge_link(resource, client_remote_addr, secret, host, expire_epoch):
    # Set variables to forge link
    old_resource = b'/s/LuaJIT-2.0.5.tar.gz'
    old_client_remote_addr = b'172.17.0.1'

    old_host = b'http://localhost:8080'

    # You should keep this secret... well... secret!
    old_secret = b'AM1ghtyS3cr3t!'

    # Generate expire timestamp
    now = datetime.utcnow()
    expire_dt = now + timedelta(hours=1)
    old_expire_epoch = str.encode(expire_dt.strftime('%s'))

    # md5 hash the string
    uncoded = expire_epoch + resource + client_remote_addr + ' '.encode() +secret
    md5hashed = hashlib.md5(uncoded).digest()

    # Base64 encode and transform the string
    b64 = b64encode(md5hashed)
    unpadded_b64url = b64.replace(b'+', b'-').replace(b'/', b'_').replace(b'=', b'')

    # Format and generate the link
    linkformat = "{}{}?md5={}&expires={}"
    securelink = linkformat.format(
    host.decode(),
    resource.decode(),
    unpadded_b64url.decode(),
    expire_epoch.decode()
    )

    # Print the link
    print(securelink)

def get_expiration_default_value():
    """
    1 hour in the future
    """
    now = datetime.now(timezone.utc)
    expire_dt = now + timedelta(hours=1)
    return str(int(expire_dt.timestamp()))

@click.command()
@click.option('--path', '-p', required=True, type=click.STRING, help='Full path to the S3 object')
@click.option('--remote_address', '-r', required=True, type=click.STRING, help='IP address of the client')
@click.option('--host_url', '-h', required=True, type=click.STRING, help='Full URL of the reverse proxy')
@click.option('--secret', '-s', required=True, prompt=True, hide_input=True, confirmation_prompt=True, type=click.STRING, help='Secret configured in NGINX')
@click.option('--expiration_timestamp', '-e', default=get_expiration_default_value(), type=click.STRING, help=' Link\'s expiration timestamp', show_default=True)
def generate_link(path, remote_address, host_url, secret, expiration_timestamp):
    """
    Generates a link that expires.

    Example:
      ./link-generator-example.py -p /s/file.tar.gz -r 172.17.0.1 -h http://localhost:9090 -s changeme
    """
    forge_link(path.encode(), remote_address.encode(), secret.encode(), host_url.encode(), expiration_timestamp.encode())

if __name__ == '__main__':
    generate_link()