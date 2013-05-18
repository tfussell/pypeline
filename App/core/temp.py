import contextlib

@contextlib.contextmanager
def tempdir():
    import shutil
    import tempfile

    temporary_directory = None

    try:
        temporary_directory = tempfile.mkdtemp(suffix='PyPipeline')
        yield temporary_directory
    finally:
        if temporary_directory:
            shutil.rmtree(temporary_directory)
