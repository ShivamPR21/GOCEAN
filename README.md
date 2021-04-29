# GOCEAN

Ocean Current Components extraction and analysis pipeline, built on python3. The package provides comprehensive tools to
dig-inside the satellite altimetry and geoid based data analysis.

## Library Modules
1. I/O:
  - GeoidIO: Reads geoid data for geoid height above reference ellipsoid.
  - SSHIO: Reads sea surface height above the reference ellipsoid.
2. Preprocessing: The module implements filters for the system to remove or supress outliers.
3. Currents: This is where we work on the actual physics
  - MDT: Extracts out raw MDT from mean SSH and Geoid
  - Components: Extracts out current components for the ocean grid
4. Analysis: The module is yet to be implemented
  - Targets the working of clustering based analysis of the ocean systems.
  - PCA dimension changes for better analysis.


> To understand the comeplete working of the library please look at the tutorial notebook in test/notebooks/goceanIO.ipynb


### Examples
```For Usage related information please view the test/notebooks/goceanIO.ipynb```

Follow the following steps to get the things working.
```
mkdir gocean_ws && cd gocean_ws
git clone https://gitlab.com/ShivamPR21/gocean.gitlab
cd gocean
code .
```

Run the given .ipynb notebook in test folder

### package steup
```
mkdir gocean_ws && cd gocean_ws
git clone https://gitlab.com/ShivamPR21/gocean.git
cd gocean && python steup.py
```

After this append the path to this directory in your system path as a python-path.

### The pdf containing documentation is also included in Docs folder. 
