# Changelog

## Unreleased

- eea.ldapadmin 5.1: Plone 6 Classic UI templates (plain jQuery instead of
  RequireJS, jQuery 3 fixes, Plone 6 layout, Operations in the right column)
- LDAP control panel: add/remove/move buttons of the attribute maps. The
  `yafowil.widget.dict` and `yafowil.widget.array` wheels install with
  underscore `.dist-info` names, so `yafowil.plone` left their JS/CSS out of
  its bundle; the image renames them to the dotted names, and embeds their
  icons in the widget CSS (relative image URLs do not resolve in the bundle)

## 6.1.4-1 (2026-10-29)

- Initial scaffold: Plone 6.1 Classic image based on `eeacms/plone-backend:6.1.4-23`
  with `eea.ldapadmin`, `eea.usersdb`, `eea.userseditor`, `naaya.ldapdump`
- Site setup script creating the account tools at the old portal paths,
  including `/ldap-roles` and `/ldap-organisations`
- naaya.ldapdump 2.0.1 from eggshop.eaudeweb.ro (Python 3 / Zope 5 port); drop yaml workaround
- naaya.ldapdump 2.0.3 (closes the SQLite connection after dumps and reads)
- eea.ldapadmin 5.0 and eea.userseditor 3.0 (Plone 6 / Zope 5+ releases); drop the
  dnspython workaround (eea.ldapadmin 5.0 no longer depends on sparql-client)
- `scripts/dump_ldap.py` for the LDAP cache cron job
- Image tests (EEA harness plus `eionet-tools`), Jenkinsfile, release docs
- Local development stack: test LDAP with Eionet schema, mailtrap
