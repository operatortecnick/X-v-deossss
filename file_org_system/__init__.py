"""
File Organization System - Professional File Management and Computer Analysis

A comprehensive system that analyzes computers, suggests file organization improvements,
and creates professional layouts with cloud integration.
"""

__version__ = "1.0.0"
__author__ = "File Organization System Team"
__email__ = "info@fileorgsystem.com"

from .core.main_controller import FileOrgController
from .analyzers.system_analyzer import SystemAnalyzer
from .organizers.file_organizer import FileOrganizer
from .layouts.layout_manager import LayoutManager
from .cloud.cloud_integrator import CloudIntegrator

__all__ = [
    'FileOrgController',
    'SystemAnalyzer', 
    'FileOrganizer',
    'LayoutManager',
    'CloudIntegrator'
]