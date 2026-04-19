import requests
from requests.models import Request

def test_issue_reproduction():
    """Test that hooks parameter accepts lists of hook functions."""
    
    # Define two simple hook functions
    def hook1(response, *args, **kwargs):
        response.hook1_called = True
        return response
    
    def hook2(response, *args, **kwargs):
        response.hook2_called = True
        return response
    
    # Create a request with a list of hooks for the 'response' event
    hooks = {'response': [hook1, hook2]}
    
    # This should work but currently fails because the list gets wrapped in another list
    request = Request(
        url='http://httpbin.org/get',
        method='GET',
        hooks=hooks
    )
    
    # Verify that both hooks are properly registered
    # The hooks should be individual callables, not a list wrapped in a list
    assert len(request.hooks['response']) == 2
    assert callable(request.hooks['response'][0])
    assert callable(request.hooks['response'][1])
    
    # Verify the hooks are the actual functions we passed
    assert hook1 in request.hooks['response']
    assert hook2 in request.hooks['response']