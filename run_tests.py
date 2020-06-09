from test_server import testing_app, testing_db
from tests.functional_tests.run_functional_tests import run_functional_tests
from tests.unit_tests.run_unit_tests import run_unit_tests


if __name__ == '__main__':
    run_unit_tests()
    run_functional_tests(testing_app, testing_db)
