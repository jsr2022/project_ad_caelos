import numpy as np
from scipy.io import loadmat
import pandas as pd


def usaf1976model(file_name, path):
    """
    This function imports 1976 standard atmosphere tables from .dat files

    Args: 
    file_names (numpy array): string array (each index is a filename)
    path (string): path to file_names 

    Returns:
    pandas dataframe: data organized with table headers by altitude
    """
    pass

def nasaglobalreferencemodel(file_names, path):
    """
    This function imports the Global Reference Atmosphereic Models 
    including Thermospheres for Mars, Venus, and Earth.
    
    Args: 
    file_names (numpy array): string array (each index is a filename)
    path (string): path to file_names

    Returns:
    panda dataframe: data organized by planet with appropriate table headers 

    Example Use:
    FILL ME OUT

    Source(s):
     Hilary Justh, C. G. Justus and Vernon Keller. "Global Reference Atmospheric Models, 
     Including Thermospheres, for Mars, Venus and Earth," AIAA 2006-6394. AIAA/AAS 
     Astrodynamics Specialist Conference and Exhibit. August 2006. 
     Link: https://ntrs.nasa.gov/api/citations/20060048492/downloads/20060048492.pdf
    """
    pass

def main():
    # 
    pass


    

    

if __name__ == "__main__":
    main()