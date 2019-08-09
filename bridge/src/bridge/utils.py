GET_RESOURCES_SQL = """\
SELECT f.file, f.sha1, mf.filename, f.media_type
FROM files f
    NATURAL JOIN module_files mf
    NATURAL JOIN modules m
WHERE ident_hash(m.uuid, m.major_version, m.minor_version) = %s
"""


def get_resources(cursor, ident_hash):
    cursor.execute(GET_RESOURCES_SQL, (ident_hash,))
    for resource in cursor.fetchall():
        yield resource[0], resource[1], dict(
            zip(('filename', 'media_type'), resource[2:]))
