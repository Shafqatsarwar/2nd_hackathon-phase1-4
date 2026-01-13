"""
Data Visualization Skill
Automatically creates insightful visualizations from datasets to help identify trends, patterns, and outliers.
"""
import random
import math
from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Union
from datetime import datetime
from enum import Enum

class ChartType(Enum):
    BAR = "bar"
    LINE = "line"
    PIE = "pie"
    SCATTER = "scatter"
    HEATMAP = "heatmap"
    HISTOGRAM = "histogram"
    AREA = "area"

class DataType(Enum):
    NUMERIC = "numeric"
    CATEGORICAL = "categorical"
    DATE = "date"
    BOOLEAN = "boolean"

@dataclass
class VisualizationConfig:
    title: str
    chart_type: ChartType
    width: int = 800
    height: int = 600
    color_scheme: str = "default"
    show_legend: bool = True
    show_grid: bool = True

@dataclass
class Dataset:
    name: str
    columns: List[str]
    data: List[Dict[str, Any]]
    row_count: int

@dataclass
class VisualizationResult:
    title: str
    chart_type: str
    description: str
    insights: List[str]
    recommendations: List[str]
    mock_chart_data: Dict[str, Any]  # Since we can't actually generate charts without visualization libraries

class DataVisualizer:
    """
    Skill to automatically create insightful visualizations from datasets.
    """

    def __init__(self):
        self.color_schemes = {
            'default': ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'],
            'pastel': ['#aec7e8', '#ffbb78', '#98df8a', '#ff9896', '#c5b0d5'],
            'vibrant': ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#feca57'],
            'monochrome': ['#2c3e50', '#34495e', '#7f8c8d', '#95a5a6', '#bdc3c7']
        }

        self.chart_recommendations = {
            'time_series': [ChartType.LINE, ChartType.AREA],
            'comparison': [ChartType.BAR, ChartType.LINE],
            'distribution': [ChartType.HISTOGRAM, ChartType.SCATTER],
            'composition': [ChartType.PIE, ChartType.BAR],
            'correlation': [ChartType.SCATTER, ChartType.HEATMAP]
        }

    def analyze_dataset(self, data: List[Dict[str, Any]]) -> Dataset:
        """
        Analyze the structure and content of the dataset.
        """
        if not data:
            raise ValueError("Dataset is empty")

        columns = list(data[0].keys()) if data else []
        row_count = len(data)

        return Dataset(
            name="Auto-generated Dataset",
            columns=columns,
            data=data,
            row_count=row_count
        )

    def detect_data_types(self, dataset: Dataset) -> Dict[str, DataType]:
        """
        Detect the data type for each column in the dataset.
        """
        types = {}

        for col in dataset.columns:
            # Sample values from the column
            sample_values = [row[col] for row in dataset.data if col in row and row[col] is not None][:10]

            # Determine the most common type in the sample
            numeric_count = 0
            date_count = 0
            boolean_count = 0

            for val in sample_values:
                if isinstance(val, (int, float)):
                    numeric_count += 1
                elif isinstance(val, str):
                    # Check if it looks like a date
                    if any(x in val for x in ['/', '-', ':']):
                        date_count += 1
                    elif val.lower() in ['true', 'false', 'yes', 'no', '1', '0']:
                        boolean_count += 1

            # Determine dominant type
            total = len(sample_values)
            if numeric_count == total or (numeric_count / total) > 0.8:
                types[col] = DataType.NUMERIC
            elif date_count == total or (date_count / total) > 0.8:
                types[col] = DataType.DATE
            elif boolean_count == total or (boolean_count / total) > 0.8:
                types[col] = DataType.BOOLEAN
            else:
                types[col] = DataType.CATEGORICAL

        return types

    def suggest_visualizations(self, dataset: Dataset, data_types: Dict[str, DataType]) -> List[VisualizationConfig]:
        """
        Suggest appropriate visualizations based on the dataset structure.
        """
        suggestions = []

        # Identify potential visualization scenarios
        numeric_cols = [col for col, dt in data_types.items() if dt == DataType.NUMERIC]
        categorical_cols = [col for col, dt in data_types.items() if dt == DataType.CATEGORICAL]
        date_cols = [col for col, dt in data_types.items() if dt == DataType.DATE]

        # Time series visualization
        if date_cols and numeric_cols:
            suggestions.append(VisualizationConfig(
                title=f"Trend Analysis: {numeric_cols[0]} over {date_cols[0]}",
                chart_type=ChartType.LINE,
                color_scheme="vibrant"
            ))

        # Comparison visualization
        if len(categorical_cols) >= 1 and len(numeric_cols) >= 1:
            suggestions.append(VisualizationConfig(
                title=f"Comparison: {numeric_cols[0]} by {categorical_cols[0]}",
                chart_type=ChartType.BAR,
                color_scheme="default"
            ))

        # Distribution visualization
        if len(numeric_cols) >= 1:
            suggestions.append(VisualizationConfig(
                title=f"Distribution of {numeric_cols[0]}",
                chart_type=ChartType.HISTOGRAM,
                color_scheme="pastel"
            ))

        # Correlation visualization
        if len(numeric_cols) >= 2:
            suggestions.append(VisualizationConfig(
                title=f"Correlation: {numeric_cols[0]} vs {numeric_cols[1]}",
                chart_type=ChartType.SCATTER,
                color_scheme="monochrome"
            ))

        # Composition visualization
        if len(categorical_cols) >= 1 and len(numeric_cols) >= 1:
            suggestions.append(VisualizationConfig(
                title=f"Composition: {categorical_cols[0]} Distribution",
                chart_type=ChartType.PIE,
                color_scheme="vibrant"
            ))

        return suggestions

    def calculate_basic_stats(self, dataset: Dataset, data_types: Dict[str, DataType]) -> Dict[str, Dict[str, float]]:
        """
        Calculate basic statistics for numeric columns.
        """
        stats = {}

        for col, dt in data_types.items():
            if dt == DataType.NUMERIC:
                values = [row[col] for row in dataset.data if isinstance(row.get(col), (int, float))]

                if values:
                    n = len(values)
                    mean = sum(values) / n
                    variance = sum((x - mean) ** 2 for x in values) / n
                    std_dev = math.sqrt(variance)

                    # Calculate median
                    sorted_vals = sorted(values)
                    median = sorted_vals[n // 2] if n % 2 == 1 else (sorted_vals[n // 2 - 1] + sorted_vals[n // 2]) / 2

                    stats[col] = {
                        'mean': mean,
                        'median': median,
                        'std_dev': std_dev,
                        'min': min(values),
                        'max': max(values),
                        'count': n
                    }

        return stats

    def identify_outliers(self, dataset: Dataset, data_types: Dict[str, DataType], threshold: float = 2.0) -> Dict[str, List[Any]]:
        """
        Identify outliers in numeric columns using standard deviation.
        """
        outliers = {}

        for col, dt in data_types.items():
            if dt == DataType.NUMERIC:
                values = [row[col] for row in dataset.data if isinstance(row.get(col), (int, float))]

                if values:
                    n = len(values)
                    mean = sum(values) / n
                    variance = sum((x - mean) ** 2 for x in values) / n
                    std_dev = math.sqrt(variance)

                    # Identify outliers (values beyond threshold standard deviations)
                    col_outliers = []
                    for row in dataset.data:
                        if col in row and isinstance(row[col], (int, float)):
                            z_score = abs((row[col] - mean) / std_dev) if std_dev != 0 else 0
                            if z_score > threshold:
                                col_outliers.append(row[col])

                    if col_outliers:
                        outliers[col] = col_outliers

        return outliers

    def generate_insights(self, dataset: Dataset, data_types: Dict[str, DataType], stats: Dict[str, Dict[str, float]], outliers: Dict[str, List[Any]]) -> List[str]:
        """
        Generate insights about the dataset.
        """
        insights = []

        # Dataset overview
        insights.append(f"Dataset contains {dataset.row_count} rows and {len(dataset.columns)} columns.")

        # Numeric column insights
        numeric_cols = [col for col, dt in data_types.items() if dt == DataType.NUMERIC]
        if numeric_cols:
            insights.append(f"Found {len(numeric_cols)} numeric columns for analysis.")

        # Categorical column insights
        categorical_cols = [col for col, dt in data_types.items() if dt == DataType.CATEGORICAL]
        if categorical_cols:
            insights.append(f"Found {len(categorical_cols)} categorical columns that can be used for grouping.")

        # Date column insights
        date_cols = [col for col, dt in data_types.items() if dt == DataType.DATE]
        if date_cols:
            insights.append(f"Found {len(date_cols)} date columns suitable for time-series analysis.")

        # Statistical insights
        for col, col_stats in stats.items():
            insights.append(f"{col} has mean of {col_stats['mean']:.2f} and standard deviation of {col_stats['std_dev']:.2f}.")

        # Outlier insights
        for col, col_outliers in outliers.items():
            if col_outliers:
                insights.append(f"Detected {len(col_outliers)} outliers in column '{col}'.")

        return insights

    def generate_recommendations(self, dataset: Dataset, data_types: Dict[str, DataType]) -> List[str]:
        """
        Generate recommendations for further analysis.
        """
        recommendations = []

        # Data quality recommendations
        if dataset.row_count < 100:
            recommendations.append("Dataset is relatively small. Consider collecting more data for robust analysis.")

        # Visualization recommendations
        numeric_cols = [col for col, dt in data_types.items() if dt == DataType.NUMERIC]
        categorical_cols = [col for col, dt in data_types.items() if dt == DataType.CATEGORICAL]

        if len(numeric_cols) >= 2:
            recommendations.append("Consider creating a correlation matrix to explore relationships between numeric variables.")

        if len(categorical_cols) >= 1 and len(numeric_cols) >= 1:
            recommendations.append("Group numeric data by categorical variables to identify patterns.")

        # Missing data recommendations
        total_cells = dataset.row_count * len(dataset.columns)
        missing_count = 0
        for row in dataset.data:
            for col in dataset.columns:
                if col not in row or row[col] is None:
                    missing_count += 1

        if missing_count > 0:
            missing_percent = (missing_count / total_cells) * 100
            recommendations.append(f"Dataset has {missing_percent:.1f}% missing values. Consider imputation strategies.")

        if not recommendations:
            recommendations.append("Data appears to be in good shape. Proceed with exploratory analysis.")

        return recommendations

    def generate_mock_chart_data(self, config: VisualizationConfig, dataset: Dataset, data_types: Dict[str, DataType]) -> Dict[str, Any]:
        """
        Generate mock chart data structure (since we can't create actual charts without visualization libraries).
        """
        # This simulates what chart data would look like for each chart type
        chart_data = {
            'title': config.title,
            'chart_type': config.chart_type.value,
            'data': [],
            'labels': [],
            'colors': self.color_schemes.get(config.color_scheme, self.color_schemes['default']),
            'metadata': {
                'width': config.width,
                'height': config.height,
                'generated_at': datetime.now().isoformat()
            }
        }

        # Generate sample data points based on chart type
        if config.chart_type == ChartType.BAR:
            # Sample bar chart data
            categorical_cols = [col for col, dt in data_types.items() if dt == DataType.CATEGORICAL][:5]  # Limit to 5
            numeric_cols = [col for col, dt in data_types.items() if dt == DataType.NUMERIC][:1]  # Use first numeric

            if categorical_cols and numeric_cols:
                # Sample data for categories
                cat_col = categorical_cols[0]
                num_col = numeric_cols[0]

                # Count occurrences or aggregate numeric values by category
                cat_counts = {}
                for row in dataset.data:
                    cat_val = row.get(cat_col)
                    num_val = row.get(num_col)
                    if cat_val is not None and num_val is not None and isinstance(num_val, (int, float)):
                        if cat_val in cat_counts:
                            cat_counts[cat_val] += num_val
                        else:
                            cat_counts[cat_val] = num_val

                chart_data['labels'] = list(cat_counts.keys())[:5]  # Limit to 5
                chart_data['data'] = list(cat_counts.values())[:5]

        elif config.chart_type == ChartType.LINE:
            # Sample line chart data
            date_cols = [col for col, dt in data_types.items() if dt == DataType.DATE][:1]
            numeric_cols = [col for col, dt in data_types.items() if dt == DataType.NUMERIC][:1]

            if date_cols and numeric_cols:
                date_col = date_cols[0]
                num_col = numeric_cols[0]

                # Create time series data
                date_num_pairs = []
                for row in dataset.data:
                    date_val = row.get(date_col)
                    num_val = row.get(num_col)
                    if date_val is not None and num_val is not None and isinstance(num_val, (int, float)):
                        date_num_pairs.append((str(date_val), num_val))

                # Sort by date and limit
                date_num_pairs.sort(key=lambda x: x[0])
                date_num_pairs = date_num_pairs[:20]  # Limit to 20 points

                if date_num_pairs:
                    chart_data['labels'] = [pair[0] for pair in date_num_pairs]
                    chart_data['data'] = [pair[1] for pair in date_num_pairs]

        elif config.chart_type == ChartType.PIE:
            # Sample pie chart data
            categorical_cols = [col for col, dt in data_types.items() if dt == DataType.CATEGORICAL][:1]

            if categorical_cols:
                cat_col = categorical_cols[0]

                # Count occurrences of each category
                cat_counts = {}
                for row in dataset.data:
                    cat_val = row.get(cat_col)
                    if cat_val is not None:
                        cat_counts[cat_val] = cat_counts.get(cat_val, 0) + 1

                chart_data['labels'] = list(cat_counts.keys())[:5]  # Limit to 5
                chart_data['data'] = list(cat_counts.values())[:5]

        elif config.chart_type == ChartType.SCATTER:
            # Sample scatter plot data
            numeric_cols = [col for col, dt in data_types.items() if dt == DataType.NUMERIC][:2]  # Need 2 numeric cols

            if len(numeric_cols) >= 2:
                x_col = numeric_cols[0]
                y_col = numeric_cols[1]

                points = []
                for row in dataset.data:
                    x_val = row.get(x_col)
                    y_val = row.get(y_col)
                    if x_val is not None and y_val is not None and isinstance(x_val, (int, float)) and isinstance(y_val, (int, float)):
                        points.append({'x': x_val, 'y': y_val})

                chart_data['data'] = points[:50]  # Limit to 50 points

        elif config.chart_type == ChartType.HISTOGRAM:
            # Sample histogram data
            numeric_cols = [col for col, dt in data_types.items() if dt == DataType.NUMERIC][:1]

            if numeric_cols:
                num_col = numeric_cols[0]

                # Collect numeric values
                values = []
                for row in dataset.data:
                    num_val = row.get(num_col)
                    if num_val is not None and isinstance(num_val, (int, float)):
                        values.append(num_val)

                if values:
                    # Create bins for histogram
                    if len(values) > 1:
                        min_val = min(values)
                        max_val = max(values)
                        range_val = max_val - min_val
                        bin_size = range_val / 10 if range_val > 0 else 1

                        bins = [0] * 10
                        for val in values:
                            bin_idx = min(int((val - min_val) / bin_size), 9)
                            bins[bin_idx] += 1

                        chart_data['labels'] = [f"{min_val + i*bin_size:.1f}-{min_val + (i+1)*bin_size:.1f}" for i in range(10)]
                        chart_data['data'] = bins

        return chart_data

    def create_visualization(self, data: List[Dict[str, Any]], config: VisualizationConfig) -> VisualizationResult:
        """
        Create a visualization based on the configuration and data.
        """
        # Analyze the dataset
        dataset = self.analyze_dataset(data)
        data_types = self.detect_data_types(dataset)

        # Calculate statistics and identify outliers
        stats = self.calculate_basic_stats(dataset, data_types)
        outliers = self.identify_outliers(dataset, data_types)

        # Generate insights and recommendations
        insights = self.generate_insights(dataset, data_types, stats, outliers)
        recommendations = self.generate_recommendations(dataset, data_types)

        # Generate mock chart data
        mock_chart_data = self.generate_mock_chart_data(config, dataset, data_types)

        return VisualizationResult(
            title=config.title,
            chart_type=config.chart_type.value,
            description=f"Visualization of {dataset.name} dataset showing {config.chart_type.value} chart for {config.title.lower()}",
            insights=insights,
            recommendations=recommendations,
            mock_chart_data=mock_chart_data
        )

    def create_dashboard(self, data: List[Dict[str, Any]]) -> List[VisualizationResult]:
        """
        Create a comprehensive dashboard with multiple visualizations.
        """
        # Analyze the dataset
        dataset = self.analyze_dataset(data)
        data_types = self.detect_data_types(dataset)

        # Get visualization suggestions
        viz_configs = self.suggest_visualizations(dataset, data_types)

        # Create visualizations
        dashboard = []
        for config in viz_configs:
            viz_result = self.create_visualization(data, config)
            dashboard.append(viz_result)

        return dashboard

def create_data_visualizer_skill():
    """Factory function to create the data visualizer skill."""
    return DataVisualizer()

# Example usage
if __name__ == "__main__":
    # Sample dataset
    sample_data = [
        {"date": "2024-01-01", "sales": 1200, "region": "North", "product": "A"},
        {"date": "2024-01-02", "sales": 1500, "region": "South", "product": "B"},
        {"date": "2024-01-03", "sales": 900, "region": "North", "product": "A"},
        {"date": "2024-01-04", "sales": 2100, "region": "East", "product": "C"},
        {"date": "2024-01-05", "sales": 1800, "region": "West", "product": "A"},
        {"date": "2024-01-06", "sales": 1600, "region": "North", "product": "B"},
        {"date": "2024-01-07", "sales": 1400, "region": "South", "product": "C"},
    ]

    visualizer = create_data_visualizer_skill()

    # Create a specific visualization
    config = VisualizationConfig(
        title="Sales Trend Over Time",
        chart_type=ChartType.LINE,
        color_scheme="vibrant"
    )

    result = visualizer.create_visualization(sample_data, config)
    print(f"Title: {result.title}")
    print(f"Chart Type: {result.chart_type}")
    print(f"Description: {result.description}")
    print(f"Insights: {result.insights}")
    print(f"Recommendations: {result.recommendations}")
    print(f"Mock Chart Data Keys: {list(result.mock_chart_data.keys())}")

    print("\n" + "="*50 + "\n")

    # Create a dashboard
    dashboard = visualizer.create_dashboard(sample_data)
    print(f"Dashboard contains {len(dashboard)} visualizations:")
    for i, viz in enumerate(dashboard, 1):
        print(f"{i}. {viz.title} ({viz.chart_type})")
        print(f"   Insights: {len(viz.insights)} points")
        print(f"   Recommendations: {len(viz.recommendations)} points")