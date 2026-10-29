"""Refresh the naaya.ldapdump SQLite cache (user search, duplicate checks).

Run from cron, as the plone user, against the same $LDAP_DISK_STORAGE volume
the backend uses:

    /app/bin/python /app/scripts/dump_ldap.py

bin/dump_ldap cannot be used: it is eea.ldapadmin's wrapper and expects the
storage path as an argument.
"""
import os
import sys

from naaya.ldapdump.main import dump_ldap


def main():
    storage = os.environ.get("LDAP_DISK_STORAGE", "/data/ldapdump")
    config = os.path.join(storage, "config.yaml")
    if not os.path.exists(config):
        sys.exit("%s not found; run scripts/setup_tools.py first" % config)
    dump_ldap(config)


if __name__ == "__main__":
    main()
