KPL/FK
 
   FILE: C:\Users\stasb\YandexDisk\py\spice\SRG_GMAT\kernels/fk/earthstns_iau_earth.tf
 
   This file was created by PINPOINT.
 
   PINPOINT Version 3.2.0 --- September 6, 2016
   PINPOINT RUN DATE/TIME:    2019-02-25T15:00:14
   PINPOINT DEFINITIONS FILE: C:\Users\stasb\YandexDisk\py\spice\SRG_GMAT/defs/earthstns_iau_earth.defs
   PINPOINT PCK FILE:         C:\Users\stasb\YandexDisk\py\spice\SRG_GMAT\kernels/pck/pck00010.tpc
   PINPOINT SPK FILE:         C:\Users\stasb\YandexDisk\py\spice\SRG_GMAT\kernels/spk/earthstns_iau_earth.bsp
 
   The input definitions file is appended to this
   file as a comment block.
 
 
   Body-name mapping follows:
 
\begindata
 
   NAIF_BODY_NAME                      += 'YEVPATORIA'
   NAIF_BODY_CODE                      += 399600
 
   NAIF_BODY_NAME                      += 'USSURIYSK'
   NAIF_BODY_CODE                      += 399601
 
   NAIF_BODY_NAME                      += 'BEAR'
   NAIF_BODY_CODE                      += 399602
 
   NAIF_BODY_NAME                      += 'MALARGUE'
   NAIF_BODY_CODE                      += 399603
 
   NAIF_BODY_NAME                      += 'KALYAZIN'
   NAIF_BODY_CODE                      += 399604
 
\begintext
 
 
   Reference frame specifications follow:
 
 
   Topocentric frame YEVPATORIA_TOPO
 
      The Z axis of this frame points toward the zenith.
      The X axis of this frame points North.
 
      Topocentric frame YEVPATORIA_TOPO is centered at the
      site YEVPATORIA, which has Cartesian coordinates
 
         X (km):                  0.3757865059000E+04
         Y (km):                  0.2457894032000E+04
         Z (km):                  0.4520032776000E+04
 
      and planetodetic coordinates
 
         Longitude (deg):        33.1873588568742
         Latitude  (deg):        45.3813633029733
         Altitude   (km):         0.3955223775108E+01
 
      These planetodetic coordinates are expressed relative to
      a reference spheroid having the dimensions
 
         Equatorial radius (km):  6.3781366000000E+03
         Polar radius      (km):  6.3567519000000E+03
 
      All of the above coordinates are relative to the frame IAU_EARTH.
 
 
\begindata
 
   FRAME_YEVPATORIA_TOPO               =  1399600
   FRAME_1399600_NAME                  =  'YEVPATORIA_TOPO'
   FRAME_1399600_CLASS                 =  4
   FRAME_1399600_CLASS_ID              =  1399600
   FRAME_1399600_CENTER                =  399600
 
   OBJECT_399600_FRAME                 =  'YEVPATORIA_TOPO'
 
   TKFRAME_1399600_RELATIVE            =  'IAU_EARTH'
   TKFRAME_1399600_SPEC                =  'ANGLES'
   TKFRAME_1399600_UNITS               =  'DEGREES'
   TKFRAME_1399600_AXES                =  ( 3, 2, 3 )
   TKFRAME_1399600_ANGLES              =  (  -33.1873588568742,
                                             -44.6186366970267,
                                             180.0000000000000 )
 
 
\begintext
 
   Topocentric frame USSURIYSK_TOPO
 
      The Z axis of this frame points toward the zenith.
      The X axis of this frame points North.
 
      Topocentric frame USSURIYSK_TOPO is centered at the
      site USSURIYSK, which has Cartesian coordinates
 
         X (km):                 -0.3051412535000E+04
         Y (km):                  0.3417979615000E+04
         Z (km):                  0.4427164562000E+04
 
      and planetodetic coordinates
 
         Longitude (deg):       131.7569885256476
         Latitude  (deg):        44.2083086153931
         Altitude   (km):         0.3517473912299E+01
 
      These planetodetic coordinates are expressed relative to
      a reference spheroid having the dimensions
 
         Equatorial radius (km):  6.3781366000000E+03
         Polar radius      (km):  6.3567519000000E+03
 
      All of the above coordinates are relative to the frame IAU_EARTH.
 
 
