"""
Export Utilities Module

This module provides functionality for exporting data in various formats.
It includes JSON, CSV, and Excel export capabilities.

Author: Rami Drive School
Date: 2024
"""

import json
import csv
import os
from typing import Dict, Any, List, Optional, Union, Iterator
from datetime import datetime
import logging
import pandas as pd
from pathlib import Path

logger = logging.getLogger(__name__)

class ExportError(Exception):
    """Export error."""
    pass

class ExportManager:
    """Export manager."""
    
    def __init__(
        self,
        export_dir: str = "exports",
        max_size: int = 100 * 1024 * 1024  # 100MB
    ):
        """Initialize export manager.
        
        Args:
            export_dir: Export directory
            max_size: Maximum file size in bytes
        """
        self.export_dir = export_dir
        self.max_size = max_size
        
        # Create export directory if it doesn't exist
        os.makedirs(export_dir, exist_ok=True)
    
    def export_json(
        self,
        data: Union[Dict[str, Any], List[Dict[str, Any]]],
        filename: str,
        pretty: bool = True
    ) -> str:
        """Export data to JSON.
        
        Args:
            data: Data to export
            filename: Output filename
            pretty: Whether to pretty print
            
        Returns:
            Path to exported file
        
        Raises:
            ExportError: If export fails
        """
        try:
            # Create file path
            file_path = os.path.join(
                self.export_dir,
                f"{filename}.json"
            )
            
            # Write data to file
            with open(file_path, "w") as f:
                if pretty:
                    json.dump(data, f, indent=2)
                else:
                    json.dump(data, f)
            
            return file_path
        except Exception as e:
            raise ExportError(f"Error exporting JSON: {str(e)}")
    
    def export_csv(
        self,
        data: List[Dict[str, Any]],
        filename: str,
        delimiter: str = ",",
        quotechar: str = '"'
    ) -> str:
        """Export data to CSV.
        
        Args:
            data: Data to export
            filename: Output filename
            delimiter: Field delimiter
            quotechar: Quote character
            
        Returns:
            Path to exported file
        
        Raises:
            ExportError: If export fails
        """
        try:
            # Create file path
            file_path = os.path.join(
                self.export_dir,
                f"{filename}.csv"
            )
            
            # Get field names
            fieldnames = list(data[0].keys())
            
            # Write data to file
            with open(file_path, "w", newline="") as f:
                writer = csv.DictWriter(
                    f,
                    fieldnames=fieldnames,
                    delimiter=delimiter,
                    quotechar=quotechar
                )
                writer.writeheader()
                writer.writerows(data)
            
            return file_path
        except Exception as e:
            raise ExportError(f"Error exporting CSV: {str(e)}")
    
    def export_excel(
        self,
        data: List[Dict[str, Any]],
        filename: str,
        sheet_name: str = "Sheet1"
    ) -> str:
        """Export data to Excel.
        
        Args:
            data: Data to export
            filename: Output filename
            sheet_name: Sheet name
            
        Returns:
            Path to exported file
        
        Raises:
            ExportError: If export fails
        """
        try:
            # Create file path
            file_path = os.path.join(
                self.export_dir,
                f"{filename}.xlsx"
            )
            
            # Convert data to DataFrame
            df = pd.DataFrame(data)
            
            # Write data to file
            df.to_excel(
                file_path,
                sheet_name=sheet_name,
                index=False
            )
            
            return file_path
        except Exception as e:
            raise ExportError(f"Error exporting Excel: {str(e)}")
    
    def export_data(
        self,
        data: Union[Dict[str, Any], List[Dict[str, Any]]],
        filename: str,
        format: str = "json",
        **kwargs
    ) -> str:
        """Export data.
        
        Args:
            data: Data to export
            filename: Output filename
            format: Export format
            **kwargs: Additional arguments
            
        Returns:
            Path to exported file
        
        Raises:
            ExportError: If export fails
        """
        if format == "json":
            return self.export_json(data, filename, **kwargs)
        elif format == "csv":
            return self.export_csv(data, filename, **kwargs)
        elif format == "excel":
            return self.export_excel(data, filename, **kwargs)
        else:
            raise ExportError(f"Unsupported format: {format}")
    
    def export_stream(
        self,
        data_iterator: Iterator[Dict[str, Any]],
        filename: str,
        format: str = "json",
        batch_size: int = 1000,
        **kwargs
    ) -> str:
        """Export data stream.
        
        Args:
            data_iterator: Data iterator
            filename: Output filename
            format: Export format
            batch_size: Batch size
            **kwargs: Additional arguments
            
        Returns:
            Path to exported file
        
        Raises:
            ExportError: If export fails
        """
        try:
            # Create file path
            file_path = os.path.join(
                self.export_dir,
                f"{filename}.{format}"
            )
            
            if format == "json":
                # Write opening bracket
                with open(file_path, "w") as f:
                    f.write("[\n")
                
                # Write data in batches
                first = True
                batch = []
                
                for item in data_iterator:
                    batch.append(item)
                    
                    if len(batch) >= batch_size:
                        with open(file_path, "a") as f:
                            for item in batch:
                                if not first:
                                    f.write(",\n")
                                f.write(json.dumps(item, indent=2))
                                first = False
                        
                        batch = []
                
                # Write remaining items
                if batch:
                    with open(file_path, "a") as f:
                        for item in batch:
                            if not first:
                                f.write(",\n")
                            f.write(json.dumps(item, indent=2))
                            first = False
                
                # Write closing bracket
                with open(file_path, "a") as f:
                    f.write("\n]")
            
            elif format == "csv":
                # Get field names from first item
                first_item = next(data_iterator)
                fieldnames = list(first_item.keys())
                
                # Write header
                with open(file_path, "w", newline="") as f:
                    writer = csv.DictWriter(
                        f,
                        fieldnames=fieldnames,
                        **kwargs
                    )
                    writer.writeheader()
                    writer.writerow(first_item)
                
                # Write data in batches
                batch = []
                
                for item in data_iterator:
                    batch.append(item)
                    
                    if len(batch) >= batch_size:
                        with open(file_path, "a", newline="") as f:
                            writer = csv.DictWriter(
                                f,
                                fieldnames=fieldnames,
                                **kwargs
                            )
                            writer.writerows(batch)
                        
                        batch = []
                
                # Write remaining items
                if batch:
                    with open(file_path, "a", newline="") as f:
                        writer = csv.DictWriter(
                            f,
                            fieldnames=fieldnames,
                            **kwargs
                        )
                        writer.writerows(batch)
            
            elif format == "excel":
                # Convert iterator to list
                data = list(data_iterator)
                
                # Export to Excel
                return self.export_excel(data, filename, **kwargs)
            
            else:
                raise ExportError(f"Unsupported format: {format}")
            
            return file_path
        except Exception as e:
            raise ExportError(f"Error exporting stream: {str(e)}")
    
    def get_export_size(self, file_path: str) -> int:
        """Get export file size.
        
        Args:
            file_path: File path
            
        Returns:
            File size in bytes
        """
        return os.path.getsize(file_path)
    
    def check_export_size(self, file_path: str) -> bool:
        """Check export file size.
        
        Args:
            file_path: File path
            
        Returns:
            True if size is within limit, False otherwise
        """
        return self.get_export_size(file_path) <= self.max_size
    
    def cleanup_exports(
        self,
        max_age_days: int = 30
    ) -> None:
        """Clean up old exports.
        
        Args:
            max_age_days: Maximum age in days
        """
        try:
            # Get current time
            now = datetime.now()
            
            # Iterate through export directory
            for file_path in Path(self.export_dir).glob("*"):
                # Skip directories
                if file_path.is_dir():
                    continue
                
                # Get file age
                file_age = now - datetime.fromtimestamp(
                    file_path.stat().st_mtime
                )
                
                # Remove old files
                if file_age.days > max_age_days:
                    file_path.unlink()
        except Exception as e:
            logger.error(f"Error cleaning up exports: {str(e)}")
    
    def get_export_info(self, file_path: str) -> Dict[str, Any]:
        """Get export file information.
        
        Args:
            file_path: File path
            
        Returns:
            File information dictionary
        """
        try:
            # Get file stats
            stats = os.stat(file_path)
            
            return {
                "path": file_path,
                "size": stats.st_size,
                "created": datetime.fromtimestamp(
                    stats.st_ctime
                ).isoformat(),
                "modified": datetime.fromtimestamp(
                    stats.st_mtime
                ).isoformat(),
                "format": os.path.splitext(file_path)[1][1:]
            }
        except Exception as e:
            raise ExportError(f"Error getting export info: {str(e)}")
    
    def list_exports(
        self,
        format: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """List exports.
        
        Args:
            format: Export format
            
        Returns:
            List of export information dictionaries
        """
        try:
            exports = []
            
            # Iterate through export directory
            for file_path in Path(self.export_dir).glob("*"):
                # Skip directories
                if file_path.is_dir():
                    continue
                
                # Check format
                if format and file_path.suffix[1:] != format:
                    continue
                
                # Get file info
                exports.append(
                    self.get_export_info(str(file_path))
                )
            
            return exports
        except Exception as e:
            raise ExportError(f"Error listing exports: {str(e)}")
    
    def delete_export(self, file_path: str) -> None:
        """Delete export.
        
        Args:
            file_path: File path
            
        Raises:
            ExportError: If deletion fails
        """
        try:
            os.remove(file_path)
        except Exception as e:
            raise ExportError(f"Error deleting export: {str(e)}")
    
    def move_export(
        self,
        file_path: str,
        new_path: str
    ) -> str:
        """Move export.
        
        Args:
            file_path: Source file path
            new_path: Destination file path
            
        Returns:
            New file path
        
        Raises:
            ExportError: If move fails
        """
        try:
            # Create destination directory if it doesn't exist
            os.makedirs(os.path.dirname(new_path), exist_ok=True)
            
            # Move file
            os.rename(file_path, new_path)
            
            return new_path
        except Exception as e:
            raise ExportError(f"Error moving export: {str(e)}")
    
    def copy_export(
        self,
        file_path: str,
        new_path: str
    ) -> str:
        """Copy export.
        
        Args:
            file_path: Source file path
            new_path: Destination file path
            
        Returns:
            New file path
        
        Raises:
            ExportError: If copy fails
        """
        try:
            # Create destination directory if it doesn't exist
            os.makedirs(os.path.dirname(new_path), exist_ok=True)
            
            # Copy file
            import shutil
            shutil.copy2(file_path, new_path)
            
            return new_path
        except Exception as e:
            raise ExportError(f"Error copying export: {str(e)}") 