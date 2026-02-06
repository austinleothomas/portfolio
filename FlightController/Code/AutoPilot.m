function [StopTime,y,t,StopIndex] = AutoPilot(Gains,Beta)
% -------------------------------------------------------------------------
% Autopilot model (originally from UF EAS 4710 Spring '25) modified for use
% as an objective function for optimization purposes. The design variables
% here are the seven gain values passed as inputs, and the objective
% function value is the time required for the simulated aircraft to pass
% through two waypoints. The waypoints, state-space dynamics, and problem
% parameters are identical to those from the original problem.
% -------------------------------------------------------------------------


% -------------------------------------------------------------------------
% We suppress warnings.
% -------------------------------------------------------------------------
warning('off','all')
% -------------------------------------------------------------------------


% -------------------------------------------------------------------------
% We unpack the gains.
% -------------------------------------------------------------------------
Kd = Gains(1);
Kh = Gains(2);
Kk = Gains(3);
Kq = Gains(4);
Kt = Gains(5);
Kp = Gains(6);
Kr = Gains(7);
% -------------------------------------------------------------------------


% -------------------------------------------------------------------------
% We define all constant values.
% -------------------------------------------------------------------------
% We define the waypoints and a counter as global variables and then set
% these values.
global waypoint;	% counter 
global y1;		    % waypoint 1
global y2;		    % waypoint 2
global y3;		    % waypoint 3
waypoint = 1;
y1 = [5000;400;1000];
y2 = [-1000;10000;300];
y3 = [100;-10000;2000];

% We set trim conditions.
V = 500;		% velocity at trim
H = 0;			% altitude at trim

% We define longitudinal dynamics with states of u, alpha, theta, q, h, x.
Along = [-0.0507         20.6655      -9.8100     -0.7028     0 0 ;
         -0.6683         -5.0225       0           1          0 0 ;
            0             0            0           1          0 0 ;
          0.0404         -0.01123      0          -0.13443    0 0 ;
            0            -14.5308    -15.9850      0          0 0 ;
            1              0           0.6979      0          0 0];
Blong = [0;0;0;-.019781;0;0];
Clong = [0 0 0 0 0 1;0 0 0 0 1 0;1 0 0 0 0 0;
	0 57 0 0 0 0;0 0 57 0 0 0;0 0 0 57 0 0];
Dlong = zeros(6,1);

% We define lateral-directional dynamics with states of beta, phi, psi, p,
% r, y.
Alatd = [-0.2008       0.2807       0         0.7823      -0.4131     0;
          0            0            0         1            1          0;
          0            0            0         0            1.0863     0;
         -9.8100       0            0        -6.1404       1          0;
          0.0935       0            0        -0.2186      -0.2807     0;
          1           -0.0016      15.9848    0            0          0];
Blatd = [.00012049 .00032897;0 0;0 0;-.1031578 .020987;-.002133 -.010715;0 0];
Clatd = [0 0 0 0 0 1;57 0 0 0 0 0;0 0 57 0 0 0;
	0 57 0 0 0 0;0 0 0 57 0 0;0 0 0 0 57 0];
Dlatd = zeros(6,2);

% We define longitudinal actuator
Aele = -10;
Bele = 10 * Beta;
Cele = -1;
Dele = 0;

% We define lateral-directional actuators
Aact = [-20.2 0;0 -20.1];
Bact = [20.2 0;0 20.2] * Beta;
Cact = [-1 0;0 -1];
Dact = [0 0;0 0];
% -------------------------------------------------------------------------


% -------------------------------------------------------------------------
% We define the controller.
% -------------------------------------------------------------------------
% We define a low-pass filter on altitude command
[Aalt,Balt,Calt,Dalt] = tf2ss([1 .3],[3 7.2]);

% We define a washout filter on yaw rate.
Atau = -1;
Btau = 1;
Ctau = -1;
Dtau = 1;
% -------------------------------------------------------------------------


% -------------------------------------------------------------------------
% We add variables to the base workspace.
% -------------------------------------------------------------------------
assignin('base','Aact',Aact);
assignin('base','Aele',Aele);
assignin('base','V',V);
assignin('base','Kq',Kq);
assignin('base','Kp',Kp);
assignin('base','Kk',Kk);
assignin('base','Kt',Kt);
assignin('base','Kh',Kh);
assignin('base','Kd',Kd);
assignin('base','Kr',Kr);
assignin('base','Alatd',Alatd);
assignin('base','Along',Along);
assignin('base','Atau',Atau);
assignin('base','Bact',Bact);
assignin('base','Bele',Bele);
assignin('base','Blatd',Blatd);
assignin('base','Blong',Blong);
assignin('base','Aalt',Aalt);
assignin('base','Btau',Btau);
assignin('base','Cact',Cact);
assignin('base','Cele',Cele);
assignin('base','Clatd',Clatd);
assignin('base','Clong',Clong);
assignin('base','Balt',Balt);
assignin('base','Ctau',Ctau);
assignin('base','Dact',Dact);
assignin('base','Dele',Dele);
assignin('base','Dlatd',Dlatd);
assignin('base','Dlong',Dlong);
assignin('base','Calt',Calt);
assignin('base','Dtau',Dtau);
assignin('base','Dalt',Dalt);
% -------------------------------------------------------------------------


% -------------------------------------------------------------------------
% We run the simulation and process results.
% -------------------------------------------------------------------------
% We run the simulation.
try
    [t,~,y] = sim('eas4710_waypoint_block',[0 100]);
catch
    StopTime = 100;
    y = NaN;
    StopIndex = NaN;
end

% We identify the objective function value.
AltCmd = y(:,10);
StopIndex = find(AltCmd(1:end-1) == 300 & AltCmd(2:end) == 2000) + 1;
if isempty(StopIndex)
    StopTime = t(end);
else
    StopTime = t(StopIndex);
% -------------------------------------------------------------------------


% -------------------------------------------------------------------------
% We un-suppress warnings.
% -------------------------------------------------------------------------
warning('on','all')
% -------------------------------------------------------------------------


% -------------------------------------------------------------------------
% We terminate the function.
% -------------------------------------------------------------------------
end
% -------------------------------------------------------------------------