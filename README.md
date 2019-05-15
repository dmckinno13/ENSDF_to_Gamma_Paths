# ENSDF_to_Gamma_Paths
File to read in ENSDF file for beta-decay and break it into a file for each gamma path possible.

Main use is the 'run' function. Inputs are <path to file>, which nuclei it is (ex: 97Rb), what the daughter is (ex: 97Sr), and the error allowance for finding the next level by subtracting a gamma from the current level. In general, an error allowance of 1.0 has worked, but occasionally 2.0 is needed.
