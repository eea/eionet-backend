# Eionet backend: local development

Runs everything in Docker: Plone 6 backend, a local test LDAP server with the
Eionet schema and fake data, and Mailpit to catch outgoing email.

The add-ons are cloned into `./sources` and mounted into the container, so
template and JavaScript changes show up without rebuilding.

## Pre-requirements

* Docker with Compose v2
* On Apple Silicon: the EEA images are `linux/amd64` only and run emulated (slower, but works)

## Install

    cd develop
    make            # clone sources + build images
    make start      # start Plone (creates the Classic site on first run), LDAP, Mailpit
    make setup      # create the account tools in the site

Then open:

* Plone: http://localhost:8080/Plone (`admin:admin`)
* Dashboard: http://localhost:8080/Plone/eionet-account-tools/eionet_account_tools
* Password reset: http://localhost:8080/Plone/password-reset
* Mail (Mailpit, no login): http://localhost:8888

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

## Develop add-ons

Branches are set in `sources.ini`. After changing them:

    make sources && make build && make start

Check for local changes or pull all sources:

    make status
    make pull
