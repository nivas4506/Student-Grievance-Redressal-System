"""
Grievance Visualization Module
Creates charts and graphs using Matplotlib.
Demonstrates: Matplotlib, Data Visualization, Charts
"""

import os

try:
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("[WARNING] Matplotlib not installed. Run: pip install matplotlib")

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False


class GrievanceVisualizer:
    """
    Visualizer class for creating charts and graphs.
    Uses Matplotlib for visualization.
    """
    
    # Color schemes
    COLORS = {
        'primary': '#3498db',
        'success': '#2ecc71',
        'warning': '#f39c12',
        'danger': '#e74c3c',
        'info': '#17a2b8',
        'dark': '#2c3e50'
    }
    
    STATUS_COLORS = {
        'Pending': '#f39c12',
        'In Progress': '#3498db',
        'Resolved': '#2ecc71',
        'Rejected': '#e74c3c'
    }
    
    CATEGORY_COLORS = [
        '#3498db', '#2ecc71', '#e74c3c', 
        '#f39c12', '#9b59b6', '#1abc9c'
    ]
    
    def __init__(self, analyzer=None):
        """
        Initialize visualizer with optional analyzer.
        
        Args:
            analyzer: GrievanceAnalyzer instance
        """
        self.analyzer = analyzer
        self.output_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 
            'data', 'charts'
        )
        
        # Create output directory if not exists
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def _check_matplotlib(self):
        """Check if matplotlib is available."""
        if not MATPLOTLIB_AVAILABLE:
            print("[ERROR] Matplotlib not available. Install with: pip install matplotlib")
            return False
        return True
    
    def create_status_pie_chart(self, save=False, show=True):
        """
        Create pie chart showing grievance status distribution.
        
        Args:
            save (bool): Save chart to file
            show (bool): Display chart
            
        Returns:
            str: Path to saved file (if saved)
        """
        if not self._check_matplotlib():
            return None
        
        status_counts = self.analyzer.get_status_counts()
        
        if not status_counts:
            print("[INFO] No data available for chart")
            return None
        
        labels = list(status_counts.keys())
        sizes = list(status_counts.values())
        colors = [self.STATUS_COLORS.get(s, '#95a5a6') for s in labels]
        
        fig, ax = plt.subplots(figsize=(8, 6))
        
        wedges, texts, autotexts = ax.pie(
            sizes, 
            labels=labels, 
            colors=colors,
            autopct='%1.1f%%',
            startangle=90,
            explode=[0.05] * len(labels)
        )
        
        ax.set_title('Grievance Status Distribution', fontsize=14, fontweight='bold')
        
        # Style the labels
        for text in texts:
            text.set_fontsize(11)
        for autotext in autotexts:
            autotext.set_fontsize(10)
            autotext.set_fontweight('bold')
        
        plt.tight_layout()
        
        if save:
            filepath = os.path.join(self.output_dir, 'status_pie_chart.png')
            plt.savefig(filepath, dpi=150, bbox_inches='tight')
            print(f"[INFO] Chart saved: {filepath}")
        
        if show:
            plt.show()
        else:
            plt.close()
        
        return filepath if save else None
    
    def create_category_bar_chart(self, save=False, show=True):
        """
        Create bar chart showing grievances by category.
        
        Args:
            save (bool): Save chart to file
            show (bool): Display chart
            
        Returns:
            str: Path to saved file (if saved)
        """
        if not self._check_matplotlib():
            return None
        
        category_counts = self.analyzer.get_category_counts()
        
        if not category_counts:
            print("[INFO] No data available for chart")
            return None
        
        categories = list(category_counts.keys())
        counts = list(category_counts.values())
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        bars = ax.bar(categories, counts, color=self.CATEGORY_COLORS[:len(categories)])
        
        ax.set_xlabel('Category', fontsize=12)
        ax.set_ylabel('Number of Grievances', fontsize=12)
        ax.set_title('Grievances by Category', fontsize=14, fontweight='bold')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{int(height)}',
                       xy=(bar.get_x() + bar.get_width() / 2, height),
                       xytext=(0, 3),
                       textcoords="offset points",
                       ha='center', va='bottom',
                       fontweight='bold')
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        if save:
            filepath = os.path.join(self.output_dir, 'category_bar_chart.png')
            plt.savefig(filepath, dpi=150, bbox_inches='tight')
            print(f"[INFO] Chart saved: {filepath}")
        
        if show:
            plt.show()
        else:
            plt.close()
        
        return filepath if save else None
    
    def create_monthly_trend_line(self, save=False, show=True):
        """
        Create line chart showing monthly grievance trend.
        
        Args:
            save (bool): Save chart to file
            show (bool): Display chart
            
        Returns:
            str: Path to saved file (if saved)
        """
        if not self._check_matplotlib():
            return None
        
        monthly_data = self.analyzer.get_monthly_trend()
        
        if not monthly_data:
            print("[INFO] No data available for chart")
            return None
        
        months = list(monthly_data.keys())
        counts = list(monthly_data.values())
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        ax.plot(months, counts, marker='o', linewidth=2, 
                color=self.COLORS['primary'], markersize=8)
        ax.fill_between(months, counts, alpha=0.3, color=self.COLORS['primary'])
        
        ax.set_xlabel('Month', fontsize=12)
        ax.set_ylabel('Number of Grievances', fontsize=12)
        ax.set_title('Monthly Grievance Trend', fontsize=14, fontweight='bold')
        
        # Add value labels
        for i, (m, c) in enumerate(zip(months, counts)):
            ax.annotate(f'{c}', (m, c), textcoords="offset points",
                       xytext=(0, 10), ha='center', fontweight='bold')
        
        plt.xticks(rotation=45, ha='right')
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        
        if save:
            filepath = os.path.join(self.output_dir, 'monthly_trend.png')
            plt.savefig(filepath, dpi=150, bbox_inches='tight')
            print(f"[INFO] Chart saved: {filepath}")
        
        if show:
            plt.show()
        else:
            plt.close()
        
        return filepath if save else None
    
    def create_status_category_heatmap(self, save=False, show=True):
        """
        Create heatmap showing status vs category distribution.
        
        Args:
            save (bool): Save chart to file
            show (bool): Display chart
            
        Returns:
            str: Path to saved file (if saved)
        """
        if not self._check_matplotlib():
            return None
        
        matrix = self.analyzer.get_category_status_matrix()
        
        if matrix is None or matrix.empty:
            print("[INFO] No data available for chart")
            return None
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        im = ax.imshow(matrix.values, cmap='YlOrRd', aspect='auto')
        
        ax.set_xticks(range(len(matrix.columns)))
        ax.set_yticks(range(len(matrix.index)))
        ax.set_xticklabels(matrix.columns)
        ax.set_yticklabels(matrix.index)
        
        # Add value annotations
        for i in range(len(matrix.index)):
            for j in range(len(matrix.columns)):
                value = matrix.values[i, j]
                color = 'white' if value > matrix.values.max() / 2 else 'black'
                ax.text(j, i, str(value), ha='center', va='center', 
                       color=color, fontweight='bold')
        
        ax.set_xlabel('Status', fontsize=12)
        ax.set_ylabel('Category', fontsize=12)
        ax.set_title('Category vs Status Heatmap', fontsize=14, fontweight='bold')
        
        plt.colorbar(im, ax=ax, label='Count')
        plt.tight_layout()
        
        if save:
            filepath = os.path.join(self.output_dir, 'heatmap.png')
            plt.savefig(filepath, dpi=150, bbox_inches='tight')
            print(f"[INFO] Chart saved: {filepath}")
        
        if show:
            plt.show()
        else:
            plt.close()
        
        return filepath if save else None
    
    def create_summary_dashboard(self, save=False, show=True):
        """
        Create comprehensive dashboard with multiple charts.
        
        Args:
            save (bool): Save chart to file
            show (bool): Display chart
            
        Returns:
            str: Path to saved file (if saved)
        """
        if not self._check_matplotlib():
            return None
        
        stats = self.analyzer.get_summary_statistics()
        
        fig = plt.figure(figsize=(14, 10))
        fig.suptitle('GRIEVANCE SYSTEM DASHBOARD', fontsize=16, fontweight='bold')
        
        # 1. Status Pie Chart (Top Left)
        ax1 = fig.add_subplot(2, 2, 1)
        status_counts = stats['status_breakdown']
        if status_counts:
            labels = list(status_counts.keys())
            sizes = list(status_counts.values())
            colors = [self.STATUS_COLORS.get(s, '#95a5a6') for s in labels]
            ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
            ax1.set_title('Status Distribution')
        
        # 2. Category Bar Chart (Top Right)
        ax2 = fig.add_subplot(2, 2, 2)
        category_counts = stats['category_breakdown']
        if category_counts:
            categories = list(category_counts.keys())
            counts = list(category_counts.values())
            bars = ax2.bar(categories, counts, color=self.CATEGORY_COLORS[:len(categories)])
            ax2.set_title('Grievances by Category')
            ax2.set_xlabel('Category')
            ax2.set_ylabel('Count')
            plt.sca(ax2)
            plt.xticks(rotation=45, ha='right')
        
        # 3. Summary Stats (Bottom Left)
        ax3 = fig.add_subplot(2, 2, 3)
        ax3.axis('off')
        summary_text = f"""
        SUMMARY STATISTICS
        ══════════════════════════════
        
        Total Grievances: {stats['total_grievances']}
        
        Pending: {stats['pending_count']}
        
        Resolution Rate: {stats['resolution_rate']}%
        
        Top Category: {stats['top_categories'][0][0] if stats['top_categories'] else 'N/A'}
        """
        ax3.text(0.1, 0.5, summary_text, transform=ax3.transAxes, 
                fontsize=12, verticalalignment='center', fontfamily='monospace',
                bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.5))
        
        # 4. Monthly Trend (Bottom Right)
        ax4 = fig.add_subplot(2, 2, 4)
        monthly = stats['monthly_trend']
        if monthly:
            months = list(monthly.keys())
            counts = list(monthly.values())
            ax4.plot(months, counts, marker='o', linewidth=2, color=self.COLORS['primary'])
            ax4.fill_between(months, counts, alpha=0.3, color=self.COLORS['primary'])
            ax4.set_title('Monthly Trend')
            ax4.set_xlabel('Month')
            ax4.set_ylabel('Count')
            ax4.grid(True, alpha=0.3)
            plt.sca(ax4)
            plt.xticks(rotation=45, ha='right')
        
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        
        if save:
            filepath = os.path.join(self.output_dir, 'dashboard.png')
            plt.savefig(filepath, dpi=150, bbox_inches='tight')
            print(f"[INFO] Dashboard saved: {filepath}")
        
        if show:
            plt.show()
        else:
            plt.close()
        
        return filepath if save else None
    
    def generate_all_charts(self, save=True, show=False):
        """
        Generate all available charts.
        
        Args:
            save (bool): Save charts to files
            show (bool): Display charts
            
        Returns:
            list: Paths to saved files
        """
        saved_files = []
        
        print("\n[INFO] Generating charts...")
        
        result = self.create_status_pie_chart(save=save, show=show)
        if result:
            saved_files.append(result)
        
        result = self.create_category_bar_chart(save=save, show=show)
        if result:
            saved_files.append(result)
        
        result = self.create_monthly_trend_line(save=save, show=show)
        if result:
            saved_files.append(result)
        
        result = self.create_summary_dashboard(save=save, show=show)
        if result:
            saved_files.append(result)
        
        print(f"[INFO] Generated {len(saved_files)} charts")
        
        return saved_files


if __name__ == "__main__":
    from analytics.analyzer import GrievanceAnalyzer
    
    analyzer = GrievanceAnalyzer()
    visualizer = GrievanceVisualizer(analyzer)
    
    # Generate all charts
    visualizer.generate_all_charts(save=True, show=True)
