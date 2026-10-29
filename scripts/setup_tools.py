"""Create the Eionet account tools inside the Plone site.

Run after the site exists:

    bin/zconsole run etc/zope.conf scripts/setup_tools.py

Idempotent: existing objects are left untouched. Paths mirror the old Eionet
portal, because the add-on templates hard-code some of them
(e.g. /eionet-account-tools/eionet_account_tools/users).
"""
from AccessControl.SecurityManagement import newSecurityManager
from Testing.makerequest import makerequest
from plone import api
from zope.component.hooks import setSite

import logging
import os
import transaction
import yaml

from eea.ldapadmin.dashboard import Dashboard
from eea.ldapadmin.orgs_editor import OrganisationsEditor
from eea.ldapadmin.pwreset_tool import PasswordResetTool
from eea.ldapadmin.roles_editor import RolesEditor
from eea.ldapadmin.users_admin import UsersAdmin
from eea.userseditor.userdetails import UserDetails
from eea.userseditor.users_editor import UsersEditor


logging.basicConfig(format="%(message)s")
logger = logging.getLogger("setup_tools")
logger.setLevel(logging.INFO)

SITE_ID = os.getenv("SITE", os.getenv("SITE_ID", "Plone"))

LDAP_CONFIG = {
    "ldap_server": os.environ["LDAP_SERVER"],
    "admin_dn": os.environ["LDAP_ADMIN_DN"],
    "admin_pw": os.environ["LDAP_ADMIN_PW"],
    "secondary_admin_dn": os.getenv("LDAP_SECONDARY_DN", ""),
    "secondary_admin_pw": os.getenv("LDAP_SECONDARY_PW", ""),
    "users_rdn": "uid",
    "users_dn": os.getenv("LDAP_USERS_DN", "ou=Users,o=EIONET,l=Europe"),
    "orgs_dn": os.getenv("LDAP_ORGS_DN",
                         "ou=Organisations,o=EIONET,l=Europe"),
    "roles_dn": os.getenv("LDAP_ROLES_DN", "ou=Roles,o=EIONET,l=Europe"),
}

# (parent path, id, title, class); "" = site root
TOOLS = [
    ("eionet-account-tools", "eionet_account_tools",
     "Eionet User Account Tools", Dashboard),
    ("eionet-account-tools/eionet_account_tools", "users",
     "User Admin", UsersAdmin),
    ("eionet-account-tools/eionet_account_tools", "organisations",
     "Organisations", OrganisationsEditor),
    ("eionet-account-tools/eionet_account_tools", "roles",
     "Roles Editor", RolesEditor),
    # Root-level instances linked from Forum, Projects and the NFP pages
    ("", "ldap-roles", "Roles", RolesEditor),
    ("", "ldap-organisations", "Organisations", OrganisationsEditor),
    ("", "password-reset", "Password Reset", PasswordResetTool),
    ("profile", "profile-editor", "Eionet account", UsersEditor),
    ("directory", "user", "User details", UserDetails),
]

# Plone folders that hold the tools; published so non-owners can reach them
FOLDERS = [
    ("eionet-account-tools", "Eionet Account Tools"),
    ("profile", "Profile"),
    ("directory", "Directory"),
]

# Folder -> tool shown when the folder itself is opened
DEFAULT_PAGES = {
    "eionet-account-tools": "eionet_account_tools",
    "profile": "profile-editor",
}


def ensure_folder(site, folder_id, title):
    if folder_id in site.objectIds():
        return site[folder_id]
    folder = api.content.create(
        container=site, type="Folder", id=folder_id, title=title)
    api.content.transition(obj=folder, transition="publish")
    logger.info("Created folder /%s", folder_id)
    return folder


def set_default_page(site, folder_id, page_id):
    folder = site[folder_id]
    if getattr(folder.aq_base, "default_page", None) != page_id:
        folder.default_page = page_id
        logger.info("Default page of /%s -> %s", folder_id, page_id)


def ensure_tool(site, parent_path, tool_id, title, klass):
    parent = site.unrestrictedTraverse(parent_path) if parent_path else site
    if tool_id in parent.objectIds():
        logger.info("Exists: %s/%s", parent_path, tool_id)
        return
    obj = klass() if klass is Dashboard else klass(dict(LDAP_CONFIG))
    obj.title = title
    obj._setId(tool_id)
    parent._setObject(tool_id, obj)
    logger.info("Created %s at %s/%s", klass.meta_type, parent_path, tool_id)


def write_ldapdump_config():
    """config.yaml for naaya.ldapdump (search/duplicate-check cache)."""
    storage = os.getenv("LDAP_DISK_STORAGE")
    if not storage:
        return
    path = os.path.join(storage, "config.yaml")
    if os.path.exists(path):
        return
    host, _, port = LDAP_CONFIG["ldap_server"].partition(":")
    with open(path, "w") as config_file:
        yaml.safe_dump({
            "ldap": {
                "host": host,
                "port": int(port or 636),
                "encoding": "utf-8",
                "root_DNs": [LDAP_CONFIG["users_dn"]],
                "dn": LDAP_CONFIG["secondary_admin_dn"],
                "password": LDAP_CONFIG["secondary_admin_pw"],
            },
            "sqlite": {"path": "./ldap_eionet_europa_eu.db"},
            "logging": {"file": "./log.txt"},
        }, config_file)
    logger.info("Wrote %s", path)


def configure_mailhost(site):
    host = os.getenv("MAILHOST")
    if not host:
        return
    port = int(os.getenv("MAILPORT", "25"))
    # Plone 6 reads the registry records; keep the MailHost object in sync
    api.portal.set_registry_record("plone.smtp_host", host)
    api.portal.set_registry_record("plone.smtp_port", port)
    mailhost = site.MailHost
    mailhost.smtp_host = host
    mailhost.smtp_port = port
    api.portal.set_registry_record(
        "plone.email_from_address",
        os.getenv("MAIL_FROM", "helpdesk@example.com"))
    api.portal.set_registry_record(
        "plone.email_from_name", os.getenv("MAIL_FROM_NAME", "Eionet"))
    logger.info("MailHost -> %s:%s", host, mailhost.smtp_port)


def main(app):
    app = makerequest(app)
    admin = app.acl_users.getUserById("admin").__of__(app.acl_users)
    newSecurityManager(None, admin)

    site = app[SITE_ID]
    setSite(site)

    for folder_id, title in FOLDERS:
        ensure_folder(site, folder_id, title)
    for parent_path, tool_id, title, klass in TOOLS:
        ensure_tool(site, parent_path, tool_id, title, klass)
    for folder_id, page_id in DEFAULT_PAGES.items():
        set_default_page(site, folder_id, page_id)
    configure_mailhost(site)
    write_ldapdump_config()

    transaction.commit()
    logger.info("Done.")


main(globals()["app"])
