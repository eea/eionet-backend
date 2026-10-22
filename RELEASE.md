## Release

### Automatic release using Jenkins

#### Release flow

The release flow is split in 2 Jenkins jobs:

* A job that runs on every commit on master and creates a production ready GitHub release and tag
* A job that runs on every new tag (including the one created in the first job):
    * A new Docker image is built and released automatically on [DockerHub](https://hub.docker.com/r/eeacms/eionet-backend) with the release tag.

Release tags follow `<Plone version>-<n>`, e.g. `6.1.4-1`, computed by
`calculate_next_release.sh` from the `FROM` line of the `Dockerfile`.

#### How to start a Production release

* The automatic release is started by creating a [Pull Request](../../compare/master...develop) from `develop` to `master`. The pull request status checks correlated to the branch and PR Jenkins jobs need to be processed successfully. 1 review from a github user with rights is mandatory.
* It runs on every commit on `master` branch, which is protected from direct commits, only allowing pull request merge commits.
* The automatic release is done by [Jenkins](https://ci.eionet.europa.eu). Automated release scripts are located in the `eeacms/gitflow` docker image.

### Before the first release

The image must start and pass `./test/run.sh eeacms/eionet-backend:<tag>` with the
pinned add-on releases alone (no `develop/sources`). See the README.

## Production

The image is deployed with Rancher. See [README](README.md#production) for the
environment variables, volumes, first-run commands and cron jobs.
