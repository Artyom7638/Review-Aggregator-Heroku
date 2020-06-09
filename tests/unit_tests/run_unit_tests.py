from tests.unit_tests.auth_test import test_login
from tests.unit_tests.review_test import test_review_rights
from tests.unit_tests.search_test import test_search


def run_unit_tests():
    test_login()
    test_search()
    test_review_rights()


if __name__ == '__main__':
    run_unit_tests()
