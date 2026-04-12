# -*- coding: utf-8 -*-

import pytest
import requests
from requests.sessions import Session
from requests.compat import is_py2


class TestSessionBinaryMethod:
    """Test that Session handles binary method names correctly."""
    
    @pytest.mark.skipif(is_py2, reason="Python 2 doesn't have this issue")
    def test_binary_method_conversion(self):
        """Test that binary method names are properly converted to strings."""
        session = Session()
        
        # Mock the send method to capture the prepared request
        prepared_requests = []
        original_send = session.send
        
        def mock_send(request, **kwargs):
            prepared_requests.append(request)
            # Create a mock response to avoid actual HTTP call
            from requests.models import Response
            response = Response()
            response.status_code = 200
            response._content = b'test content'
            response.headers = {}
            response.url = request.url
            return response
        
        session.send = mock_send
        
        # Test with binary method name
        try:
            session.request(b'GET', 'http://example.com')
            
            # Verify the method was properly converted
            assert len(prepared_requests) == 1
            prepared_request = prepared_requests[0]
            assert prepared_request.method == 'GET'
            assert isinstance(prepared_request.method, str)
            assert prepared_request.method != "b'GET'"
        finally:
            session.send = original_send
    
    @pytest.mark.skipif(is_py2, reason="Python 2 doesn't have this issue")
    def test_various_binary_methods(self):
        """Test various HTTP methods as binary strings."""
        session = Session()
        
        prepared_requests = []
        original_send = session.send
        
        def mock_send(request, **kwargs):
            prepared_requests.append(request)
            from requests.models import Response
            response = Response()
            response.status_code = 200
            response._content = b'test content'
            response.headers = {}
            response.url = request.url
            return response
        
        session.send = mock_send
        
        methods = [b'GET', b'POST', b'PUT', b'DELETE', b'HEAD', b'OPTIONS', b'PATCH']
        
        try:
            for method in methods:
                session.request(method, 'http://example.com')
            
            # Verify all methods were properly converted
            assert len(prepared_requests) == len(methods)
            for i, method in enumerate(methods):
                expected_method = method.decode('utf-8')
                actual_method = prepared_requests[i].method
                assert actual_method == expected_method
                assert isinstance(actual_method, str)
                assert not actual_method.startswith("b'")
        finally:
            session.send = original_send
    
    def test_regular_string_method_unchanged(self):
        """Test that regular string methods work as before."""
        session = Session()
        
        prepared_requests = []
        original_send = session.send
        
        def mock_send(request, **kwargs):
            prepared_requests.append(request)
            from requests.models import Response
            response = Response()
            response.status_code = 200
            response._content = b'test content'
            response.headers = {}
            response.url = request.url
            return response
        
        session.send = mock_send
        
        try:
            session.request('GET', 'http://example.com')
            
            assert len(prepared_requests) == 1
            prepared_request = prepared_requests[0]
            assert prepared_request.method == 'GET'
            assert isinstance(prepared_request.method, str)
        finally:
            session.send = original_send
