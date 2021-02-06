# DTXtoPNG
![screenshot](https://i.imgur.com/TcsJ8Pc.png)

This python program converts [DTXMania](https://ko.osdn.net/projects/dtxmania/) simfiles to image files. (*.dtx → *.png)

## Requirements
* This code is tested with [Python 3.6.8](https://www.python.org/downloads/release/python-368/) and [Python Imaging Library: Pillow 8.1.0](https://pillow.readthedocs.io/)

## How to Run
1. Install all the requirements if needed
2. [Download](https://github.com/shian0346/DTXtoPNG/archive/main.zip) the code
3. put the simfiles under the `input` folder
    * you can delete the example input files included in the downloaded code
4. run `convert.py`
5. check the `output` folder for the converted images

## Notes
* This program is tested mostly with official charts. Customs charts and incorrectly written charts might not be correctly converted. Please refer to the DTX file format specifications below for the correct formatting of DTX simfiles.
* This program only takes ten channels as valid inputs:
```
 11 = HH (HiHatClose)
 12 = SD (Snare)
 13 = BD (BassDrum)
 14 = HT (HighTom)
 15 = LT (LowTom)
 16 = CY (Cymbal)
 17 = FT (FloorTom)
 1A = LC (LeftCymbal)
 1B = LP (BassDrum)
 1C = LP (HiHatPedal)
```
* These two channels are ignored:
```
 18 = HiHatOpen
 19 = RideCymbal
```
* Game speed is set to 4.0

## Useful Links

[GITADORA DrumMania Official Charts](https://approvedtx.blogspot.com/p/gitadora-drummania.html) by APPROVED DTX

[DTX file format specifications](https://osdn.net/projects/dtxmania/wiki/DTX%20data%20format)
