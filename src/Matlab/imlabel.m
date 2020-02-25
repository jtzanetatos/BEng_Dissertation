function [ CC, centroids, objCounter, num ] = imlabel( fgc, conncomp, minsizeofCC )
%% Identify connected components / label the objects
%   -------------------------------------------------------------------   %
%   The function utilizes the blwabel command to identify any number of
%   objects that have an 8-pixel connection. Afterwards if the vertical
%   length of the object is lower that the threshold, the functions sets
%   said object's coordinates to 0, in order to remove it since it isn't a
%   useful object for this implementation. Finally, it calculates the
%   centroid for each squared-object in order to display a label to number the
%   object

objCounter = 0; % counter for num of objects in scene
[CC,num] = bwlabel(fgc,conncomp); 
for i = 1:num
    [r, c] = find(CC==i);
    szr = length(r);
    if szr > minsizeofCC
            objCounter = objCounter + 1;
            CC = gather(CC); % Copy the array back to MATLAB workspace.
            %Uncomment if the system's GPU is supported
            CC(r,c)= objCounter;
    else %if  szr < thresh
            CC = gather(CC); % Uncomment if the system's GPU is supported
            CC(r,c)= 0;
    end
end
s = regionprops(CC,'centroid');
centroids = cat(1, s.Centroid);

end