import sys
from unittest.mock import MagicMock
import importlib.util

# ✅ Global mock for torchvision to bypass environment-specific RuntimeError (e.g., missing nms operator)
# This allows transformers and sentence-transformers to function correctly for text tasks
# even if the torchvision binary extensions are broken in this environment.
try:
    import torchvision
    # Test if it's broken by trying to access a potentially problematic submodule
    from torchvision.transforms.v2 import functional
except Exception:
    for pkg in ["torchvision", "torchvision.ops", "torchvision.transforms", "torchvision.transforms.v2", "torchvision.io"]:
        mock = MagicMock()
        mock.__path__ = []
        mock.__spec__ = importlib.util.spec_from_loader(pkg, None)
        sys.modules[pkg] = mock