\begindata
 
   FRAME_USSURIYSK_TOPO                =  1399601
   FRAME_1399601_NAME                  =  'USSURIYSK_TOPO'
   FRAME_1399601_CLASS                 =  4
   FRAME_1399601_CLASS_ID              =  1399601
   FRAME_1399601_CENTER                =  399601
 
   OBJECT_399601_FRAME                 =  'USSURIYSK_TOPO'
 
   TKFRAME_1399601_RELATIVE            =  'IAU_EARTH'
   TKFRAME_1399601_SPEC                =  'ANGLES'
   TKFRAME_1399601_UNITS               =  'DEGREES'
   TKFRAME_1399601_AXES                =  ( 3, 2, 3 )
   TKFRAME_1399601_ANGLES              =  ( -131.7569885256476,
                                             -45.7916913846070,
                                             180.0000000000000 )
 
 
\begintext
 
   Topocentric frame BEAR_TOPO
 
      The Z axis of this frame points toward the zenith.
      The X axis of this frame points North.
 
      Topocentric frame BEAR_TOPO is centered at the
      site BEAR, which has Cartesian coordinates
 
         X (km):                  0.2828465915700E+04
         Y (km):                  0.2205999848800E+04
         Z (km):                  0.5256212922700E+04
 
      and planetodetic coordinates
 
         Longitude (deg):        37.9516670001940
         Latitude  (deg):        55.8680559997635
         Altitude   (km):         0.6979588279524E-07
 
      These planetodetic coordinates are expressed relative to
      a reference spheroid having the dimensions
 
         Equatorial radius (km):  6.3781366000000E+03
         Polar radius      (km):  6.3567519000000E+03
 
      All of the above coordinates are relative to the frame IAU_EARTH.
 
 
\begindata
 
   FRAME_BEAR_TOPO                     =  1399602
   FRAME_1399602_NAME                  =  'BEAR_TOPO'
   FRAME_1399602_CLASS                 =  4
   FRAME_1399602_CLASS_ID              =  1399602
   FRAME_1399602_CENTER                =  399602
 
   OBJECT_399602_FRAME                 =  'BEAR_TOPO'
 
   TKFRAME_1399602_RELATIVE            =  'IAU_EARTH'
   TKFRAME_1399602_SPEC                =  'ANGLES'
   TKFRAME_1399602_UNITS               =  'DEGREES'
   TKFRAME_1399602_AXES                =  ( 3, 2, 3 )
   TKFRAME_1399602_ANGLES              =  (  -37.9516670001940,
                                             -34.1319440002365,
                                             180.0000000000000 )
 
 
\begintext
 
   Topocentric frame MALARGUE_TOPO
 
      The Z axis of this frame points toward the zenith.
      The X axis of this frame points North.
 
      Topocentric frame MALARGUE_TOPO is centered at the
      site MALARGUE, which has Cartesian coordinates
 
         X (km):                  0.1823351396600E+04
         Y (km):                 -0.4850433681500E+04
         Z (km):                 -0.3708961487400E+04
 
      and planetodetic coordinates
 
         Longitude (deg):       -69.3980000002700
         Latitude  (deg):       -35.7760000002355
         Altitude   (km):         0.1550000035074E+01
 
      These planetodetic coordinates are expressed relative to
      a reference spheroid having the dimensions
 
         Equatorial radius (km):  6.3781366000000E+03
         Polar radius      (km):  6.3567519000000E+03
 
      All of the above coordinates are relative to the frame IAU_EARTH.
 
 
\begindata
 
   FRAME_MALARGUE_TOPO                 =  1399603
   FRAME_1399603_NAME                  =  'MALARGUE_TOPO'
   FRAME_1399603_CLASS                 =  4
   FRAME_1399603_CLASS_ID              =  1399603
   FRAME_1399603_CENTER                =  399603
 
   OBJECT_399603_FRAME                 =  'MALARGUE_TOPO'
 
   TKFRAME_1399603_RELATIVE            =  'IAU_EARTH'
   TKFRAME_1399603_SPEC                =  'ANGLES'
   TKFRAME_1399603_UNITS               =  'DEGREES'
   TKFRAME_1399603_AXES                =  ( 3, 2, 3 )
   TKFRAME_1399603_ANGLES              =  ( -290.6019999997300,
                                            -125.7760000002355,
                                             180.0000000000000 )
 
 
\begintext
 
   Topocentric frame KALYAZIN_TOPO
 
      The Z axis of this frame points toward the zenith.
      The X axis of this frame points North.
 
      Topocentric frame KALYAZIN_TOPO is centered at the
      site KALYAZIN, which has Cartesian coordinates
 
         X (km):                  0.2731190445000E+04
         Y (km):                  0.2126198279000E+04
         Z (km):                  0.5339535645000E+04
 
      and planetodetic coordinates
 
         Longitude (deg):        37.9003203804960
         Latitude  (deg):        57.2230164260905
         Altitude   (km):         0.1784892792229E+00
 
      These planetodetic coordinates are expressed relative to
      a reference spheroid having the dimensions
 
         Equatorial radius (km):  6.3781366000000E+03
         Polar radius      (km):  6.3567519000000E+03
 
      All of the above coordinates are relative to the frame IAU_EARTH.
 
 
