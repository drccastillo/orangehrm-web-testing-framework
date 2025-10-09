"""
Mixins for Interface Segregation Principle.
Allow pages to include only the capabilities they need.
"""
from .element_finder_mixin import ElementFinderMixin
from .element_interactor_mixin import ElementInteractorMixin
from .element_validator_mixin import ElementValidatorMixin
from .navigation_mixin import NavigationMixin
from .javascript_mixin import JavaScriptMixin
from .visual_debug_mixin import VisualDebugMixin

__all__ = [
    'ElementFinderMixin',
    'ElementInteractorMixin',
    'ElementValidatorMixin',
    'NavigationMixin',
    'JavaScriptMixin',
    'VisualDebugMixin',
]
