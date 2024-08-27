import importlib
import os
import sys
import unittest

from application.models.db.company_model import Base
from application.models.db.connection import engine


def discover_and_run_tests(test_directory):
    # Discover all the test cases in the specified directory
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=test_directory)

    # Run the test suite
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Return appropriate exit code
    if result.wasSuccessful():
        return 0
    else:
        return 1


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    importlib.import_module("migration")

    os.environ["PYTHON_ENV"] = "TEST"
    sys.path.insert(0, "tests")
    result = discover_and_run_tests("tests")

    Base.metadata.drop_all(engine)
    sys.exit(result)
