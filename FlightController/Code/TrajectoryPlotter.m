function TrajectoryPlotter(Gains,isSave,FileName)
% -------------------------------------------------------------------------
% Function to run simulation and generate a trajectory plot.
% -------------------------------------------------------------------------


% -------------------------------------------------------------------------
% We define the waypoint coordinates.
% -------------------------------------------------------------------------
y1 = [5000;400;1000];
y2 = [-1000;10000;300];
% -------------------------------------------------------------------------


% -------------------------------------------------------------------------
% We call on the simulation function to generate trajectory data.
% -------------------------------------------------------------------------
[~,y,~,StopIndex] = AutoPilot(Gains,1);
% -------------------------------------------------------------------------


% -------------------------------------------------------------------------
% We define plotting values.
% -------------------------------------------------------------------------
FontSize = 11;
FontType = 'Cambria';

% -------------------------------------------------------------------------
% We generate the trajectory plot and save if needed.
% -------------------------------------------------------------------------
figure(1)
plot3(y(1:StopIndex,2),y(1:StopIndex,1),y(1:StopIndex,11),'k', ...
    y1(2),y1(1),y1(3),'ro', ...
    y2(2),y2(1),y2(3),'ro');
ax = gca;
ax.FontName = FontType;
ax.FontSize = FontSize;
zlabel('Altitude [m]','FontSize',FontSize,'FontName',FontType);
ylabel('Eastward Position [m]','FontSize',FontSize,'FontName',FontType);
xlabel('Northward Position [m]','FontSize',FontSize,'FontName',FontType);

if isSave
    saveas(gcf,FileName)
end
% -------------------------------------------------------------------------