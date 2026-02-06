## Set-Up

(I)     Clone Repo

    git clone https://github.com/austinleothomas/portfolio
    cd portfolio

(II)    Initiate Virtual Environment (Optional)

    python -m venv venv
    venv\Scripts\Activate

(III)   Install Packages

    pip install -r Assignment#/requirements.txt

(IV)    Execute Desired Script

    python Code\ProjMaster.py

## Folder Contents

\Code
    => AutoPilot.m                      autopilot model, represented as a MATLAB function; this calls
                                        on Simulink to simulate the aircraft dynamics for given control
                                        inputs, returning key simulation results

    => eas4710_waypoint_block.mdl       master Simulink model for autopilot simulation (.mdl); this
                                        was not authored by me

    => eas4710_waypoint_block.slxc      master Simulink model for autopilot simulation (.slxc); this
                                        was not authored by me

    => eas4710_waypoint_set.m           background MATLAB code to support Simulink model; this was not
                                        authored by me

    => eas4710_waypoint_xyz.m           background MATLAB code to support Simulink model; this was not
                                        authored by me

    => eas4710_waypoint_yaw.m           background MATLAB code to support Simulink model; this was not
                                        authored by me

    => Plotting.py                      script used to generate data plots for the report

    => ProjMaster.py                    script used to run all optimization processes for this project;
                                        this also contains the Gauss-Seidel coupled model representation

    => TrajectoryPlotter.m              script used to generate 3D trajectory plots; this is a MATLAB
                                        function which, when passed a gain vector, returns the trajectory
                                        plot for the aircraft dynamics under those gains
                                        
    => requirements.txt                 file containing packages needed to run Python scripts above;
                                        note that the MATLAB scripts require certain MATLAB toolboxes
                                        (namely Simulink and Control System Toolbox) ... if you have
                                        most basic controls toolboxes installed you should be okay

Thomas_FinalProject.pdf                 file containing the report for this project; I highly recommend
                                        skimming this first to understand the project scope before
                                        playing around with the code

## Note to User
Most of the above files you will want to leave alone. TrajectoryPlotter.m is probably the best one
to play around with: you can pass different gain vectors to the function and immediately get a visual
representation of how the dynamics change. If you want to tune gains, start with those presented in the
report and diverge from there: the vast majority of the design space will yield unstable results and thus
nonsense plots. If you are more interested in the optimization side of the project, feel free to play
around with ProjMaster.py. The script is written such that all user-tunable parameters (i.e. deciding
which algorithm or algorithm parameters you want to use) is all handled at the top of the script, so
you shouldn't need to modify any of the deep code unless you want to. The world is your oyster here.
Modify any of the eas4710_.....m files at your own peril -- those are courtesy of an old professor, and
at this point only he and God know how they work.

## Project Overview
This project takes an autopilot controller from an undergrad course and improves upon performance
by applying graduate-level numerical optimization techniques. The autopilot simulation consists of
three PID controllers (seven total gains) which controls a simulated aircraft (based on real OTS
drone dynamics) through a simulated flight space. The objective of the optimization problem was
to tune the seven gains (i.e. the gains were the design variables) to minimize the flight time of
the aircraft passing through two waypoints in the flight space (i.e. the obejctive function was
flight time). Several gradient-free optimization methods were applied to the problem. Then, a coupled
system was introduced whereby Gauss-Seidel iteration yielded a secondary control scaling parameter,
called beta, which scaled back the control input to the system while holding flight time roughly
constant. Passing this coupled system to a multidisciplinary solver allowed for optimization of the
objective function while implicitly considering the total control effort required to achieve the
optimal response.