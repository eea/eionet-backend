# Local test LDAP with the Eionet schema. NOT for production.
FROM eeacms/ldapservice:v4.1

# eea.usersdb always connects over ldaps://, so serve TLS with a throwaway
# self-signed certificate (the client does not verify it).
RUN yum install -y openssl \
    && openssl req -x509 -nodes -newkey rsa:2048 -days 3650 \
       -subj "/CN=ldap" \
       -keyout /etc/pki/tls/private/server.key \
       -out /etc/pki/tls/certs/server.crt \
    && chown ldap:ldap /etc/pki/tls/private/server.key \
    && yum clean all

COPY seed.ldif /seed.ldif
