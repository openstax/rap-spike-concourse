# Database Content Bridge Utility

This application extracts content from the database to the filesystem. Deployed as a Docker Container for use within Concourse-CI, but can also be used as an independent command to invoke from the commandline.

## Installation

See the Dockerfile for custom installation. <;0)

## Usage

```
echo $source-prams-data | docker run -rm -v $(PWD):/var/output openstax/rap-spike--bridge /opt/resource/out
```


## Concourse Interface

This project acts as a Concourse Resource for extracting content from the CNX Database.

## Source Configuration

* `db`: The database connection URL (e.g. `postgresql://rhaptos@cnx-db/repository`)

## Behavior

### `check`: Produce timestamps satisfying the interval.

Not implemented

### `in`: Report the given time.

Extracts the content specified by the given `ident_hash`. The contents of `index.cnxml`, `index.cnxml.html` and any resource files are extracted to `$1`.

The files in `$1` are identified by their SHA1 hash. These files also have an accompanying metadata file named `<SHA1>.metadata.json`.

#### Parameters

* `ident_hash`: The ident-hash of a specific piece of content (page or book) (e.g. `4b5aaf32-1de1-419b-bdc0-4e0a7f6daf0f@27`)

### `out`: Produce the current time.

Not implemented

#### Parameters

*None.*


## License

This software is subject to the provisions of the GNU Affero General
Public License Version 3.0 (AGPL). See license.txt for details.
Copyright (c) 2019 Rice University