\begindata
 
   FRAME_KALYAZIN_TOPO                 =  1399604
   FRAME_1399604_NAME                  =  'KALYAZIN_TOPO'
   FRAME_1399604_CLASS                 =  4
   FRAME_1399604_CLASS_ID              =  1399604
   FRAME_1399604_CENTER                =  399604
 
   OBJECT_399604_FRAME                 =  'KALYAZIN_TOPO'
 
   TKFRAME_1399604_RELATIVE            =  'IAU_EARTH'
   TKFRAME_1399604_SPEC                =  'ANGLES'
   TKFRAME_1399604_UNITS               =  'DEGREES'
   TKFRAME_1399604_AXES                =  ( 3, 2, 3 )
   TKFRAME_1399604_ANGLES              =  (  -37.9003203804960,
                                             -32.7769835739095,
                                             180.0000000000000 )
 
\begintext
 
 
Definitions file C:\Users\stasb\YandexDisk\py\spice\SRG_GMAT/defs/earthstns_iau_earth.defs
--------------------------------------------------------------------------------
 
begintext
 
   SPK for DSN Station Locations for ExoMars project
   =====================================================================
   Creation date:                        2015 August   14 18:00
   Created by:                           Anton Ledkov  (IKI)
 
 
   Position data
   -------------
 
   Station locations in the IAU_EARTH frame at the specified epoch are:
 
   Antenna   Diameter     x (km)            y (km)          z (km)
 
 
   399600      70m      3757865.059373    2457894.032181    4520032.776132
   399601      70m     -3051412.535231    3417979.615289    4427164.562618
   399602      67       2828.4659157      2205.9998488      5256.2129227
   399603      35       1823.3513966     -4850.4336815     -3708.9614874
   399603      64       2731190.445       2126198.279       5339535.645
 
 
   399600 - the YEVPATORIA RT-70 radio telescope at the Center for Deep
            Space Communications, YEVPATORIA, Crimea, Ukraine
 
   399601 - the Galenki RT-70 radio telescope at the USSURIYSK Astrophysical
            Observatory, Galenki (USSURIYSK), Russia
 
   399602  - "Bear Lakes", Russia
 
   399603  - The Malargue station, Deep Space Antenna 3
 
   399604  - Kalyazin Radio Astronomy Observation
            (http://www.asc.rssi.ru/Kalyazin/russian/rt.html)
 
 
   Input Data
 
begindata
 
   SITES               = (
                           'YEVPATORIA',
                           'USSURIYSK',
                           'BEAR',
                           'MALARGUE',
                           'KALYAZIN'
                                         )
 
 
   YEVPATORIA_CENTER   = 399
   YEVPATORIA_FRAME    = 'IAU_EARTH'
   YEVPATORIA_IDCODE   = 399600
   YEVPATORIA_XYZ      = ( +3757.865059,
                           +2457.894032,
                           +4520.032776  )
   YEVPATORIA_UP       = 'Z'
   YEVPATORIA_NORTH    = 'X'
 
 
 
   USSURIYSK_CENTER    = 399
   USSURIYSK_FRAME     = 'IAU_EARTH'
   USSURIYSK_IDCODE    = 399601
   USSURIYSK_XYZ       = ( -3051.412535,
                           +3417.979615,
                           +4427.164562  )
   USSURIYSK_UP        = 'Z'
   USSURIYSK_NORTH     = 'X'
 
 
 
   BEAR_CENTER          = 399
   BEAR_FRAME           = 'IAU_EARTH'
   BEAR_IDCODE          = 399602
   BEAR_XYZ             = ( 2828.4659157,
                            2205.9998488,
                            5256.2129227)
   BEAR_UP              = 'Z'
   BEAR_NORTH           = 'X'
 
 
 
   MALARGUE_CENTER      = 399
   MALARGUE_FRAME       = 'IAU_EARTH'
   MALARGUE_IDCODE      = 399603
   MALARGUE_XYZ         = (1823.3513966,
                          -4850.4336815,
                          -3708.9614874 )
   MALARGUE_UP          = 'Z'
   MALARGUE_NORTH       = 'X'
 
 
   KALYAZIN_CENTER      = 399
   KALYAZIN_FRAME       = 'IAU_EARTH'
   KALYAZIN_IDCODE      = 399604
   KALYAZIN_XYZ         = (2731.190445,
                           2126.198279,
                           5339.535645 )
   KALYAZIN_UP          = 'Z'
   KALYAZIN_NORTH       = 'X'
 
begintext
 
begintext
 
[End of definitions file]
 
