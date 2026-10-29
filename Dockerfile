FROM eeacms/plone-backend:6.1.4-23

# Classic UI site; drop the base image's Volto profile (eea.kitkat:default)
ENV TYPE=classic \
    PROFILES="" \
    ANSWERS=eionet \
    LDAP_DISK_STORAGE=/data/ldapdump

COPY requirements.txt constraints.txt /app/
COPY etc/package-includes/ /app/etc/package-includes/
COPY scripts/eionet.json scripts/setup_tools.py scripts/dump_ldap.py /app/scripts/

RUN ./bin/pip install -r requirements.txt -c constraints.txt \
    && mkdir -p $LDAP_DISK_STORAGE \
    && chown -R plone:plone $LDAP_DISK_STORAGE \
    && find /app -not -user plone -exec chown plone:plone {} \+
