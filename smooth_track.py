
# Inspired by the instructions from:
# https://scummos.blogspot.com/2012/11/blender-exporting-camera-tracking.html
# author: Sascha Schleef

import bpy

"""
exports a track to a csv file
"""
def export_track(track,name="tr"):
    fn = 'data/{2}_{0}_{1}.csv'.format(clip.name.split('.')[0], track.name,name)
    with open(fn, 'w') as f:
        frameno = 0
        while True:
            markerAtFrame = track.markers.find_frame(frameno)
            if not markerAtFrame:
                break
            frameno += 1
            coords = markerAtFrame.co.xy
            f.write('{0} {1}\n'.format(coords[0], coords[1]))
            
"""
imports a track from a csv file
"""        
def import_track_csv(filename, clip,track):
    pass
    #to be implemented

"""
adds two 2-tupels together 
"""
def addtup(x,y):
    return (x[0]+y[0],x[1]+y[1])

"""
sums up a list of 2-tuples
"""
def tuplistmean(window):
    summe=(0,0)
    for i in window:
        summe=(summe[0]+i[0],summe[1]+i[1])
    return (summe[0]/len(window),summe[1]/len(window))

"""
takes the mean M(i) of tracker positions a window around a frame i 
and calculates the shift relative to that mean: M(i)-i.
Using this as absolute input for a "Transform"-node on the basis of 
a motion tracking of a shaked but moving object results in an deshaked 
image.
windowsize: frames before and frames after current frame.
            with this a true mean or a predictive mean can be calculated
            to prevent tracke doject from leaving the picture.
"""
def interpol_track(track,windowsize=(20,20)):
    coordslist=[]
    meanlist=[]
    frameno = 0
    while True:
        markerAtFrame = track.markers.find_frame(frameno)
        if not markerAtFrame:
            break
        frameno += 1
        coordslist.append(markerAtFrame.co.xy)
    length=len(coordslist)
    for i in range(length):
        window=coordslist[max([0,i-windowsize[0]]):min([length-1,i+windowsize[1]])]
        mean=tuplistmean(window)
        meanlist.append((mean[0]-coordslist[i][0],mean[1]-coordslist[i][1]))
    return meanlist

"""
saves a stabilizing tracker sequence to a clip on the basis of
a tracked object path by calculating the mean movement
"""
def new_interpol_track(D,clip,track,new_name,windowsize=(20,20)):
    D.movieclips[clip].tracking.tracks.new(track+"_"+new_name,1)
    meanlist=interpol_track(D.movieclips[clip].tracking.tracks[track],windowsize=windowsize)
    print(meanlist)
    for i, coord in enumerate(meanlist):
        D.movieclips[clip].tracking.tracks[track+"_"+new_name].markers.insert_frame(i,coord)
        

D = bpy.data
new_interpol_track(D,"VSS_1663.MOV","Track","stabi")

