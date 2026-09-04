This repository contains selected LAMMPS input scripts used for the molecular dynamics simulations associated with the dissertation Shock-Induced Energy Transfer across a Gas--Liquid Interface.

The files currently provided correspond primarily to the 7 bar, Mach 7 case and are intended to document the simulation workflow and force-field implementation.

Included scripts

shock_generation_nitrogen_mach7.in
Generates and develops the Mach 7 nitrogen shock using a moving piston.

interface_equilibration_7bar.in
Equilibrates the initially constructed nitrogen--n-dodecane system at 7 bar and 300 K to allow a natural gas--liquid interface to develop before shock interaction.

shock_interface_7bar_mach7.in
Performs the final Mach 7 shock--interface interaction simulation after the developed nitrogen shock and equilibrated nitrogen--n-dodecane interface have been combined.

Important: configuration-specific values

These scripts are not intended to be used unchanged for a different simulation geometry or shock condition.

Several values depend directly on the specific molecular configuration and must be checked and modified before running a new case.

Boundary and wall positions

Commands containing explicit positions, for example

fix piston all wall/piston zlo pos 18218.8852137715 vel 0.02030 units box
fix far all wall/reflect zhi 22200 units box

are specific to the simulation box from which the original case was constructed.

For a new configuration, the following must be checked against the actual simulation-box dimensions:

piston starting position;

lower and upper z boundaries;

reflecting-wall position;

location of the gas--liquid interface;

amount of unshocked nitrogen retained ahead of the shock;

total length of the shock-normal domain.

Hard-coded boundary positions should therefore not be copied directly into another case without checking the corresponding LAMMPS data file.

Shock strength and piston velocity

The piston velocity must be selected for the required incident shock Mach number and initial thermodynamic state.

The Mach 7 scripts use

vel 0.02030

in LAMMPS real units, corresponding to approximately

0.02030 Angstrom/fs = 2030 m/s

This value is specific to the Mach 7 nitrogen case used in this work.

For another Mach number, temperature, gas model, or thermodynamic state, the required piston velocity must be recalculated before running the simulation. The present work determined piston velocity from the normal-shock relations using the heat-capacity ratio associated with the flexible two-site nitrogen model.

Do not assume that the Mach 7 piston velocity is transferable to another case.

Input data files

Each script expects a particular LAMMPS data file. These filenames may need to be changed to match the configuration being used.

For example:

read_data equilibrium_gas_nitrogen_30x.data

or

read_data dodecane_nitrogen_int_7bar_input.data

The data file contains the simulation-box dimensions, atom coordinates, molecule topology, masses, and other configuration-specific information.

Force field

The scripts use the force-field coefficients employed in the dissertation simulations:

united-atom TraPPE-based n-dodecane;

two-site nitrogen model;

flexible harmonic C--C and N--N bonds;

harmonic bond-angle potential;

OPLS torsional potential;

14 Angstrom Lennard--Jones cut-off;

Lorentz--Berthelot mixing through LAMMPS pair_modify mix arithmetic;

no analytical long-range Lennard--Jones tail correction.

The numerical coefficients in the supplied scripts correspond to the implementation used for this work and should only be altered if a different molecular model is intentionally being used.

Time step

All supplied production scripts use

timestep 1.0

which corresponds to 1 fs in LAMMPS real units.

This time step was selected to resolve the highest-frequency flexible bond vibration represented by the model.

Spatial binning and diagnostics

Profile bin widths, output frequencies, restart frequencies, run lengths, and load-balancing settings were selected for the original simulations.

Values such as

compute bins all chunk/atom bin/1d z lower 10.0 units box

or

compute bins all chunk/atom bin/1d z lower 20.0 units box

should be reviewed if the system dimensions, required spatial resolution, or analysis procedure are changed.

Likewise, run lengths such as

run 200000

or

run 700000

are case-specific and should not be interpreted as universal simulation durations.

Recommended workflow for adapting the scripts

Before using these inputs for another case:

Prepare and inspect the new LAMMPS data file.

Confirm the simulation-box dimensions and interface position.

Recalculate the required piston velocity for the desired shock Mach number.

Update all explicit piston and reflecting-wall positions.

Confirm that the shock has sufficient distance to develop before reaching the interface.

Check the spatial bin width and temp/profile settings.

Adjust run duration and restart frequency as required.

Confirm that output filenames do not overwrite results from another case.

Visualise the initial configuration before starting a long production run.

Scope

The scripts are provided primarily for reproducibility and documentation of the methodology used in the dissertation. They should be treated as reference inputs for the 7 bar Mach 7 workflow rather than universal LAMMPS templates.

Other pressure and Mach-number cases require corresponding changes to the simulation geometry, gas population, piston velocity, shock-development distance, and potentially the duration of the simulation.

Author

Klaudia Izabela Lysakowska
University of Cambridge
2026
