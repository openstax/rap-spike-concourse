import os
import sys
import json
from functools import wraps


ENV_VAR_NAMES = (
    'BUILD_ID',
    'BUILD_NAME',
    'BUILD_JOB_NAME',
    'BUILD_PIPELINE_NAME',
    'BUILD_TEAM_NAME',
    'ATC_EXTERNAL_URL',
)


def get_environ():
    """Returns the environment variables for the job
    Note, these variables aren't available on `check`,
    so the results of this function will be an empty dict in that case.

    """
    e = {}
    for var in ENV_VAR_NAMES:
        v = os.environ.get(var)
        if v: e[var] = v
    return e



def concourse_method(required_source=None, required_params=None):
    def decorator(func):
        @wraps(func)
        def wrapper():
            env = get_environ()
            try:
                input_ = json.load(sys.stdin)
            except json.decoder.JSONDecodeError:
                print("problem decoding the given JSON input", file=sys.stderr)
                sys.exit(1)
            # TODO verify required values specified by
            #      `required_source` & `required_params`
            print(json.dumps(func(input_, env)))
            return 0
        return wrapper
    return decorator
