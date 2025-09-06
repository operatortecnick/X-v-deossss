"""
System Analyzer - Comprehensive computer and file system analysis

This module provides comprehensive analysis of computer systems including:
- Hardware analysis (CPU, Memory, Storage, Network)
- Software analysis (OS, Installed programs, Running processes)
- File system analysis (Structure, Usage, Organization issues)
- Performance analysis (Disk usage, Memory usage, System health)
"""

import os
import platform
import psutil
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional
from ..utils.logger import get_logger

logger = get_logger(__name__)

class SystemAnalyzer:
    """Comprehensive system analysis functionality"""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the system analyzer with configuration"""
        self.config = config
        self.analysis_depth = config['system']['analysis_depth']
        logger.info(f"SystemAnalyzer initialized with depth: {self.analysis_depth}")
    
    def analyze_complete_system(self, target_path: str = ".", depth: str = None,
                              include_hardware: bool = True, include_software: bool = True,
                              include_files: bool = True, include_performance: bool = True) -> Dict[str, Any]:
        """
        Perform comprehensive system analysis
        
        Args:
            target_path: Path to analyze
            depth: Analysis depth override
            include_hardware: Include hardware analysis
            include_software: Include software analysis
            include_files: Include file system analysis
            include_performance: Include performance analysis
            
        Returns:
            Complete analysis results
        """
        if depth is None:
            depth = self.analysis_depth
        
        logger.info(f"Starting comprehensive system analysis - Target: {target_path}, Depth: {depth}")
        
        analysis_start = datetime.now()
        results = {
            'analysis_metadata': {
                'timestamp': analysis_start.isoformat(),
                'target_path': os.path.abspath(target_path),
                'depth': depth,
                'analyzer_version': '1.0.0'
            }
        }
        
        try:
            # Hardware Analysis
            if include_hardware:
                logger.info("Performing hardware analysis...")
                results['hardware'] = self._analyze_hardware(depth)
            
            # Software Analysis
            if include_software:
                logger.info("Performing software analysis...")
                results['software'] = self._analyze_software(depth)
            
            # File System Analysis
            if include_files:
                logger.info("Performing file system analysis...")
                results['file_system'] = self._analyze_file_system(target_path, depth)
            
            # Performance Analysis
            if include_performance:
                logger.info("Performing performance analysis...")
                results['performance'] = self._analyze_performance(depth)
            
            # Analysis Summary
            analysis_end = datetime.now()
            duration = (analysis_end - analysis_start).total_seconds()
            
            results['analysis_summary'] = {
                'start_time': analysis_start.isoformat(),
                'end_time': analysis_end.isoformat(),
                'duration_seconds': duration,
                'components_analyzed': [k for k in results.keys() if k != 'analysis_metadata'],
                'total_issues_found': self._count_issues(results),
                'recommendations_generated': self._count_recommendations(results)
            }
            
            logger.info(f"System analysis completed successfully in {duration:.2f}s")
            return results
            
        except Exception as e:
            logger.error(f"System analysis failed: {e}")
            raise
    
    def _analyze_hardware(self, depth: str) -> Dict[str, Any]:
        """Analyze hardware components"""
        hardware_data = {
            'cpu': self._get_cpu_info(depth),
            'memory': self._get_memory_info(depth),
            'storage': self._get_storage_info(depth),
            'network': self._get_network_info(depth) if depth in ['standard', 'comprehensive'] else {}
        }
        
        if depth == 'comprehensive':
            hardware_data['sensors'] = self._get_sensor_info()
            hardware_data['boot_time'] = datetime.fromtimestamp(psutil.boot_time()).isoformat()
        
        return hardware_data
    
    def _get_cpu_info(self, depth: str) -> Dict[str, Any]:
        """Get CPU information"""
        cpu_info = {
            'physical_cores': psutil.cpu_count(logical=False),
            'logical_cores': psutil.cpu_count(logical=True),
            'architecture': platform.architecture()[0],
            'processor': platform.processor()
        }
        
        if depth == 'comprehensive':
            try:
                cpu_info['frequency'] = dict(psutil.cpu_freq()._asdict()) if psutil.cpu_freq() else {}
                cpu_info['usage_per_core'] = psutil.cpu_percent(interval=1, percpu=True)
            except:
                pass
        
        return cpu_info
    
    def _get_memory_info(self, depth: str) -> Dict[str, Any]:
        """Get memory information"""
        virtual_mem = psutil.virtual_memory()
        memory_info = {
            'total_gb': round(virtual_mem.total / (1024**3), 2),
            'available_gb': round(virtual_mem.available / (1024**3), 2),
            'used_gb': round(virtual_mem.used / (1024**3), 2),
            'percentage_used': virtual_mem.percent
        }
        
        if depth in ['standard', 'comprehensive']:
            swap_mem = psutil.swap_memory()
            memory_info['swap'] = {
                'total_gb': round(swap_mem.total / (1024**3), 2),
                'used_gb': round(swap_mem.used / (1024**3), 2),
                'percentage_used': swap_mem.percent
            }
        
        return memory_info
    
    def _get_storage_info(self, depth: str) -> Dict[str, Any]:
        """Get storage information"""
        storage_info = {'drives': []}
        
        # Get all disk partitions
        partitions = psutil.disk_partitions()
        
        for partition in partitions:
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                drive_info = {
                    'device': partition.device,
                    'mountpoint': partition.mountpoint,
                    'file_system': partition.fstype,
                    'total_gb': round(usage.total / (1024**3), 2),
                    'used_gb': round(usage.used / (1024**3), 2),
                    'free_gb': round(usage.free / (1024**3), 2),
                    'percentage_used': round((usage.used / usage.total) * 100, 2)
                }
                storage_info['drives'].append(drive_info)
            except PermissionError:
                # Skip drives we can't access
                continue
        
        if depth == 'comprehensive':
            try:
                disk_io = psutil.disk_io_counters()
                if disk_io:
                    storage_info['io_stats'] = dict(disk_io._asdict())
            except:
                pass
        
        return storage_info
    
    def _get_network_info(self, depth: str) -> Dict[str, Any]:
        """Get network information"""
        network_info = {}
        
        try:
            # Network interfaces
            network_info['interfaces'] = {}
            for interface, addresses in psutil.net_if_addrs().items():
                network_info['interfaces'][interface] = [
                    {
                        'family': addr.family.name,
                        'address': addr.address,
                        'netmask': addr.netmask,
                        'broadcast': addr.broadcast
                    }
                    for addr in addresses
                ]
            
            if depth == 'comprehensive':
                # Network IO statistics
                net_io = psutil.net_io_counters()
                if net_io:
                    network_info['io_stats'] = dict(net_io._asdict())
        except:
            pass
        
        return network_info
    
    def _get_sensor_info(self) -> Dict[str, Any]:
        """Get sensor information (temperature, fans, etc.)"""
        sensor_info = {}
        
        try:
            # Temperature sensors
            if hasattr(psutil, 'sensors_temperatures'):
                temps = psutil.sensors_temperatures()
                if temps:
                    sensor_info['temperatures'] = {
                        name: [{'label': temp.label, 'current': temp.current, 'high': temp.high, 'critical': temp.critical}
                               for temp in temp_list]
                        for name, temp_list in temps.items()
                    }
            
            # Fan sensors
            if hasattr(psutil, 'sensors_fans'):
                fans = psutil.sensors_fans()
                if fans:
                    sensor_info['fans'] = {
                        name: [{'label': fan.label, 'current': fan.current}
                               for fan in fan_list]
                        for name, fan_list in fans.items()
                    }
        except:
            pass
        
        return sensor_info
    
    def _analyze_software(self, depth: str) -> Dict[str, Any]:
        """Analyze software and operating system"""
        software_data = {
            'operating_system': self._get_os_info(),
            'python_environment': self._get_python_info(),
        }
        
        if depth in ['standard', 'comprehensive']:
            software_data['processes'] = self._get_process_info(depth)
        
        if depth == 'comprehensive':
            software_data['services'] = self._get_services_info()
            software_data['environment_variables'] = dict(os.environ) if len(os.environ) < 100 else {'count': len(os.environ)}
        
        return software_data
    
    def _get_os_info(self) -> Dict[str, Any]:
        """Get operating system information"""
        return {
            'system': platform.system(),
            'release': platform.release(),
            'version': platform.version(),
            'machine': platform.machine(),
            'platform': platform.platform(),
            'node': platform.node()
        }
    
    def _get_python_info(self) -> Dict[str, Any]:
        """Get Python environment information"""
        return {
            'version': platform.python_version(),
            'implementation': platform.python_implementation(),
            'executable': os.sys.executable,
            'path': os.sys.path[:5]  # First 5 paths only
        }
    
    def _get_process_info(self, depth: str) -> Dict[str, Any]:
        """Get running process information"""
        processes = []
        
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    proc_info = proc.info
                    if depth == 'comprehensive' or proc_info['cpu_percent'] > 1.0 or proc_info['memory_percent'] > 1.0:
                        processes.append(proc_info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
        except:
            pass
        
        # Sort by CPU usage
        processes.sort(key=lambda x: x.get('cpu_percent', 0), reverse=True)
        
        return {
            'total_count': len(list(psutil.process_iter())),
            'top_processes': processes[:20]  # Top 20 processes
        }
    
    def _get_services_info(self) -> Dict[str, Any]:
        """Get system services information (Windows only)"""
        services_info = {'supported': False}
        
        if platform.system() == 'Windows':
            try:
                services_info = {
                    'supported': True,
                    'note': 'Service enumeration requires additional Windows-specific implementation'
                }
            except ImportError:
                services_info['note'] = 'Windows service utilities not available'
        else:
            services_info['note'] = 'Service enumeration not supported on this platform'
        
        return services_info
    
    def _analyze_file_system(self, target_path: str, depth: str) -> Dict[str, Any]:
        """Analyze file system structure and organization"""
        path_obj = Path(target_path)
        
        file_system_data = {
            'target_info': {
                'path': str(path_obj.absolute()),
                'exists': path_obj.exists(),
                'is_directory': path_obj.is_dir() if path_obj.exists() else False,
                'permissions': oct(path_obj.stat().st_mode)[-3:] if path_obj.exists() else None
            },
            'disk_usage': self._get_disk_usage(target_path),
            'directory_structure': self._analyze_directory_structure(target_path, depth)
        }
        
        if depth in ['standard', 'comprehensive']:
            file_system_data['file_analysis'] = self._analyze_files(target_path, depth)
            file_system_data['organization_issues'] = self._identify_organization_issues(target_path)
        
        if depth == 'comprehensive':
            file_system_data['duplicate_files'] = self._find_duplicate_files(target_path)
            file_system_data['large_files'] = self._find_large_files(target_path)
            file_system_data['file_age_analysis'] = self._analyze_file_ages(target_path)
        
        return file_system_data
    
    def _analyze_directory_structure(self, target_path: str, depth: str) -> Dict[str, Any]:
        """Analyze directory structure"""
        path_obj = Path(target_path)
        
        if not path_obj.exists() or not path_obj.is_dir():
            return {'error': 'Target path is not a valid directory'}
        
        structure = {
            'total_directories': 0,
            'total_files': 0,
            'max_depth': 0,
            'directory_tree': {}
        }
        
        try:
            max_depth = 3 if depth == 'basic' else 5 if depth == 'standard' else 10
            
            def scan_directory(dir_path: Path, current_depth: int = 0) -> Dict[str, Any]:
                if current_depth > max_depth:
                    return {'truncated': True}
                
                dir_info = {
                    'type': 'directory',
                    'size_bytes': 0,
                    'file_count': 0,
                    'subdirectory_count': 0,
                    'children': {}
                }
                
                try:
                    for item in dir_path.iterdir():
                        if item.is_file():
                            structure['total_files'] += 1
                            dir_info['file_count'] += 1
                            try:
                                file_size = item.stat().st_size
                                dir_info['size_bytes'] += file_size
                                dir_info['children'][item.name] = {
                                    'type': 'file',
                                    'size_bytes': file_size,
                                    'extension': item.suffix.lower()
                                }
                            except (OSError, PermissionError):
                                pass
                        elif item.is_dir():
                            structure['total_directories'] += 1
                            dir_info['subdirectory_count'] += 1
                            structure['max_depth'] = max(structure['max_depth'], current_depth + 1)
                            
                            if current_depth < max_depth:
                                subdir_info = scan_directory(item, current_depth + 1)
                                dir_info['children'][item.name] = subdir_info
                                dir_info['size_bytes'] += subdir_info.get('size_bytes', 0)
                except PermissionError:
                    dir_info['access_denied'] = True
                
                return dir_info
            
            structure['directory_tree'] = scan_directory(path_obj)
            
        except Exception as e:
            structure['error'] = str(e)
        
        return structure
    
    def _analyze_files(self, target_path: str, depth: str) -> Dict[str, Any]:
        """Analyze files in the target directory"""
        path_obj = Path(target_path)
        
        if not path_obj.exists():
            return {'error': 'Target path does not exist'}
        
        file_analysis = {
            'file_types': {},
            'size_distribution': {'small': 0, 'medium': 0, 'large': 0, 'huge': 0},
            'total_size_bytes': 0,
            'file_count': 0
        }
        
        try:
            # Size thresholds (in bytes)
            small_threshold = 1024 * 1024  # 1MB
            medium_threshold = 100 * 1024 * 1024  # 100MB
            large_threshold = 1024 * 1024 * 1024  # 1GB
            
            def analyze_file(file_path: Path):
                try:
                    file_stat = file_path.stat()
                    size = file_stat.st_size
                    extension = file_path.suffix.lower()
                    
                    file_analysis['total_size_bytes'] += size
                    file_analysis['file_count'] += 1
                    
                    # Track file types
                    if extension:
                        if extension not in file_analysis['file_types']:
                            file_analysis['file_types'][extension] = {'count': 0, 'total_size': 0}
                        file_analysis['file_types'][extension]['count'] += 1
                        file_analysis['file_types'][extension]['total_size'] += size
                    
                    # Size distribution
                    if size < small_threshold:
                        file_analysis['size_distribution']['small'] += 1
                    elif size < medium_threshold:
                        file_analysis['size_distribution']['medium'] += 1
                    elif size < large_threshold:
                        file_analysis['size_distribution']['large'] += 1
                    else:
                        file_analysis['size_distribution']['huge'] += 1
                        
                except (OSError, PermissionError):
                    pass
            
            # Scan files
            max_files = 1000 if depth == 'basic' else 5000 if depth == 'standard' else float('inf')
            files_scanned = 0
            
            for file_path in path_obj.rglob('*'):
                if file_path.is_file() and files_scanned < max_files:
                    analyze_file(file_path)
                    files_scanned += 1
            
            if files_scanned >= max_files:
                file_analysis['note'] = f'Analysis limited to {max_files} files'
                
        except Exception as e:
            file_analysis['error'] = str(e)
        
        return file_analysis
    
    def _identify_organization_issues(self, target_path: str) -> List[Dict[str, Any]]:
        """Identify file organization issues"""
        issues = []
        path_obj = Path(target_path)
        
        if not path_obj.exists() or not path_obj.is_dir():
            return issues
        
        try:
            # Issue 1: Too many files in root directory
            root_files = [f for f in path_obj.iterdir() if f.is_file()]
            if len(root_files) > 20:
                issues.append({
                    'type': 'too_many_root_files',
                    'severity': 'medium',
                    'description': f'{len(root_files)} files in root directory - consider organizing into folders',
                    'recommendation': 'Create subdirectories to categorize files'
                })
            
            # Issue 2: Mixed file types in same directory
            file_extensions = set()
            for file_path in path_obj.iterdir():
                if file_path.is_file():
                    file_extensions.add(file_path.suffix.lower())
            
            if len(file_extensions) > 10:
                issues.append({
                    'type': 'mixed_file_types',
                    'severity': 'low',
                    'description': f'{len(file_extensions)} different file types in same directory',
                    'recommendation': 'Separate files by type into different folders'
                })
            
            # Issue 3: Deep nested directories
            max_depth = 0
            for item in path_obj.rglob('*'):
                if item.is_dir():
                    depth = len(item.relative_to(path_obj).parts)
                    max_depth = max(max_depth, depth)
            
            if max_depth > 8:
                issues.append({
                    'type': 'deep_nesting',
                    'severity': 'medium',
                    'description': f'Directory structure is {max_depth} levels deep',
                    'recommendation': 'Consider flattening directory structure'
                })
                
        except Exception as e:
            issues.append({
                'type': 'analysis_error',
                'severity': 'high',
                'description': f'Error analyzing organization: {e}',
                'recommendation': 'Check file permissions and path accessibility'
            })
        
        return issues
    
    def _find_duplicate_files(self, target_path: str) -> Dict[str, Any]:
        """Find potential duplicate files (basic implementation)"""
        duplicates_info = {
            'by_size': {},
            'by_name': {},
            'total_potential_duplicates': 0
        }
        
        try:
            path_obj = Path(target_path)
            files_by_size = {}
            files_by_name = {}
            
            for file_path in path_obj.rglob('*'):
                if file_path.is_file():
                    try:
                        size = file_path.stat().st_size
                        name = file_path.name
                        
                        # Group by size
                        if size not in files_by_size:
                            files_by_size[size] = []
                        files_by_size[size].append(str(file_path))
                        
                        # Group by name
                        if name not in files_by_name:
                            files_by_name[name] = []
                        files_by_name[name].append(str(file_path))
                        
                    except (OSError, PermissionError):
                        pass
            
            # Find duplicates by size
            for size, paths in files_by_size.items():
                if len(paths) > 1:
                    duplicates_info['by_size'][f'{size}_bytes'] = paths[:10]  # Limit to 10 files
            
            # Find duplicates by name
            for name, paths in files_by_name.items():
                if len(paths) > 1:
                    duplicates_info['by_name'][name] = paths[:10]  # Limit to 10 files
            
            duplicates_info['total_potential_duplicates'] = (
                len(duplicates_info['by_size']) + len(duplicates_info['by_name'])
            )
            
        except Exception as e:
            duplicates_info['error'] = str(e)
        
        return duplicates_info
    
    def _find_large_files(self, target_path: str, min_size_mb: int = 100) -> List[Dict[str, Any]]:
        """Find large files"""
        large_files = []
        min_size_bytes = min_size_mb * 1024 * 1024
        
        try:
            path_obj = Path(target_path)
            
            for file_path in path_obj.rglob('*'):
                if file_path.is_file():
                    try:
                        size = file_path.stat().st_size
                        if size >= min_size_bytes:
                            large_files.append({
                                'path': str(file_path),
                                'size_bytes': size,
                                'size_mb': round(size / (1024**2), 2),
                                'extension': file_path.suffix.lower()
                            })
                    except (OSError, PermissionError):
                        pass
            
            # Sort by size descending
            large_files.sort(key=lambda x: x['size_bytes'], reverse=True)
            
        except Exception as e:
            large_files = [{'error': str(e)}]
        
        return large_files[:50]  # Return top 50 largest files
    
    def _analyze_file_ages(self, target_path: str) -> Dict[str, Any]:
        """Analyze file age distribution"""
        age_analysis = {
            'very_old': 0,    # > 2 years
            'old': 0,         # 6 months - 2 years
            'recent': 0,      # 1 month - 6 months
            'very_recent': 0, # < 1 month
            'oldest_file': None,
            'newest_file': None
        }
        
        try:
            path_obj = Path(target_path)
            now = datetime.now().timestamp()
            
            oldest_time = float('inf')
            newest_time = 0
            oldest_file = None
            newest_file = None
            
            # Time thresholds
            month = 30 * 24 * 3600
            six_months = 6 * month
            two_years = 2 * 365 * 24 * 3600
            
            for file_path in path_obj.rglob('*'):
                if file_path.is_file():
                    try:
                        mtime = file_path.stat().st_mtime
                        age = now - mtime
                        
                        # Track oldest and newest
                        if mtime < oldest_time:
                            oldest_time = mtime
                            oldest_file = str(file_path)
                        if mtime > newest_time:
                            newest_time = mtime
                            newest_file = str(file_path)
                        
                        # Categorize by age
                        if age > two_years:
                            age_analysis['very_old'] += 1
                        elif age > six_months:
                            age_analysis['old'] += 1
                        elif age > month:
                            age_analysis['recent'] += 1
                        else:
                            age_analysis['very_recent'] += 1
                            
                    except (OSError, PermissionError):
                        pass
            
            if oldest_file:
                age_analysis['oldest_file'] = {
                    'path': oldest_file,
                    'date': datetime.fromtimestamp(oldest_time).isoformat()
                }
            
            if newest_file:
                age_analysis['newest_file'] = {
                    'path': newest_file,
                    'date': datetime.fromtimestamp(newest_time).isoformat()
                }
                
        except Exception as e:
            age_analysis['error'] = str(e)
        
        return age_analysis
    
    def _analyze_performance(self, depth: str) -> Dict[str, Any]:
        """Analyze system performance metrics"""
        performance_data = {
            'cpu_usage': psutil.cpu_percent(interval=1),
            'memory_usage': dict(psutil.virtual_memory()._asdict()),
            'disk_io': dict(psutil.disk_io_counters()._asdict()) if psutil.disk_io_counters() else {},
        }
        
        if depth in ['standard', 'comprehensive']:
            performance_data['cpu_per_core'] = psutil.cpu_percent(interval=1, percpu=True)
            performance_data['memory_detailed'] = dict(psutil.virtual_memory()._asdict())
            performance_data['swap_usage'] = dict(psutil.swap_memory()._asdict())
        
        if depth == 'comprehensive':
            performance_data['network_io'] = dict(psutil.net_io_counters()._asdict())
            performance_data['load_average'] = os.getloadavg() if hasattr(os, 'getloadavg') else None
            performance_data['cpu_freq'] = dict(psutil.cpu_freq()._asdict()) if psutil.cpu_freq() else {}
        
        return performance_data
    
    def _get_disk_usage(self, target_path: str) -> Dict[str, Any]:
        """Get disk usage for target path"""
        try:
            usage = psutil.disk_usage(target_path)
            return {
                'total_gb': round(usage.total / (1024**3), 2),
                'used_gb': round(usage.used / (1024**3), 2),
                'free_gb': round(usage.free / (1024**3), 2),
                'percentage_used': round((usage.used / usage.total) * 100, 2)
            }
        except Exception as e:
            return {'error': str(e)}
    
    def _count_issues(self, results: Dict[str, Any]) -> int:
        """Count total issues found in analysis"""
        count = 0
        
        # Count file system organization issues
        if 'file_system' in results and 'organization_issues' in results['file_system']:
            count += len(results['file_system']['organization_issues'])
        
        # Count performance issues (simplified)
        if 'performance' in results:
            perf = results['performance']
            if 'cpu_usage' in perf and perf['cpu_usage'] > 80:
                count += 1
            if 'memory_usage' in perf and perf['memory_usage'].get('percent', 0) > 85:
                count += 1
        
        # Count storage issues
        if 'hardware' in results and 'storage' in results['hardware']:
            for drive in results['hardware']['storage'].get('drives', []):
                if drive.get('percentage_used', 0) > 90:
                    count += 1
        
        return count
    
    def _count_recommendations(self, results: Dict[str, Any]) -> int:
        """Count total recommendations generated"""
        count = 0
        
        # Count organization issue recommendations
        if 'file_system' in results and 'organization_issues' in results['file_system']:
            count += len(results['file_system']['organization_issues'])
        
        return count
    
    def generate_analysis_report(self, analysis_results: Dict[str, Any]) -> str:
        """
        Generate a comprehensive analysis report
        
        Args:
            analysis_results: Results from analyze_complete_system
            
        Returns:
            Path to generated report file
        """
        try:
            # Create reports directory
            reports_dir = Path("reports")
            reports_dir.mkdir(exist_ok=True)
            
            # Generate report filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_path = reports_dir / f"system_analysis_report_{timestamp}.json"
            
            # Add report metadata
            report_data = {
                'report_metadata': {
                    'generated_at': datetime.now().isoformat(),
                    'report_version': '1.0.0',
                    'generator': 'File Organization System - System Analyzer'
                },
                'analysis_results': analysis_results
            }
            
            # Write report
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=2, default=str)
            
            logger.info(f"Analysis report generated: {report_path}")
            return str(report_path)
            
        except Exception as e:
            logger.error(f"Failed to generate analysis report: {e}")
            raise