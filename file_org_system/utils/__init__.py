"""
Configuration Loader - Handles loading and validation of system configuration
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional

class ConfigLoader:
    """Handles loading and validation of configuration files"""
    
    @staticmethod
    def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Load configuration from YAML file
        
        Args:
            config_path: Path to config file (default: config.yaml in project root)
            
        Returns:
            Configuration dictionary
        """
        if config_path is None:
            # Default to config.yaml in project root
            project_root = Path(__file__).parent.parent.parent
            config_path = project_root / "config.yaml"
        
        config_path = Path(config_path)
        
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        try:
            with open(config_path, 'r', encoding='utf-8') as file:
                config = yaml.safe_load(file)
            
            # Validate configuration structure
            ConfigLoader._validate_config(config)
            
            return config
            
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in configuration file: {e}")
        except Exception as e:
            raise RuntimeError(f"Failed to load configuration: {e}")
    
    @staticmethod
    def _validate_config(config: Dict[str, Any]) -> None:
        """
        Validate configuration structure and required fields
        
        Args:
            config: Configuration dictionary to validate
        """
        required_sections = ['system', 'file_organization', 'cloud', 'layout']
        
        for section in required_sections:
            if section not in config:
                raise ValueError(f"Missing required configuration section: {section}")
        
        # Validate system section
        system_config = config['system']
        if 'analysis_depth' not in system_config:
            raise ValueError("Missing 'analysis_depth' in system configuration")
        
        valid_depths = ['basic', 'standard', 'comprehensive']
        if system_config['analysis_depth'] not in valid_depths:
            raise ValueError(f"Invalid analysis_depth. Must be one of: {valid_depths}")
        
        # Validate file organization section
        file_org_config = config['file_organization']
        if 'categories' not in file_org_config:
            raise ValueError("Missing 'categories' in file_organization configuration")
        
        # Validate cloud section
        cloud_config = config['cloud']
        if 'providers' not in cloud_config:
            raise ValueError("Missing 'providers' in cloud configuration")
        
        # Validate layout section
        layout_config = config['layout']
        if 'style' not in layout_config:
            raise ValueError("Missing 'style' in layout configuration")
    
    @staticmethod
    def get_default_config() -> Dict[str, Any]:
        """
        Get default configuration
        
        Returns:
            Default configuration dictionary
        """
        return {
            'system': {
                'analysis_depth': 'comprehensive',
                'backup_before_changes': True,
                'create_reports': True
            },
            'file_organization': {
                'categories': {
                    'documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt'],
                    'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp'],
                    'videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm'],
                    'audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma'],
                    'archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'],
                    'code': ['.py', '.js', '.html', '.css', '.cpp', '.java', '.c', '.php'],
                    'spreadsheets': ['.xls', '.xlsx', '.csv', '.ods'],
                    'presentations': ['.ppt', '.pptx', '.odp']
                },
                'organization_rules': {
                    'create_year_folders': True,
                    'create_type_folders': True,
                    'remove_duplicates': True,
                    'optimize_names': True
                }
            },
            'cloud': {
                'providers': {
                    'aws': {'enabled': False, 'bucket_name': '', 'region': 'us-east-1'},
                    'google': {'enabled': False, 'bucket_name': '', 'project_id': ''},
                    'azure': {'enabled': False, 'container_name': '', 'account_name': ''}
                },
                'sync_options': {
                    'auto_upload': False,
                    'compress_before_upload': True,
                    'encryption_enabled': True
                }
            },
            'layout': {
                'style': 'professional',
                'theme': 'modern',
                'generate_thumbnails': True,
                'create_shortcuts': True,
                'organize_desktop': True
            }
        }