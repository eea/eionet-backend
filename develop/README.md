# Eionet Admin Tools: local development

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

## Known issues (Plone 6 port in progress)

The add-ons' `develop` branches do not start on Plone 6 yet. Until the ported
branches land in `sources.ini`, apply this local, uncommitted fix in `./sources`:

    grep -rl "from App.class_init import" sources --include='*.py' \
      | xargs sed -i '' 's/from App.class_init import/from AccessControl.class_init import/'

With that, the site starts, the tools are created, and they read from LDAP.
Remaining issues found so far:

| Area | Issue |
|---|---|
| Add-ons (Python) | `App.class_init` removed in Zope 5 (`api_tool`, `pwreset_tool`, `roles_editor`, `users_admin`, `users_editor`) |
| Add-ons (Python) | `yaml.load()` without Loader in `eea.ldapadmin/eionet_profile.py` and `naaya.ldapdump` (patched in the image for `naaya.ldapdump`) |
| Add-ons (deps) | `sparql-client` pins `dnspython<2` (worked around in the Dockerfiles); test-only packages (`plone.app.robotframework`, selenium, …) in `install_requires` |
| Add-ons (ZCML) | `/directory/user?uid=…` returns the object repr: needs a `browser:defaultView` (works as `/directory/user/index_html?uid=…`) |
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
