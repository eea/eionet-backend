#!/usr/bin/env bash
globalTests+=(
        utc
        no-hard-coded-passwords
        override-cmd
)

imageTests+=(
	[eeacms/eionet-backend]='
		plone-basics
		plone-site
		plone-arbitrary-user
		plone-listenport
		plone-zeoclient
		plone-relstorage
		eionet-tools
	'
)

globalExcludeTests+=(

)
