#!/usr/bin/env python3
"""
File Organization System - Main Application Entry Point

This script provides a comprehensive file organization system that:
- Analyzes computer systems completely
- Suggests and applies file organization modifications  
- Creates professional, clean, dynamic layouts
- Integrates with cloud storage for virtual memory management
"""

import sys
import os
import click
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from file_org_system.core.main_controller import FileOrgController
from file_org_system.utils.config_loader import ConfigLoader
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

@click.group()
@click.version_option(version="1.0.0")
def cli():
    """File Organization System - Professional Computer Analysis and File Management"""
    pass

@cli.command()
@click.option('--path', '-p', default='.', help='Path to analyze (default: current directory)')
@click.option('--depth', '-d', default='comprehensive', 
              type=click.Choice(['basic', 'standard', 'comprehensive']),
              help='Analysis depth level')
@click.option('--report', '-r', is_flag=True, help='Generate detailed analysis report')
def analyze(path, depth, report):
    """Analyze computer system and file structure comprehensively"""
    console.print(Panel.fit("🔍 [bold blue]System Analysis Starting[/bold blue]", 
                           border_style="blue"))
    
    try:
        controller = FileOrgController()
        results = controller.analyze_system(path, depth, generate_report=report)
        
        console.print(f"✅ Analysis completed successfully!")
        if report:
            console.print(f"📄 Report saved to: {results.get('report_path', 'N/A')}")
            
    except Exception as e:
        console.print(f"❌ [red]Error during analysis: {e}[/red]")
        sys.exit(1)

@cli.command()
@click.option('--path', '-p', default='.', help='Path to organize (default: current directory)')
@click.option('--apply', '-a', is_flag=True, help='Apply organization changes (default: preview only)')
@click.option('--backup', '-b', is_flag=True, help='Create backup before changes')
def organize(path, apply, backup):
    """Organize and categorize files professionally"""
    console.print(Panel.fit("📁 [bold green]File Organization Starting[/bold green]", 
                           border_style="green"))
    
    try:
        controller = FileOrgController()
        results = controller.organize_files(path, apply_changes=apply, create_backup=backup)
        
        if apply:
            console.print(f"✅ Organization applied successfully!")
            console.print(f"📊 Files processed: {results.get('files_processed', 0)}")
        else:
            console.print(f"👀 Preview mode - no changes applied")
            console.print(f"📋 Suggestions generated: {results.get('suggestions_count', 0)}")
            
    except Exception as e:
        console.print(f"❌ [red]Error during organization: {e}[/red]")
        sys.exit(1)

@cli.command()
@click.option('--style', '-s', default='professional', 
              type=click.Choice(['professional', 'minimal', 'dynamic']),
              help='Layout style')
@click.option('--theme', '-t', default='modern',
              type=click.Choice(['modern', 'classic', 'corporate']),
              help='Layout theme')
@click.option('--apply', '-a', is_flag=True, help='Apply layout changes')
def layout(style, theme, apply):
    """Create professional, clean and dynamic layouts"""
    console.print(Panel.fit("🎨 [bold magenta]Layout Generation Starting[/bold magenta]", 
                           border_style="magenta"))
    
    try:
        controller = FileOrgController()
        results = controller.create_layout(style, theme, apply_changes=apply)
        
        if apply:
            console.print(f"✅ Layout applied successfully!")
        else:
            console.print(f"👀 Preview mode - layout prepared")
            
        console.print(f"🎯 Layout style: {style} / Theme: {theme}")
            
    except Exception as e:
        console.print(f"❌ [red]Error during layout creation: {e}[/red]")
        sys.exit(1)

@cli.command()
@click.option('--provider', '-p', type=click.Choice(['aws', 'google', 'azure']),
              help='Cloud provider')
@click.option('--upload', '-u', is_flag=True, help='Upload files to cloud')
@click.option('--sync', '-s', is_flag=True, help='Sync with cloud storage')
def cloud(provider, upload, sync):
    """Integrate with cloud storage for virtual memory management"""
    console.print(Panel.fit("☁️ [bold cyan]Cloud Integration Starting[/bold cyan]", 
                           border_style="cyan"))
    
    try:
        controller = FileOrgController()
        results = controller.cloud_integration(provider, upload=upload, sync=sync)
        
        console.print(f"✅ Cloud operation completed!")
        if upload:
            console.print(f"📤 Files uploaded: {results.get('uploaded_count', 0)}")
        if sync:
            console.print(f"🔄 Sync status: {results.get('sync_status', 'Unknown')}")
            
    except Exception as e:
        console.print(f"❌ [red]Error during cloud integration: {e}[/red]")
        sys.exit(1)

@cli.command()
@click.option('--path', '-p', default='.', help='Path to process (default: current directory)')
@click.option('--apply', '-a', is_flag=True, help='Apply all changes')
@click.option('--backup', '-b', is_flag=True, help='Create backup before changes')
def complete(path, apply, backup):
    """Run complete file organization workflow (analyze -> organize -> layout -> cloud)"""
    console.print(Panel.fit("🚀 [bold yellow]Complete Workflow Starting[/bold yellow]", 
                           border_style="yellow"))
    
    try:
        controller = FileOrgController()
        results = controller.complete_workflow(path, apply_changes=apply, create_backup=backup)
        
        console.print(f"✅ Complete workflow finished successfully!")
        console.print(f"📊 Total operations: {results.get('total_operations', 0)}")
        console.print(f"⏱️  Duration: {results.get('duration', 'N/A')}")
            
    except Exception as e:
        console.print(f"❌ [red]Error during complete workflow: {e}[/red]")
        sys.exit(1)

@cli.command()
def status():
    """Show system status and configuration"""
    console.print(Panel.fit("ℹ️ [bold white]System Status[/bold white]", 
                           border_style="white"))
    
    try:
        config = ConfigLoader.load_config()
        console.print("📋 Configuration loaded successfully")
        console.print(f"🔧 Analysis depth: {config['system']['analysis_depth']}")
        console.print(f"💾 Backup enabled: {config['system']['backup_before_changes']}")
        console.print(f"☁️  Cloud providers configured: {len([p for p in config['cloud']['providers'] if config['cloud']['providers'][p]['enabled']])}")
        
    except Exception as e:
        console.print(f"❌ [red]Error checking status: {e}[/red]")
        sys.exit(1)

if __name__ == '__main__':
    # Show welcome banner
    welcome_text = Text("File Organization System", style="bold blue")
    welcome_text.append("\nComprehensive Computer Analysis & File Management", style="italic")
    console.print(Panel(welcome_text, border_style="blue", padding=(1, 2)))
    
    cli()