def pytest_generate_tests(metafunc):
    # called once per each test function
    if getattr(metafunc.cls, "params", None) is None:
        return
    elif metafunc.function.__name__ not in metafunc.cls.params:
        return
    funcarglist = metafunc.cls.params[metafunc.function.__name__]
    argnames = sorted(funcarglist[0])
    metafunc.parametrize(
        argnames, [[funcargs[name] for name in argnames] for funcargs in funcarglist]
    )
