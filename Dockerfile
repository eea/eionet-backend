FROM eeacms/plone-backend:6.1.4-23

# Classic UI site; drop the base image's Volto profile (eea.kitkat:default)
ENV TYPE=classic \
    PROFILES="" \
    ANSWERS=eionet \
    LDAP_DISK_STORAGE=/data/ldapdump

COPY requirements.txt constraints.txt /app/
COPY etc/package-includes/ /app/etc/package-includes/
COPY scripts/eionet.json scripts/setup_tools.py /app/scripts/

# sparql-client 3.9.dev1 (via eea.ldapadmin) pins dnspython<2, which fails on
# Python 3.12 (collections.MutableMapping). It never imports dns, so restore the
# base image's dnspython. Remove once sparql-client drops the pin.
RUN ./bin/pip install -r requirements.txt -c constraints.txt \
    && ./bin/pip install dnspython==2.8.0 \
    && mkdir -p $LDAP_DISK_STORAGE \
    && chown -R plone:plone $LDAP_DISK_STORAGE \
    && find /app -not -user plone -exec chown plone:plone {} \+
