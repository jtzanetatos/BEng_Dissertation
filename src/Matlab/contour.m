function fgc = contour(fg, ns1)

%% Function to capture the sillouete of an object using morphological operators
%   ------------------------------------------------------------------   %
%   
%   The following function is utilized to capture the sillouete of any
%   present objects. 
%   The function firstly, creates a morphological structuring element,
%   specifically, a disk where nsl is the radius of the disk. Afterwards it
%   converts the foreground image into a gpuArray element for improved
%   speed processing. Then it implements a 2-D median filter to remove any
%   noise from the image. A morphological operator is used to fill isolated
%   interior pixels. Finally, it utilizes the imclose morphological
%   operator, to morphologically close the image

st = strel('disk', ns1);
fg = gpuArray(fg); % Uncomment if the system's GPU is supported. Can be automated
fg = medfilt2(fg, [7, 7]);
fg = bwmorph(fg, 'fill');
fgc = imclose(fg, st);
end