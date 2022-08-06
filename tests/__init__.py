__all__ = [
    'TEST_DATA_DIR',
]


def get_testdata_dir():
    import os
    root_dir = os.path.dirname(os.path.abspath(__file__))
    testdata_dir = os.path.join(root_dir, "testdata")
    return testdata_dir


TEST_DATA_DIR = get_testdata_dir()
