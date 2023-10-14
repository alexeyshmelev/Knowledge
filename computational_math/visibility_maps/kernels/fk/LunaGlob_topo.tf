KPL/FK
 
   FILE: kernels/fk/LunaGlob_topo.tf
 
   This file was created by PINPOINT.
 
   PINPOINT Version 3.3.0 --- December 13, 2021
   PINPOINT RUN DATE/TIME:    2022-04-26T19:17:11
   PINPOINT DEFINITIONS FILE: LunaGlob_site.def
   PINPOINT PCK FILE:         kernels/pck/pck00010.tpc
   PINPOINT SPK FILE:         kernels/spk/LunaGlob_site.bsp
 
   The input definitions file is appended to this
   file as a comment block.
 
 
   Body-name mapping follows:
 
\begindata
 
   NAIF_BODY_NAME                      += 'LG_SITE1'
   NAIF_BODY_CODE                      += -201
 
   NAIF_BODY_NAME                      += 'LG_SITE2'
   NAIF_BODY_CODE                      += -202
 
\begintext
 
 
   Reference frame specifications follow:
 
 
   Topocentric frame LG_SITE1_TOPO
 
      The Z axis of this frame points toward the zenith.
      The X axis of this frame points North.
 
      Topocentric frame LG_SITE1_TOPO is centered at the
      site LG_SITE1, which has Cartesian coordinates
 
         X (km):                  0.4401059009297E+03
         Y (km):                  0.4182877109832E+03
         Z (km):                 -0.1627851635379E+04
 
      and planetodetic coordinates
 
         Longitude (deg):        43.5440000000000
         Latitude  (deg):       -69.5450000000000
         Altitude   (km):         0.0000000000000E+00
 
      These planetodetic coordinates are expressed relative to
      a reference spheroid having the dimensions
 
         Equatorial radius (km):  1.7374000000000E+03
         Polar radius      (km):  1.7374000000000E+03
 
      All of the above coordinates are relative to the frame IAU_MOON.
 
 
\begindata
 
   FRAME_LG_SITE1_TOPO                 =  -201001
   FRAME_-201001_NAME                  =  'LG_SITE1_TOPO'
   FRAME_-201001_CLASS                 =  4
   FRAME_-201001_CLASS_ID              =  -201001
   FRAME_-201001_CENTER                =  -201
 
   OBJECT_-201_FRAME                   =  'LG_SITE1_TOPO'
 
   TKFRAME_-201001_RELATIVE            =  'IAU_MOON'
   TKFRAME_-201001_SPEC                =  'ANGLES'
   TKFRAME_-201001_UNITS               =  'DEGREES'
   TKFRAME_-201001_AXES                =  ( 3, 2, 3 )
   TKFRAME_-201001_ANGLES              =  (  -43.5440000000000,
                                            -159.5450000000000,
                                             180.0000000000000 )
 
 
\begintext
 
   Topocentric frame LG_SITE2_TOPO
 
      The Z axis of this frame points toward the zenith.
      The X axis of this frame points North.
 
      Topocentric frame LG_SITE2_TOPO is centered at the
      site LG_SITE2, which has Cartesian coordinates
 
         X (km):                  0.5874922791521E+03
         Y (km):                  0.2279912084221E+03
         Z (km):                 -0.1619083565113E+04
 
      and planetodetic coordinates
 
         Longitude (deg):        21.2100000000000
         Latitude  (deg):       -68.7330000000000
         Altitude   (km):         0.0000000000000E+00
 
      These planetodetic coordinates are expressed relative to
      a reference spheroid having the dimensions
 
         Equatorial radius (km):  1.7374000000000E+03
         Polar radius      (km):  1.7374000000000E+03
 
      All of the above coordinates are relative to the frame IAU_MOON.
 
 
\begindata
 
   FRAME_LG_SITE2_TOPO                 =  -202001
   FRAME_-202001_NAME                  =  'LG_SITE2_TOPO'
   FRAME_-202001_CLASS                 =  4
   FRAME_-202001_CLASS_ID              =  -202001
   FRAME_-202001_CENTER                =  -202
 
   OBJECT_-202_FRAME                   =  'LG_SITE2_TOPO'
 
   TKFRAME_-202001_RELATIVE            =  'IAU_MOON'
   TKFRAME_-202001_SPEC                =  'ANGLES'
   TKFRAME_-202001_UNITS               =  'DEGREES'
   TKFRAME_-202001_AXES                =  ( 3, 2, 3 )
   TKFRAME_-202001_ANGLES              =  (  -21.2100000000000,
                                            -158.7330000000000,
                                             180.0000000000000 )
 
\begintext
 
 
Definitions file LunaGlob_site.def
--------------------------------------------------------------------------------
 
Site 1, Moon, Solar System
Lat: -69.545 deg,  Lon: 43.544 deg
 
Site 2, Moon, Solar System
Lat: -68.733 deg,  Lon: 21.210 deg
 
Created by Stanislav Bober, IKI
 
begindata
 
SITES = ('LG_SITE1', 'LG_SITE2')
 
LG_SITE1_TOPO_FRAME = 'LG_SITE1_TOPO'
LG_SITE1_TOPO_ID    = -201001
LG_SITE1_FRAME      = 'IAU_MOON'
LG_SITE1_IDCODE     = -201
LG_SITE1_LATLON     = ( -69.545, 43.544, 0.0 )
LG_SITE1_CENTER     = 301
LG_SITE1_BOUNDS     = ( @2020-01-01T00:00:00.0, @2040-01-01T00:00:00.0 )
LG_SITE1_UP         =  'Z'
LG_SITE1_NORTH      =  'X'
 
LG_SITE2_TOPO_FRAME = 'LG_SITE2_TOPO'
LG_SITE2_TOPO_ID    = -202001
LG_SITE2_FRAME      = 'IAU_MOON'
LG_SITE2_IDCODE     = -202
LG_SITE2_LATLON     = ( -68.733, 21.210, 0.0 )
LG_SITE2_CENTER     = 301
LG_SITE2_BOUNDS     = ( @2020-01-01T00:00:00.0, @2040-01-01T00:00:00.0 )
LG_SITE2_UP         =  'Z'
LG_SITE2_NORTH      =  'X'
 
begintext
 
[End of definitions file]
 
