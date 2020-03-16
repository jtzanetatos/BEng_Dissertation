#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 13:14:01 2020

@author: iason
"""


import cv2 as cv
import numpy as np
from scipy.stats import mode
from skimage.measure import label
import wx
# TODO: Implement GTK+3 module; implement OS check; implement cupy for efficiency.
# Implement NumPy's array iteration.

def get_path(wildcard):
    '''
    

    Parameters
    ----------
    wildcard : TYPE
        DESCRIPTION.

    Returns
    -------
    path : TYPE
        DESCRIPTION.

    '''
    
    
    app = wx.App(None)
    style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
    dialog = wx.FileDialog(None, 'Open', wildcard=wildcard, style=style)
    if dialog.ShowModal() == wx.ID_OK:
        path = dialog.GetPath()
    else:
        path = None
    dialog.Destroy()
    return path

def imBackSup(fr_bw, bg_bw, threshold):
    '''
    

    Parameters
    ----------
    fr_bw : TYPE
        DESCRIPTION.
    bg_bw : TYPE
        DESCRIPTION.
    threshold : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    '''
    
    # Evaluate in/out frames dimensions
    height, width = bg_bw.shape
    
    # Evaluate abs difference between background model & current frame
    fr_diff = np.abs((np.uint32(fr_bw) - np.uint32(bg_bw)))
    
    # Allocate output frame
    fg = np.zeros((height, width), dtype=np.uint8)
    
    # Loop through input frame's elements & implement threshold filtering
    # (High pass theshold filtering)
    # TODO: implement NumPy approach on array iteration
    fg = np.where(fr_diff > threshold, np.uint8(fr_bw), np.uint8(0))
    # for i in range(width):
    #     for k in range(height):
    #         # Current element belongs in foreground
    #         if (fr_diff[i, k] > threshold):
    #             fg[i, k] = fr_bw[i, k]
    #         # Element belongs in background
    #         else:
    #             fg[i, k] = np.uint8(0)
    # Set current frame as background model for next iteration
    bg_bw = fr_bw
    
    # Return foreground & background models
    return (np.array((fg, bg_bw)))

def contour(fg, ns1, nsNN):
    '''
    

    Parameters
    ----------
    fg : TYPE
        DESCRIPTION.
    ns1 : TYPE
        DESCRIPTION.

    Returns
    -------
    fgc : TYPE
        DESCRIPTION.

    '''
    
    # Apply median filtering on foregound frame
    fg = cv.medianBlur(fg, ksize=nsNN)
    
    # Create disk structuring element
    st = cv.getStructuringElement(cv.MORPH_ELLIPSE, ksize=(ns1, ns1))
    
    # Apply morphological closing on frame; MATLAB's 'fill' operation omitted.
    fgc = cv.morphologyEx(fg, cv.MORPH_CLOSE, kernel=st, iterations=1)
    
    # Return captured contour
    return fgc

# def imlabel(fgc, conncomp, minsizeofCC):
    
    
#     # Counter for num of objects in scene
#     objCounter = 0
    
    

# def imcluster(num, fgc):
#     #TODO: Further develop function.
    
    
#     # Mean value
#     meanvar = np.mean(allAeras)
    
#     # Most frequent value
#     freqvar = mode(allAeras)
    
#     # Evaluate distance from mean value
#     distance = (allAeras - meanvar) / (num - 1)
    
#     # Loop through each cluster
#     for i in range(num):
#         thisCentroid = 
#         # Current cluster greater than frequent area value
#         if distance[i] > freqvar:
#             clusterTemp[i] = thisCentroid
            

def main():
    
    
    # Select video file; at the time, .avi & .mp4 files supported.
    #TODO: implement appropriate wildcard argument
    vid_file = get_path('*.avi')
    
    # Create video reader object
    vidObj = cv.VideoCapture(vid_file)
    
    # Read first frame as background
    ret, bg = vidObj.read()
    
    # Convert background to greyscale
    bg_bw = cv.cvtColor(bg, cv.COLOR_BGR2GRAY)
    
    # Background pixel value threshold
    thresh = 25
    
    # Structure disk radius
    ns1 = 15
    
    # Kernel size/neighborhood windows for median filter
    nsNN = 7
    
    # Initialize RGB output frame
    fgcRGB = np.zeros_like(bg, dtype=np.uint8)
    
    # Frame counter
    cntr = 0
    
    while ret:
        # Read current frame
        ret, fr = vidObj.read()
        
        # Break at end of video stream
        if ret == False:
            break
        
        # Convert current frame to greyscale
        fr_bw = cv.cvtColor(fr, cv.COLOR_BGR2GRAY)
        
        # Background subtraction
        fg, bg_bw = imBackSup(fr_bw, bg_bw, threshold=thresh)
        
        # Contour extraction
        fgc = contour(fg, ns1, nsNN)
        
        # Object labeling
        # imlabel(fgc, conncomp, minsizeofCC)
        
        # Shadow removal & crowd analysis function
        # cluster = imcluster()
        
        # Convert Grayscale frame to RGB
        fgcRGB[:, :, 0] = np.uint8(fgc) * np.uint8(fr[:, :, 0])
        fgcRGB[:, :, 1] = np.uint8(fgc) * np.uint8(fr[:, :, 1])
        fgcRGB[:, :, 2] = np.uint8(fgc) * np.uint8(fr[:, :, 2])
        
        # Increment counter
        cntr += 1
        
        # Show current frame
        cv.imshow('Frame', fgcRGB)
        
    # Release capture & close all windows
    vidObj.release()
    cv.destroyAllWindows()

if __name__ == '__main__':
    main()