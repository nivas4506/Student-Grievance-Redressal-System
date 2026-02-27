"""
Grievance Analyzer Module
Performs data analysis on grievances using Pandas.
Demonstrates: Pandas, Data Analysis, Aggregation
"""

import os
import json
from datetime import datetime

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    print("[WARNING] Pandas not installed. Run: pip install pandas")


class GrievanceAnalyzer:
    """
    Analyzer class for grievance data analysis.
    Uses Pandas for efficient data processing.
    """
    
    def __init__(self, data_path=None):
        """
        Initialize analyzer with data path.
        
        Args:
            data_path (str): Path to grievances data file
        """
        if data_path is None:
            data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                     'data', 'grievances.json')
        self.data_path = data_path
        self.df = None
        self._load_data()
    
    def _load_data(self):
        """Load data from JSON file into Pandas DataFrame."""
        if not PANDAS_AVAILABLE:
            return
        
        try:
            with open(self.data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if data:
                self.df = pd.DataFrame(data)
                # Convert date columns
                if 'created_at' in self.df.columns:
                    self.df['created_at'] = pd.to_datetime(self.df['created_at'])
                if 'updated_at' in self.df.columns:
                    self.df['updated_at'] = pd.to_datetime(self.df['updated_at'])
            else:
                self.df = pd.DataFrame()
                
        except FileNotFoundError:
            print(f"[WARNING] File not found: {self.data_path}")
            self.df = pd.DataFrame()
        except json.JSONDecodeError:
            print(f"[ERROR] Invalid JSON in file: {self.data_path}")
            self.df = pd.DataFrame()
    
    def reload_data(self):
        """Reload data from file."""
        self._load_data()
    
    def get_total_grievances(self):
        """
        Get total number of grievances.
        
        Returns:
            int: Total count
        """
        if self.df is None or self.df.empty:
            return 0
        return len(self.df)
    
    def get_status_counts(self):
        """
        Get count of grievances by status.
        
        Returns:
            dict: Status counts {status: count}
        """
        if self.df is None or self.df.empty:
            return {}
        
        counts = self.df.groupby('status').size()
        return counts.to_dict()
    
    def get_category_counts(self):
        """
        Get count of grievances by category.
        
        Returns:
            dict: Category counts {category: count}
        """
        if self.df is None or self.df.empty:
            return {}
        
        counts = self.df.groupby('category').size()
        return counts.to_dict()
    
    def get_monthly_trend(self):
        """
        Get monthly grievance submission trend.
        
        Returns:
            dict: Monthly counts {month: count}
        """
        if self.df is None or self.df.empty or 'created_at' not in self.df.columns:
            return {}
        
        monthly = self.df.groupby(self.df['created_at'].dt.to_period('M')).size()
        return {str(k): v for k, v in monthly.to_dict().items()}
    
    def get_resolution_rate(self):
        """
        Calculate grievance resolution rate.
        
        Returns:
            float: Resolution rate (0-100)
        """
        if self.df is None or self.df.empty:
            return 0.0
        
        resolved = len(self.df[self.df['status'] == 'Resolved'])
        total = len(self.df)
        
        return (resolved / total * 100) if total > 0 else 0.0
    
    def get_pending_count(self):
        """
        Get count of pending grievances.
        
        Returns:
            int: Pending count
        """
        if self.df is None or self.df.empty:
            return 0
        
        return len(self.df[self.df['status'] == 'Pending'])
    
    def get_category_status_matrix(self):
        """
        Get cross-tabulation of category and status.
        
        Returns:
            DataFrame: Cross-tabulation matrix
        """
        if self.df is None or self.df.empty:
            return None
        
        return pd.crosstab(self.df['category'], self.df['status'])
    
    def get_top_categories(self, n=5):
        """
        Get top N categories by grievance count.
        
        Args:
            n (int): Number of categories to return
            
        Returns:
            list: List of (category, count) tuples
        """
        if self.df is None or self.df.empty:
            return []
        
        counts = self.df['category'].value_counts().head(n)
        return list(counts.items())
    
    def get_average_resolution_time(self):
        """
        Calculate average time to resolve grievances.
        
        Returns:
            float: Average days to resolution
        """
        if self.df is None or self.df.empty:
            return 0.0
        
        resolved = self.df[self.df['status'] == 'Resolved'].copy()
        
        if resolved.empty or 'resolved_at' not in resolved.columns:
            return 0.0
        
        resolved['resolved_at'] = pd.to_datetime(resolved['resolved_at'])
        resolved['resolution_time'] = (resolved['resolved_at'] - resolved['created_at']).dt.days
        
        return resolved['resolution_time'].mean()
    
    def get_summary_statistics(self):
        """
        Get comprehensive summary statistics.
        
        Returns:
            dict: Summary statistics
        """
        return {
            'total_grievances': self.get_total_grievances(),
            'pending_count': self.get_pending_count(),
            'resolution_rate': round(self.get_resolution_rate(), 2),
            'status_breakdown': self.get_status_counts(),
            'category_breakdown': self.get_category_counts(),
            'top_categories': self.get_top_categories(3),
            'monthly_trend': self.get_monthly_trend()
        }
    
    def generate_report(self):
        """
        Generate a formatted text report.
        
        Returns:
            str: Formatted report string
        """
        stats = self.get_summary_statistics()
        
        report = []
        report.append("=" * 60)
        report.append("       GRIEVANCE ANALYTICS REPORT")
        report.append("=" * 60)
        report.append(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("\n--- OVERVIEW ---")
        report.append(f"Total Grievances: {stats['total_grievances']}")
        report.append(f"Pending: {stats['pending_count']}")
        report.append(f"Resolution Rate: {stats['resolution_rate']}%")
        
        report.append("\n--- STATUS BREAKDOWN ---")
        for status, count in stats['status_breakdown'].items():
            report.append(f"  {status}: {count}")
        
        report.append("\n--- CATEGORY BREAKDOWN ---")
        for category, count in stats['category_breakdown'].items():
            report.append(f"  {category}: {count}")
        
        report.append("\n--- TOP CATEGORIES ---")
        for i, (cat, count) in enumerate(stats['top_categories'], 1):
            report.append(f"  {i}. {cat}: {count}")
        
        report.append("\n" + "=" * 60)
        
        return "\n".join(report)
    
    def export_to_csv(self, output_path=None):
        """
        Export data to CSV file.
        
        Args:
            output_path (str): Output file path
            
        Returns:
            bool: True if successful
        """
        if self.df is None or self.df.empty:
            return False
        
        if output_path is None:
            output_path = os.path.join(os.path.dirname(self.data_path), 'grievances.csv')
        
        try:
            self.df.to_csv(output_path, index=False)
            print(f"[INFO] Data exported to: {output_path}")
            return True
        except Exception as e:
            print(f"[ERROR] Export failed: {e}")
            return False


# Standalone function for quick analysis
def analyze_grievances(data_path=None):
    """
    Quick function to analyze grievances.
    
    Args:
        data_path (str): Path to data file
        
    Returns:
        dict: Summary statistics
    """
    analyzer = GrievanceAnalyzer(data_path)
    return analyzer.get_summary_statistics()


if __name__ == "__main__":
    # Test the analyzer
    analyzer = GrievanceAnalyzer()
    print(analyzer.generate_report())
