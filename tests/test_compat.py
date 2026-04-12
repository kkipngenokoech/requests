# -*- coding: utf-8 -*-

import sys
import pytest
from requests.compat import builtin_str, is_py2, is_py3


class TestBuiltinStr:
    """Test builtin_str function handles binary strings correctly."""
    
    def test_regular_string(self):
        """Test that regular strings are handled correctly."""
        result = builtin_str('GET')
        assert result == 'GET'
        assert isinstance(result, str)
    
    def test_unicode_string(self):
        """Test that unicode strings are handled correctly."""
        if is_py2:
            result = builtin_str(u'GET')
            assert result == 'GET'
        else:
            result = builtin_str('GET')
            assert result == 'GET'
            assert isinstance(result, str)
    
    def test_binary_string(self):
        """Test that binary strings are decoded properly."""
        result = builtin_str(b'GET')
        if is_py2:
            # In Python 2, bytes and str are the same
            assert result == 'GET'
        else:
            # In Python 3, should decode bytes to str
            assert result == 'GET'
            assert isinstance(result, str)
            assert result != "b'GET'"  # Should not be string representation
    
    def test_binary_string_with_utf8(self):
        """Test that binary strings with UTF-8 content are decoded properly."""
        result = builtin_str(b'POST')
        assert result == 'POST'
        assert isinstance(result, str)
    
    def test_none_value(self):
        """Test that None values are handled correctly."""
        result = builtin_str(None)
        assert result == 'None'
    
    def test_integer_value(self):
        """Test that integer values are converted to string."""
        result = builtin_str(123)
        assert result == '123'
        assert isinstance(result, str)
    
    @pytest.mark.skipif(is_py2, reason="Python 2 doesn't have this issue")
    def test_binary_method_names(self):
        """Test common HTTP method names as binary strings."""
        methods = [b'GET', b'POST', b'PUT', b'DELETE', b'HEAD', b'OPTIONS', b'PATCH']
        for method in methods:
            result = builtin_str(method)
            expected = method.decode('utf-8')
            assert result == expected
            assert isinstance(result, str)
            # Ensure it's not the string representation
            assert not result.startswith("b'")
