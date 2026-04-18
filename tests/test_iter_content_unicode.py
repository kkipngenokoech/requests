import requests
import json
from requests.models import Response
from requests.structures import CaseInsensitiveDict
from io import BytesIO

def test_issue_reproduction():
    # Create a mock response with JSON content
    response = Response()
    response.status_code = 200
    response.headers = CaseInsensitiveDict({'Content-Type': 'application/json; charset=utf-8'})
    response.encoding = 'utf-8'
    
    # Set up raw content as bytes (JSON data)
    json_data = '{"key": "value"}'
    json_bytes = json_data.encode('utf-8')
    response.raw = BytesIO(json_bytes)
    response._content = json_bytes
    response._content_consumed = False
    
    # Test that r.text returns unicode
    text_result = response.text
    assert isinstance(text_result, str), f"r.text should return unicode, got {type(text_result)}"
    
    # Reset raw for iter_content test
    response.raw = BytesIO(json_bytes)
    response._content_consumed = False
    
    # Test that iter_content with decode_unicode=True should also return unicode
    iter_result = next(response.iter_content(16*1024, decode_unicode=True))
    assert isinstance(iter_result, str), f"iter_content(decode_unicode=True) should return unicode, got {type(iter_result)} with value {repr(iter_result)}"
    
    # Both should have the same content
    assert text_result == iter_result, "Both r.text and iter_content(decode_unicode=True) should return the same unicode content"