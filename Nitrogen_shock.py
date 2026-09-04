# =============================================================================
# Shock-induced energy transfer across a gas-liquid interface
# Mach 7 nitrogen shock generation
#
# LAMMPS input script used to generate the developed Mach 7 nitrogen shock
# prior to coupling with the equilibrated gas-liquid interface.
#
# Atom types:
#   1 = CH3 united-atom site (n-dodecane; retained for force-field consistency)
#   2 = CH2 united-atom site (n-dodecane; retained for force-field consistency)
#   3 = N site (two-site N2 model)
#
# Notes:
#   - units real
#   - timestep uses the LAMMPS default for real units unless otherwise specified
#     in the data/restart workflow
#   - x and y remain periodic
#   - z is converted from periodic to non-periodic after reading the data file
#   - shock is generated using a moving piston at zlo
#   - a stationary reflecting wall is imposed at the far z boundary
#   - long-range LJ tail corrections are disabled
#   - unlike LJ interactions are generated using arithmetic mixing
#
# Required input data file:
#   equilibrium_gas_nitrogen_30x.data
# =============================================================================

clear

# -----------------------------------------------------------------------------
# Initial simulation settings
# The data file is first read with periodic boundaries, after which the
# shock-normal z direction is changed to non-periodic.
# -----------------------------------------------------------------------------
units       real
dimension   3
boundary    p p p
atom_style  full

package omp 1
suffix omp

neighbor     2.0 bin
neigh_modify every 1 delay 0 check yes

# -----------------------------------------------------------------------------
# Interatomic potential
# -----------------------------------------------------------------------------
pair_style   lj/cut/omp 14.0
pair_modify  mix arithmetic tail no

bond_style      harmonic/omp
angle_style     harmonic/omp
dihedral_style  opls/omp

# Exclude 1-2, 1-3 and 1-4 intramolecular LJ interactions
special_bonds lj 0.0 0.0 0.0

# -----------------------------------------------------------------------------
# Initial configuration
# -----------------------------------------------------------------------------
read_data equilibrium_gas_nitrogen_30x.data

# -----------------------------------------------------------------------------
# Force-field coefficients
# -----------------------------------------------------------------------------

# Lennard-Jones parameters: epsilon [kcal/mol], sigma [Angstrom]
pair_coeff 1 1 0.194726 3.75
pair_coeff 2 2 0.091402 3.95
pair_coeff 3 3 0.071744 3.31786

# Harmonic bonds: K [kcal/mol/Angstrom^2], r0 [Angstrom]
# LAMMPS convention: E = K (r-r0)^2
bond_coeff 1 315.0 1.54
bond_coeff 2 1651.0 1.10

# Harmonic angle: K [kcal/mol/rad^2], theta0 [degrees]
angle_coeff 1 62.1 114.0

# OPLS dihedral coefficients [kcal/mol]
dihedral_coeff 1 1.4109 -0.2710 3.1447 0.0

# -----------------------------------------------------------------------------
# Boundary conversion for piston-driven shock generation
# -----------------------------------------------------------------------------
change_box all boundary p p s

# Reset image flags after changing the shock-normal boundary condition
set group all image 0 0 0

# Use a larger neighbour-bin size for the elongated shock domain
neighbor     2.0 bin
neigh_modify binsize 100.0

# -----------------------------------------------------------------------------
# Dynamics and shock generation
# -----------------------------------------------------------------------------
fix integrate all nve

# Mach 7 piston condition
# 0.02030 Angstrom/fs = 2030 m/s
fix piston all wall/piston zlo pos 0.0 vel 0.02030 units box

# Stationary reflecting boundary at the far end of the gas domain
fix far all wall/reflect zhi 22200 units box

# Dynamic load balancing along the shock-normal direction
fix load_balance all balance 1000 1.05 shift z 20 1.05

# -----------------------------------------------------------------------------
# Streaming-corrected temperature and spatial profiles
# -----------------------------------------------------------------------------

# 20 Angstrom bins along z
compute bins all chunk/atom bin/1d z lower 20.0 units box

# Remove local z-directed streaming velocity before evaluating temperature
compute Trel all temp/profile 0 0 1 z 1225 out bin

# Number density, temperature and z-directed streaming velocity
fix profiles all ave/chunk 100 10 1000 bins \
    density/number temp vz bias Trel \
    file profiles_mach7.dat

thermo_modify temp Trel

# -----------------------------------------------------------------------------
# Thermodynamic output
# -----------------------------------------------------------------------------
thermo_style custom step time temp press etotal
thermo 1000

# -----------------------------------------------------------------------------
# Restart files
# Alternating restart files protect against loss of progress if the walltime
# limit is reached before the final data file is written.
# -----------------------------------------------------------------------------
restart 100000 shock_restart_1_mach7.restart shock_restart_2_mach7.restart

# -----------------------------------------------------------------------------
# Shock-development run
# -----------------------------------------------------------------------------
run 700000

# Final developed shock configuration
write_data shock_nitrogen_mach7.data

print "Mach 7 piston-driven nitrogen shock generation complete."
