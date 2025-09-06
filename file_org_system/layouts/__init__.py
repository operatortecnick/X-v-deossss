"""
Layout Manager - Professional layout creation and management

This module provides professional layout generation including:
- Dynamic layout styles (professional, minimal, dynamic)
- Theme application (modern, classic, corporate)
- Desktop organization and shortcuts
- Professional folder icons and thumbnails
- Clean and organized visual presentation
"""

import os
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional
from ..utils.logger import get_logger

logger = get_logger(__name__)

class LayoutManager:
    """Professional layout creation and management"""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the layout manager with configuration"""
        self.config = config
        self.layout_config = config['layout']
        logger.info("LayoutManager initialized")
    
    def generate_layout_config(self, style: str = "professional", 
                             theme: str = "modern") -> Dict[str, Any]:
        """
        Generate layout configuration based on style and theme
        
        Args:
            style: Layout style (professional, minimal, dynamic)
            theme: Layout theme (modern, classic, corporate)
            
        Returns:
            Layout configuration dictionary
        """
        logger.info(f"Generating layout config - Style: {style}, Theme: {theme}")
        
        config = {
            'style': style,
            'theme': theme,
            'created_at': datetime.now().isoformat(),
            'colors': self._get_theme_colors(theme),
            'typography': self._get_typography_settings(style, theme),
            'spacing': self._get_spacing_settings(style),
            'icons': self._get_icon_settings(theme),
            'layout_rules': self._get_layout_rules(style),
            'folder_organization': self._get_folder_organization_rules(style),
            'desktop_settings': self._get_desktop_settings(style, theme)
        }
        
        return config
    
    def create_layout_elements(self, layout_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create layout elements based on configuration
        
        Args:
            layout_config: Configuration from generate_layout_config
            
        Returns:
            Dictionary with created layout elements
        """
        logger.info("Creating layout elements")
        
        elements = {
            'folder_icons': self._create_folder_icons(layout_config),
            'shortcuts': self._create_shortcuts(layout_config),
            'thumbnails': self._create_thumbnails(layout_config),
            'organization_structure': self._create_organization_structure(layout_config),
            'desktop_arrangement': self._create_desktop_arrangement(layout_config),
            'style_sheets': self._create_style_definitions(layout_config)
        }
        
        return elements
    
    def apply_layout(self, layout_config: Dict[str, Any], 
                    layout_elements: Dict[str, Any]) -> None:
        """
        Apply layout configuration and elements to the system
        
        Args:
            layout_config: Layout configuration
            layout_elements: Layout elements to apply
        """
        logger.info("Applying layout configuration")
        
        try:
            # Apply folder organization
            if self.layout_config.get('organize_desktop', True):
                self._apply_desktop_organization(layout_elements['desktop_arrangement'])
            
            # Create shortcuts
            if self.layout_config.get('create_shortcuts', True):
                self._apply_shortcuts(layout_elements['shortcuts'])
            
            # Generate thumbnails
            if self.layout_config.get('generate_thumbnails', True):
                self._apply_thumbnails(layout_elements['thumbnails'])
            
            # Apply folder icons
            self._apply_folder_icons(layout_elements['folder_icons'])
            
            # Save layout configuration
            self._save_layout_configuration(layout_config, layout_elements)
            
            logger.info("Layout applied successfully")
            
        except Exception as e:
            logger.error(f"Failed to apply layout: {e}")
            raise
    
    def _get_theme_colors(self, theme: str) -> Dict[str, str]:
        """Get color scheme for theme"""
        color_schemes = {
            'modern': {
                'primary': '#2563eb',      # Blue
                'secondary': '#64748b',    # Slate
                'accent': '#06b6d4',       # Cyan
                'background': '#f8fafc',   # Light gray
                'surface': '#ffffff',      # White
                'text_primary': '#1e293b', # Dark slate
                'text_secondary': '#64748b' # Slate
            },
            'classic': {
                'primary': '#1f2937',      # Gray
                'secondary': '#6b7280',    # Gray
                'accent': '#d97706',       # Amber
                'background': '#f9fafb',   # Light gray
                'surface': '#ffffff',      # White
                'text_primary': '#111827', # Dark gray
                'text_secondary': '#6b7280' # Gray
            },
            'corporate': {
                'primary': '#1e40af',      # Blue
                'secondary': '#374151',    # Gray
                'accent': '#059669',       # Green
                'background': '#f3f4f6',   # Light gray
                'surface': '#ffffff',      # White
                'text_primary': '#1f2937', # Dark gray
                'text_secondary': '#4b5563' # Gray
            }
        }
        
        return color_schemes.get(theme, color_schemes['modern'])
    
    def _get_typography_settings(self, style: str, theme: str) -> Dict[str, Any]:
        """Get typography settings for style and theme"""
        typography = {
            'professional': {
                'font_family': 'Segoe UI, Tahoma, Geneva, Verdana, sans-serif',
                'heading_size': '16px',
                'body_size': '14px',
                'small_size': '12px',
                'weight_normal': '400',
                'weight_bold': '600',
                'line_height': '1.5'
            },
            'minimal': {
                'font_family': 'Arial, Helvetica, sans-serif',
                'heading_size': '15px',
                'body_size': '13px',
                'small_size': '11px',
                'weight_normal': '400',
                'weight_bold': '500',
                'line_height': '1.4'
            },
            'dynamic': {
                'font_family': 'Inter, system-ui, sans-serif',
                'heading_size': '17px',
                'body_size': '15px',
                'small_size': '13px',
                'weight_normal': '400',
                'weight_bold': '700',
                'line_height': '1.6'
            }
        }
        
        return typography.get(style, typography['professional'])
    
    def _get_spacing_settings(self, style: str) -> Dict[str, str]:
        """Get spacing settings for style"""
        spacing = {
            'professional': {
                'small': '8px',
                'medium': '16px',
                'large': '24px',
                'xlarge': '32px'
            },
            'minimal': {
                'small': '4px',
                'medium': '8px',
                'large': '16px',
                'xlarge': '24px'
            },
            'dynamic': {
                'small': '12px',
                'medium': '20px',
                'large': '32px',
                'xlarge': '48px'
            }
        }
        
        return spacing.get(style, spacing['professional'])
    
    def _get_icon_settings(self, theme: str) -> Dict[str, Any]:
        """Get icon settings for theme"""
        return {
            'size': '32px' if theme == 'corporate' else '24px',
            'style': 'outline' if theme == 'minimal' else 'filled',
            'color_scheme': 'monochrome' if theme == 'classic' else 'colored'
        }
    
    def _get_layout_rules(self, style: str) -> Dict[str, Any]:
        """Get layout rules for style"""
        rules = {
            'professional': {
                'grid_columns': 4,
                'item_spacing': 16,
                'group_spacing': 32,
                'alignment': 'left',
                'sort_order': 'alphabetical'
            },
            'minimal': {
                'grid_columns': 3,
                'item_spacing': 8,
                'group_spacing': 16,
                'alignment': 'center',
                'sort_order': 'type'
            },
            'dynamic': {
                'grid_columns': 5,
                'item_spacing': 20,
                'group_spacing': 40,
                'alignment': 'justified',
                'sort_order': 'recent'
            }
        }
        
        return rules.get(style, rules['professional'])
    
    def _get_folder_organization_rules(self, style: str) -> Dict[str, Any]:
        """Get folder organization rules for style"""
        return {
            'create_category_folders': True,
            'use_color_coding': style in ['professional', 'dynamic'],
            'show_folder_previews': style == 'dynamic',
            'custom_icons': style in ['professional', 'corporate'],
            'sort_by_priority': style == 'professional'
        }
    
    def _get_desktop_settings(self, style: str, theme: str) -> Dict[str, Any]:
        """Get desktop organization settings"""
        return {
            'organize_icons': True,
            'create_shortcuts': True,
            'group_by_category': style == 'professional',
            'auto_arrange': style != 'minimal',
            'show_desktop_info': style == 'dynamic',
            'wallpaper_style': theme
        }
    
    def _create_folder_icons(self, layout_config: Dict[str, Any]) -> Dict[str, Any]:
        """Create folder icon assignments"""
        logger.info("Creating folder icon assignments")
        
        icon_mappings = {
            'Documents': '📄',
            'Images': '🖼️',
            'Videos': '🎬',
            'Audio': '🎵',
            'Archives': '📦',
            'Code': '💻',
            'Spreadsheets': '📊',
            'Presentations': '📋',
            'Applications': '⚙️',
            'System': '🔧',
            'Temporary': '🗑️',
            'Other': '📁'
        }
        
        style = layout_config['style']
        theme = layout_config['theme']
        
        if theme == 'corporate':
            # Use more professional icons for corporate theme
            icon_mappings.update({
                'Documents': '📋',
                'Images': '📸',
                'Videos': '📹',
                'Audio': '🔊',
                'Code': '⌨️'
            })
        
        return {
            'mappings': icon_mappings,
            'style': style,
            'theme': theme,
            'size': layout_config['icons']['size']
        }
    
    def _create_shortcuts(self, layout_config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create shortcut definitions"""
        logger.info("Creating shortcuts")
        
        shortcuts = [
            {
                'name': 'File Organization System',
                'target': 'main.py',
                'icon': '🗂️',
                'description': 'Launch File Organization System'
            },
            {
                'name': 'System Analysis',
                'target': 'main.py analyze',
                'icon': '🔍',
                'description': 'Analyze computer system'
            },
            {
                'name': 'Organize Files',
                'target': 'main.py organize',
                'icon': '📁',
                'description': 'Organize and categorize files'
            },
            {
                'name': 'Layout Manager',
                'target': 'main.py layout',
                'icon': '🎨',
                'description': 'Create professional layouts'
            },
            {
                'name': 'Cloud Integration',
                'target': 'main.py cloud',
                'icon': '☁️',
                'description': 'Sync with cloud storage'
            }
        ]
        
        return shortcuts
    
    def _create_thumbnails(self, layout_config: Dict[str, Any]) -> Dict[str, Any]:
        """Create thumbnail generation settings"""
        logger.info("Creating thumbnail settings")
        
        return {
            'enabled': True,
            'size': (128, 128),
            'quality': 85,
            'formats': ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
            'cache_location': '.thumbnails',
            'max_file_size': 50 * 1024 * 1024,  # 50MB
            'background_color': layout_config['colors']['background']
        }
    
    def _create_organization_structure(self, layout_config: Dict[str, Any]) -> Dict[str, Any]:
        """Create organization structure definition"""
        logger.info("Creating organization structure")
        
        structure = {
            'main_categories': [
                'Documents', 'Images', 'Videos', 'Audio',
                'Archives', 'Code', 'Spreadsheets', 'Presentations'
            ],
            'subcategories': {
                'Documents': ['PDFs', 'Word Documents', 'Text Files'],
                'Images': ['Photos', 'Screenshots', 'Graphics'],
                'Videos': ['Movies', 'Clips', 'Tutorials'],
                'Code': ['Python', 'JavaScript', 'Web', 'Data']
            },
            'special_folders': {
                'Recent': 'Files modified in last 30 days',
                'Large Files': 'Files larger than 100MB',
                'Duplicates': 'Potential duplicate files',
                'Archive': 'Old files for backup'
            },
            'layout_style': layout_config['style'],
            'sort_order': layout_config['layout_rules']['sort_order']
        }
        
        return structure
    
    def _create_desktop_arrangement(self, layout_config: Dict[str, Any]) -> Dict[str, Any]:
        """Create desktop arrangement plan"""
        logger.info("Creating desktop arrangement")
        
        arrangement = {
            'zones': {
                'top_left': 'Frequently used applications',
                'top_right': 'System utilities and tools',
                'bottom_left': 'File organization shortcuts',
                'bottom_right': 'Cloud and backup tools',
                'center': 'Current project files'
            },
            'grid_size': layout_config['layout_rules']['grid_columns'],
            'spacing': layout_config['spacing']['medium'],
            'auto_arrange': layout_config['desktop_settings']['auto_arrange'],
            'group_by_type': layout_config['desktop_settings']['group_by_category']
        }
        
        return arrangement
    
    def _create_style_definitions(self, layout_config: Dict[str, Any]) -> Dict[str, str]:
        """Create CSS-like style definitions for layout"""
        logger.info("Creating style definitions")
        
        colors = layout_config['colors']
        typography = layout_config['typography']
        spacing = layout_config['spacing']
        
        styles = {
            'folder_style': f"""
                background-color: {colors['surface']};
                border: 1px solid {colors['secondary']};
                border-radius: 8px;
                padding: {spacing['medium']};
                margin: {spacing['small']};
                font-family: {typography['font_family']};
                font-size: {typography['body_size']};
                color: {colors['text_primary']};
            """,
            'header_style': f"""
                font-family: {typography['font_family']};
                font-size: {typography['heading_size']};
                font-weight: {typography['weight_bold']};
                color: {colors['primary']};
                margin-bottom: {spacing['medium']};
            """,
            'icon_style': f"""
                width: {layout_config['icons']['size']};
                height: {layout_config['icons']['size']};
                margin-right: {spacing['small']};
            """
        }
        
        return styles
    
    def _apply_desktop_organization(self, desktop_arrangement: Dict[str, Any]) -> None:
        """Apply desktop organization settings"""
        logger.info("Applying desktop organization")
        
        try:
            # Create desktop organization plan file
            desktop_plan_path = Path("desktop_organization_plan.json")
            with open(desktop_plan_path, 'w', encoding='utf-8') as f:
                json.dump(desktop_arrangement, f, indent=2)
            
            logger.info(f"Desktop organization plan saved to: {desktop_plan_path}")
            
        except Exception as e:
            logger.warning(f"Could not apply desktop organization: {e}")
    
    def _apply_shortcuts(self, shortcuts: List[Dict[str, Any]]) -> None:
        """Apply shortcut creation"""
        logger.info("Applying shortcuts")
        
        try:
            # Create shortcuts directory
            shortcuts_dir = Path("shortcuts")
            shortcuts_dir.mkdir(exist_ok=True)
            
            for shortcut in shortcuts:
                shortcut_file = shortcuts_dir / f"{shortcut['name']}.json"
                with open(shortcut_file, 'w', encoding='utf-8') as f:
                    json.dump(shortcut, f, indent=2)
            
            logger.info(f"Created {len(shortcuts)} shortcuts in {shortcuts_dir}")
            
        except Exception as e:
            logger.warning(f"Could not create shortcuts: {e}")
    
    def _apply_thumbnails(self, thumbnail_settings: Dict[str, Any]) -> None:
        """Apply thumbnail generation settings"""
        logger.info("Applying thumbnail settings")
        
        try:
            # Create thumbnails directory
            thumbnails_dir = Path(thumbnail_settings['cache_location'])
            thumbnails_dir.mkdir(exist_ok=True)
            
            # Save thumbnail configuration
            config_file = thumbnails_dir / "config.json"
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(thumbnail_settings, f, indent=2)
            
            logger.info(f"Thumbnail settings configured in: {thumbnails_dir}")
            
        except Exception as e:
            logger.warning(f"Could not configure thumbnails: {e}")
    
    def _apply_folder_icons(self, folder_icons: Dict[str, Any]) -> None:
        """Apply folder icon assignments"""
        logger.info("Applying folder icons")
        
        try:
            # Create folder icons configuration
            icons_config_path = Path("folder_icons_config.json")
            with open(icons_config_path, 'w', encoding='utf-8') as f:
                json.dump(folder_icons, f, indent=2)
            
            logger.info(f"Folder icons configuration saved to: {icons_config_path}")
            
        except Exception as e:
            logger.warning(f"Could not apply folder icons: {e}")
    
    def _save_layout_configuration(self, layout_config: Dict[str, Any], 
                                  layout_elements: Dict[str, Any]) -> None:
        """Save complete layout configuration"""
        logger.info("Saving layout configuration")
        
        try:
            # Create layouts directory
            layouts_dir = Path("layouts")
            layouts_dir.mkdir(exist_ok=True)
            
            # Save complete layout
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            layout_file = layouts_dir / f"layout_{layout_config['style']}_{layout_config['theme']}_{timestamp}.json"
            
            complete_layout = {
                'config': layout_config,
                'elements': layout_elements,
                'applied_at': datetime.now().isoformat()
            }
            
            with open(layout_file, 'w', encoding='utf-8') as f:
                json.dump(complete_layout, f, indent=2, default=str)
            
            logger.info(f"Complete layout configuration saved to: {layout_file}")
            
        except Exception as e:
            logger.error(f"Failed to save layout configuration: {e}")
            raise
    
    def get_available_styles(self) -> List[str]:
        """Get list of available layout styles"""
        return ['professional', 'minimal', 'dynamic']
    
    def get_available_themes(self) -> List[str]:
        """Get list of available layout themes"""
        return ['modern', 'classic', 'corporate']
    
    def preview_layout(self, style: str = "professional", 
                      theme: str = "modern") -> Dict[str, Any]:
        """
        Generate layout preview without applying changes
        
        Args:
            style: Layout style
            theme: Layout theme
            
        Returns:
            Layout preview information
        """
        logger.info(f"Generating layout preview - Style: {style}, Theme: {theme}")
        
        config = self.generate_layout_config(style, theme)
        elements = self.create_layout_elements(config)
        
        preview = {
            'style': style,
            'theme': theme,
            'colors': config['colors'],
            'preview_elements': {
                'folder_count': len(elements['folder_icons']['mappings']),
                'shortcuts_count': len(elements['shortcuts']),
                'organization_categories': len(elements['organization_structure']['main_categories']),
                'desktop_zones': len(elements['desktop_arrangement']['zones'])
            },
            'features': {
                'thumbnails_enabled': elements['thumbnails']['enabled'],
                'auto_arrange': elements['desktop_arrangement']['auto_arrange'],
                'color_coding': config['folder_organization']['use_color_coding'],
                'custom_icons': config['folder_organization']['custom_icons']
            },
            'estimated_changes': {
                'folders_to_organize': len(elements['organization_structure']['main_categories']),
                'shortcuts_to_create': len(elements['shortcuts']),
                'icons_to_update': len(elements['folder_icons']['mappings'])
            }
        }
        
        return preview