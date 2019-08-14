import json
from pathlib import Path

import click
import psycopg2

from .utils import get_resources, get_content, ContentNotFoundError


def gen_resource_filepath(dest_dir, sha1):
    return dest_dir / sha1


def gen_resource_metadata_filepath(dest_dir, sha1):
    return dest_dir / f'{sha1}.metadata.json'


@click.command()
@click.option('-o', '--output-dir', default='.',
              type=click.Path(exists=True, file_okay=False, writable=False))
@click.argument('ident_hash')
@click.argument('db_url', envvar='DB_URL')
def extract(output_dir, ident_hash, db_url):
    """Extracts the requested content by ``ident_hash`` to the filesystem"""
    dest_dir = Path(output_dir).resolve()

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
            content = get_content(cursor, ident_hash)
            with (dest_dir / 'archive-response.raw.json').open('w') as f:
                f.write(json.dumps(content, sort_keys=True, indent=2))


@click.group()
def main():
    pass


main.add_command(extract)
    

if __name__ == '__main__':
    main()
