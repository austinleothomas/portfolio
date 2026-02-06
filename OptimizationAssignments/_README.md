## Set-Up

(I)     Clone Repo

    git clone https://github.com/austinleothomas/portfolio
    cd portfolio

(II)    Initiate Virtual Environment (Optional)

    python -m venv venv
    venv\Scripts\Activate

(III)   Install Packages

    pip install -r Assignment#/requirements.txt
    pip install -e .

(IV)    Execute Desired Script

    python Assignment#\prob#_#.py

## Folder Contents

\Assignment#
    =>  requirements.txt file containing necessary packages
    =>  .py files for each problem in the assignment
    =>  .pdf file containing the organized report
\Toolbox
    =>  .py files for custom modules used throughout (dependencies 
        handled by assignment requriements.txt files)

## File Contents

Assignment 1:   Exploration of graphical, analytic, and OTS optimization of basic
                functions. Includes a summary and analysis of a relevant research
                paper in the field of optimization.

Assignment 2:   A comprehensive exploration of self-written line search algorithms,
                including application of backtracking and strong Wolfe line
                search algorithms to trivial and nontrivial optimization problems.

Assignment 3:   A comprehensive exploration of basic unconstrained, gradient-based
                optimziation algorithms. Both conjugate gradient and steepest descent
                algorithms were employed, each tested with both backtracking and strong
                Wolfe linea search methods.

Assignment 4:   A comprehensive exploration of constrained, gradient-based optimization
                algorithms, including: interior / exterior penalty methods and an
                equality-constrained SQP algorithms. Analytic methods were also briefly
                explored.

Assignment 5:   A comprehensive exploration of numerical methods for gradient estimation,
                including such methods as: finite-differencing, complex-step methods, 
                direct / adjoint implitict analytic differentiation techniques, and
                algorithmic differentiation with operator overloading.

Assignment 6:   A comprehensive exploration of gradient-free optimization via a particle
                swarm algorithm. The performance of a self-written PSO algorithm was
                compared to that of a self-written CG algorithm when both were applied to
                a number of trivial and nontrivial (noisy, discontinuous) functions.