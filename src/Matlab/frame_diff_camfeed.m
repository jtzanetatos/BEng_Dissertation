% This m-file implements the frame difference algorithm for background
% subtraction.  It may be used free of charge for any purpose 

%clearvars -global
clear all
close all hidden

% Video file selection dialog box
[filename,pathname] = uigetfile({'*.avi';'*.mp4'},'Select the video file');

% Construct a multimedia reader object associated with avi files.
vidObj = VideoReader(fullfile(pathname, filename));

% read first frame as background
bg = readFrame(vidObj);

bg_bw = rgb2gray(bg);           % convert background to greyscale


%% dialogue box for setup variables

prompt = {'Video Feed Start Read Time (sec):',...
    'Results Visualization (no: 0 / yes: 1)',...
    'Output Video Filename:'
    };
dlg_title = 'Input';
num_lines = 1;
defaultans = {'0','1',filename '_out'};
answer = inputdlg(prompt,dlg_title,num_lines,defaultans);


%% ----------------------- set video viewer and frame size variables -----------------------
width = vidObj.Width;
height = vidObj.Height;
fg = zeros(height, width); % Create dummy variable to store foreground values
% if plot image is required for visualization
flag = str2num(answer{2});
if flag == 1
    fflag = figure;
    figure(fflag);
    set(fflag, 'Position', round( get(0, 'Screensize')));
end

% You can specify that reading should start at n seconds from the
% beginning using
starttime = str2num(answer{1});
vidObj.CurrentTime = starttime;


filename = answer{3};
framerate = vidObj.FrameRate;
if flag==1
        writerObj = VideoWriter([filename,'.avi']); 
        writerObj.FrameRate = framerate; 
        open(writerObj);
end
%% --------------------- get and process frames for n times-----------------
disp('processing initiated...') 
thresh = 25;    % threshold for pixel value to consider as background/foreground
ns1 = 15; % neighborhood for frame dilation (dilation not present, only usage in imclose)
nsNN = [7, 7]; % neighborhood window for median filter

counter = 0; % this is a counter / useful to know when using a while-loop
while hasFrame(vidObj)   
    fr = readFrame(vidObj);    % read current frame
    fr_bw = rgb2gray(fr);      % convert frame to grayscale
    
    [ fg, bg_bw ] = imBackSub( fr_bw , bg_bw, thresh ); % Background Subtraction function
    
    %fgc = contour(fg, ns1); % Contour extraction function
    
    %[ CC, centroids, objCounter, num] = imlabel( fgc, 8, 80 ); % Object labeling function
    
    %[cluster] = imcluster(CC, objCounter, fgc); % Shadow removal & crowd analysis function

    % plotting some results
    counter=counter+1; % increase counter
    % interactively plot if needed
    if flag == 1
        figure(fflag)
    	drawnow % ensure figure window is updated
        %subplot(1,2,1);imshow(fr); 
        %title(['Original Frame #',num2str(counter)]);
        %make the colour image clusteres visible
        %fgc = gather(fgc); % Gather the fgc variable back into the MATLAB workspace
%         fgcRGB(:,:,1) = (uint8(fgc).*uint8(fr(:,:,1)));
%         fgcRGB(:,:,2) = (uint8(fgc).*uint8(fr(:,:,2)));
%         fgcRGB(:,:,3) = (uint8(fgc).*uint8(fr(:,:,3)));
        % make visible estimated labelled objects
         subplot(1,1,1); 
         imshow(fg);
        hold on
%         if objCounter~=0
%             plot(centroids(:,1),centroids(:,2), '+', 'MarkerSize', 10);
%             for i=1:objCounter
%                 strObj = ['#',num2str(i)];
%                 text(centroids(i,1),centroids(i,2), strObj,... 
%                 'HorizontalAlignment','center',...
%                 'FontWeight','bold','FontSize',10,...
%                 'Color','red')
%             end
%         end
        hold off
%         title(['Foreground Labelled Clusters #',num2str(objCounter)]);
        frame = getframe(gcf); % 'gcf' can handle if you zoom in to take a movie.
        writeVideo(writerObj, frame);
    end
end

disp('Background subtraction, foreground labelling: DONE...')
close(writerObj);  %stop(vidObj);
