#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 13:14:01 2020

@author: iason
"""


import cv2 as cv
import numpy as np
import wx
# TODO: Implement GTK+3 module; implement OS check; implement cupy for efficiency.
# Implement NumPy's array iteration

def get_path(wildcard):
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
    height, width = bg_bw.shape()
    
    # Evaluate abs difference between background model & current frame
    fr_diff = np.abs((np.uint32(fr_bw) - np.uint32(bg_bw)))
    
    # Allocate output frame
    fg = np.zeros((height, width), dtype=np.uint8)
    
    # Loop through input frame's elements & implement threshold filtering
    # (High pass theshold filtering)
    # TODO: implement NumPy approach on array iteration
    for i in range(width):
        for k in range(height):
            # Current element belongs in foreground
            if (fr_diff[i, k] > threshold):
                fg[i, k] = fr_bw[i, k]
            # Element belongs in background
            else:
                fg[i, k] = np.uint8(0)
    # Set current frame as background model for next iteration
    bg_bw = fr_bw
    
    # Return foreground & background models
    return (np.array((fr_bw, bg_bw)))

def contour(fg, ns1):
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
    fg = cv.medianBlur(fg, ksize=7)
    
    # Create disk structuring element
    st = cv.getStructuringElement(cv.MORPH_ELLIPSE, ns1)
    
    # Apply morphological closing on frame; MATLAB's 'fill' operation omitted.
    fgc = cv.MorphologyEx(fg, cv.MORPH_CLOSE, element=st, iterations=1)
    
    # Return captured contour
    return fgc

def imlabel(fgc, conncomp, minsizeofCC):
    
    
    # Counter for num of objects in scene
    objCounter = 0
    
    

def imcluster(num, fgc):
    
    
    

def main():
    
    
    # Select video file; at the time, .avi & .mp4 files supported.
    #TODO: implement appropriate wildcard argument
    vid_file = get_path('*.avi', '*.mp4')
    
    # Create video reader object
    vidObj = cv.VideoCapture(vid_file)
    
    # Read first frame as background
    ret, bg = vidObj.read()
    
    # Convert background to greyscale
    bg_bw = cv.cvtColor(bg, cv.COLOR_BGR2GRAY)
    
    # Background pixel value threshold
    thresh = 25
    
    while ret:
        # Read current frame
        ret, fr = vidObj.read()
        
        # Convert current frame to greyscale
        fr_bw = cv.cvtColor(fr_bw, cv.COLOR_BGR2GRAY)
        
        # Background subtraction
        fg, bg_bw = imBackSup(fr_bw, bg_bw, threshold=thresh)
        
        # Contour extraction
        fgc = contour(fg, ns1)
        
        # Object labeling
        imlabel(fgc, conncomp, minsizeofCC)

if __name__ == '__main__':
    main()