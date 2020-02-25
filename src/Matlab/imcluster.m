function [ cluster] = imcluster(num, fgc)
%%  Function to identify and eliminate clusters
%   --------------------------------------------------------------------  %
%   The function calculates the total area for every object in the current
%   frame. It calculates the average and frequent value for the allAreas
%   matrix. Afterwards it calculates the standard deviation. The function
%   then loops for every object present in the current frame, storing the
%   current object's area and comparing the distance of the current object
%   with the most frequent value. 

fgc = gather(fgc); % Uncomment if the system's GPU is supported
fgtemp = size(fgc); % Create dummy matrix to combine with fgc image
cluster = size(fgc); % Preallocate cluster to appease the MATLAB gods
getarea = regionprops(fgc,'Area'); % Get the area of all the objects in the frame

allAreas = [getarea.Area]; % Store all area values into an array

meanvar = mean(allAreas); % Find the average/mean value
freqvar = mode(allAreas,2); % Find the most frequent value 
medianvar = median(allAreas,2); % Find the median value

distance = (allAreas - meanvar) / (num-1); % Calculate the distance from the mean value

k = 0; % If loop counter, useful to know how many times the if loop was used
for a=1:num
    thisCentroid = [getarea(a).Area]; % Variable to select the current cluster
        if distance(a) > freqvar
            k = k +1;
            clusterTemp(a) = thisCentroid; % Variable to select the desirable clusters
            [sortedAreas, sortIndexes] = sort(clusterTemp, 'descend'); % Store and index the selected clusters
            for j = 1:k
                biggestCluster = ismember(fgc, sortIndexes(k)); 
            end
        end
end