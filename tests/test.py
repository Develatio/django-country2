import os
import argparse
import sys

from nose.core import run


os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings'

def main():
    description = "Runs django-country unit and/or integration tests."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-t', '--service-tests', action='append', default=[],
                        help="Run tests for a given service.  This will "
                        "run any test tagged with the specified value, "
                        "e.g -t s3 -t chat")
    known_args, remaining_args = parser.parse_known_args()
    attribute_args = []
    for service_attribute in known_args.service_tests:
        attribute_args.extend(['-a', '!notdefault,' +service_attribute])
    if not attribute_args:
        attribute_args = ['-a', '!notdefault']
    all_args = [__file__] + attribute_args + remaining_args
    print "nose command: {0}".format(' '.join(all_args))
    if run(argv=all_args):
        return 0
    else:
        return 1

if __name__ == "__main__":
    sys.exit(main())
