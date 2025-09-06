"""
Main Controller - Orchestrates all File Organization System components

This is the central controller that coordinates between system analysis,
file organization, layout management, and cloud integration.
"""

import os
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

from ..analyzers.system_analyzer import SystemAnalyzer
from ..organizers.file_organizer import FileOrganizer
from ..layouts.layout_manager import LayoutManager
from ..cloud.cloud_integrator import CloudIntegrator
from ..utils.config_loader import ConfigLoader
from ..utils.logger import get_logger

logger = get_logger(__name__)

class FileOrgController:
    """Main controller for the File Organization System"""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize the controller with configuration"""
        self.config = ConfigLoader.load_config(config_path)
        self.system_analyzer = SystemAnalyzer(self.config)
        self.file_organizer = FileOrganizer(self.config)
        self.layout_manager = LayoutManager(self.config)
        self.cloud_integrator = CloudIntegrator(self.config)
        
        logger.info("File Organization System Controller initialized")
    
    def analyze_system(self, path: str = ".", depth: str = "comprehensive", 
                      generate_report: bool = True) -> Dict[str, Any]:
        """
        Analyze computer system comprehensively
        
        Args:
            path: Path to analyze
            depth: Analysis depth (basic, standard, comprehensive)
            generate_report: Whether to generate a detailed report
            
        Returns:
            Dictionary with analysis results
        """
        logger.info(f"Starting system analysis - Path: {path}, Depth: {depth}")
        
        start_time = time.time()
        
        try:
            # Perform comprehensive system analysis
            analysis_results = self.system_analyzer.analyze_complete_system(
                target_path=path,
                depth=depth,
                include_hardware=True,
                include_software=True,
                include_files=True,
                include_performance=True
            )
            
            # Generate report if requested
            report_path = None
            if generate_report:
                report_path = self.system_analyzer.generate_analysis_report(analysis_results)
                logger.info(f"Analysis report generated: {report_path}")
            
            duration = time.time() - start_time
            
            results = {
                'success': True,
                'analysis_data': analysis_results,
                'report_path': report_path,
                'duration': f"{duration:.2f} seconds",
                'analyzed_path': path,
                'depth': depth
            }
            
            logger.info(f"System analysis completed successfully in {duration:.2f}s")
            return results
            
        except Exception as e:
            logger.error(f"System analysis failed: {e}")
            raise
    
    def organize_files(self, path: str = ".", apply_changes: bool = False,
                      create_backup: bool = None) -> Dict[str, Any]:
        """
        Organize and categorize files professionally
        
        Args:
            path: Path to organize
            apply_changes: Whether to apply changes or just preview
            create_backup: Whether to create backup (uses config default if None)
            
        Returns:
            Dictionary with organization results
        """
        logger.info(f"Starting file organization - Path: {path}, Apply: {apply_changes}")
        
        if create_backup is None:
            create_backup = self.config['system']['backup_before_changes']
        
        start_time = time.time()
        
        try:
            # Create backup if requested and applying changes
            backup_path = None
            if create_backup and apply_changes:
                backup_path = self.file_organizer.create_backup(path)
                logger.info(f"Backup created: {backup_path}")
            
            # Analyze files and generate organization suggestions
            organization_plan = self.file_organizer.analyze_and_plan_organization(path)
            
            files_processed = 0
            suggestions_count = len(organization_plan.get('operations', []))
            
            # Apply changes if requested
            if apply_changes:
                files_processed = self.file_organizer.apply_organization_plan(
                    organization_plan, path
                )
                logger.info(f"Organization applied - {files_processed} files processed")
            else:
                logger.info(f"Preview mode - {suggestions_count} suggestions generated")
            
            duration = time.time() - start_time
            
            results = {
                'success': True,
                'organization_plan': organization_plan,
                'files_processed': files_processed,
                'suggestions_count': suggestions_count,
                'backup_path': backup_path,
                'applied': apply_changes,
                'duration': f"{duration:.2f} seconds"
            }
            
            logger.info(f"File organization completed in {duration:.2f}s")
            return results
            
        except Exception as e:
            logger.error(f"File organization failed: {e}")
            raise
    
    def create_layout(self, style: str = "professional", theme: str = "modern",
                     apply_changes: bool = False) -> Dict[str, Any]:
        """
        Create professional, clean and dynamic layouts
        
        Args:
            style: Layout style (professional, minimal, dynamic)
            theme: Layout theme (modern, classic, corporate)
            apply_changes: Whether to apply layout changes
            
        Returns:
            Dictionary with layout results
        """
        logger.info(f"Creating layout - Style: {style}, Theme: {theme}, Apply: {apply_changes}")
        
        start_time = time.time()
        
        try:
            # Generate layout configuration
            layout_config = self.layout_manager.generate_layout_config(style, theme)
            
            # Create layout elements
            layout_elements = self.layout_manager.create_layout_elements(layout_config)
            
            # Apply layout if requested
            if apply_changes:
                self.layout_manager.apply_layout(layout_config, layout_elements)
                logger.info("Layout applied successfully")
            else:
                logger.info("Layout prepared in preview mode")
            
            duration = time.time() - start_time
            
            results = {
                'success': True,
                'layout_config': layout_config,
                'layout_elements': layout_elements,
                'style': style,
                'theme': theme,
                'applied': apply_changes,
                'duration': f"{duration:.2f} seconds"
            }
            
            logger.info(f"Layout creation completed in {duration:.2f}s")
            return results
            
        except Exception as e:
            logger.error(f"Layout creation failed: {e}")
            raise
    
    def cloud_integration(self, provider: Optional[str] = None, upload: bool = False,
                         sync: bool = False) -> Dict[str, Any]:
        """
        Integrate with cloud storage for virtual memory management
        
        Args:
            provider: Cloud provider (aws, google, azure) or None for auto-detect
            upload: Whether to upload files
            sync: Whether to sync with cloud
            
        Returns:
            Dictionary with cloud integration results
        """
        logger.info(f"Cloud integration - Provider: {provider}, Upload: {upload}, Sync: {sync}")
        
        start_time = time.time()
        
        try:
            # Auto-detect provider if not specified
            if not provider:
                provider = self.cloud_integrator.get_active_provider()
                
            if not provider:
                raise ValueError("No active cloud provider configured")
            
            uploaded_count = 0
            sync_status = "not_requested"
            
            # Upload files if requested
            if upload:
                uploaded_count = self.cloud_integrator.upload_organized_files(provider)
                logger.info(f"Uploaded {uploaded_count} files to {provider}")
            
            # Sync with cloud if requested
            if sync:
                sync_status = self.cloud_integrator.sync_with_cloud(provider)
                logger.info(f"Sync status: {sync_status}")
            
            duration = time.time() - start_time
            
            results = {
                'success': True,
                'provider': provider,
                'uploaded_count': uploaded_count,
                'sync_status': sync_status,
                'duration': f"{duration:.2f} seconds"
            }
            
            logger.info(f"Cloud integration completed in {duration:.2f}s")
            return results
            
        except Exception as e:
            logger.error(f"Cloud integration failed: {e}")
            raise
    
    def complete_workflow(self, path: str = ".", apply_changes: bool = False,
                         create_backup: bool = None) -> Dict[str, Any]:
        """
        Run complete file organization workflow
        
        Args:
            path: Path to process
            apply_changes: Whether to apply all changes
            create_backup: Whether to create backup
            
        Returns:
            Dictionary with complete workflow results
        """
        logger.info(f"Starting complete workflow - Path: {path}, Apply: {apply_changes}")
        
        workflow_start = time.time()
        operations = []
        
        try:
            # Step 1: System Analysis
            logger.info("Step 1/4: System Analysis")
            analysis_results = self.analyze_system(path, "comprehensive", True)
            operations.append("system_analysis")
            
            # Step 2: File Organization
            logger.info("Step 2/4: File Organization")
            organization_results = self.organize_files(path, apply_changes, create_backup)
            operations.append("file_organization")
            
            # Step 3: Layout Creation
            logger.info("Step 3/4: Layout Creation")
            layout_results = self.create_layout("professional", "modern", apply_changes)
            operations.append("layout_creation")
            
            # Step 4: Cloud Integration (if configured)
            cloud_results = None
            active_provider = self.cloud_integrator.get_active_provider()
            if active_provider:
                logger.info("Step 4/4: Cloud Integration")
                cloud_results = self.cloud_integration(active_provider, apply_changes, apply_changes)
                operations.append("cloud_integration")
            else:
                logger.info("Step 4/4: Cloud Integration - Skipped (no active provider)")
            
            total_duration = time.time() - workflow_start
            
            results = {
                'success': True,
                'total_operations': len(operations),
                'operations': operations,
                'analysis_results': analysis_results,
                'organization_results': organization_results,
                'layout_results': layout_results,
                'cloud_results': cloud_results,
                'duration': f"{total_duration:.2f} seconds",
                'path_processed': path,
                'changes_applied': apply_changes
            }
            
            logger.info(f"Complete workflow finished successfully in {total_duration:.2f}s")
            return results
            
        except Exception as e:
            logger.error(f"Complete workflow failed: {e}")
            raise