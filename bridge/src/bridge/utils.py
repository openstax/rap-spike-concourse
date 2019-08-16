import os
from pathlib import Path

import cnxdb


CNXDB_DIRECTORY = Path(cnxdb.__file__).parent
SQL_DIRECTORY = CNXDB_DIRECTORY / 'archive-sql'
GET_RESOURCES_SQL = """\
SELECT f.file, f.sha1, mf.filename, f.media_type
FROM files f
    NATURAL JOIN module_files mf
    NATURAL JOIN modules m
WHERE ident_hash(m.uuid, m.major_version, m.minor_version) = %s
"""
PORTALTYPE_TO_MIMETYPE = {
    'Module': 'application/vnd.org.cnx.module',
    'CompositeModule': 'application/vnd.org.cnx.composite-module',
    'Collection': 'application/vnd.org.cnx.collection',
    'SubCollection': 'application/vnd.org.cnx.subcollectio',
}


class ContentNotFoundError(Exception):
    pass


def _read_sql_file(name):
    with (SQL_DIRECTORY / '{}.sql'.format(name)).open('r') as f:
        return f.read()


# From cnxarchive.views.helpers.get_content_metadata
def get_content_metadata(cursor, ident_hash):
    id, version = ident_hash.split('@', 1)
    cursor.execute(_read_sql_file('get-module-metadata'), {
        'id': id, 'version': version})
    try:
        result = cursor.fetchone()[0]

        # version is what we want to return, but in the sql we're using
        # current_version because otherwise there's a "column reference is
        # ambiguous" error
        result['version'] = result.pop('current_version')

        result['mediaType'] = PORTALTYPE_TO_MIMETYPE[result['mediaType']]

        return result
    except (TypeError, IndexError):
        raise ContentNotFoundError('Content not found: {}'.format(ident_hash))


# From cnxarchive.views.content.get_content
def get_content(cursor, ident_hash):
    metadata = get_content_metadata(cursor, ident_hash)
    id, version = ident_hash.split('@', 1)
    if metadata.get('canonical'):
        canonical_id = '{}:{}'.format(metadata['canonical'], id)
    else:
        canonical_id = id
    metadata['canon_url'] = 'https://{}/contents/{}/{}'.format(
        os.getenv('CANONICAL_HOSTNAME', 'cnx.org'), canonical_id,
        '-'.join(metadata['title'].split()))
    if metadata['mediaType'] == PORTALTYPE_TO_MIMETYPE['Collection']:
        # Just get the raw tree in this spike
        as_collated = False
        cursor.execute(_read_sql_file('get-tree-by-uuid-n-version'), (
            id, version, as_collated))
        try:
            metadata['tree'] = cursor.fetchone()[0]
        except (TypeError, IndexError):
            raise ContentNotFoundError(
                'Unable to build tree for {}'.format(ident_hash))
    else:
        cursor.execute(_read_sql_file('get-resource-by-filename'), {
            'id': id, 'version': version, 'filename': 'index.cnxml.html'})
        try:
            content = cursor.fetchone()[0]
            metadata['content'] = bytes(content).decode('utf-8')
        except (TypeError, IndexError):
            raise ContentNotFoundError(
                'index.cnxml.html not found: {}'.format(ident_hash))
    return metadata


def get_resources(cursor, ident_hash):
    cursor.execute(GET_RESOURCES_SQL, (ident_hash,))
    for resource in cursor.fetchall():
        yield resource[0], resource[1], dict(
            zip(('filename', 'media_type'), resource[2:]))
