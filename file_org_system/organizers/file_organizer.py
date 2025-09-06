"""
File Organizer - Professional file categorization and organization

This module provides intelligent file organization capabilities including:
- Automatic file categorization by type, date, and content
- Professional organization strategies
- Duplicate file detection and management
- Backup creation before changes
- Smart folder structure generation
"""

import os
import shutil
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
from ..utils.logger import get_logger

logger = get_logger(__name__)

class FileOrganizer:
    """Professional file organization and categorization"""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the file organizer with configuration"""
        self.config = config
        self.categories = config['file_organization']['categories']
        self.rules = config['file_organization']['organization_rules']
        logger.info("FileOrganizer initialized with categorization rules")
    
    def analyze_and_plan_organization(self, target_path: str) -> Dict[str, Any]:
        """
        Analyze directory and create organization plan
        
        Args:
            target_path: Path to analyze and organize
            
        Returns:
            Organization plan with suggested operations
        """
        logger.info(f"Analyzing and planning organization for: {target_path}")
        
        path_obj = Path(target_path)
        if not path_obj.exists():
            raise ValueError(f"Target path does not exist: {target_path}")
        
        plan = {
            'target_path': str(path_obj.absolute()),
            'analysis_timestamp': datetime.now().isoformat(),
            'operations': [],
            'statistics': {
                'total_files': 0,
                'files_to_move': 0,
                'duplicates_found': 0,
                'folders_to_create': 0
            },
            'categories_used': set(),
            'folder_structure': {}
        }
        
        try:
            # Analyze existing files
            file_analysis = self._analyze_files_for_organization(path_obj)
            plan['file_analysis'] = file_analysis
            
            # Generate organization operations
            operations = self._generate_organization_operations(path_obj, file_analysis)
            plan['operations'] = operations
            
            # Update statistics
            plan['statistics']['total_files'] = file_analysis['total_files']
            plan['statistics']['files_to_move'] = len([op for op in operations if op['type'] == 'move'])
            plan['statistics']['duplicates_found'] = file_analysis['duplicates_count']
            plan['statistics']['folders_to_create'] = len([op for op in operations if op['type'] == 'create_folder'])
            
            # Track categories and folder structure
            for operation in operations:
                if operation['type'] == 'move':
                    category = operation.get('category')
                    if category:
                        plan['categories_used'].add(category)
                elif operation['type'] == 'create_folder':
                    folder_path = operation['target_path']
                    plan['folder_structure'][folder_path] = operation.get('purpose', 'organization')
            
            # Convert set to list for JSON serialization
            plan['categories_used'] = list(plan['categories_used'])
            
            logger.info(f"Organization plan created with {len(operations)} operations")
            return plan
            
        except Exception as e:
            logger.error(f"Failed to create organization plan: {e}")
            raise
    
    def apply_organization_plan(self, organization_plan: Dict[str, Any], 
                              target_path: str) -> int:
        """
        Apply the organization plan to reorganize files
        
        Args:
            organization_plan: Plan created by analyze_and_plan_organization
            target_path: Base path for organization
            
        Returns:
            Number of files processed
        """
        logger.info(f"Applying organization plan to: {target_path}")
        
        files_processed = 0
        
        try:
            operations = organization_plan.get('operations', [])
            
            # Sort operations: create folders first, then moves
            sorted_operations = sorted(operations, 
                                     key=lambda x: (0 if x['type'] == 'create_folder' else 1))
            
            for operation in sorted_operations:
                try:
                    if operation['type'] == 'create_folder':
                        self._execute_create_folder(operation)
                    elif operation['type'] == 'move':
                        self._execute_move_file(operation)
                        files_processed += 1
                    elif operation['type'] == 'rename':
                        self._execute_rename_file(operation)
                        files_processed += 1
                    elif operation['type'] == 'delete_duplicate':
                        self._execute_delete_duplicate(operation)
                        files_processed += 1
                    
                    logger.debug(f"Executed operation: {operation['type']} - {operation.get('source_path', 'N/A')}")
                    
                except Exception as e:
                    logger.warning(f"Failed to execute operation {operation['type']}: {e}")
                    continue
            
            logger.info(f"Organization completed - {files_processed} files processed")
            return files_processed
            
        except Exception as e:
            logger.error(f"Failed to apply organization plan: {e}")
            raise
    
    def create_backup(self, target_path: str) -> str:
        """
        Create backup of target directory before organization
        
        Args:
            target_path: Path to backup
            
        Returns:
            Path to backup directory
        """
        logger.info(f"Creating backup of: {target_path}")
        
        try:
            path_obj = Path(target_path)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"backup_{path_obj.name}_{timestamp}"
            backup_path = path_obj.parent / backup_name
            
            # Create backup
            shutil.copytree(path_obj, backup_path, dirs_exist_ok=True)
            
            logger.info(f"Backup created successfully: {backup_path}")
            return str(backup_path)
            
        except Exception as e:
            logger.error(f"Failed to create backup: {e}")
            raise
    
    def _analyze_files_for_organization(self, target_path: Path) -> Dict[str, Any]:
        """Analyze files to determine organization needs"""
        analysis = {
            'total_files': 0,
            'file_categories': {},
            'date_distribution': {},
            'size_distribution': {'small': 0, 'medium': 0, 'large': 0},
            'duplicates': [],
            'duplicates_count': 0,
            'organization_opportunities': []
        }
        
        try:
            file_hashes = {}  # For duplicate detection
            
            for file_path in target_path.rglob('*'):
                if file_path.is_file():
                    analysis['total_files'] += 1
                    
                    # Categorize file
                    category = self._categorize_file(file_path)
                    if category not in analysis['file_categories']:
                        analysis['file_categories'][category] = []
                    analysis['file_categories'][category].append(str(file_path))
                    
                    # Analyze file date
                    try:
                        mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                        year = mtime.year
                        if year not in analysis['date_distribution']:
                            analysis['date_distribution'][year] = 0
                        analysis['date_distribution'][year] += 1
                    except:
                        pass
                    
                    # Analyze file size
                    try:
                        size = file_path.stat().st_size
                        if size < 1024 * 1024:  # < 1MB
                            analysis['size_distribution']['small'] += 1
                        elif size < 100 * 1024 * 1024:  # < 100MB
                            analysis['size_distribution']['medium'] += 1
                        else:
                            analysis['size_distribution']['large'] += 1
                    except:
                        pass
                    
                    # Check for duplicates (basic hash comparison)
                    if self.rules.get('remove_duplicates', False):
                        try:
                            file_hash = self._calculate_file_hash(file_path)
                            if file_hash in file_hashes:
                                analysis['duplicates'].append({
                                    'original': file_hashes[file_hash],
                                    'duplicate': str(file_path),
                                    'hash': file_hash
                                })
                                analysis['duplicates_count'] += 1
                            else:
                                file_hashes[file_hash] = str(file_path)
                        except:
                            pass
            
            # Identify organization opportunities
            analysis['organization_opportunities'] = self._identify_organization_opportunities(analysis)
            
        except Exception as e:
            analysis['error'] = str(e)
        
        return analysis
    
    def _categorize_file(self, file_path: Path) -> str:
        """Categorize file based on extension and content"""
        extension = file_path.suffix.lower()
        
        # Check each category
        for category, extensions in self.categories.items():
            if extension in extensions:
                return category
        
        # Special cases
        if file_path.name.startswith('.'):
            return 'system'
        
        if extension in ['.exe', '.msi', '.deb', '.rpm', '.dmg']:
            return 'applications'
        
        if extension in ['.log', '.tmp', '.temp', '.cache']:
            return 'temporary'
        
        return 'other'
    
    def _generate_organization_operations(self, target_path: Path, 
                                        file_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate list of operations to organize files"""
        operations = []
        
        try:
            # Create category folders if needed
            if self.rules.get('create_type_folders', True):
                for category in file_analysis['file_categories']:
                    if category != 'other' and file_analysis['file_categories'][category]:
                        folder_path = target_path / f"{category.title()}"
                        if not folder_path.exists():
                            operations.append({
                                'type': 'create_folder',
                                'target_path': str(folder_path),
                                'purpose': f'{category} files',
                                'category': category
                            })
            
            # Create year folders if needed
            if self.rules.get('create_year_folders', True):
                for year in file_analysis['date_distribution']:
                    year_folder = target_path / str(year)
                    if not year_folder.exists():
                        operations.append({
                            'type': 'create_folder',
                            'target_path': str(year_folder),
                            'purpose': f'files from {year}',
                            'year': year
                        })
            
            # Generate move operations for files
            for category, file_paths in file_analysis['file_categories'].items():
                for file_path_str in file_paths:
                    file_path = Path(file_path_str)
                    
                    if not file_path.exists():
                        continue
                    
                    # Determine target location
                    target_location = self._determine_target_location(
                        file_path, category, target_path, file_analysis
                    )
                    
                    # Only move if target is different from current location
                    if target_location != file_path.parent:
                        operations.append({
                            'type': 'move',
                            'source_path': str(file_path),
                            'target_path': str(target_location / file_path.name),
                            'category': category,
                            'reason': f'organize {category} files'
                        })
            
            # Generate rename operations for optimized names
            if self.rules.get('optimize_names', True):
                for category, file_paths in file_analysis['file_categories'].items():
                    for file_path_str in file_paths[:10]:  # Limit to avoid too many operations
                        file_path = Path(file_path_str)
                        optimized_name = self._optimize_filename(file_path)
                        
                        if optimized_name != file_path.name:
                            operations.append({
                                'type': 'rename',
                                'source_path': str(file_path),
                                'new_name': optimized_name,
                                'reason': 'optimize filename'
                            })
            
            # Generate duplicate removal operations
            if self.rules.get('remove_duplicates', True):
                for duplicate_info in file_analysis['duplicates'][:5]:  # Limit duplicate operations
                    operations.append({
                        'type': 'delete_duplicate',
                        'duplicate_path': duplicate_info['duplicate'],
                        'original_path': duplicate_info['original'],
                        'reason': 'remove duplicate file'
                    })
            
        except Exception as e:
            logger.error(f"Failed to generate organization operations: {e}")
        
        return operations
    
    def _determine_target_location(self, file_path: Path, category: str, 
                                 base_path: Path, file_analysis: Dict[str, Any]) -> Path:
        """Determine where file should be moved"""
        target_location = base_path
        
        # Add category folder if enabled
        if self.rules.get('create_type_folders', True) and category != 'other':
            target_location = target_location / category.title()
        
        # Add year folder if enabled
        if self.rules.get('create_year_folders', True):
            try:
                mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                year = mtime.year
                
                # Only create year subfolders for certain categories or if many files
                if category in ['documents', 'images', 'videos'] or file_analysis['total_files'] > 100:
                    target_location = target_location / str(year)
            except:
                pass
        
        return target_location
    
    def _optimize_filename(self, file_path: Path) -> str:
        """Optimize filename for better organization"""
        name = file_path.stem
        extension = file_path.suffix
        
        # Remove common problematic characters
        optimized_name = name.replace(' ', '_')
        optimized_name = optimized_name.replace('(', '')
        optimized_name = optimized_name.replace(')', '')
        optimized_name = optimized_name.replace('[', '')
        optimized_name = optimized_name.replace(']', '')
        
        # Remove multiple underscores
        while '__' in optimized_name:
            optimized_name = optimized_name.replace('__', '_')
        
        # Remove leading/trailing underscores
        optimized_name = optimized_name.strip('_')
        
        # Ensure it's not empty
        if not optimized_name:
            optimized_name = 'file'
        
        return optimized_name + extension
    
    def _identify_organization_opportunities(self, analysis: Dict[str, Any]) -> List[str]:
        """Identify specific organization improvement opportunities"""
        opportunities = []
        
        # Too many files in root
        total_files = analysis['total_files']
        if total_files > 50:
            opportunities.append(f"Large number of files ({total_files}) - would benefit from categorization")
        
        # Mixed file types
        categories_count = len([cat for cat in analysis['file_categories'] if analysis['file_categories'][cat]])
        if categories_count > 5:
            opportunities.append(f"Multiple file types ({categories_count}) present - folder organization recommended")
        
        # Old files
        date_dist = analysis['date_distribution']
        if len(date_dist) > 3:
            years = sorted(date_dist.keys())
            opportunities.append(f"Files span multiple years ({years[0]}-{years[-1]}) - date-based organization recommended")
        
        # Duplicates
        if analysis['duplicates_count'] > 0:
            opportunities.append(f"Found {analysis['duplicates_count']} potential duplicate files")
        
        return opportunities
    
    def _calculate_file_hash(self, file_path: Path, chunk_size: int = 8192) -> str:
        """Calculate MD5 hash of file for duplicate detection"""
        hash_md5 = hashlib.md5()
        
        try:
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(chunk_size), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception:
            return None
    
    def _execute_create_folder(self, operation: Dict[str, Any]) -> None:
        """Execute folder creation operation"""
        folder_path = Path(operation['target_path'])
        folder_path.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Created folder: {folder_path}")
    
    def _execute_move_file(self, operation: Dict[str, Any]) -> None:
        """Execute file move operation"""
        source_path = Path(operation['source_path'])
        target_path = Path(operation['target_path'])
        
        if not source_path.exists():
            logger.warning(f"Source file not found: {source_path}")
            return
        
        # Ensure target directory exists
        target_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Handle name conflicts
        if target_path.exists():
            base_name = target_path.stem
            extension = target_path.suffix
            counter = 1
            
            while target_path.exists():
                new_name = f"{base_name}_{counter}{extension}"
                target_path = target_path.parent / new_name
                counter += 1
        
        shutil.move(str(source_path), str(target_path))
        logger.debug(f"Moved file: {source_path} -> {target_path}")
    
    def _execute_rename_file(self, operation: Dict[str, Any]) -> None:
        """Execute file rename operation"""
        source_path = Path(operation['source_path'])
        new_name = operation['new_name']
        target_path = source_path.parent / new_name
        
        if not source_path.exists():
            logger.warning(f"Source file not found: {source_path}")
            return
        
        if target_path.exists():
            logger.warning(f"Target filename already exists: {target_path}")
            return
        
        source_path.rename(target_path)
        logger.debug(f"Renamed file: {source_path.name} -> {new_name}")
    
    def _execute_delete_duplicate(self, operation: Dict[str, Any]) -> None:
        """Execute duplicate file deletion operation"""
        duplicate_path = Path(operation['duplicate_path'])
        
        if not duplicate_path.exists():
            logger.warning(f"Duplicate file not found: {duplicate_path}")
            return
        
        # Additional safety check - verify it's actually a duplicate
        original_path = Path(operation['original_path'])
        if original_path.exists():
            try:
                duplicate_hash = self._calculate_file_hash(duplicate_path)
                original_hash = self._calculate_file_hash(original_path)
                
                if duplicate_hash == original_hash:
                    duplicate_path.unlink()
                    logger.debug(f"Deleted duplicate file: {duplicate_path}")
                else:
                    logger.warning(f"Files are not identical, skipping deletion: {duplicate_path}")
            except Exception as e:
                logger.warning(f"Could not verify duplicate, skipping deletion: {e}")
        else:
            logger.warning(f"Original file not found, skipping duplicate deletion: {original_path}")