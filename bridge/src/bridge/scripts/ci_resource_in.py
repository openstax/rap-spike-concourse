import json
import sys

import psycopg2

from ..concourse import concourse_method
from ..utils import get_resources


@concourse_method(required_source=('db',), required_params=('ident_hash',))
def main(input_, environ):
    db_url = input_['source']['db']
    ident_hash = input_['params']['ident_hash']

    with psycopg2.connect(db_url) as db_conn:
        with db_conn.cursor() as cursor:
            # TODO extract the Archive API response ... not starting
            #      here because the code associated with this is a mess
            #      to untangle from it's current implementation.

            cursor.execute("select true")
            b = cursor.fetchone()[0]
            if not b:
                raise RuntimeError("didn't work")

            for content, sha1, metadata in get_resources(cursor, ident_hash):
                with open(sha1, 'wb') as f:
                    f.write(content[:])
                with open('{}.metadata.json'.format(sha1), 'w') as f:
                    json.dump(metadata, f)

    output = {'version': ident_hash}
    return output
