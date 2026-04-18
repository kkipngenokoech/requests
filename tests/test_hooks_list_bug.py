import requests
from requests.models import Request
from requests.hooks import dispatch_hook

def test_issue_reproduction():
    """Test that passing a list of hook functions fails due to improper parsing."""
    
    # Create some mock hook functions
    def hook1(response, *args, **kwargs):
        response.hook1_called = True
        return response
    
    def hook2(response, *args, **kwargs):
        response.hook2_called = True
        return response
    
    # Create a request with a list of hooks - this should work but currently fails
    hooks = {'response': [hook1, hook2]}
    
    request = Request(
        url='http://example.com',
        method='GET',
        hooks=hooks
    )
    
    # The hooks should be stored as individual callable functions
    # But currently they get wrapped in a list, making them non-callable
    assert len(request.hooks['response']) == 2, f"Expected 2 hooks, got {len(request.hooks['response'])}"
    
    # Try to dispatch the hooks - this will fail because the list is not callable
    class MockResponse:
        pass
    
    response = MockResponse()
    
    # This should work but will fail because hooks are stored as [hook1, hook2] instead of hook1, hook2
    try:
        result = dispatch_hook('response', request.hooks, response)
        # If we get here, the hooks were callable (which means the bug is fixed)
        assert hasattr(result, 'hook1_called') and hasattr(result, 'hook2_called')
    except TypeError as e:
        # This is the expected failure - the list is not callable
        assert "'list' object is not callable" in str(e)
        # This assertion will fail, demonstrating the bug
        assert False, "Bug reproduced: list of hooks is not callable"