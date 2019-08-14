# Database Content Bridge Utility

This application extracts content from the database to the filesystem. Deployed as a Docker Container for use within Concourse-CI, but can also be used as an independent command to invoke from the commandline.

## Installation

See the Dockerfile for custom installation. <;0)

Otherwise use `make build-image` to build the image.

See `make help` for additional commands.

## Usage

### As an App

```
bridge --help
```

### As a Concourse task

Execute any of the tasks in `./tasks` directory, which are also mounted within the container at `/tasks`.

## License

This software is subject to the provisions of the GNU Affero General
Public License Version 3.0 (AGPL). See license.txt for details.
Copyright (c) 2019 Rice University
