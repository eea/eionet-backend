# Eionet Admin Tools (Plone 6)

Standalone Plone 6 Classic site providing the Eionet LDAP account management
tools (formerly `/eionet-account-tools` on the Eionet Portal) until the service
is retired (2028/2029). All data lives in the Eionet LDAP server; the site only
provides the UI.

Add-ons:

* [eea.ldapadmin](https://github.com/eea/eea.ldapadmin): Users Admin, Roles Editor, Organisations, Password Reset
* [eea.userseditor](https://github.com/eea/eea.userseditor): profile editor, user details
* [eea.usersdb](https://github.com/eea/eea.usersdb): LDAP access layer
* naaya.ldapdump: SQLite cache of LDAP used for search and duplicate checks

Based on [eeacms/plone-backend](https://github.com/eea/plone-backend), following
the [eea-website-backend](https://github.com/eea/eea-website-backend) layout.

## Site layout

Created by `scripts/setup_tools.py`, mirroring the old portal paths:

| Path | Tool |
|---|---|
| `/eionet-account-tools/eionet_account_tools` | Dashboard |
| `/eionet-account-tools/eionet_account_tools/users` | User Admin |
| `/eionet-account-tools/eionet_account_tools/organisations` | Organisations |
| `/eionet-account-tools/eionet_account_tools/roles` | Roles Editor |
| `/password-reset` | Password reset (public) |
| `/profile/profile-editor` | Profile editor |
| `/directory/user` | User details |

## Configuration

| Variable | Used by | Description |
|---|---|---|
| `LDAP_SERVER` | setup script | `host:port`, always connected over `ldaps://` |
| `LDAP_ADMIN_DN`, `LDAP_ADMIN_PW` | setup script | Bind account with write access |
| `LDAP_SECONDARY_DN`, `LDAP_SECONDARY_PW` | setup script | Read-only bind account (also used by `naaya.ldapdump`) |
| `LDAP_DISK_STORAGE` | add-ons | Directory for `config.yaml`, the SQLite dump and `countries.json` (default `/data/ldapdump`) |
| `MAILHOST`, `MAILPORT` | setup script | SMTP for confirmation and reset emails |

## Develop

See [develop](develop/README.md).

## Copyright and license

The Initial Owner of the Original Code is European Environment Agency (EEA).
All Rights Reserved.

See [LICENSE.md](LICENSE.md) for details.

## Funding

[European Environment Agency (EU)](http://eea.europa.eu)
