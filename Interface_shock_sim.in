# =============================================================================
# Shock-induced energy transfer across a gas-liquid interface
# 7 bar, Mach 7 nitrogen shock impacting liquid n-dodecane
#
# LAMMPS input script used for the production shock-interface simulation.
#
# Atom types:
#   1 = CH3 united-atom site (n-dodecane)
#   2 = CH2 united-atom site (n-dodecane)
#   3 = N site (two-site N2 model)
#
# Notes:
#   - units real
#   - timestep = 1 fs
#   - x and y periodic; z non-periodic
#   - shock generated using a moving piston at zlo
#   - far z boundary is reflecting
#   - long-range LJ tail corrections are disabled
#   - unlike LJ interactions are generated using arithmetic mixing
#
# Required input data file:
#   Shock_system_7bar_mach_7_input.data
# =============================================================================

clear

# -----------------------------------------------------------------------------
# Simulation settings
# -----------------------------------------------------------------------------
units       real
dimension   3
boundary    p p s
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
# Masses, molecular topology, simulation box and initial coordinates are
# contained in the LAMMPS data file.
# -----------------------------------------------------------------------------
read_data Shock_system_7bar_mach_7_input.data

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
# LAMMPS convention: E = K (theta-theta0)^2
angle_coeff 1 62.1 114.0

# OPLS dihedral coefficients [kcal/mol]
dihedral_coeff 1 1.4109 -0.2710 3.1447 0.0

# -----------------------------------------------------------------------------
# Time integration and shock generation
# -----------------------------------------------------------------------------
timestep 1.0

fix integrate all nve

# Mach 7 piston condition
# 0.02030 Angstrom/fs = 2030 m/s
fix piston all wall/piston zlo pos 18218.8852137715 vel 0.02030 units box

# Reflecting far boundary
fix far all wall/reflect zhi EDGE units box

# -----------------------------------------------------------------------------
# Load balancing
# -----------------------------------------------------------------------------
balance 1.02 shift z 20 1.02
fix load_balance all balance 1000 1.05 shift z 20 1.02

# -----------------------------------------------------------------------------
# Groups
# -----------------------------------------------------------------------------
group nitrogen type 3
group dodecane type 1 2

# -----------------------------------------------------------------------------
# Spatial profiles
# 10 Angstrom bins along the shock-normal z direction
# -----------------------------------------------------------------------------
compute bins all chunk/atom bin/1d z lower 10.0 units box

# Standard kinetic temperature
compute Tstd all temp

# Temperature with local z-directed streaming velocity removed
compute Trel all temp/profile 0 0 1 z 1500 out bin

# Nitrogen number density, temperature and z velocity
fix profN nitrogen ave/chunk 100 10 1000 bins \
    density/number temp vz bias Trel \
    file nitrogen_number_density_7bar_mach7.dat

# Dodecane number density, temperature and z velocity
fix profD dodecane ave/chunk 100 10 1000 bins \
    density/number temp vz bias Trel \
    file dodecane_number_density_Trel_7bar_mach7.dat

# -----------------------------------------------------------------------------
# Per-atom stress tensor
# Output is binned in the same 10 Angstrom spatial bins.
# Note: stress/atom reports stress*volume; conversion to pressure is performed
# during post-processing.
# -----------------------------------------------------------------------------
compute stress all stress/atom NULL

fix profStress all ave/chunk 100 10 1000 bins \
    c_stress[1] c_stress[2] c_stress[3] \
    file stress_tensor_10A_7bar_mach7.dat

# -----------------------------------------------------------------------------
# Dodecane trajectory output
# -----------------------------------------------------------------------------
dump dodecaneAtoms dodecane custom 1000 \
    dodecane_atoms_pos_vel_7bar_mach7.lammpstrj \
    id mol type x y z vx vy vz

dump_modify dodecaneAtoms first no

# -----------------------------------------------------------------------------
# Per-atom dodecane energies
# -----------------------------------------------------------------------------
compute ke_atom all ke/atom
compute pe_atom all pe/atom

variable etot_atom atom c_pe_atom+c_ke_atom

dump energyDump dodecane custom 1000 \
    dodecane_atom_energies_7bar_mach7.dat \
    id mol type x y z c_pe_atom c_ke_atom v_etot_atom

dump_modify energyDump sort id

# -----------------------------------------------------------------------------
# Thermodynamic output
# -----------------------------------------------------------------------------
thermo_style custom step time c_Tstd c_Trel press pe ke etotal
thermo_modify temp Trel
thermo 1000

# -----------------------------------------------------------------------------
# Production run
# 200000 steps x 1 fs = 200 ps
# -----------------------------------------------------------------------------
run 200000
