function [ fg, bg_bw ] = imBackSub( fr_bw , bg_bw , threshold )
%% Function to subtract background from foreground 
%   -------------------------------------------------------------------- %
%   Function that subtracts the background from the foreground
%   The function calculates the absolute difference between the foreground
%   and the background, background being the first frame which can be
%   calibrated, and foreground being the next frame. Afterwards the two for
%   loops are utilized to scan top to bottom vertically the frame and
%   compare the values of each coordinate with the threshold. If the
%   values are lower than the threshold, the function sets said coordinates
%   to zero.
[height, width] = size(bg_bw);

fr_diff = abs(double(fr_bw) - double(bg_bw));  % cast operands as double to avoid negative overflow

thresh = threshold;
for j=1:width   
        for k=1:height
            if ((fr_diff(k,j) > thresh))% if fr_diff > thresh, then pixel in foreground
                fg(k,j) = fr_bw(k,j);
            else
                fg(k,j) = 0;
            end
        end
end
    
bg_bw = fr_bw;

end 