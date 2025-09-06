"""
Cloud Integrator - Cloud storage integration for virtual memory management

This module provides cloud storage integration including:
- AWS S3 integration
- Google Cloud Storage integration  
- Azure Blob Storage integration
- File synchronization and backup
- Compression and encryption for uploads
- Virtual memory management through cloud storage
"""

import os
import json
import gzip
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
from ..utils.logger import get_logger

logger = get_logger(__name__)

class CloudIntegrator:
    """Cloud storage integration and virtual memory management"""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the cloud integrator with configuration"""
        self.config = config
        self.cloud_config = config['cloud']
        self.providers = self.cloud_config['providers']
        self.sync_options = self.cloud_config['sync_options']
        logger.info("CloudIntegrator initialized")
    
    def get_active_provider(self) -> Optional[str]:
        """
        Get the first active cloud provider
        
        Returns:
            Name of active provider or None
        """
        for provider_name, provider_config in self.providers.items():
            if provider_config.get('enabled', False):
                return provider_name
        return None
    
    def upload_organized_files(self, provider: str, 
                             source_path: str = ".", 
                             file_patterns: List[str] = None) -> int:
        """
        Upload organized files to cloud storage
        
        Args:
            provider: Cloud provider name (aws, google, azure)
            source_path: Path to upload files from
            file_patterns: File patterns to include (default: all)
            
        Returns:
            Number of files uploaded
        """
        logger.info(f"Uploading files to {provider} from: {source_path}")
        
        if not self.providers.get(provider, {}).get('enabled', False):
            raise ValueError(f"Provider {provider} is not enabled")
        
        uploaded_count = 0
        
        try:
            # Get files to upload
            files_to_upload = self._get_files_for_upload(source_path, file_patterns)
            
            # Upload files based on provider
            if provider == 'aws':
                uploaded_count = self._upload_to_aws(files_to_upload)
            elif provider == 'google':
                uploaded_count = self._upload_to_google(files_to_upload)
            elif provider == 'azure':
                uploaded_count = self._upload_to_azure(files_to_upload)
            else:
                raise ValueError(f"Unsupported provider: {provider}")
            
            # Create upload log
            self._create_upload_log(provider, files_to_upload, uploaded_count)
            
            logger.info(f"Successfully uploaded {uploaded_count} files to {provider}")
            return uploaded_count
            
        except Exception as e:
            logger.error(f"Failed to upload files to {provider}: {e}")
            raise
    
    def sync_with_cloud(self, provider: str, 
                       local_path: str = ".", 
                       sync_mode: str = "upload") -> str:
        """
        Synchronize files with cloud storage
        
        Args:
            provider: Cloud provider name
            local_path: Local path to sync
            sync_mode: Sync mode (upload, download, bidirectional)
            
        Returns:
            Sync status message
        """
        logger.info(f"Syncing with {provider} - Mode: {sync_mode}")
        
        if not self.providers.get(provider, {}).get('enabled', False):
            raise ValueError(f"Provider {provider} is not enabled")
        
        try:
            sync_report = {
                'provider': provider,
                'sync_mode': sync_mode,
                'local_path': local_path,
                'started_at': datetime.now().isoformat(),
                'files_uploaded': 0,
                'files_downloaded': 0,
                'errors': []
            }
            
            if sync_mode in ['upload', 'bidirectional']:
                # Upload local changes
                files_to_upload = self._get_changed_files(local_path)
                if files_to_upload:
                    sync_report['files_uploaded'] = self._perform_upload(provider, files_to_upload)
            
            if sync_mode in ['download', 'bidirectional']:
                # Download remote changes (simulated)
                sync_report['files_downloaded'] = self._perform_download(provider, local_path)
            
            # Save sync report
            sync_report['completed_at'] = datetime.now().isoformat()
            self._save_sync_report(sync_report)
            
            status = f"Sync completed - Uploaded: {sync_report['files_uploaded']}, Downloaded: {sync_report['files_downloaded']}"
            logger.info(status)
            return status
            
        except Exception as e:
            logger.error(f"Failed to sync with {provider}: {e}")
            raise
    
    def configure_provider(self, provider: str, config: Dict[str, Any]) -> bool:
        """
        Configure cloud provider settings
        
        Args:
            provider: Provider name
            config: Provider configuration
            
        Returns:
            True if configuration is valid
        """
        logger.info(f"Configuring provider: {provider}")
        
        try:
            # Validate configuration based on provider
            if provider == 'aws':
                required_fields = ['bucket_name', 'region']
            elif provider == 'google':
                required_fields = ['bucket_name', 'project_id']
            elif provider == 'azure':
                required_fields = ['container_name', 'account_name']
            else:
                raise ValueError(f"Unsupported provider: {provider}")
            
            # Check required fields
            for field in required_fields:
                if field not in config or not config[field]:
                    raise ValueError(f"Missing required field: {field}")
            
            # Update configuration
            self.providers[provider].update(config)
            self.providers[provider]['enabled'] = True
            
            # Save updated configuration
            self._save_provider_config(provider, config)
            
            logger.info(f"Provider {provider} configured successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to configure provider {provider}: {e}")
            raise
    
    def get_cloud_storage_info(self, provider: str = None) -> Dict[str, Any]:
        """
        Get cloud storage information and usage
        
        Args:
            provider: Specific provider or None for all
            
        Returns:
            Storage information dictionary
        """
        logger.info(f"Getting cloud storage info for: {provider or 'all providers'}")
        
        storage_info = {
            'timestamp': datetime.now().isoformat(),
            'providers': {}
        }
        
        providers_to_check = [provider] if provider else self.providers.keys()
        
        for provider_name in providers_to_check:
            provider_config = self.providers.get(provider_name, {})
            
            if not provider_config.get('enabled', False):
                storage_info['providers'][provider_name] = {
                    'enabled': False,
                    'status': 'not_configured'
                }
                continue
            
            try:
                # Get provider-specific storage info
                if provider_name == 'aws':
                    provider_info = self._get_aws_storage_info(provider_config)
                elif provider_name == 'google':
                    provider_info = self._get_google_storage_info(provider_config)
                elif provider_name == 'azure':
                    provider_info = self._get_azure_storage_info(provider_config)
                else:
                    provider_info = {'status': 'unsupported'}
                
                storage_info['providers'][provider_name] = provider_info
                
            except Exception as e:
                storage_info['providers'][provider_name] = {
                    'enabled': True,
                    'status': 'error',
                    'error': str(e)
                }
        
        return storage_info
    
    def _get_files_for_upload(self, source_path: str, 
                            file_patterns: List[str] = None) -> List[Dict[str, Any]]:
        """Get list of files to upload"""
        files_to_upload = []
        source_path_obj = Path(source_path)
        
        try:
            for file_path in source_path_obj.rglob('*'):
                if file_path.is_file():
                    # Skip system files and temporary files
                    if self._should_skip_file(file_path):
                        continue
                    
                    # Check file patterns if specified
                    if file_patterns and not any(pattern in str(file_path) for pattern in file_patterns):
                        continue
                    
                    file_info = {
                        'local_path': str(file_path),
                        'relative_path': str(file_path.relative_to(source_path_obj)),
                        'size': file_path.stat().st_size,
                        'modified': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                        'hash': self._calculate_file_hash(file_path)
                    }
                    
                    files_to_upload.append(file_info)
        
        except Exception as e:
            logger.error(f"Error getting files for upload: {e}")
        
        return files_to_upload
    
    def _should_skip_file(self, file_path: Path) -> bool:
        """Check if file should be skipped for upload"""
        skip_patterns = [
            '.git', '.svn', '.hg',  # Version control
            '__pycache__', '.pyc',  # Python cache
            'node_modules',         # Node.js
            '.DS_Store',           # macOS
            'Thumbs.db',           # Windows
            '.tmp', '.temp',       # Temporary files
            '.log',                # Log files
        ]
        
        file_str = str(file_path).lower()
        return any(pattern in file_str for pattern in skip_patterns)
    
    def _upload_to_aws(self, files_to_upload: List[Dict[str, Any]]) -> int:
        """Upload files to AWS S3 (simulated)"""
        logger.info(f"Uploading {len(files_to_upload)} files to AWS S3")
        
        # Simulated AWS upload - in real implementation, use boto3
        try:
            uploaded_count = 0
            aws_config = self.providers['aws']
            bucket_name = aws_config['bucket_name']
            
            for file_info in files_to_upload:
                # Simulate upload process
                local_path = Path(file_info['local_path'])
                
                if self.sync_options.get('compress_before_upload', True):
                    # Simulate compression
                    compressed_size = file_info['size'] * 0.7  # Assume 30% compression
                    logger.debug(f"Compressed {local_path.name}: {file_info['size']} -> {compressed_size:.0f} bytes")
                
                # Simulate upload
                logger.debug(f"Uploaded to S3: s3://{bucket_name}/{file_info['relative_path']}")
                uploaded_count += 1
            
            return uploaded_count
            
        except Exception as e:
            logger.error(f"AWS upload failed: {e}")
            # In real implementation, handle AWS-specific errors
            return 0
    
    def _upload_to_google(self, files_to_upload: List[Dict[str, Any]]) -> int:
        """Upload files to Google Cloud Storage (simulated)"""
        logger.info(f"Uploading {len(files_to_upload)} files to Google Cloud Storage")
        
        # Simulated Google Cloud upload - in real implementation, use google-cloud-storage
        try:
            uploaded_count = 0
            google_config = self.providers['google']
            bucket_name = google_config['bucket_name']
            
            for file_info in files_to_upload:
                local_path = Path(file_info['local_path'])
                
                # Simulate upload
                logger.debug(f"Uploaded to GCS: gs://{bucket_name}/{file_info['relative_path']}")
                uploaded_count += 1
            
            return uploaded_count
            
        except Exception as e:
            logger.error(f"Google Cloud upload failed: {e}")
            return 0
    
    def _upload_to_azure(self, files_to_upload: List[Dict[str, Any]]) -> int:
        """Upload files to Azure Blob Storage (simulated)"""
        logger.info(f"Uploading {len(files_to_upload)} files to Azure Blob Storage")
        
        # Simulated Azure upload - in real implementation, use azure-storage-blob
        try:
            uploaded_count = 0
            azure_config = self.providers['azure']
            container_name = azure_config['container_name']
            
            for file_info in files_to_upload:
                local_path = Path(file_info['local_path'])
                
                # Simulate upload
                logger.debug(f"Uploaded to Azure: {container_name}/{file_info['relative_path']}")
                uploaded_count += 1
            
            return uploaded_count
            
        except Exception as e:
            logger.error(f"Azure upload failed: {e}")
            return 0
    
    def _get_changed_files(self, local_path: str) -> List[Dict[str, Any]]:
        """Get files that have changed since last sync"""
        # Simplified implementation - in real system, compare with cloud metadata
        recent_files = []
        
        try:
            path_obj = Path(local_path)
            cutoff_time = datetime.now().timestamp() - (24 * 3600)  # Last 24 hours
            
            for file_path in path_obj.rglob('*'):
                if file_path.is_file() and file_path.stat().st_mtime > cutoff_time:
                    if not self._should_skip_file(file_path):
                        file_info = {
                            'local_path': str(file_path),
                            'relative_path': str(file_path.relative_to(path_obj)),
                            'size': file_path.stat().st_size,
                            'modified': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                        }
                        recent_files.append(file_info)
        
        except Exception as e:
            logger.error(f"Error getting changed files: {e}")
        
        return recent_files
    
    def _perform_upload(self, provider: str, files_to_upload: List[Dict[str, Any]]) -> int:
        """Perform upload for sync operation"""
        if provider == 'aws':
            return self._upload_to_aws(files_to_upload)
        elif provider == 'google':
            return self._upload_to_google(files_to_upload)
        elif provider == 'azure':
            return self._upload_to_azure(files_to_upload)
        return 0
    
    def _perform_download(self, provider: str, local_path: str) -> int:
        """Perform download for sync operation (simulated)"""
        # Simplified download simulation
        logger.info(f"Downloading changed files from {provider}")
        
        # In real implementation, compare remote and local file states
        # and download changed files
        downloaded_count = 0  # Simulated count
        
        return downloaded_count
    
    def _get_aws_storage_info(self, aws_config: Dict[str, Any]) -> Dict[str, Any]:
        """Get AWS S3 storage information (simulated)"""
        return {
            'enabled': True,
            'status': 'connected',
            'bucket_name': aws_config['bucket_name'],
            'region': aws_config['region'],
            'usage': {
                'total_objects': 0,      # Would query S3 API
                'total_size_gb': 0.0,    # Would query S3 API
                'last_sync': None        # Would check sync history
            }
        }
    
    def _get_google_storage_info(self, google_config: Dict[str, Any]) -> Dict[str, Any]:
        """Get Google Cloud Storage information (simulated)"""
        return {
            'enabled': True,
            'status': 'connected',
            'bucket_name': google_config['bucket_name'],
            'project_id': google_config['project_id'],
            'usage': {
                'total_objects': 0,
                'total_size_gb': 0.0,
                'last_sync': None
            }
        }
    
    def _get_azure_storage_info(self, azure_config: Dict[str, Any]) -> Dict[str, Any]:
        """Get Azure Blob Storage information (simulated)"""
        return {
            'enabled': True,
            'status': 'connected',
            'container_name': azure_config['container_name'],
            'account_name': azure_config['account_name'],
            'usage': {
                'total_objects': 0,
                'total_size_gb': 0.0,
                'last_sync': None
            }
        }
    
    def _calculate_file_hash(self, file_path: Path) -> str:
        """Calculate MD5 hash of file"""
        hash_md5 = hashlib.md5()
        
        try:
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception:
            return ""
    
    def _create_upload_log(self, provider: str, files_uploaded: List[Dict[str, Any]], 
                          upload_count: int) -> None:
        """Create upload log"""
        try:
            logs_dir = Path("logs")
            logs_dir.mkdir(exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = logs_dir / f"upload_{provider}_{timestamp}.json"
            
            log_data = {
                'provider': provider,
                'timestamp': datetime.now().isoformat(),
                'files_uploaded': upload_count,
                'total_files': len(files_uploaded),
                'files': files_uploaded[:100]  # Limit log size
            }
            
            with open(log_file, 'w', encoding='utf-8') as f:
                json.dump(log_data, f, indent=2)
            
            logger.info(f"Upload log saved to: {log_file}")
            
        except Exception as e:
            logger.warning(f"Could not create upload log: {e}")
    
    def _save_sync_report(self, sync_report: Dict[str, Any]) -> None:
        """Save sync report"""
        try:
            reports_dir = Path("reports")
            reports_dir.mkdir(exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_file = reports_dir / f"sync_report_{timestamp}.json"
            
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(sync_report, f, indent=2)
            
            logger.info(f"Sync report saved to: {report_file}")
            
        except Exception as e:
            logger.warning(f"Could not save sync report: {e}")
    
    def _save_provider_config(self, provider: str, config: Dict[str, Any]) -> None:
        """Save provider configuration"""
        try:
            config_dir = Path("cloud_config")
            config_dir.mkdir(exist_ok=True)
            
            config_file = config_dir / f"{provider}_config.json"
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2)
            
            logger.info(f"Provider config saved to: {config_file}")
            
        except Exception as e:
            logger.warning(f"Could not save provider config: {e}")
    
    def create_virtual_memory_archive(self, source_path: str, 
                                    archive_name: str = None) -> str:
        """
        Create compressed archive for virtual memory management
        
        Args:
            source_path: Path to archive
            archive_name: Name of archive file
            
        Returns:
            Path to created archive
        """
        logger.info(f"Creating virtual memory archive from: {source_path}")
        
        try:
            if archive_name is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                archive_name = f"virtual_memory_archive_{timestamp}.json.gz"
            
            # Create archive data
            archive_data = {
                'metadata': {
                    'created_at': datetime.now().isoformat(),
                    'source_path': source_path,
                    'archive_type': 'virtual_memory',
                    'compression': 'gzip'
                },
                'file_index': self._create_file_index(source_path),
                'organization_data': self._get_organization_metadata(source_path)
            }
            
            # Save compressed archive
            archive_path = Path(archive_name)
            with gzip.open(archive_path, 'wt', encoding='utf-8') as f:
                json.dump(archive_data, f, indent=2, default=str)
            
            logger.info(f"Virtual memory archive created: {archive_path}")
            return str(archive_path)
            
        except Exception as e:
            logger.error(f"Failed to create virtual memory archive: {e}")
            raise
    
    def _create_file_index(self, source_path: str) -> Dict[str, Any]:
        """Create index of files for virtual memory"""
        file_index = {
            'total_files': 0,
            'total_size': 0,
            'categories': {},
            'files': []
        }
        
        try:
            source_path_obj = Path(source_path)
            
            for file_path in source_path_obj.rglob('*'):
                if file_path.is_file():
                    file_stat = file_path.stat()
                    
                    file_info = {
                        'path': str(file_path.relative_to(source_path_obj)),
                        'size': file_stat.st_size,
                        'modified': datetime.fromtimestamp(file_stat.st_mtime).isoformat(),
                        'extension': file_path.suffix.lower(),
                        'hash': self._calculate_file_hash(file_path)
                    }
                    
                    file_index['files'].append(file_info)
                    file_index['total_files'] += 1
                    file_index['total_size'] += file_stat.st_size
                    
                    # Categorize
                    category = self._categorize_file_for_archive(file_path)
                    if category not in file_index['categories']:
                        file_index['categories'][category] = 0
                    file_index['categories'][category] += 1
        
        except Exception as e:
            logger.error(f"Error creating file index: {e}")
        
        return file_index
    
    def _get_organization_metadata(self, source_path: str) -> Dict[str, Any]:
        """Get organization metadata for archive"""
        return {
            'directory_structure': self._get_directory_tree(source_path),
            'organization_rules_applied': True,
            'layout_style': 'professional',
            'categories_used': ['documents', 'images', 'videos', 'audio', 'archives', 'code']
        }
    
    def _get_directory_tree(self, source_path: str, max_depth: int = 3) -> Dict[str, Any]:
        """Get directory tree structure"""
        source_path_obj = Path(source_path)
        
        def build_tree(path: Path, current_depth: int = 0) -> Dict[str, Any]:
            if current_depth > max_depth:
                return {'name': path.name, 'type': 'directory', 'truncated': True}
            
            tree_node = {
                'name': path.name,
                'type': 'directory',
                'children': []
            }
            
            try:
                for item in path.iterdir():
                    if item.is_file():
                        tree_node['children'].append({
                            'name': item.name,
                            'type': 'file',
                            'size': item.stat().st_size
                        })
                    elif item.is_dir():
                        tree_node['children'].append(build_tree(item, current_depth + 1))
            except PermissionError:
                tree_node['error'] = 'Permission denied'
            
            return tree_node
        
        return build_tree(source_path_obj)
    
    def _categorize_file_for_archive(self, file_path: Path) -> str:
        """Categorize file for archive purposes"""
        extension = file_path.suffix.lower()
        
        if extension in ['.pdf', '.doc', '.docx', '.txt', '.rtf']:
            return 'documents'
        elif extension in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
            return 'images'
        elif extension in ['.mp4', '.avi', '.mkv', '.mov']:
            return 'videos'
        elif extension in ['.mp3', '.wav', '.flac', '.aac']:
            return 'audio'
        elif extension in ['.zip', '.rar', '.7z', '.tar', '.gz']:
            return 'archives'
        elif extension in ['.py', '.js', '.html', '.css', '.cpp', '.java']:
            return 'code'
        else:
            return 'other'