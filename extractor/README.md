# Database Content Extraction Utility

This application extracts content from the database to the filesystem. Deployed as a Docker Container for use within Concourse-CI, but can also be used as an independent command to invoke from the commandline.

## Installation

See the Dockerfile for custom installation. <;0)

## Usage

```
echo $source-prams-data | docker run -rm -v $(PWD):/var/output openstax/rap-spike--extractor /opt/resource/out
```
