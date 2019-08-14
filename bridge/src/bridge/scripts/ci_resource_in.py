import json
import sys
from pathlib import Path
from datetime import datetime

import psycopg2

from ..concourse import concourse_method
from ..utils import get_resources, get_content, ContentNotFoundError


def gen_resource_filepath(dest_dir, sha1):
    return dest_dir / sha1


def gen_resource_metadata_filepath(dest_dir, sha1):
    return dest_dir / f'{sha1}.metadata.json'


@concourse_method(required_source=('db',), required_params=('ident_hash',))
def main(input_, environ, args):
    dest_dir = Path(args[0])
    db_url = input_['source']['db']
    ident_hash = input_['params']['ident_hash']

    with psycopg2.connect(db_url) as db_conn:
        with db_conn.cursor() as cursor:
            # TODO extract the Archive API response ... not starting
            #      here because the code associated with this is a mess
            #      to untangle from it's current implementation.

            # A simple test for connectivity
            cursor.execute("select true")
            b = cursor.fetchone()[0]
            if not b:
                raise RuntimeError("didn't work")

            # Extract:
            #   - the named file content (e.g. index.cnxml, index.cnxml.html)
            #   - the resource files referenced in the content
            for content, sha1, metadata in get_resources(cursor, ident_hash):
                with gen_resource_filepath(dest_dir, sha1).open('wb') as f:
                    f.write(content[:])
                with gen_resource_metadata_filepath(dest_dir, sha1).open(
                        'w') as f:
                    json.dump(metadata, f)

            # Store the module metadata in a json file
            try:
                content = get_content(cursor, ident_hash)
            except ContentNotFoundError as e:
                sys.stderr.write(str(e) + '\n')
                sys.exit(1)
            with (dest_dir / 'archive-response.raw.json').open('w') as f:
                f.write(json.dumps(content, sort_keys=True, indent=2))

    version = {'timestamp': str(datetime.now().timestamp())}
    output = {
        'version': version,
        'metadata': [
            {'name': 'ident_hash', 'value': ident_hash},
        ]
    }
    return output
