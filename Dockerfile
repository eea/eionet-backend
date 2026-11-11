FROM eeacms/plone-backend:6.1.6-1

# Classic UI site; drop the base image's Volto profile (eea.kitkat:default)
# LDAPTLS_CACERT: python-ldap does not find the CA bundle on its own (ldaps)
ENV TYPE=classic \
    PROFILES="" \
    ANSWERS=eionet \
    LDAP_DISK_STORAGE=/data/ldapdump \
    LDAPTLS_CACERT=/etc/ssl/certs/ca-certificates.crt

COPY requirements.txt constraints.txt /app/
COPY etc/package-includes/ /app/etc/package-includes/
COPY scripts/eionet.json scripts/setup_tools.py scripts/dump_ldap.py /app/scripts/

RUN ./bin/pip install -r requirements.txt -c constraints.txt \
    && mkdir -p $LDAP_DISK_STORAGE \
    && chown -R plone:plone $LDAP_DISK_STORAGE \
    && find /app -not -user plone -exec chown plone:plone {} \+

# yafowil.plone 5 finds a widget's JS/CSS by its installed distribution name,
# read from the .dist-info folder. The yafowil.widget.dict and .array wheels
# install as yafowil_widget_*.dist-info ("yafowil-widget-*"), which does not
# match the dotted name they register their resources under, so the widgets
# are left out of the yafowil bundle and the LDAP control panel has no
# add/remove/move buttons. Rename the folders to the dotted names.
RUN cd /app/lib/python3.12/site-packages \
    && for d in yafowil_widget_*.dist-info; do \
         [ -e "$d" ] || continue; \
         mv "$d" "$(echo "$d" | sed 's/^yafowil_widget_/yafowil.widget./')"; \
       done

# In the bundle the widgets' relative icon URLs do not resolve: embed the icons
COPY scripts/yafowil_inline_icons.py /tmp/
RUN ./bin/python /tmp/yafowil_inline_icons.py /app/lib/python3.12/site-packages \
    && rm /tmp/yafowil_inline_icons.py
