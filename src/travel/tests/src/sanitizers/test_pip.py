import pytest
from travel.config.sanitizers.pip_sanitizer import sanitize_package, sanitize_version, sanitize_versioned_package


def test_pip_sanitizer():

    package = "stran2e-test_w"
    assert sanitize_package(package) == package
    with pytest.raises(AssertionError):
        sanitize_package(" sc0+ ")

    version = "3.4.2"
    assert sanitize_version(version) == version
    with pytest.raises(AssertionError):
        sanitize_version("9sc0' ")
    
    simple = "example==5.8.4"
    assert sanitize_versioned_package(simple) == simple
    with pytest.raises(AssertionError):
        sanitize_versioned_package("something>=3,<=5&&ok")
    with pytest.raises(AssertionError):
        sanitize_versioned_package("ok || rm -rf *")
    
    complex = "example>5.4.*, !=6.0.0,  <=6.9.8   "
    assert sanitize_versioned_package(complex) == complex
    with pytest.raises(AssertionError):
        sanitize_versioned_package(complex + ", echo ok && rm -rf *")
