import pytest
import sys
from taskmd_lite.cli import get_parser, TaskMDParser

def test_parser_unification():
    # Test External (interactive=False)
    p_ext = get_parser(interactive=False)
    
    # Passing invalid sub-command directly external should normally raise SystemExit(1)
    with pytest.raises(SystemExit) as exc:
        p_ext.parse_args(["invalid_command"])
        
    assert exc.value.code == 1
    
    # Test Internal REPL (interactive=True)
    p_int = get_parser(interactive=True)
    
    # Passing invalid sub-command internal should raise ValueError to bounce back to prompt
    with pytest.raises(ValueError) as excinfo:
        p_int.parse_args(["invalid_command"])
        
    assert "invalid choice: 'invalid_command'" in str(excinfo.value)
    
    # Ensure -h outputs help securely raising custom loop catcher
    with pytest.raises(RuntimeError) as excinfo_h:
        p_int.parse_args(["-h"])
        
    assert "InteractiveContinue" in str(excinfo_h.value)
