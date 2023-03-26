import spectral as sp
hdr = sp.envi.open("file_name_whatever.hdr")
wvl = hdr.bands.centers
rows, cols, bands = hdr.nrows, hdr.ncols, hdr.nbands
meta = hdr.metadata