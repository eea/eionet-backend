#!/bin/bash
# The image on its own: create a Classic site, run the setup script, start,
# and check the account tools are served. No LDAP server is needed for these
# pages to render.
set -eo pipefail

dir="$(dirname "$(readlink -f "$BASH_SOURCE")")"

image="$1"

PLONE_TEST_SLEEP=10
PLONE_TEST_TRIES=10

vol="eionet-tools-$RANDOM-$RANDOM"
cname="plone-container-$RANDOM-$RANDOM"
env=(
	-e SITE_ID=Plone
	-e LDAP_SERVER=ldap.invalid:636
	-e LDAP_ADMIN_DN=cn=admin,o=EIONET,l=Europe
	-e LDAP_ADMIN_PW=test #betterleaks:allow
)
docker volume create "$vol" > /dev/null
trap "docker rm -vf $cname > /dev/null 2>&1; docker volume rm $vol > /dev/null" EXIT

docker run --rm -v "$vol:/data" "${env[@]}" "$image" create-classic > /dev/null
docker run --rm -v "$vol:/data" "${env[@]}" "$image" run /app/scripts/setup_tools.py > /dev/null
docker run -d --name "$cname" -v "$vol:/data" "$image" > /dev/null

get() {
	docker run --rm -i \
		--link "$cname":plone \
		--entrypoint /app/bin/python \
		"$image" \
		-c "from urllib.request import urlopen; con = urlopen('$1'); print(con.read())"
}

get_auth() {
	docker run --rm -i \
		--link "$cname":plone \
		--entrypoint /app/bin/python \
		"$image" \
		-c "from urllib.request import urlopen, Request; request = Request('$1'); request.add_header('Authorization', 'Basic $2'); print(urlopen(request).read())"
}

. "$dir/../../retry.sh" --tries "$PLONE_TEST_TRIES" --sleep "$PLONE_TEST_SLEEP" get "http://plone:8080"

auth="$(echo -n 'admin:admin' | base64)"

# Public: password reset, anonymous
[[ "$(get 'http://plone:8080/Plone/password-reset')" == *"password"* ]]

# Admin tools: dashboard (folder default page) lists the three tools
dashboard="$(get_auth 'http://plone:8080/Plone/eionet-account-tools' "$auth")"
[[ "$dashboard" == *"Roles Editor"* ]]
[[ "$dashboard" == *"User Admin"* ]]
[[ "$dashboard" == *"Organisations"* ]]

# Root-level tool instances exist and carry the LDAP settings from the setup
# script (their main pages need a reachable LDAP, so check the settings form)
[[ "$(get_auth 'http://plone:8080/Plone/ldap-roles/manage_edit' "$auth")" == *"ldap.invalid"* ]]
[[ "$(get_auth 'http://plone:8080/Plone/ldap-organisations/manage_edit' "$auth")" == *"ldap.invalid"* ]]
