import dash
from dash import html
import dash_bootstrap_components as dbc

import pandas as pd
import numpy as np
import datetime as datetime


def sidebar(path_prefix=None, show_pages=None):

    """
    Create a sidebar with filtered navigation links
    Args:
        path_prefix (str): Only show pages with paths starting with this prefix
        show_pages (list): List of specific page paths to show
    """
    def filter_pages(page):
        if show_pages is not None:
            return page["path"] in show_pages
        if path_prefix is not None:
            return page["path"].startswith(path_prefix)
        return True  # Show all pages if no filters specified

    return html.Div(
        dbc.Nav(
            [
                dbc.NavLink(
                    [
                        html.Div(page["name"], className="ms-2"),
                    ],
                    href=page["path"],
                    active="exact",
                )
                for page in dash.page_registry.values()
                if filter_pages(page)
            ],
            vertical=True,
            pills=True,
            className="bg-light",
        )
    )

def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean a DataFrame by converting columns to appropriate data types,
    leaving missing values as NaN for later handling during calculations.
    
    Args:
        df (pd.DataFrame): Input DataFrame to clean
        
    Returns:
        pd.DataFrame: Cleaned DataFrame with appropriate data types
    """
    df = df.copy()  # Create a copy to avoid modifying original
    
    # Common date formats to try
    date_formats = [
        '%Y-%m-%d',           # 2023-12-31
        '%m/%d/%Y',           # 12/31/2023
        '%d/%m/%Y',           # 31/12/2023
        '%Y%m%d',             # 20231231
        '%B %d, %Y',          # December 31, 2023
        '%d-%b-%Y',           # 31-Dec-2023
    ]
    
    for column in df.columns:
        # Remove leading/trailing whitespace
        if df[column].dtype == 'object':
            df[column] = df[column].str.strip()
        
        # Try converting to numeric first
        try:
            # Check if column contains percentage values
            if df[column].dtype == 'object' and df[column].str.contains('%').any():
                df[column] = df[column].str.rstrip('%').astype('float') / 100.0
            else:
                df[column] = pd.to_numeric(df[column])
            continue  # Skip date conversion if numeric conversion succeeded
        except (ValueError, TypeError):
            pass

        # Try converting to datetime with specific formats
        if df[column].dtype == 'object':
            date_converted = False
            for date_format in date_formats:
                try:
                    df[column] = pd.to_datetime(df[column], format=date_format)
                    date_converted = True
                    break
                except (ValueError, TypeError):
                    continue
            
            # If no date format worked, keep as string
            if not date_converted:
                df[column] = df[column].astype(str)
    
    return df

