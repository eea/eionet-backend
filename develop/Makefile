##############################################################################
# Run:
#    make
#    make start
#    make setup
#
# Go to:
#
#     http://localhost:8080/Plone   (admin:admin)
#
##############################################################################
# SETUP MAKE
#
## Defensive settings for make: https://tech.davis-hansson.com/p/make/
SHELL:=bash
.ONESHELL:
.SHELLFLAGS:=-eu -o pipefail -O inherit_errexit -c
.SILENT:
.DELETE_ON_ERROR:
MAKEFLAGS+=--warn-undefined-variables
MAKEFLAGS+=--no-builtin-rules

IMAGE=eeacms/eionet-backend
PLATFORM=linux/amd64

# Top-level targets
.PHONY: all
all: sources build

.PHONY: sources
sources:		## Clone the add-ons from sources.ini into ./sources
	./scripts/clone.sh

.PHONY: build
build:			## Build the release image and the develop image
	docker build --platform $(PLATFORM) -t $(IMAGE) ..
	docker compose build

.PHONY: start
start:			## Start Plone, test LDAP and mailtrap (creates the site on first run)
	docker compose up -d
	echo "Plone:    http://localhost:8080/Plone (admin:admin)"
	echo "Mailtrap: http://localhost:8888"

.PHONY: setup
setup:			## Create the account tools inside the site (idempotent)
	docker compose stop backend
	docker compose run --rm backend run /app/scripts/setup_tools.py
	docker compose start backend

.PHONY: dump
dump:			## Refresh the naaya.ldapdump SQLite cache from LDAP
	docker compose exec -u plone backend bin/python -c \
	  'from eea.ldapadmin.ldapdump import dump_ldap; dump_ldap("/data/ldapdump")'

.PHONY: stop
stop:			## Stop all services
	docker compose stop

.PHONY: logs
logs:			## Follow Plone logs
	docker compose logs -f backend

.PHONY: status
status: 		## Check sources for changes
	./scripts/status.sh

.PHONY: pull
pull:			## Pull sources from git
	./scripts/pull.sh

.PHONY: clean
clean:			## Remove containers and volumes (site, LDAP data)
	docker compose down -v

.PHONY: help
help:			## Show this help.
	@echo -e "$$(grep -hE '^\S+:.*##' $(MAKEFILE_LIST) | sed -e 's/:.*##\s*/:/' -e 's/^\(.\+\):\(.*\)/\\x1b[36m\1\\x1b[m:\2/' | column -c2 -t -s :)"
	head -n 11 Makefile
