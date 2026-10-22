# Eionet backend (Plone 6)

Standalone Plone 6 Classic site providing the Eionet LDAP account management
tools (formerly `/eionet-account-tools` on the Eionet Portal). All data lives in the Eionet LDAP server; the site only
provides the UI.

Add-ons:

- [eea.ldapadmin](https://github.com/eea/eea.ldapadmin): Users Admin, Roles Editor, Organisations, Password Reset
- [eea.userseditor](https://github.com/eea/eea.userseditor): profile editor, user details
- [eea.usersdb](https://github.com/eea/eea.usersdb): LDAP access layer
- naaya.ldapdump: SQLite cache of LDAP used for search and duplicate checks

Based on [eeacms/plone-backend](https://github.com/eea/plone-backend)

## Site layout

Created by `scripts/setup_tools.py`, mirroring the old portal paths:

| Path                                                       | Tool                    |
| ---------------------------------------------------------- | ----------------------- |
| `/eionet-account-tools/eionet_account_tools`               | Dashboard               |
| `/eionet-account-tools/eionet_account_tools/users`         | User Admin              |
| `/eionet-account-tools/eionet_account_tools/organisations` | Organisations           |
| `/eionet-account-tools/eionet_account_tools/roles`         | Roles Editor            |
| `/ldap-roles`                                              | Roles Editor (root)     |
| `/ldap-organisations`                                      | Organisations (root)    |
| `/password-reset`                                          | Password reset (public) |
| `/profile/profile-editor`                                  | Profile editor          |
| `/directory/user`                                          | User details            |

## Configuration

| Variable                                 | Used by      | Description                                                                                  |
| ---------------------------------------- | ------------ | -------------------------------------------------------------------------------------------- |
| `LDAP_SERVER`                            | setup script | `host:port`, always connected over `ldaps://`                                                |
| `LDAP_ADMIN_DN`, `LDAP_ADMIN_PW`         | setup script | Bind account with write access                                                               |
| `LDAP_SECONDARY_DN`, `LDAP_SECONDARY_PW` | setup script | Read-only bind account (also used by `naaya.ldapdump`)                                       |
| `LDAP_DISK_STORAGE`                      | add-ons      | Directory for `config.yaml`, the SQLite dump and `countries.json` (default `/data/ldapdump`) |
| `MAILHOST`, `MAILPORT`                   | setup script | SMTP for confirmation and reset emails                                                       |
| `MAIL_FROM`, `MAIL_FROM_NAME`            | setup script | Sender address and name                                                                      |

Database settings (`ZEO_ADDRESS`, `RELSTORAGE_DSN`, …) are those of
[eeacms/plone-backend](https://github.com/eea/plone-backend#supported-environment-variables).
The setup script stores the LDAP settings in each tool, so the `LDAP_*`
variables are only needed when it runs.

## Production

### Volumes

| Path | Content |
|---|---|
| `/data` | Plone database (filestorage and blobs), unless ZEO/RelStorage is used |
| `/data/ldapdump` | `config.yaml`, SQLite cache, `countries.json`. Must be shared by the backend and the cron jobs |

### First run

Run once against the production database, with the backend stopped (filestorage)
or running (ZEO/RelStorage):

    # 1. Create the Classic site (id "Plone")
    docker run --rm -v <data>:/data eeacms/eionet-backend create-classic

    # 2. Create the tools; pass the LDAP_* and MAIL* variables
    docker run --rm -v <data>:/data -e LDAP_SERVER=… -e LDAP_ADMIN_DN=… … \
      eeacms/eionet-backend run /app/scripts/setup_tools.py

Then (re)start the backend: `naaya.ldapdump` reads `config.yaml` at start-up.
Do not set `SITE`: the base image's automatic site creation is for development only.

The setup script is idempotent; re-running it keeps existing tools and their settings.

### Cron jobs

Same image, same `/data/ldapdump` volume, run as the `plone` user:

| Schedule | Command | Purpose |
|---|---|---|
| nightly | `/app/bin/python /app/scripts/dump_ldap.py` | Refresh the SQLite cache used by User Admin search and duplicate checks |
| daily | `/app/bin/update_countries` | Refresh `countries.json` from `https://cr.eionet.europa.eu/sparql` |

### Public URL

Serve the site at the domain root with Zope virtual hosting, e.g.
`/VirtualHostBase/https/<domain>:443/Plone/VirtualHostRoot/`, so URLs are
`https://<domain>/eionet-account-tools`. The add-on templates use root-relative
links such as `/directory/user`, which only work with the site at the root.

## Tests

    docker build -t eeacms/eionet-backend .
    ./test/run.sh eeacms/eionet-backend

## Release

See [RELEASE.md](RELEASE.md).

## Develop

See [develop](develop/README.md).

## Copyright and license

The Initial Owner of the Original Code is European Environment Agency (EEA).
All Rights Reserved.

See [LICENSE.md](LICENSE.md) for details.

## Funding

[European Environment Agency (EU)](http://eea.europa.eu)
