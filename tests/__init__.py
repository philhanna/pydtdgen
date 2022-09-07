__all__ = [
    'TEST_DATA_DIR',
]


def get_testdata_dir():
    import os
    init_file = os.path.abspath(__file__)
    tests_dir = os.path.dirname(init_file)
    project_root_dir = os.path.abspath(os.path.join(tests_dir, ".."))
    testdata_dir = os.path.join(project_root_dir, "testdata")
    return testdata_dir


TEST_DATA_DIR = get_testdata_dir()
