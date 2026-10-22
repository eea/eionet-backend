# Eionet backend: local development

Runs everything in Docker: Plone 6 backend, a local test LDAP server with the
Eionet schema and fake data, and mailtrap to catch outgoing email.

The add-ons are cloned into `./sources` and mounted into the container, so
template and JavaScript changes show up without rebuilding.

## Pre-requirements

* Docker with Compose v2
* On Apple Silicon: the EEA images are `linux/amd64` only and run emulated (slower, but works)

## Install

    cd develop
    make            # clone sources + build images
    make start      # start Plone (creates the Classic site on first run), LDAP, mailtrap
    make setup      # create the account tools in the site

Then open:

* Plone: http://localhost:8080/Plone (`admin:admin`)
* Dashboard: http://localhost:8080/Plone/eionet-account-tools/eionet_account_tools
* Password reset: http://localhost:8080/Plone/password-reset
* Mailtrap: http://localhost:8888

## Test LDAP

`ldap/seed.ldif` loads a small fake directory on first start. All passwords are `secret`.

| Account | DN | Notes |
|---|---|---|
| Admin bind | `cn=Eionet Administrator,o=EIONET,l=Europe` | Root DN, write access |
| Read-only bind | `cn=Accounts Browser,o=EIONET,l=Europe` | |
| Users | `uid=testadmin`, `uid=anna`, `uid=marco` | `anna` is NFP for Denmark |

Query it from the host:

    LDAPTLS_REQCERT=never ldapsearch -H ldaps://localhost:1636 \
      -D "cn=Accounts Browser,o=EIONET,l=Europe" -w secret \
      -b "o=EIONET,l=Europe" "(uid=*)"

To reset the data: `make clean && make start && make setup`.

Refresh the SQLite cache that User Admin uses for search and duplicate checks
(production runs this from cron):

    make dump

## Known issues (Plone 6 port in progress)

The released add-ons and their `develop` branches do not start on Plone 6.
`sources.ini` therefore uses the `plone6` branches of `eea.ldapadmin` and
`eea.userseditor` until they are merged and released. If your `./sources`
checkouts predate this, switch them and rebuild:

    git -C sources/eea.ldapadmin checkout plone6
    git -C sources/eea.userseditor checkout plone6
    make build && make start

Fixed on the `plone6` branches:

* `App.class_init` (removed in Zope 5) → `AccessControl.class_init`
* `sparql-client` (pins `dnspython<2`) replaced by `requests`
* `jellyfish>=1.0`, unpinned `colander`, `naaya.ldapdump>=2.0`, test packages moved to the test extra
* `yaml.safe_load` in `eionet_profile.py`
* default view for `/directory/user?uid=…`

Remaining:

| Area | Issue |
|---|---|
| Image | `dnspython` override in the Dockerfiles: remove once the `plone6` releases are pinned |
| Add-ons (packaging) | `bin/dump_ldap` is `eea.ldapadmin`'s wrapper, which needs the storage path as an argument; use `scripts/dump_ldap.py` (`make dump`) |
| UI | `require()` / `requirejs()` in 15 templates: DataTables, jQuery UI, tipsy, select2 do not load |
| UI | `userdetails/simple.zpt:82`: `int(path('repeat/role/odd'))` fails under Chameleon |
| UI | Plone 5 markup/classes; links to `www.eionet.europa.eu/styles/eionet2007/*.css` |
| Local LDAP | No password policy overlay, so `pwdChangedTime` / expiry are not shown |

## Develop add-ons

Branches are set in `sources.ini`. After changing them:

    make sources && make build && make start

Check for local changes or pull all sources:

    make status
    make pull
