import pytest
from unittest.mock import Mock, patch
from requests.auth import HTTPDigestAuth
from requests import Request, PreparedRequest


class TestDigestAuthSemicolon:
    """Test HTTPDigestAuth handling of semicolons in URL paths."""

    def setup_method(self):
        self.auth = HTTPDigestAuth('username', 'password')
        self.auth.init_per_thread_state()
        # Set up a mock challenge
        self.auth._thread_local.chal = {
            'realm': 'test',
            'nonce': 'testnonce',
            'qop': 'auth',
            'algorithm': 'MD5'
        }
        self.auth._thread_local.last_nonce = 'testnonce'
        self.auth._thread_local.nonce_count = 1

    def test_semicolon_in_path_preserved(self):
        """Test that semicolons in URL paths are preserved in the uri field."""
        url = "https://example.com/path/with;semicolon/more?query=value"
        
        header = self.auth.build_digest_header('GET', url)
        
        assert 'uri="/path/with;semicolon/more?query=value"' in header

    def test_multiple_semicolons_preserved(self):
        """Test that multiple semicolons in URL paths are preserved."""
        url = "https://example.com/path;param1=value1;param2=value2/more?query=value"
        
        header = self.auth.build_digest_header('GET', url)
        
        assert 'uri="/path;param1=value1;param2=value2/more?query=value"' in header

    def test_semicolon_without_query_params(self):
        """Test semicolons in path without query parameters."""
        url = "https://example.com/path/with;semicolon"
        
        header = self.auth.build_digest_header('GET', url)
        
        assert 'uri="/path/with;semicolon"' in header

    def test_musicbrainz_example(self):
        """Test the specific MusicBrainz example from the issue."""
        url = "https://musicbrainz.org/ws/2/collection/53f4a001-eb45-4b72-9ec5-41109e88710d/releases/7dc2cfbd-5bd8-4ebc-b20b-4344985431da;38347564-5ef3-46dd-ad87-fe6d6f1e7b19?fmt=json&client=manual-python-requests-test"
        
        header = self.auth.build_digest_header('PUT', url)
        
        expected_uri = '/ws/2/collection/53f4a001-eb45-4b72-9ec5-41109e88710d/releases/7dc2cfbd-5bd8-4ebc-b20b-4344985431da;38347564-5ef3-46dd-ad87-fe6d6f1e7b19?fmt=json&client=manual-python-requests-test'
        assert f'uri="{expected_uri}"' in header

    def test_root_path_with_semicolon(self):
        """Test semicolon in root path."""
        url = "https://example.com/;param=value"
        
        header = self.auth.build_digest_header('GET', url)
        
        assert 'uri="/;param=value"' in header

    def test_empty_path_fallback(self):
        """Test that empty paths still default to '/'."""
        url = "https://example.com"
        
        header = self.auth.build_digest_header('GET', url)
        
        assert 'uri="/"' in header

    def test_path_with_fragment_removed(self):
        """Test that fragments are properly removed from the uri."""
        url = "https://example.com/path;param=value?query=test#fragment"
        
        header = self.auth.build_digest_header('GET', url)
        
        assert 'uri="/path;param=value?query=test"' in header
        assert '#fragment' not in header

    def test_semicolon_in_query_params(self):
        """Test semicolons in query parameters are preserved."""
        url = "https://example.com/path?param1=value;with;semicolons&param2=value2"
        
        header = self.auth.build_digest_header('GET', url)
        
        assert 'uri="/path?param1=value;with;semicolons&param2=value2"' in header

    def test_complex_url_with_semicolons(self):
        """Test complex URL with semicolons in both path and query."""
        url = "https://example.com/path;pathparam=value/subpath;anotherparam?query;param=value&normal=param"
        
        header = self.auth.build_digest_header('GET', url)
        
        assert 'uri="/path;pathparam=value/subpath;anotherparam?query;param=value&normal=param"' in header
