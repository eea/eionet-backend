# Changelog

## Unreleased

- Initial scaffold: Plone 6.1 Classic image based on `eeacms/plone-backend:6.1.4-23`
  with `eea.ldapadmin`, `eea.usersdb`, `eea.userseditor`, `naaya.ldapdump`
- Site setup script creating the account tools at the old portal paths,
  including `/ldap-roles` and `/ldap-organisations`
- naaya.ldapdump 2.0.1 from eggshop.eaudeweb.ro (Python 3 / Zope 5 port); drop yaml workaround
- naaya.ldapdump 2.0.3 (closes the SQLite connection after dumps and reads)
- `scripts/dump_ldap.py` for the LDAP cache cron job
- Image tests (EEA harness plus `eionet-tools`), Jenkinsfile, release docs
- Local development stack: test LDAP with Eionet schema, mailtrap
