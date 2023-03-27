import spectral as sp
import numpy as np

# path to the ENVI header file
hdr_file = r'C:\Users\edwar\OneDrive\VS-Code\GitHub Stuff\HyperGix2.0\images\Pic1.hdr'

# read the ENVI header file
hdr = sp.envi.read_envi_header(hdr_file)

# extract some metadata
num_bands = hdr['bands']
wavelengths = np.array([float(w) for w in hdr['wavelength']])
interleave = hdr['interleave']
rows, cols = hdr['lines'], hdr['samples']
datatype = hdr['data type']

# print the metadata
print(f'Number of bands: {num_bands}')
print(f'Wavelength range: {wavelengths[0]:.1f} - {wavelengths[-1]:.1f} nm')
print(f'Interleave: {interleave}')
print(f'Spatial dimensions: {rows} rows x {cols} columns')
print(f'Data type: {datatype}')
