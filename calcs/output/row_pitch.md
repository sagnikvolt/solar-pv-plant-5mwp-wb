# Row pitch calculation (output of calcs/row_pitch.py)

```
Window 10:00-14:00: pitch >= 6.08 m, GCR = 0.75
Window 09:00-15:00: pitch >= 6.43 m, GCR = 0.71
Table slope width 4.556 m, rise 1.558 m, footprint 4.281 m
  hour  9.0  elev  26.5  az  -46.5  pitch needed 6.43
  hour 10.0  elev  35.5  az  -34.3  pitch needed 6.08
  hour 11.0  elev  41.7  az  -18.6  pitch needed 5.94
  hour 12.0  elev  44.0  az    0.0  pitch needed 5.90
  hour 13.0  elev  41.7  az   18.6  pitch needed 5.94
  hour 14.0  elev  35.5  az   34.3  pitch needed 6.08
  hour 15.0  elev  26.5  az   46.5  pitch needed 6.43
```

Chosen pitch: **7.0 m** (GCR 65%). It is 0.6 m wider than the 6.4 m needed for no shading at 9:00 to 15:00 on the winter solstice, trading land for less shading and more rear-side gain on the bifacial modules. PVsyst linear near-shading loss at 7.0 m: 2.26%. A pitch sweep (6.4 / 8 / 9 m) is still to be run.
