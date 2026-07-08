# rel-f1 driver-dnf train first sampled sequence, seq_len=1024

Target: `driver-dnf:Train#0` / `did_not_finish of driver-dnf` / pos `1`

| pos | role | table | split | row | column | value | row_time | f2p |
|---:|---|---|---|---:|---|---|---|---|
| 0 | FEAT | driver-dnf | Train | 0 | date of driver-dnf | 2004-08-04 | 2004-08-04 | drivers:Db#20 |
| 1 | TARGET+COL+FEAT | driver-dnf | Train | 0 | did_not_finish of driver-dnf | [MASK:boolean] label=1 | 2004-08-04 | drivers:Db#20 |
| 2 | FEAT | drivers | Db | 20 | driverRef of drivers | fisichella |  |  |
| 3 | FEAT | drivers | Db | 20 | code of drivers | FIS |  |  |
| 4 | FEAT | drivers | Db | 20 | forename of drivers | Giancarlo |  |  |
| 5 | FEAT | drivers | Db | 20 | surname of drivers | Fisichella |  |  |
| 6 | FEAT | drivers | Db | 20 | dob of drivers | datetime_z=-0.83203 |  |  |
| 7 | FEAT | drivers | Db | 20 | nationality of drivers | Italian |  |  |
| 8 | DRIVER_NBR_INDIRECT | results | Db | 15909 | number of results | number_z=-0.38672 | 1997-09-21 | races:Db#610; drivers:Db#20; constructors:Db#16 |
| 9 | DRIVER_NBR_INDIRECT | results | Db | 15909 | grid of results | number_z=0.39258 | 1997-09-21 | races:Db#610; drivers:Db#20; constructors:Db#16 |
| 10 | DRIVER_NBR_INDIRECT | results | Db | 15909 | position of results | number_z=-0.82422 | 1997-09-21 | races:Db#610; drivers:Db#20; constructors:Db#16 |
| 11 | DRIVER_NBR_INDIRECT | results | Db | 15909 | positionOrder of results | number_z=-1.1484 | 1997-09-21 | races:Db#610; drivers:Db#20; constructors:Db#16 |
| 12 | DRIVER_NBR_INDIRECT | results | Db | 15909 | points of results | number_z=0.25977 | 1997-09-21 | races:Db#610; drivers:Db#20; constructors:Db#16 |
| 13 | DRIVER_NBR_INDIRECT | results | Db | 15909 | laps of results | number_z=0.83984 | 1997-09-21 | races:Db#610; drivers:Db#20; constructors:Db#16 |
| 14 | DRIVER_NBR_INDIRECT | results | Db | 15909 | milliseconds of results | number_z=-0.57031 | 1997-09-21 | races:Db#610; drivers:Db#20; constructors:Db#16 |
| 15 | DRIVER_NBR_INDIRECT | results | Db | 15909 | statusId of results | number_z=-0.62891 | 1997-09-21 | races:Db#610; drivers:Db#20; constructors:Db#16 |
| 16 | DRIVER_NBR_INDIRECT | results | Db | 15909 | date of results | 1997-09-21 | 1997-09-21 | races:Db#610; drivers:Db#20; constructors:Db#16 |
| 17 | FULL_ONLY | constructors | Db | 16 | constructorRef of constructors | jordan |  |  |
| 18 | FULL_ONLY | constructors | Db | 16 | name of constructors | Jordan |  |  |
| 19 | FULL_ONLY | constructors | Db | 16 | nationality of constructors | Irish |  |  |
| 20 | FULL_ONLY | races | Db | 610 | year of races | number_z=0.24512 | 1997-09-21 | circuits:Db#69 |
| 21 | FULL_ONLY | races | Db | 610 | round of races | number_z=1.0859 | 1997-09-21 | circuits:Db#69 |
| 22 | FULL_ONLY | races | Db | 610 | name of races | Austrian Grand Prix | 1997-09-21 | circuits:Db#69 |
| 23 | FULL_ONLY | races | Db | 610 | date of races | 1997-09-21 | 1997-09-21 | circuits:Db#69 |
| 24 | FULL_ONLY | races | Db | 610 | time of races | 00:00:00 | 1997-09-21 | circuits:Db#69 |
| 25 | FULL_ONLY | circuits | Db | 69 | circuitRef of circuits | red_bull_ring |  |  |
| 26 | FULL_ONLY | circuits | Db | 69 | name of circuits | Red Bull Ring |  |  |
| 27 | FULL_ONLY | circuits | Db | 69 | location of circuits | Spielberg |  |  |
| 28 | FULL_ONLY | circuits | Db | 69 | country of circuits | Austria |  |  |
| 29 | FULL_ONLY | circuits | Db | 69 | lat of circuits | number_z=0.60547 |  |  |
| 30 | FULL_ONLY | circuits | Db | 69 | lng of circuits | number_z=0.20898 |  |  |
| 31 | FULL_ONLY | circuits | Db | 69 | alt of circuits | number_z=1.1797 |  |  |
| 32 | DRIVER_NBR_INDIRECT | driver-dnf | Train | 10008 | date of driver-dnf | 1999-08-31 | 1999-08-31 | drivers:Db#20 |
| 33 | COL+DRIVER_NBR_INDIRECT | driver-dnf | Train | 10008 | did_not_finish of driver-dnf | 1 | 1999-08-31 | drivers:Db#20 |
| 34 | DRIVER_NBR_INDIRECT | qualifying | Db | 1493 | number of qualifying | number_z=-0.62109 | 2001-09-29 | races:Db#678; drivers:Db#20; constructors:Db#21 |
| 35 | DRIVER_NBR_INDIRECT | qualifying | Db | 1493 | position of qualifying | number_z=0.12012 | 2001-09-29 | races:Db#678; drivers:Db#20; constructors:Db#21 |
| 36 | DRIVER_NBR_INDIRECT | qualifying | Db | 1493 | date of qualifying | 2001-09-29 | 2001-09-29 | races:Db#678; drivers:Db#20; constructors:Db#21 |
| 37 | FULL_ONLY | constructors | Db | 21 | constructorRef of constructors | benetton |  |  |
| 38 | FULL_ONLY | constructors | Db | 21 | name of constructors | Benetton |  |  |
| 39 | FULL_ONLY | constructors | Db | 21 | nationality of constructors | Italian |  |  |
| 40 | FULL_ONLY | races | Db | 678 | year of races | number_z=0.44336 | 2001-09-30 | circuits:Db#18 |
| 41 | FULL_ONLY | races | Db | 678 | round of races | number_z=1.4766 | 2001-09-30 | circuits:Db#18 |
| 42 | FULL_ONLY | races | Db | 678 | name of races | United States Grand Prix | 2001-09-30 | circuits:Db#18 |
| 43 | FULL_ONLY | races | Db | 678 | date of races | 2001-09-30 | 2001-09-30 | circuits:Db#18 |
| 44 | FULL_ONLY | races | Db | 678 | time of races | 00:00:00 | 2001-09-30 | circuits:Db#18 |
| 45 | FULL_ONLY | circuits | Db | 18 | circuitRef of circuits | indianapolis |  |  |
| 46 | FULL_ONLY | circuits | Db | 18 | name of circuits | Indianapolis Motor Speedway |  |  |
| 47 | FULL_ONLY | circuits | Db | 18 | location of circuits | Indianapolis |  |  |
| 48 | FULL_ONLY | circuits | Db | 18 | country of circuits | USA |  |  |
| 49 | FULL_ONLY | circuits | Db | 18 | lat of circuits | number_z=0.2793 |  |  |
| 50 | FULL_ONLY | circuits | Db | 18 | lng of circuits | number_z=-1.3359 |  |  |
| 51 | FULL_ONLY | circuits | Db | 18 | alt of circuits | number_z=-0.068848 |  |  |
| 52 | DRIVER_NBR_INDIRECT | standings | Db | 24625 | points of standings | number_z=0.12695 | 2000-09-24 | races:Db#660; drivers:Db#20 |
| 53 | DRIVER_NBR_INDIRECT | standings | Db | 24625 | position of standings | number_z=-0.84766 | 2000-09-24 | races:Db#660; drivers:Db#20 |
| 54 | DRIVER_NBR_INDIRECT | standings | Db | 24625 | wins of standings | number_z=-0.27148 | 2000-09-24 | races:Db#660; drivers:Db#20 |
| 55 | DRIVER_NBR_INDIRECT | standings | Db | 24625 | date of standings | 2000-09-24 | 2000-09-24 | races:Db#660; drivers:Db#20 |
| 56 | FULL_ONLY | races | Db | 660 | year of races | number_z=0.39258 | 2000-09-24 | circuits:Db#18 |
| 57 | FULL_ONLY | races | Db | 660 | round of races | number_z=1.2812 | 2000-09-24 | circuits:Db#18 |
| 58 | FULL_ONLY | races | Db | 660 | name of races | United States Grand Prix | 2000-09-24 | circuits:Db#18 |
| 59 | FULL_ONLY | races | Db | 660 | date of races | 2000-09-24 | 2000-09-24 | circuits:Db#18 |
| 60 | FULL_ONLY | races | Db | 660 | time of races | 00:00:00 | 2000-09-24 | circuits:Db#18 |
| 61 | DRIVER_NBR_INDIRECT | driver-dnf | Train | 5796 | date of driver-dnf | 1996-06-17 | 1996-06-17 | drivers:Db#20 |
| 62 | COL+DRIVER_NBR_INDIRECT | driver-dnf | Train | 5796 | did_not_finish of driver-dnf | 1 | 1996-06-17 | drivers:Db#20 |
| 63 | DRIVER_NBR_INDIRECT | standings | Db | 24371 | points of standings | number_z=-0.1543 | 2000-04-23 | races:Db#649; drivers:Db#20 |
| 64 | DRIVER_NBR_INDIRECT | standings | Db | 24371 | position of standings | number_z=-0.84766 | 2000-04-23 | races:Db#649; drivers:Db#20 |
| 65 | DRIVER_NBR_INDIRECT | standings | Db | 24371 | wins of standings | number_z=-0.27148 | 2000-04-23 | races:Db#649; drivers:Db#20 |
| 66 | DRIVER_NBR_INDIRECT | standings | Db | 24371 | date of standings | 2000-04-23 | 2000-04-23 | races:Db#649; drivers:Db#20 |
| 67 | FULL_ONLY | races | Db | 649 | year of races | number_z=0.39258 | 2000-04-23 | circuits:Db#8 |
| 68 | FULL_ONLY | races | Db | 649 | round of races | number_z=-0.88281 | 2000-04-23 | circuits:Db#8 |
| 69 | FULL_ONLY | races | Db | 649 | name of races | British Grand Prix | 2000-04-23 | circuits:Db#8 |
| 70 | FULL_ONLY | races | Db | 649 | date of races | 2000-04-23 | 2000-04-23 | circuits:Db#8 |
| 71 | FULL_ONLY | races | Db | 649 | time of races | 00:00:00 | 2000-04-23 | circuits:Db#8 |
| 72 | FULL_ONLY | circuits | Db | 8 | circuitRef of circuits | silverstone |  |  |
| 73 | FULL_ONLY | circuits | Db | 8 | name of circuits | Silverstone Circuit |  |  |
| 74 | FULL_ONLY | circuits | Db | 8 | location of circuits | Silverstone |  |  |
| 75 | FULL_ONLY | circuits | Db | 8 | country of circuits | UK |  |  |
| 76 | FULL_ONLY | circuits | Db | 8 | lat of circuits | number_z=0.81641 |  |  |
| 77 | FULL_ONLY | circuits | Db | 8 | lng of circuits | number_z=-0.031982 |  |  |
| 78 | FULL_ONLY | circuits | Db | 8 | alt of circuits | number_z=-0.26172 |  |  |
| 79 | DRIVER_NBR_INDIRECT | results | Db | 16862 | number of results | number_z=-0.45117 | 2000-07-02 | races:Db#654; drivers:Db#20; constructors:Db#21 |
| 80 | DRIVER_NBR_INDIRECT | results | Db | 16862 | grid of results | number_z=0.39258 | 2000-07-02 | races:Db#654; drivers:Db#20; constructors:Db#21 |
| 81 | DRIVER_NBR_INDIRECT | results | Db | 16862 | position of results | number_z=0.21484 | 2000-07-02 | races:Db#654; drivers:Db#20; constructors:Db#21 |
| 82 | DRIVER_NBR_INDIRECT | results | Db | 16862 | positionOrder of results | number_z=-0.5 | 2000-07-02 | races:Db#654; drivers:Db#20; constructors:Db#21 |
| 83 | DRIVER_NBR_INDIRECT | results | Db | 16862 | points of results | number_z=-0.45117 | 2000-07-02 | races:Db#654; drivers:Db#20; constructors:Db#21 |
| 84 | DRIVER_NBR_INDIRECT | results | Db | 16862 | laps of results | number_z=0.83984 | 2000-07-02 | races:Db#654; drivers:Db#20; constructors:Db#21 |
| 85 | DRIVER_NBR_INDIRECT | results | Db | 16862 | statusId of results | number_z=-0.24805 | 2000-07-02 | races:Db#654; drivers:Db#20; constructors:Db#21 |
| 86 | DRIVER_NBR_INDIRECT | results | Db | 16862 | date of results | 2000-07-02 | 2000-07-02 | races:Db#654; drivers:Db#20; constructors:Db#21 |
| 87 | FULL_ONLY | races | Db | 654 | year of races | number_z=0.39258 | 2000-07-02 | circuits:Db#7 |
| 88 | FULL_ONLY | races | Db | 654 | round of races | number_z=0.099609 | 2000-07-02 | circuits:Db#7 |
| 89 | FULL_ONLY | races | Db | 654 | name of races | French Grand Prix | 2000-07-02 | circuits:Db#7 |
| 90 | FULL_ONLY | races | Db | 654 | date of races | 2000-07-02 | 2000-07-02 | circuits:Db#7 |
| 91 | FULL_ONLY | races | Db | 654 | time of races | 00:00:00 | 2000-07-02 | circuits:Db#7 |
| 92 | FULL_ONLY | circuits | Db | 7 | circuitRef of circuits | magny_cours |  |  |
| 93 | FULL_ONLY | circuits | Db | 7 | name of circuits | Circuit de Nevers Magny-Cours |  |  |
| 94 | FULL_ONLY | circuits | Db | 7 | location of circuits | Magny Cours |  |  |
| 95 | FULL_ONLY | circuits | Db | 7 | country of circuits | France |  |  |
| 96 | FULL_ONLY | circuits | Db | 7 | lat of circuits | number_z=0.58984 |  |  |
| 97 | FULL_ONLY | circuits | Db | 7 | lng of circuits | number_z=0.031738 |  |  |
| 98 | FULL_ONLY | circuits | Db | 7 | alt of circuits | number_z=-0.05542 |  |  |
| 99 | DRIVER_NBR_INDIRECT | driver-dnf | Train | 5742 | date of driver-dnf | 2000-03-28 | 2000-03-28 | drivers:Db#20 |
| 100 | COL+DRIVER_NBR_INDIRECT | driver-dnf | Train | 5742 | did_not_finish of driver-dnf | 1 | 2000-03-28 | drivers:Db#20 |
| 101 | DRIVER_NBR_INDIRECT | driver-dnf | Train | 3636 | date of driver-dnf | 1998-03-09 | 1998-03-09 | drivers:Db#20 |
| 102 | COL+DRIVER_NBR_INDIRECT | driver-dnf | Train | 3636 | did_not_finish of driver-dnf | 1 | 1998-03-09 | drivers:Db#20 |
| 103 | DRIVER_NBR_INDIRECT | driver-dnf | Train | 10723 | date of driver-dnf | 2002-08-15 | 2002-08-15 | drivers:Db#20 |
| 104 | COL+DRIVER_NBR_INDIRECT | driver-dnf | Train | 10723 | did_not_finish of driver-dnf | 1 | 2002-08-15 | drivers:Db#20 |
| 105 | DRIVER_NBR_INDIRECT | driver-dnf | Train | 1400 | date of driver-dnf | 2002-03-18 | 2002-03-18 | drivers:Db#20 |
| 106 | COL+DRIVER_NBR_INDIRECT | driver-dnf | Train | 1400 | did_not_finish of driver-dnf | 1 | 2002-03-18 | drivers:Db#20 |
| 107 | DRIVER_NBR_INDIRECT | results | Db | 17797 | number of results | number_z=-0.45117 | 2003-03-09 | races:Db#697; drivers:Db#20; constructors:Db#16 |
| 108 | DRIVER_NBR_INDIRECT | results | Db | 17797 | grid of results | number_z=0.25391 | 2003-03-09 | races:Db#697; drivers:Db#20; constructors:Db#16 |
| 109 | DRIVER_NBR_INDIRECT | results | Db | 17797 | positionOrder of results | number_z=-0.11084 | 2003-03-09 | races:Db#697; drivers:Db#20; constructors:Db#16 |
| 110 | DRIVER_NBR_INDIRECT | results | Db | 17797 | points of results | number_z=-0.45117 | 2003-03-09 | races:Db#697; drivers:Db#20; constructors:Db#16 |
| 111 | DRIVER_NBR_INDIRECT | results | Db | 17797 | laps of results | number_z=0.19922 | 2003-03-09 | races:Db#697; drivers:Db#20; constructors:Db#16 |
| 112 | DRIVER_NBR_INDIRECT | results | Db | 17797 | statusId of results | number_z=-0.43945 | 2003-03-09 | races:Db#697; drivers:Db#20; constructors:Db#16 |
| 113 | DRIVER_NBR_INDIRECT | results | Db | 17797 | date of results | 2003-03-09 | 2003-03-09 | races:Db#697; drivers:Db#20; constructors:Db#16 |
| 114 | FULL_ONLY | races | Db | 697 | year of races | number_z=0.53906 | 2003-03-09 | circuits:Db#0 |
| 115 | FULL_ONLY | races | Db | 697 | round of races | number_z=-1.4766 | 2003-03-09 | circuits:Db#0 |
| 116 | FULL_ONLY | races | Db | 697 | name of races | Australian Grand Prix | 2003-03-09 | circuits:Db#0 |
| 117 | FULL_ONLY | races | Db | 697 | date of races | 2003-03-09 | 2003-03-09 | circuits:Db#0 |
| 118 | FULL_ONLY | races | Db | 697 | time of races | 00:00:00 | 2003-03-09 | circuits:Db#0 |
| 119 | FULL_ONLY | circuits | Db | 0 | circuitRef of circuits | albert_park |  |  |
| 120 | FULL_ONLY | circuits | Db | 0 | name of circuits | Albert Park Grand Prix Circuit |  |  |
| 121 | FULL_ONLY | circuits | Db | 0 | location of circuits | Melbourne |  |  |
| 122 | FULL_ONLY | circuits | Db | 0 | country of circuits | Australia |  |  |
| 123 | FULL_ONLY | circuits | Db | 0 | lat of circuits | number_z=-3.125 |  |  |
| 124 | FULL_ONLY | circuits | Db | 0 | lng of circuits | number_z=2.2031 |  |  |
| 125 | FULL_ONLY | circuits | Db | 0 | alt of circuits | number_z=-0.65234 |  |  |
| 126 | DRIVER_NBR_INDIRECT | qualifying | Db | 2032 | number of qualifying | number_z=-0.39844 | 2004-06-19 | races:Db#721; drivers:Db#20; constructors:Db#14 |
| 127 | DRIVER_NBR_INDIRECT | qualifying | Db | 2032 | position of qualifying | number_z=0.4375 | 2004-06-19 | races:Db#721; drivers:Db#20; constructors:Db#14 |
| 128 | DRIVER_NBR_INDIRECT | qualifying | Db | 2032 | date of qualifying | 2004-06-19 | 2004-06-19 | races:Db#721; drivers:Db#20; constructors:Db#14 |
| 129 | FULL_ONLY | constructors | Db | 14 | constructorRef of constructors | sauber |  |  |
| 130 | FULL_ONLY | constructors | Db | 14 | name of constructors | Sauber |  |  |
| 131 | FULL_ONLY | constructors | Db | 14 | nationality of constructors | Swiss |  |  |
| 132 | FULL_ONLY | races | Db | 721 | year of races | number_z=0.58984 | 2004-06-20 | circuits:Db#18 |
| 133 | FULL_ONLY | races | Db | 721 | round of races | number_z=0.099609 | 2004-06-20 | circuits:Db#18 |
| 134 | FULL_ONLY | races | Db | 721 | name of races | United States Grand Prix | 2004-06-20 | circuits:Db#18 |
| 135 | FULL_ONLY | races | Db | 721 | date of races | 2004-06-20 | 2004-06-20 | circuits:Db#18 |
| 136 | FULL_ONLY | races | Db | 721 | time of races | 00:00:00 | 2004-06-20 | circuits:Db#18 |
| 137 | DRIVER_NBR_INDIRECT | standings | Db | 24800 | points of standings | number_z=-0.35156 | 2001-05-27 | races:Db#669; drivers:Db#20 |
| 138 | DRIVER_NBR_INDIRECT | standings | Db | 24800 | position of standings | number_z=-0.2373 | 2001-05-27 | races:Db#669; drivers:Db#20 |
| 139 | DRIVER_NBR_INDIRECT | standings | Db | 24800 | wins of standings | number_z=-0.27148 | 2001-05-27 | races:Db#669; drivers:Db#20 |
| 140 | DRIVER_NBR_INDIRECT | standings | Db | 24800 | date of standings | 2001-05-27 | 2001-05-27 | races:Db#669; drivers:Db#20 |
| 141 | FULL_ONLY | races | Db | 669 | year of races | number_z=0.44336 | 2001-05-27 | circuits:Db#5 |
| 142 | FULL_ONLY | races | Db | 669 | round of races | number_z=-0.29492 | 2001-05-27 | circuits:Db#5 |
| 143 | FULL_ONLY | races | Db | 669 | name of races | Monaco Grand Prix | 2001-05-27 | circuits:Db#5 |
| 144 | FULL_ONLY | races | Db | 669 | date of races | 2001-05-27 | 2001-05-27 | circuits:Db#5 |
| 145 | FULL_ONLY | races | Db | 669 | time of races | 00:00:00 | 2001-05-27 | circuits:Db#5 |
| 146 | FULL_ONLY | circuits | Db | 5 | circuitRef of circuits | monaco |  |  |
| 147 | FULL_ONLY | circuits | Db | 5 | name of circuits | Circuit de Monaco |  |  |
| 148 | FULL_ONLY | circuits | Db | 5 | location of circuits | Monte-Carlo |  |  |
| 149 | FULL_ONLY | circuits | Db | 5 | country of circuits | Monaco |  |  |
| 150 | FULL_ONLY | circuits | Db | 5 | lat of circuits | number_z=0.45117 |  |  |
| 151 | FULL_ONLY | circuits | Db | 5 | lng of circuits | number_z=0.09668 |  |  |
| 152 | FULL_ONLY | circuits | Db | 5 | alt of circuits | number_z=-0.66016 |  |  |
| 153 | DRIVER_NBR_INDIRECT | results | Db | 18210 | number of results | number_z=-0.45117 | 2004-05-23 | races:Db#718; drivers:Db#20; constructors:Db#14 |
| 154 | DRIVER_NBR_INDIRECT | results | Db | 18210 | grid of results | number_z=-0.16113 | 2004-05-23 | races:Db#718; drivers:Db#20; constructors:Db#14 |
| 155 | DRIVER_NBR_INDIRECT | results | Db | 18210 | positionOrder of results | number_z=0.79688 | 2004-05-23 | races:Db#718; drivers:Db#20; constructors:Db#14 |
| 156 | DRIVER_NBR_INDIRECT | results | Db | 18210 | points of results | number_z=-0.45117 | 2004-05-23 | races:Db#718; drivers:Db#20; constructors:Db#14 |
| 157 | DRIVER_NBR_INDIRECT | results | Db | 18210 | laps of results | number_z=-1.4844 | 2004-05-23 | races:Db#718; drivers:Db#20; constructors:Db#14 |
| 158 | DRIVER_NBR_INDIRECT | results | Db | 18210 | fastestLap of results | number_z=-2.4219 | 2004-05-23 | races:Db#718; drivers:Db#20; constructors:Db#14 |
| 159 | DRIVER_NBR_INDIRECT | results | Db | 18210 | rank of results | number_z=0.91016 | 2004-05-23 | races:Db#718; drivers:Db#20; constructors:Db#14 |
| 160 | DRIVER_NBR_INDIRECT | results | Db | 18210 | statusId of results | number_z=-0.51562 | 2004-05-23 | races:Db#718; drivers:Db#20; constructors:Db#14 |
| 161 | DRIVER_NBR_INDIRECT | results | Db | 18210 | date of results | 2004-05-23 | 2004-05-23 | races:Db#718; drivers:Db#20; constructors:Db#14 |
| 162 | FULL_ONLY | races | Db | 718 | year of races | number_z=0.58984 | 2004-05-23 | circuits:Db#5 |
| 163 | FULL_ONLY | races | Db | 718 | round of races | number_z=-0.49023 | 2004-05-23 | circuits:Db#5 |
| 164 | FULL_ONLY | races | Db | 718 | name of races | Monaco Grand Prix | 2004-05-23 | circuits:Db#5 |
| 165 | FULL_ONLY | races | Db | 718 | date of races | 2004-05-23 | 2004-05-23 | circuits:Db#5 |
| 166 | FULL_ONLY | races | Db | 718 | time of races | 00:00:00 | 2004-05-23 | circuits:Db#5 |
| 167 | DRIVER_NBR_INDIRECT | results | Db | 15832 | number of results | number_z=-0.38672 | 1997-08-10 | races:Db#607; drivers:Db#20; constructors:Db#16 |
| 168 | DRIVER_NBR_INDIRECT | results | Db | 15832 | grid of results | number_z=0.25391 | 1997-08-10 | races:Db#607; drivers:Db#20; constructors:Db#16 |
| 169 | DRIVER_NBR_INDIRECT | results | Db | 15832 | positionOrder of results | number_z=0.53906 | 1997-08-10 | races:Db#607; drivers:Db#20; constructors:Db#16 |
| 170 | DRIVER_NBR_INDIRECT | results | Db | 15832 | points of results | number_z=-0.45117 | 1997-08-10 | races:Db#607; drivers:Db#20; constructors:Db#16 |
| 171 | DRIVER_NBR_INDIRECT | results | Db | 15832 | laps of results | number_z=-0.13672 | 1997-08-10 | races:Db#607; drivers:Db#20; constructors:Db#16 |
| 172 | DRIVER_NBR_INDIRECT | results | Db | 15832 | statusId of results | number_z=0.09668 | 1997-08-10 | races:Db#607; drivers:Db#20; constructors:Db#16 |
| 173 | DRIVER_NBR_INDIRECT | results | Db | 15832 | date of results | 1997-08-10 | 1997-08-10 | races:Db#607; drivers:Db#20; constructors:Db#16 |
| 174 | FULL_ONLY | races | Db | 607 | year of races | number_z=0.24512 | 1997-08-10 | circuits:Db#10 |
| 175 | FULL_ONLY | races | Db | 607 | round of races | number_z=0.49414 | 1997-08-10 | circuits:Db#10 |
| 176 | FULL_ONLY | races | Db | 607 | name of races | Hungarian Grand Prix | 1997-08-10 | circuits:Db#10 |
| 177 | FULL_ONLY | races | Db | 607 | date of races | 1997-08-10 | 1997-08-10 | circuits:Db#10 |
| 178 | FULL_ONLY | races | Db | 607 | time of races | 00:00:00 | 1997-08-10 | circuits:Db#10 |
| 179 | FULL_ONLY | circuits | Db | 10 | circuitRef of circuits | hungaroring |  |  |
| 180 | FULL_ONLY | circuits | Db | 10 | name of circuits | Hungaroring |  |  |
| 181 | FULL_ONLY | circuits | Db | 10 | location of circuits | Budapest |  |  |
| 182 | FULL_ONLY | circuits | Db | 10 | country of circuits | Hungary |  |  |
| 183 | FULL_ONLY | circuits | Db | 10 | lat of circuits | number_z=0.62109 |  |  |
| 184 | FULL_ONLY | circuits | Db | 10 | lng of circuits | number_z=0.27734 |  |  |
| 185 | FULL_ONLY | circuits | Db | 10 | alt of circuits | number_z=0.043213 |  |  |
| 186 | DRIVER_NBR_INDIRECT | driver-dnf | Train | 3648 | date of driver-dnf | 1996-04-18 | 1996-04-18 | drivers:Db#20 |
| 187 | COL+DRIVER_NBR_INDIRECT | driver-dnf | Train | 3648 | did_not_finish of driver-dnf | 1 | 1996-04-18 | drivers:Db#20 |
| 188 | DRIVER_NBR_INDIRECT | qualifying | Db | 1966 | number of qualifying | number_z=-0.39844 | 2004-05-08 | races:Db#717; drivers:Db#20; constructors:Db#14 |
| 189 | DRIVER_NBR_INDIRECT | qualifying | Db | 1966 | position of qualifying | number_z=0.12012 | 2004-05-08 | races:Db#717; drivers:Db#20; constructors:Db#14 |
| 190 | DRIVER_NBR_INDIRECT | qualifying | Db | 1966 | date of qualifying | 2004-05-08 | 2004-05-08 | races:Db#717; drivers:Db#20; constructors:Db#14 |
| 191 | FULL_ONLY | races | Db | 717 | year of races | number_z=0.58984 | 2004-05-09 | circuits:Db#3 |
| 192 | FULL_ONLY | races | Db | 717 | round of races | number_z=-0.6875 | 2004-05-09 | circuits:Db#3 |
| 193 | FULL_ONLY | races | Db | 717 | name of races | Spanish Grand Prix | 2004-05-09 | circuits:Db#3 |
| 194 | FULL_ONLY | races | Db | 717 | date of races | 2004-05-09 | 2004-05-09 | circuits:Db#3 |
| 195 | FULL_ONLY | races | Db | 717 | time of races | 00:00:00 | 2004-05-09 | circuits:Db#3 |
| 196 | FULL_ONLY | circuits | Db | 3 | circuitRef of circuits | catalunya |  |  |
| 197 | FULL_ONLY | circuits | Db | 3 | name of circuits | Circuit de Barcelona-Catalunya |  |  |
| 198 | FULL_ONLY | circuits | Db | 3 | location of circuits | Montmeló |  |  |
| 199 | FULL_ONLY | circuits | Db | 3 | country of circuits | Spain |  |  |
| 200 | FULL_ONLY | circuits | Db | 3 | lat of circuits | number_z=0.35547 |  |  |
| 201 | FULL_ONLY | circuits | Db | 3 | lng of circuits | number_z=0.018066 |  |  |
| 202 | FULL_ONLY | circuits | Db | 3 | alt of circuits | number_z=-0.38086 |  |  |
| 203 | DRIVER_NBR_INDIRECT | standings | Db | 24573 | points of standings | number_z=0.12695 | 2000-08-27 | races:Db#658; drivers:Db#20 |
| 204 | DRIVER_NBR_INDIRECT | standings | Db | 24573 | position of standings | number_z=-0.84766 | 2000-08-27 | races:Db#658; drivers:Db#20 |
| 205 | DRIVER_NBR_INDIRECT | standings | Db | 24573 | wins of standings | number_z=-0.27148 | 2000-08-27 | races:Db#658; drivers:Db#20 |
| 206 | DRIVER_NBR_INDIRECT | standings | Db | 24573 | date of standings | 2000-08-27 | 2000-08-27 | races:Db#658; drivers:Db#20 |
| 207 | FULL_ONLY | races | Db | 658 | year of races | number_z=0.39258 | 2000-08-27 | circuits:Db#12 |
| 208 | FULL_ONLY | races | Db | 658 | round of races | number_z=0.88672 | 2000-08-27 | circuits:Db#12 |
| 209 | FULL_ONLY | races | Db | 658 | name of races | Belgian Grand Prix | 2000-08-27 | circuits:Db#12 |
| 210 | FULL_ONLY | races | Db | 658 | date of races | 2000-08-27 | 2000-08-27 | circuits:Db#12 |
| 211 | FULL_ONLY | races | Db | 658 | time of races | 00:00:00 | 2000-08-27 | circuits:Db#12 |
| 212 | FULL_ONLY | circuits | Db | 12 | circuitRef of circuits | spa |  |  |
| 213 | FULL_ONLY | circuits | Db | 12 | name of circuits | Circuit de Spa-Francorchamps |  |  |
| 214 | FULL_ONLY | circuits | Db | 12 | location of circuits | Spa |  |  |
| 215 | FULL_ONLY | circuits | Db | 12 | country of circuits | Belgium |  |  |
| 216 | FULL_ONLY | circuits | Db | 12 | lat of circuits | number_z=0.74609 |  |  |
| 217 | FULL_ONLY | circuits | Db | 12 | lng of circuits | number_z=0.074707 |  |  |
| 218 | FULL_ONLY | circuits | Db | 12 | alt of circuits | number_z=0.41797 |  |  |
| 219 | DRIVER_NBR_INDIRECT | results | Db | 17051 | number of results | number_z=-0.45117 | 2000-10-22 | races:Db#662; drivers:Db#20; constructors:Db#21 |
| 220 | DRIVER_NBR_INDIRECT | results | Db | 17051 | grid of results | number_z=0.25391 | 2000-10-22 | races:Db#662; drivers:Db#20; constructors:Db#21 |
| 221 | DRIVER_NBR_INDIRECT | results | Db | 17051 | position of results | number_z=0.21484 | 2000-10-22 | races:Db#662; drivers:Db#20; constructors:Db#21 |
| 222 | DRIVER_NBR_INDIRECT | results | Db | 17051 | positionOrder of results | number_z=-0.5 | 2000-10-22 | races:Db#662; drivers:Db#20; constructors:Db#21 |
| 223 | DRIVER_NBR_INDIRECT | results | Db | 17051 | points of results | number_z=-0.45117 | 2000-10-22 | races:Db#662; drivers:Db#20; constructors:Db#21 |
| 224 | DRIVER_NBR_INDIRECT | results | Db | 17051 | laps of results | number_z=0.30078 | 2000-10-22 | races:Db#662; drivers:Db#20; constructors:Db#21 |
| 225 | DRIVER_NBR_INDIRECT | results | Db | 17051 | statusId of results | number_z=-0.24805 | 2000-10-22 | races:Db#662; drivers:Db#20; constructors:Db#21 |
| 226 | DRIVER_NBR_INDIRECT | results | Db | 17051 | date of results | 2000-10-22 | 2000-10-22 | races:Db#662; drivers:Db#20; constructors:Db#21 |
| 227 | FULL_ONLY | races | Db | 662 | year of races | number_z=0.39258 | 2000-10-22 | circuits:Db#1 |
| 228 | FULL_ONLY | races | Db | 662 | round of races | number_z=1.6719 | 2000-10-22 | circuits:Db#1 |
| 229 | FULL_ONLY | races | Db | 662 | name of races | Malaysian Grand Prix | 2000-10-22 | circuits:Db#1 |
| 230 | FULL_ONLY | races | Db | 662 | date of races | 2000-10-22 | 2000-10-22 | circuits:Db#1 |
| 231 | FULL_ONLY | races | Db | 662 | time of races | 00:00:00 | 2000-10-22 | circuits:Db#1 |
| 232 | FULL_ONLY | circuits | Db | 1 | circuitRef of circuits | sepang |  |  |
| 233 | FULL_ONLY | circuits | Db | 1 | name of circuits | Sepang International Circuit |  |  |
| 234 | FULL_ONLY | circuits | Db | 1 | location of circuits | Kuala Lumpur |  |  |
| 235 | FULL_ONLY | circuits | Db | 1 | country of circuits | Malaysia |  |  |
| 236 | FULL_ONLY | circuits | Db | 1 | lat of circuits | number_z=-1.3438 |  |  |
| 237 | FULL_ONLY | circuits | Db | 1 | lng of circuits | number_z=1.5391 |  |  |
| 238 | FULL_ONLY | circuits | Db | 1 | alt of circuits | number_z=-0.62891 |  |  |
| 239 | DRIVER_NBR_INDIRECT | results | Db | 18322 | number of results | number_z=-0.45117 | 2004-07-11 | races:Db#723; drivers:Db#20; constructors:Db#14 |
| 240 | DRIVER_NBR_INDIRECT | results | Db | 18322 | grid of results | number_z=1.2188 | 2004-07-11 | races:Db#723; drivers:Db#20; constructors:Db#14 |
| 241 | DRIVER_NBR_INDIRECT | results | Db | 18322 | position of results | number_z=-0.4082 | 2004-07-11 | races:Db#723; drivers:Db#20; constructors:Db#14 |
| 242 | DRIVER_NBR_INDIRECT | results | Db | 18322 | positionOrder of results | number_z=-0.89062 | 2004-07-11 | races:Db#723; drivers:Db#20; constructors:Db#14 |
| 243 | DRIVER_NBR_INDIRECT | results | Db | 18322 | points of results | number_z=0.25977 | 2004-07-11 | races:Db#723; drivers:Db#20; constructors:Db#14 |
| 244 | DRIVER_NBR_INDIRECT | results | Db | 18322 | laps of results | number_z=0.46875 | 2004-07-11 | races:Db#723; drivers:Db#20; constructors:Db#14 |
| 245 | DRIVER_NBR_INDIRECT | results | Db | 18322 | milliseconds of results | number_z=-0.67188 | 2004-07-11 | races:Db#723; drivers:Db#20; constructors:Db#14 |
| 246 | DRIVER_NBR_INDIRECT | results | Db | 18322 | fastestLap of results | number_z=-1.2266 | 2004-07-11 | races:Db#723; drivers:Db#20; constructors:Db#14 |
| 247 | DRIVER_NBR_INDIRECT | results | Db | 18322 | rank of results | number_z=-0.87891 | 2004-07-11 | races:Db#723; drivers:Db#20; constructors:Db#14 |
| 248 | DRIVER_NBR_INDIRECT | results | Db | 18322 | statusId of results | number_z=-0.62891 | 2004-07-11 | races:Db#723; drivers:Db#20; constructors:Db#14 |
| 249 | DRIVER_NBR_INDIRECT | results | Db | 18322 | date of results | 2004-07-11 | 2004-07-11 | races:Db#723; drivers:Db#20; constructors:Db#14 |
| 250 | FULL_ONLY | races | Db | 723 | year of races | number_z=0.58984 | 2004-07-11 | circuits:Db#8 |
| 251 | FULL_ONLY | races | Db | 723 | round of races | number_z=0.49414 | 2004-07-11 | circuits:Db#8 |
| 252 | FULL_ONLY | races | Db | 723 | name of races | British Grand Prix | 2004-07-11 | circuits:Db#8 |
| 253 | FULL_ONLY | races | Db | 723 | date of races | 2004-07-11 | 2004-07-11 | circuits:Db#8 |
| 254 | FULL_ONLY | races | Db | 723 | time of races | 00:00:00 | 2004-07-11 | circuits:Db#8 |
| 255 | DRIVER_NBR_INDIRECT | qualifying | Db | 1730 | number of qualifying | number_z=-0.39844 | 2003-07-05 | races:Db#706; drivers:Db#20; constructors:Db#16 |
| 256 | DRIVER_NBR_INDIRECT | qualifying | Db | 1730 | position of qualifying | number_z=0.91406 | 2003-07-05 | races:Db#706; drivers:Db#20; constructors:Db#16 |
| 257 | DRIVER_NBR_INDIRECT | qualifying | Db | 1730 | date of qualifying | 2003-07-05 | 2003-07-05 | races:Db#706; drivers:Db#20; constructors:Db#16 |
| 258 | FULL_ONLY | races | Db | 706 | year of races | number_z=0.53906 | 2003-07-06 | circuits:Db#7 |
| 259 | FULL_ONLY | races | Db | 706 | round of races | number_z=0.29688 | 2003-07-06 | circuits:Db#7 |
| 260 | FULL_ONLY | races | Db | 706 | name of races | French Grand Prix | 2003-07-06 | circuits:Db#7 |
| 261 | FULL_ONLY | races | Db | 706 | date of races | 2003-07-06 | 2003-07-06 | circuits:Db#7 |
| 262 | FULL_ONLY | races | Db | 706 | time of races | 00:00:00 | 2003-07-06 | circuits:Db#7 |
| 263 | DRIVER_NBR_INDIRECT | standings | Db | 24846 | points of standings | number_z=-0.35156 | 2001-06-24 | races:Db#671; drivers:Db#20 |
| 264 | DRIVER_NBR_INDIRECT | standings | Db | 24846 | position of standings | number_z=-0.17676 | 2001-06-24 | races:Db#671; drivers:Db#20 |
| 265 | DRIVER_NBR_INDIRECT | standings | Db | 24846 | wins of standings | number_z=-0.27148 | 2001-06-24 | races:Db#671; drivers:Db#20 |
| 266 | DRIVER_NBR_INDIRECT | standings | Db | 24846 | date of standings | 2001-06-24 | 2001-06-24 | races:Db#671; drivers:Db#20 |
| 267 | FULL_ONLY | races | Db | 671 | year of races | number_z=0.44336 | 2001-06-24 | circuits:Db#19 |
| 268 | FULL_ONLY | races | Db | 671 | round of races | number_z=0.099609 | 2001-06-24 | circuits:Db#19 |
| 269 | FULL_ONLY | races | Db | 671 | name of races | European Grand Prix | 2001-06-24 | circuits:Db#19 |
| 270 | FULL_ONLY | races | Db | 671 | date of races | 2001-06-24 | 2001-06-24 | circuits:Db#19 |
| 271 | FULL_ONLY | races | Db | 671 | time of races | 00:00:00 | 2001-06-24 | circuits:Db#19 |
| 272 | FULL_ONLY | circuits | Db | 19 | circuitRef of circuits | nurburgring |  |  |
| 273 | FULL_ONLY | circuits | Db | 19 | name of circuits | Nürburgring |  |  |
| 274 | FULL_ONLY | circuits | Db | 19 | location of circuits | Nürburg |  |  |
| 275 | FULL_ONLY | circuits | Db | 19 | country of circuits | Germany |  |  |
| 276 | FULL_ONLY | circuits | Db | 19 | lat of circuits | number_z=0.74219 |  |  |
| 277 | FULL_ONLY | circuits | Db | 19 | lng of circuits | number_z=0.089844 |  |  |
| 278 | FULL_ONLY | circuits | Db | 19 | alt of circuits | number_z=0.90234 |  |  |
| 279 | DRIVER_NBR_INDIRECT | qualifying | Db | 897 | number of qualifying | number_z=0.16113 | 1996-05-04 | races:Db#585; drivers:Db#20; constructors:Db#17 |
| 280 | DRIVER_NBR_INDIRECT | qualifying | Db | 897 | position of qualifying | number_z=1.2344 | 1996-05-04 | races:Db#585; drivers:Db#20; constructors:Db#17 |
| 281 | DRIVER_NBR_INDIRECT | qualifying | Db | 897 | date of qualifying | 1996-05-04 | 1996-05-04 | races:Db#585; drivers:Db#20; constructors:Db#17 |
| 282 | FULL_ONLY | constructors | Db | 17 | constructorRef of constructors | minardi |  |  |
| 283 | FULL_ONLY | constructors | Db | 17 | name of constructors | Minardi |  |  |
| 284 | FULL_ONLY | constructors | Db | 17 | nationality of constructors | Italian |  |  |
| 285 | FULL_ONLY | races | Db | 585 | year of races | number_z=0.19629 | 1996-05-05 | circuits:Db#20 |
| 286 | FULL_ONLY | races | Db | 585 | round of races | number_z=-0.6875 | 1996-05-05 | circuits:Db#20 |
| 287 | FULL_ONLY | races | Db | 585 | name of races | San Marino Grand Prix | 1996-05-05 | circuits:Db#20 |
| 288 | FULL_ONLY | races | Db | 585 | date of races | 1996-05-05 | 1996-05-05 | circuits:Db#20 |
| 289 | FULL_ONLY | races | Db | 585 | time of races | 00:00:00 | 1996-05-05 | circuits:Db#20 |
| 290 | FULL_ONLY | circuits | Db | 20 | circuitRef of circuits | imola |  |  |
| 291 | FULL_ONLY | circuits | Db | 20 | name of circuits | Autodromo Enzo e Dino Ferrari |  |  |
| 292 | FULL_ONLY | circuits | Db | 20 | location of circuits | Imola |  |  |
| 293 | FULL_ONLY | circuits | Db | 20 | country of circuits | Italy |  |  |
| 294 | FULL_ONLY | circuits | Db | 20 | lat of circuits | number_z=0.47852 |  |  |
| 295 | FULL_ONLY | circuits | Db | 20 | lng of circuits | number_z=0.16211 |  |  |
| 296 | FULL_ONLY | circuits | Db | 20 | alt of circuits | number_z=-0.57812 |  |  |
| 297 | DRIVER_NBR_INDIRECT | qualifying | Db | 1929 | number of qualifying | number_z=-0.39844 | 2004-04-24 | races:Db#716; drivers:Db#20; constructors:Db#14 |
| 298 | DRIVER_NBR_INDIRECT | qualifying | Db | 1929 | position of qualifying | number_z=1.2344 | 2004-04-24 | races:Db#716; drivers:Db#20; constructors:Db#14 |
| 299 | DRIVER_NBR_INDIRECT | qualifying | Db | 1929 | date of qualifying | 2004-04-24 | 2004-04-24 | races:Db#716; drivers:Db#20; constructors:Db#14 |
| 300 | FULL_ONLY | races | Db | 716 | year of races | number_z=0.58984 | 2004-04-25 | circuits:Db#20 |
| 301 | FULL_ONLY | races | Db | 716 | round of races | number_z=-0.88281 | 2004-04-25 | circuits:Db#20 |
| 302 | FULL_ONLY | races | Db | 716 | name of races | San Marino Grand Prix | 2004-04-25 | circuits:Db#20 |
| 303 | FULL_ONLY | races | Db | 716 | date of races | 2004-04-25 | 2004-04-25 | circuits:Db#20 |
| 304 | FULL_ONLY | races | Db | 716 | time of races | 00:00:00 | 2004-04-25 | circuits:Db#20 |
| 305 | DRIVER_NBR_INDIRECT | standings | Db | 23640 | points of standings | number_z=0.18262 | 1997-10-26 | races:Db#613; drivers:Db#20 |
| 306 | DRIVER_NBR_INDIRECT | standings | Db | 23640 | position of standings | number_z=-0.72656 | 1997-10-26 | races:Db#613; drivers:Db#20 |
| 307 | DRIVER_NBR_INDIRECT | standings | Db | 23640 | wins of standings | number_z=-0.27148 | 1997-10-26 | races:Db#613; drivers:Db#20 |
| 308 | DRIVER_NBR_INDIRECT | standings | Db | 23640 | date of standings | 1997-10-26 | 1997-10-26 | races:Db#613; drivers:Db#20 |
| 309 | FULL_ONLY | races | Db | 613 | year of races | number_z=0.24512 | 1997-10-26 | circuits:Db#25 |
| 310 | FULL_ONLY | races | Db | 613 | round of races | number_z=1.6719 | 1997-10-26 | circuits:Db#25 |
| 311 | FULL_ONLY | races | Db | 613 | name of races | European Grand Prix | 1997-10-26 | circuits:Db#25 |
| 312 | FULL_ONLY | races | Db | 613 | date of races | 1997-10-26 | 1997-10-26 | circuits:Db#25 |
| 313 | FULL_ONLY | races | Db | 613 | time of races | 00:00:00 | 1997-10-26 | circuits:Db#25 |
| 314 | FULL_ONLY | circuits | Db | 25 | circuitRef of circuits | jerez |  |  |
| 315 | FULL_ONLY | circuits | Db | 25 | name of circuits | Circuito de Jerez |  |  |
| 316 | FULL_ONLY | circuits | Db | 25 | location of circuits | Jerez de la Frontera |  |  |
| 317 | FULL_ONLY | circuits | Db | 25 | country of circuits | Spain |  |  |
| 318 | FULL_ONLY | circuits | Db | 25 | lat of circuits | number_z=0.14355 |  |  |
| 319 | FULL_ONLY | circuits | Db | 25 | lng of circuits | number_z=-0.1084 |  |  |
| 320 | FULL_ONLY | circuits | Db | 25 | alt of circuits | number_z=-0.57812 |  |  |
| 321 | DRIVER_NBR_INDIRECT | driver-dnf | Train | 3569 | date of driver-dnf | 2003-04-12 | 2003-04-12 | drivers:Db#20 |
| 322 | COL+DRIVER_NBR_INDIRECT | driver-dnf | Train | 3569 | did_not_finish of driver-dnf | 1 | 2003-04-12 | drivers:Db#20 |
| 323 | DRIVER_NBR_INDIRECT | qualifying | Db | 1926 | number of qualifying | number_z=-0.39844 | 2004-04-03 | races:Db#715; drivers:Db#20; constructors:Db#14 |
| 324 | DRIVER_NBR_INDIRECT | qualifying | Db | 1926 | position of qualifying | number_z=-0.038818 | 2004-04-03 | races:Db#715; drivers:Db#20; constructors:Db#14 |
| 325 | DRIVER_NBR_INDIRECT | qualifying | Db | 1926 | date of qualifying | 2004-04-03 | 2004-04-03 | races:Db#715; drivers:Db#20; constructors:Db#14 |
| 326 | FULL_ONLY | races | Db | 715 | year of races | number_z=0.58984 | 2004-04-04 | circuits:Db#2 |
| 327 | FULL_ONLY | races | Db | 715 | round of races | number_z=-1.0781 | 2004-04-04 | circuits:Db#2 |
| 328 | FULL_ONLY | races | Db | 715 | name of races | Bahrain Grand Prix | 2004-04-04 | circuits:Db#2 |
| 329 | FULL_ONLY | races | Db | 715 | date of races | 2004-04-04 | 2004-04-04 | circuits:Db#2 |
| 330 | FULL_ONLY | races | Db | 715 | time of races | 00:00:00 | 2004-04-04 | circuits:Db#2 |
| 331 | FULL_ONLY | circuits | Db | 2 | circuitRef of circuits | bahrain |  |  |
| 332 | FULL_ONLY | circuits | Db | 2 | name of circuits | Bahrain International Circuit |  |  |
| 333 | FULL_ONLY | circuits | Db | 2 | location of circuits | Sakhir |  |  |
| 334 | FULL_ONLY | circuits | Db | 2 | country of circuits | Bahrain |  |  |
| 335 | FULL_ONLY | circuits | Db | 2 | lat of circuits | number_z=-0.32422 |  |  |
| 336 | FULL_ONLY | circuits | Db | 2 | lng of circuits | number_z=0.75391 |  |  |
| 337 | FULL_ONLY | circuits | Db | 2 | alt of circuits | number_z=-0.66016 |  |  |
| 338 | DRIVER_NBR_INDIRECT | qualifying | Db | 1999 | number of qualifying | number_z=-0.39844 | 2004-05-29 | races:Db#719; drivers:Db#20; constructors:Db#14 |
| 339 | DRIVER_NBR_INDIRECT | qualifying | Db | 1999 | position of qualifying | number_z=1.2344 | 2004-05-29 | races:Db#719; drivers:Db#20; constructors:Db#14 |
| 340 | DRIVER_NBR_INDIRECT | qualifying | Db | 1999 | date of qualifying | 2004-05-29 | 2004-05-29 | races:Db#719; drivers:Db#20; constructors:Db#14 |
| 341 | FULL_ONLY | races | Db | 719 | year of races | number_z=0.58984 | 2004-05-30 | circuits:Db#19 |
| 342 | FULL_ONLY | races | Db | 719 | round of races | number_z=-0.29492 | 2004-05-30 | circuits:Db#19 |
| 343 | FULL_ONLY | races | Db | 719 | name of races | European Grand Prix | 2004-05-30 | circuits:Db#19 |
| 344 | FULL_ONLY | races | Db | 719 | date of races | 2004-05-30 | 2004-05-30 | circuits:Db#19 |
| 345 | FULL_ONLY | races | Db | 719 | time of races | 00:00:00 | 2004-05-30 | circuits:Db#19 |
| 346 | DRIVER_NBR_INDIRECT | standings | Db | 24177 | points of standings | number_z=-0.013794 | 1999-08-15 | races:Db#640; drivers:Db#20 |
| 347 | DRIVER_NBR_INDIRECT | standings | Db | 24177 | position of standings | number_z=-0.78516 | 1999-08-15 | races:Db#640; drivers:Db#20 |
| 348 | DRIVER_NBR_INDIRECT | standings | Db | 24177 | wins of standings | number_z=-0.27148 | 1999-08-15 | races:Db#640; drivers:Db#20 |
| 349 | DRIVER_NBR_INDIRECT | standings | Db | 24177 | date of standings | 1999-08-15 | 1999-08-15 | races:Db#640; drivers:Db#20 |
| 350 | FULL_ONLY | races | Db | 640 | year of races | number_z=0.34375 | 1999-08-15 | circuits:Db#10 |
| 351 | FULL_ONLY | races | Db | 640 | round of races | number_z=0.49414 | 1999-08-15 | circuits:Db#10 |
| 352 | FULL_ONLY | races | Db | 640 | name of races | Hungarian Grand Prix | 1999-08-15 | circuits:Db#10 |
| 353 | FULL_ONLY | races | Db | 640 | date of races | 1999-08-15 | 1999-08-15 | circuits:Db#10 |
| 354 | FULL_ONLY | races | Db | 640 | time of races | 00:00:00 | 1999-08-15 | circuits:Db#10 |
| 355 | DRIVER_NBR_INDIRECT | results | Db | 16071 | number of results | number_z=-0.84766 | 1998-05-10 | races:Db#618; drivers:Db#20; constructors:Db#21 |
| 356 | DRIVER_NBR_INDIRECT | results | Db | 16071 | grid of results | number_z=-0.99219 | 1998-05-10 | races:Db#618; drivers:Db#20; constructors:Db#21 |
| 357 | DRIVER_NBR_INDIRECT | results | Db | 16071 | positionOrder of results | number_z=0.79688 | 1998-05-10 | races:Db#618; drivers:Db#20; constructors:Db#21 |
| 358 | DRIVER_NBR_INDIRECT | results | Db | 16071 | points of results | number_z=-0.45117 | 1998-05-10 | races:Db#618; drivers:Db#20; constructors:Db#21 |
| 359 | DRIVER_NBR_INDIRECT | results | Db | 16071 | laps of results | number_z=-0.60938 | 1998-05-10 | races:Db#618; drivers:Db#20; constructors:Db#21 |
| 360 | DRIVER_NBR_INDIRECT | results | Db | 16071 | statusId of results | number_z=-0.51562 | 1998-05-10 | races:Db#618; drivers:Db#20; constructors:Db#21 |
| 361 | DRIVER_NBR_INDIRECT | results | Db | 16071 | date of results | 1998-05-10 | 1998-05-10 | races:Db#618; drivers:Db#20; constructors:Db#21 |
| 362 | FULL_ONLY | races | Db | 618 | year of races | number_z=0.29492 | 1998-05-10 | circuits:Db#3 |
| 363 | FULL_ONLY | races | Db | 618 | round of races | number_z=-0.6875 | 1998-05-10 | circuits:Db#3 |
| 364 | FULL_ONLY | races | Db | 618 | name of races | Spanish Grand Prix | 1998-05-10 | circuits:Db#3 |
| 365 | FULL_ONLY | races | Db | 618 | date of races | 1998-05-10 | 1998-05-10 | circuits:Db#3 |
| 366 | FULL_ONLY | races | Db | 618 | time of races | 00:00:00 | 1998-05-10 | circuits:Db#3 |
| 367 | DRIVER_NBR_INDIRECT | standings | Db | 24010 | points of standings | number_z=-0.23828 | 1999-05-02 | races:Db#632; drivers:Db#20 |
| 368 | DRIVER_NBR_INDIRECT | standings | Db | 24010 | position of standings | number_z=-0.72656 | 1999-05-02 | races:Db#632; drivers:Db#20 |
| 369 | DRIVER_NBR_INDIRECT | standings | Db | 24010 | wins of standings | number_z=-0.27148 | 1999-05-02 | races:Db#632; drivers:Db#20 |
| 370 | DRIVER_NBR_INDIRECT | standings | Db | 24010 | date of standings | 1999-05-02 | 1999-05-02 | races:Db#632; drivers:Db#20 |
| 371 | FULL_ONLY | races | Db | 632 | year of races | number_z=0.34375 | 1999-05-02 | circuits:Db#20 |
| 372 | FULL_ONLY | races | Db | 632 | round of races | number_z=-1.0781 | 1999-05-02 | circuits:Db#20 |
| 373 | FULL_ONLY | races | Db | 632 | name of races | San Marino Grand Prix | 1999-05-02 | circuits:Db#20 |
| 374 | FULL_ONLY | races | Db | 632 | date of races | 1999-05-02 | 1999-05-02 | circuits:Db#20 |
| 375 | FULL_ONLY | races | Db | 632 | time of races | 00:00:00 | 1999-05-02 | circuits:Db#20 |
| 376 | DRIVER_NBR_INDIRECT | driver-dnf | Train | 1466 | date of driver-dnf | 1998-04-08 | 1998-04-08 | drivers:Db#20 |
| 377 | COL+DRIVER_NBR_INDIRECT | driver-dnf | Train | 1466 | did_not_finish of driver-dnf | 1 | 1998-04-08 | drivers:Db#20 |
| 378 | DRIVER_NBR_INDIRECT | results | Db | 16652 | number of results | number_z=-0.58203 | 1999-10-17 | races:Db#644; drivers:Db#20; constructors:Db#21 |
| 379 | DRIVER_NBR_INDIRECT | results | Db | 16652 | grid of results | number_z=-0.023193 | 1999-10-17 | races:Db#644; drivers:Db#20; constructors:Db#21 |
| 380 | DRIVER_NBR_INDIRECT | results | Db | 16652 | position of results | number_z=0.62891 | 1999-10-17 | races:Db#644; drivers:Db#20; constructors:Db#21 |
| 381 | DRIVER_NBR_INDIRECT | results | Db | 16652 | positionOrder of results | number_z=-0.24121 | 1999-10-17 | races:Db#644; drivers:Db#20; constructors:Db#21 |
| 382 | DRIVER_NBR_INDIRECT | results | Db | 16652 | points of results | number_z=-0.45117 | 1999-10-17 | races:Db#644; drivers:Db#20; constructors:Db#21 |
| 383 | DRIVER_NBR_INDIRECT | results | Db | 16652 | laps of results | number_z=0.19922 | 1999-10-17 | races:Db#644; drivers:Db#20; constructors:Db#21 |
| 384 | DRIVER_NBR_INDIRECT | results | Db | 16652 | statusId of results | number_z=-0.13281 | 1999-10-17 | races:Db#644; drivers:Db#20; constructors:Db#21 |
| 385 | DRIVER_NBR_INDIRECT | results | Db | 16652 | date of results | 1999-10-17 | 1999-10-17 | races:Db#644; drivers:Db#20; constructors:Db#21 |
| 386 | FULL_ONLY | races | Db | 644 | year of races | number_z=0.34375 | 1999-10-17 | circuits:Db#1 |
| 387 | FULL_ONLY | races | Db | 644 | round of races | number_z=1.2812 | 1999-10-17 | circuits:Db#1 |
| 388 | FULL_ONLY | races | Db | 644 | name of races | Malaysian Grand Prix | 1999-10-17 | circuits:Db#1 |
| 389 | FULL_ONLY | races | Db | 644 | date of races | 1999-10-17 | 1999-10-17 | circuits:Db#1 |
| 390 | FULL_ONLY | races | Db | 644 | time of races | 00:00:00 | 1999-10-17 | circuits:Db#1 |
| 391 | DRIVER_NBR_INDIRECT | standings | Db | 23860 | points of standings | number_z=0.04248 | 1998-08-02 | races:Db#624; drivers:Db#20 |
| 392 | DRIVER_NBR_INDIRECT | standings | Db | 23860 | position of standings | number_z=-0.78516 | 1998-08-02 | races:Db#624; drivers:Db#20 |
| 393 | DRIVER_NBR_INDIRECT | standings | Db | 23860 | wins of standings | number_z=-0.27148 | 1998-08-02 | races:Db#624; drivers:Db#20 |
| 394 | DRIVER_NBR_INDIRECT | standings | Db | 23860 | date of standings | 1998-08-02 | 1998-08-02 | races:Db#624; drivers:Db#20 |
| 395 | FULL_ONLY | races | Db | 624 | year of races | number_z=0.29492 | 1998-08-02 | circuits:Db#9 |
| 396 | FULL_ONLY | races | Db | 624 | round of races | number_z=0.49414 | 1998-08-02 | circuits:Db#9 |
| 397 | FULL_ONLY | races | Db | 624 | name of races | German Grand Prix | 1998-08-02 | circuits:Db#9 |
| 398 | FULL_ONLY | races | Db | 624 | date of races | 1998-08-02 | 1998-08-02 | circuits:Db#9 |
| 399 | FULL_ONLY | races | Db | 624 | time of races | 00:00:00 | 1998-08-02 | circuits:Db#9 |
| 400 | FULL_ONLY | circuits | Db | 9 | circuitRef of circuits | hockenheimring |  |  |
| 401 | FULL_ONLY | circuits | Db | 9 | name of circuits | Hockenheimring |  |  |
| 402 | FULL_ONLY | circuits | Db | 9 | location of circuits | Hockenheim |  |  |
| 403 | FULL_ONLY | circuits | Db | 9 | country of circuits | Germany |  |  |
| 404 | FULL_ONLY | circuits | Db | 9 | lat of circuits | number_z=0.69531 |  |  |
| 405 | FULL_ONLY | circuits | Db | 9 | lng of circuits | number_z=0.11426 |  |  |
| 406 | FULL_ONLY | circuits | Db | 9 | alt of circuits | number_z=-0.39844 |  |  |
| 407 | DRIVER_NBR_INDIRECT | standings | Db | 23052 | points of standings | number_z=-0.37891 | 1996-06-02 | races:Db#587; drivers:Db#20 |
| 408 | DRIVER_NBR_INDIRECT | standings | Db | 23052 | position of standings | number_z=0.12793 | 1996-06-02 | races:Db#587; drivers:Db#20 |
| 409 | DRIVER_NBR_INDIRECT | standings | Db | 23052 | wins of standings | number_z=-0.27148 | 1996-06-02 | races:Db#587; drivers:Db#20 |
| 410 | DRIVER_NBR_INDIRECT | standings | Db | 23052 | date of standings | 1996-06-02 | 1996-06-02 | races:Db#587; drivers:Db#20 |
| 411 | FULL_ONLY | races | Db | 587 | year of races | number_z=0.19629 | 1996-06-02 | circuits:Db#3 |
| 412 | FULL_ONLY | races | Db | 587 | round of races | number_z=-0.29492 | 1996-06-02 | circuits:Db#3 |
| 413 | FULL_ONLY | races | Db | 587 | name of races | Spanish Grand Prix | 1996-06-02 | circuits:Db#3 |
| 414 | FULL_ONLY | races | Db | 587 | date of races | 1996-06-02 | 1996-06-02 | circuits:Db#3 |
| 415 | FULL_ONLY | races | Db | 587 | time of races | 00:00:00 | 1996-06-02 | circuits:Db#3 |
| 416 | DRIVER_NBR_INDIRECT | standings | Db | 25347 | points of standings | number_z=-0.18262 | 2002-09-15 | races:Db#694; drivers:Db#20 |
| 417 | DRIVER_NBR_INDIRECT | standings | Db | 25347 | position of standings | number_z=-0.54297 | 2002-09-15 | races:Db#694; drivers:Db#20 |
| 418 | DRIVER_NBR_INDIRECT | standings | Db | 25347 | wins of standings | number_z=-0.27148 | 2002-09-15 | races:Db#694; drivers:Db#20 |
| 419 | DRIVER_NBR_INDIRECT | standings | Db | 25347 | date of standings | 2002-09-15 | 2002-09-15 | races:Db#694; drivers:Db#20 |
| 420 | FULL_ONLY | races | Db | 694 | year of races | number_z=0.49219 | 2002-09-15 | circuits:Db#13 |
| 421 | FULL_ONLY | races | Db | 694 | round of races | number_z=1.2812 | 2002-09-15 | circuits:Db#13 |
| 422 | FULL_ONLY | races | Db | 694 | name of races | Italian Grand Prix | 2002-09-15 | circuits:Db#13 |
| 423 | FULL_ONLY | races | Db | 694 | date of races | 2002-09-15 | 2002-09-15 | circuits:Db#13 |
| 424 | FULL_ONLY | races | Db | 694 | time of races | 00:00:00 | 2002-09-15 | circuits:Db#13 |
| 425 | FULL_ONLY | circuits | Db | 13 | circuitRef of circuits | monza |  |  |
| 426 | FULL_ONLY | circuits | Db | 13 | name of circuits | Autodromo Nazionale di Monza |  |  |
| 427 | FULL_ONLY | circuits | Db | 13 | location of circuits | Monza |  |  |
| 428 | FULL_ONLY | circuits | Db | 13 | country of circuits | Italy |  |  |
| 429 | FULL_ONLY | circuits | Db | 13 | lat of circuits | number_z=0.53516 |  |  |
| 430 | FULL_ONLY | circuits | Db | 13 | lng of circuits | number_z=0.125 |  |  |
| 431 | FULL_ONLY | circuits | Db | 13 | alt of circuits | number_z=-0.23633 |  |  |
| 432 | DRIVER_NBR_INDIRECT | standings | Db | 24245 | points of standings | number_z=-0.013794 | 1999-09-26 | races:Db#643; drivers:Db#20 |
| 433 | DRIVER_NBR_INDIRECT | standings | Db | 24245 | position of standings | number_z=-0.72656 | 1999-09-26 | races:Db#643; drivers:Db#20 |
| 434 | DRIVER_NBR_INDIRECT | standings | Db | 24245 | wins of standings | number_z=-0.27148 | 1999-09-26 | races:Db#643; drivers:Db#20 |
| 435 | DRIVER_NBR_INDIRECT | standings | Db | 24245 | date of standings | 1999-09-26 | 1999-09-26 | races:Db#643; drivers:Db#20 |
| 436 | FULL_ONLY | races | Db | 643 | year of races | number_z=0.34375 | 1999-09-26 | circuits:Db#19 |
| 437 | FULL_ONLY | races | Db | 643 | round of races | number_z=1.0859 | 1999-09-26 | circuits:Db#19 |
| 438 | FULL_ONLY | races | Db | 643 | name of races | European Grand Prix | 1999-09-26 | circuits:Db#19 |
| 439 | FULL_ONLY | races | Db | 643 | date of races | 1999-09-26 | 1999-09-26 | circuits:Db#19 |
| 440 | FULL_ONLY | races | Db | 643 | time of races | 00:00:00 | 1999-09-26 | circuits:Db#19 |
| 441 | DRIVER_NBR_INDIRECT | results | Db | 15778 | number of results | number_z=-0.38672 | 1997-06-29 | races:Db#604; drivers:Db#20; constructors:Db#16 |
| 442 | DRIVER_NBR_INDIRECT | results | Db | 15778 | grid of results | number_z=-0.023193 | 1997-06-29 | races:Db#604; drivers:Db#20; constructors:Db#16 |
| 443 | DRIVER_NBR_INDIRECT | results | Db | 15778 | position of results | number_z=0.21484 | 1997-06-29 | races:Db#604; drivers:Db#20; constructors:Db#16 |
| 444 | DRIVER_NBR_INDIRECT | results | Db | 15778 | positionOrder of results | number_z=-0.5 | 1997-06-29 | races:Db#604; drivers:Db#20; constructors:Db#16 |
| 445 | DRIVER_NBR_INDIRECT | results | Db | 15778 | points of results | number_z=-0.45117 | 1997-06-29 | races:Db#604; drivers:Db#20; constructors:Db#16 |
| 446 | DRIVER_NBR_INDIRECT | results | Db | 15778 | laps of results | number_z=0.83984 | 1997-06-29 | races:Db#604; drivers:Db#20; constructors:Db#16 |
| 447 | DRIVER_NBR_INDIRECT | results | Db | 15778 | statusId of results | number_z=-0.24805 | 1997-06-29 | races:Db#604; drivers:Db#20; constructors:Db#16 |
| 448 | DRIVER_NBR_INDIRECT | results | Db | 15778 | date of results | 1997-06-29 | 1997-06-29 | races:Db#604; drivers:Db#20; constructors:Db#16 |
| 449 | FULL_ONLY | races | Db | 604 | year of races | number_z=0.24512 | 1997-06-29 | circuits:Db#7 |
| 450 | FULL_ONLY | races | Db | 604 | round of races | number_z=-0.097168 | 1997-06-29 | circuits:Db#7 |
| 451 | FULL_ONLY | races | Db | 604 | name of races | French Grand Prix | 1997-06-29 | circuits:Db#7 |
| 452 | FULL_ONLY | races | Db | 604 | date of races | 1997-06-29 | 1997-06-29 | circuits:Db#7 |
| 453 | FULL_ONLY | races | Db | 604 | time of races | 00:00:00 | 1997-06-29 | circuits:Db#7 |
| 454 | DRIVER_NBR_INDIRECT | results | Db | 16927 | number of results | number_z=-0.45117 | 2000-08-13 | races:Db#657; drivers:Db#20; constructors:Db#21 |
| 455 | DRIVER_NBR_INDIRECT | results | Db | 16927 | grid of results | number_z=-0.57812 | 2000-08-13 | races:Db#657; drivers:Db#20; constructors:Db#21 |
| 456 | DRIVER_NBR_INDIRECT | results | Db | 16927 | positionOrder of results | number_z=0.92969 | 2000-08-13 | races:Db#657; drivers:Db#20; constructors:Db#21 |
| 457 | DRIVER_NBR_INDIRECT | results | Db | 16927 | points of results | number_z=-0.45117 | 2000-08-13 | races:Db#657; drivers:Db#20; constructors:Db#21 |
| 458 | DRIVER_NBR_INDIRECT | results | Db | 16927 | laps of results | number_z=-0.50781 | 2000-08-13 | races:Db#657; drivers:Db#20; constructors:Db#21 |
| 459 | DRIVER_NBR_INDIRECT | results | Db | 16927 | statusId of results | number_z=0.21094 | 2000-08-13 | races:Db#657; drivers:Db#20; constructors:Db#21 |
| 460 | DRIVER_NBR_INDIRECT | results | Db | 16927 | date of results | 2000-08-13 | 2000-08-13 | races:Db#657; drivers:Db#20; constructors:Db#21 |
| 461 | FULL_ONLY | races | Db | 657 | year of races | number_z=0.39258 | 2000-08-13 | circuits:Db#10 |
| 462 | FULL_ONLY | races | Db | 657 | round of races | number_z=0.69141 | 2000-08-13 | circuits:Db#10 |
| 463 | FULL_ONLY | races | Db | 657 | name of races | Hungarian Grand Prix | 2000-08-13 | circuits:Db#10 |
| 464 | FULL_ONLY | races | Db | 657 | date of races | 2000-08-13 | 2000-08-13 | circuits:Db#10 |
| 465 | FULL_ONLY | races | Db | 657 | time of races | 00:00:00 | 2000-08-13 | circuits:Db#10 |
| 466 | DRIVER_NBR_INDIRECT | standings | Db | 23484 | points of standings | number_z=-0.1543 | 1997-08-10 | races:Db#607; drivers:Db#20 |
| 467 | DRIVER_NBR_INDIRECT | standings | Db | 23484 | position of standings | number_z=-0.48242 | 1997-08-10 | races:Db#607; drivers:Db#20 |
| 468 | DRIVER_NBR_INDIRECT | standings | Db | 23484 | wins of standings | number_z=-0.27148 | 1997-08-10 | races:Db#607; drivers:Db#20 |
| 469 | DRIVER_NBR_INDIRECT | standings | Db | 23484 | date of standings | 1997-08-10 | 1997-08-10 | races:Db#607; drivers:Db#20 |
| 470 | DRIVER_NBR_INDIRECT | results | Db | 17573 | number of results | number_z=-0.58203 | 2002-05-26 | races:Db#686; drivers:Db#20; constructors:Db#16 |
| 471 | DRIVER_NBR_INDIRECT | results | Db | 17573 | grid of results | number_z=-0.023193 | 2002-05-26 | races:Db#686; drivers:Db#20; constructors:Db#16 |
| 472 | DRIVER_NBR_INDIRECT | results | Db | 17573 | position of results | number_z=-0.61719 | 2002-05-26 | races:Db#686; drivers:Db#20; constructors:Db#16 |
| 473 | DRIVER_NBR_INDIRECT | results | Db | 17573 | positionOrder of results | number_z=-1.0234 | 2002-05-26 | races:Db#686; drivers:Db#20; constructors:Db#16 |
| 474 | DRIVER_NBR_INDIRECT | results | Db | 17573 | points of results | number_z=0.022095 | 2002-05-26 | races:Db#686; drivers:Db#20; constructors:Db#16 |
| 475 | DRIVER_NBR_INDIRECT | results | Db | 17573 | laps of results | number_z=1.0391 | 2002-05-26 | races:Db#686; drivers:Db#20; constructors:Db#16 |
| 476 | DRIVER_NBR_INDIRECT | results | Db | 17573 | statusId of results | number_z=-0.24805 | 2002-05-26 | races:Db#686; drivers:Db#20; constructors:Db#16 |
| 477 | DRIVER_NBR_INDIRECT | results | Db | 17573 | date of results | 2002-05-26 | 2002-05-26 | races:Db#686; drivers:Db#20; constructors:Db#16 |
| 478 | FULL_ONLY | races | Db | 686 | year of races | number_z=0.49219 | 2002-05-26 | circuits:Db#5 |
| 479 | FULL_ONLY | races | Db | 686 | round of races | number_z=-0.29492 | 2002-05-26 | circuits:Db#5 |
| 480 | FULL_ONLY | races | Db | 686 | name of races | Monaco Grand Prix | 2002-05-26 | circuits:Db#5 |
| 481 | FULL_ONLY | races | Db | 686 | date of races | 2002-05-26 | 2002-05-26 | circuits:Db#5 |
| 482 | FULL_ONLY | races | Db | 686 | time of races | 00:00:00 | 2002-05-26 | circuits:Db#5 |
| 483 | DRIVER_NBR_INDIRECT | results | Db | 16345 | number of results | number_z=-0.58203 | 1999-03-07 | races:Db#630; drivers:Db#20; constructors:Db#21 |
| 484 | DRIVER_NBR_INDIRECT | results | Db | 16345 | grid of results | number_z=-0.57812 | 1999-03-07 | races:Db#630; drivers:Db#20; constructors:Db#21 |
| 485 | DRIVER_NBR_INDIRECT | results | Db | 16345 | position of results | number_z=-0.82422 | 1999-03-07 | races:Db#630; drivers:Db#20; constructors:Db#21 |
| 486 | DRIVER_NBR_INDIRECT | results | Db | 16345 | positionOrder of results | number_z=-1.1484 | 1999-03-07 | races:Db#630; drivers:Db#20; constructors:Db#21 |
| 487 | DRIVER_NBR_INDIRECT | results | Db | 16345 | points of results | number_z=0.25977 | 1999-03-07 | races:Db#630; drivers:Db#20; constructors:Db#21 |
| 488 | DRIVER_NBR_INDIRECT | results | Db | 16345 | laps of results | number_z=0.36719 | 1999-03-07 | races:Db#630; drivers:Db#20; constructors:Db#21 |
| 489 | DRIVER_NBR_INDIRECT | results | Db | 16345 | milliseconds of results | number_z=-0.29102 | 1999-03-07 | races:Db#630; drivers:Db#20; constructors:Db#21 |
| 490 | DRIVER_NBR_INDIRECT | results | Db | 16345 | statusId of results | number_z=-0.62891 | 1999-03-07 | races:Db#630; drivers:Db#20; constructors:Db#21 |
| 491 | DRIVER_NBR_INDIRECT | results | Db | 16345 | date of results | 1999-03-07 | 1999-03-07 | races:Db#630; drivers:Db#20; constructors:Db#21 |
| 492 | FULL_ONLY | races | Db | 630 | year of races | number_z=0.34375 | 1999-03-07 | circuits:Db#0 |
| 493 | FULL_ONLY | races | Db | 630 | round of races | number_z=-1.4766 | 1999-03-07 | circuits:Db#0 |
| 494 | FULL_ONLY | races | Db | 630 | name of races | Australian Grand Prix | 1999-03-07 | circuits:Db#0 |
| 495 | FULL_ONLY | races | Db | 630 | date of races | 1999-03-07 | 1999-03-07 | circuits:Db#0 |
| 496 | FULL_ONLY | races | Db | 630 | time of races | 00:00:00 | 1999-03-07 | circuits:Db#0 |
| 497 | DRIVER_NBR_INDIRECT | standings | Db | 24028 | points of standings | number_z=-0.18262 | 1999-05-16 | races:Db#633; drivers:Db#20 |
| 498 | DRIVER_NBR_INDIRECT | standings | Db | 24028 | position of standings | number_z=-0.84766 | 1999-05-16 | races:Db#633; drivers:Db#20 |
| 499 | DRIVER_NBR_INDIRECT | standings | Db | 24028 | wins of standings | number_z=-0.27148 | 1999-05-16 | races:Db#633; drivers:Db#20 |
| 500 | DRIVER_NBR_INDIRECT | standings | Db | 24028 | date of standings | 1999-05-16 | 1999-05-16 | races:Db#633; drivers:Db#20 |
| 501 | FULL_ONLY | races | Db | 633 | year of races | number_z=0.34375 | 1999-05-16 | circuits:Db#5 |
| 502 | FULL_ONLY | races | Db | 633 | round of races | number_z=-0.88281 | 1999-05-16 | circuits:Db#5 |
| 503 | FULL_ONLY | races | Db | 633 | name of races | Monaco Grand Prix | 1999-05-16 | circuits:Db#5 |
| 504 | FULL_ONLY | races | Db | 633 | date of races | 1999-05-16 | 1999-05-16 | circuits:Db#5 |
| 505 | FULL_ONLY | races | Db | 633 | time of races | 00:00:00 | 1999-05-16 | circuits:Db#5 |
| 506 | DRIVER_NBR_INDIRECT | driver-dnf | Train | 8671 | date of driver-dnf | 1996-02-18 | 1996-02-18 | drivers:Db#20 |
| 507 | COL+DRIVER_NBR_INDIRECT | driver-dnf | Train | 8671 | did_not_finish of driver-dnf | 1 | 1996-02-18 | drivers:Db#20 |
| 508 | DRIVER_NBR_INDIRECT | results | Db | 15640 | number of results | number_z=-0.38672 | 1997-03-30 | races:Db#598; drivers:Db#20; constructors:Db#16 |
| 509 | DRIVER_NBR_INDIRECT | results | Db | 15640 | grid of results | number_z=-0.57812 | 1997-03-30 | races:Db#598; drivers:Db#20; constructors:Db#16 |
| 510 | DRIVER_NBR_INDIRECT | results | Db | 15640 | position of results | number_z=0.006958 | 1997-03-30 | races:Db#598; drivers:Db#20; constructors:Db#16 |
| 511 | DRIVER_NBR_INDIRECT | results | Db | 15640 | positionOrder of results | number_z=-0.62891 | 1997-03-30 | races:Db#598; drivers:Db#20; constructors:Db#16 |
| 512 | DRIVER_NBR_INDIRECT | results | Db | 15640 | points of results | number_z=-0.45117 | 1997-03-30 | races:Db#598; drivers:Db#20; constructors:Db#16 |
| 513 | DRIVER_NBR_INDIRECT | results | Db | 15640 | laps of results | number_z=0.87109 | 1997-03-30 | races:Db#598; drivers:Db#20; constructors:Db#16 |
| 514 | DRIVER_NBR_INDIRECT | results | Db | 15640 | milliseconds of results | number_z=-0.23438 | 1997-03-30 | races:Db#598; drivers:Db#20; constructors:Db#16 |
| 515 | DRIVER_NBR_INDIRECT | results | Db | 15640 | statusId of results | number_z=-0.62891 | 1997-03-30 | races:Db#598; drivers:Db#20; constructors:Db#16 |
| 516 | DRIVER_NBR_INDIRECT | results | Db | 15640 | date of results | 1997-03-30 | 1997-03-30 | races:Db#598; drivers:Db#20; constructors:Db#16 |
| 517 | FULL_ONLY | races | Db | 598 | year of races | number_z=0.24512 | 1997-03-30 | circuits:Db#17 |
| 518 | FULL_ONLY | races | Db | 598 | round of races | number_z=-1.2812 | 1997-03-30 | circuits:Db#17 |
| 519 | FULL_ONLY | races | Db | 598 | name of races | Brazilian Grand Prix | 1997-03-30 | circuits:Db#17 |
| 520 | FULL_ONLY | races | Db | 598 | date of races | 1997-03-30 | 1997-03-30 | circuits:Db#17 |
| 521 | FULL_ONLY | races | Db | 598 | time of races | 00:00:00 | 1997-03-30 | circuits:Db#17 |
| 522 | FULL_ONLY | circuits | Db | 17 | circuitRef of circuits | interlagos |  |  |
| 523 | FULL_ONLY | circuits | Db | 17 | name of circuits | Autódromo José Carlos Pace |  |  |
| 524 | FULL_ONLY | circuits | Db | 17 | location of circuits | São Paulo |  |  |
| 525 | FULL_ONLY | circuits | Db | 17 | country of circuits | Brazil |  |  |
| 526 | FULL_ONLY | circuits | Db | 17 | lat of circuits | number_z=-2.5 |  |  |
| 527 | FULL_ONLY | circuits | Db | 17 | lng of circuits | number_z=-0.73047 |  |  |
| 528 | FULL_ONLY | circuits | Db | 17 | alt of circuits | number_z=1.4688 |  |  |
| 529 | DRIVER_NBR_INDIRECT | standings | Db | 23681 | points of standings | number_z=-0.35156 | 1998-04-12 | races:Db#616; drivers:Db#20 |
| 530 | DRIVER_NBR_INDIRECT | standings | Db | 23681 | position of standings | number_z=-0.66406 | 1998-04-12 | races:Db#616; drivers:Db#20 |
| 531 | DRIVER_NBR_INDIRECT | standings | Db | 23681 | wins of standings | number_z=-0.27148 | 1998-04-12 | races:Db#616; drivers:Db#20 |
| 532 | DRIVER_NBR_INDIRECT | standings | Db | 23681 | date of standings | 1998-04-12 | 1998-04-12 | races:Db#616; drivers:Db#20 |
| 533 | FULL_ONLY | races | Db | 616 | year of races | number_z=0.29492 | 1998-04-12 | circuits:Db#24 |
| 534 | FULL_ONLY | races | Db | 616 | round of races | number_z=-1.0781 | 1998-04-12 | circuits:Db#24 |
| 535 | FULL_ONLY | races | Db | 616 | name of races | Argentine Grand Prix | 1998-04-12 | circuits:Db#24 |
| 536 | FULL_ONLY | races | Db | 616 | date of races | 1998-04-12 | 1998-04-12 | circuits:Db#24 |
| 537 | FULL_ONLY | races | Db | 616 | time of races | 00:00:00 | 1998-04-12 | circuits:Db#24 |
| 538 | FULL_ONLY | circuits | Db | 24 | circuitRef of circuits | galvez |  |  |
| 539 | FULL_ONLY | circuits | Db | 24 | name of circuits | Autódromo Juan y Oscar Gálvez |  |  |
| 540 | FULL_ONLY | circuits | Db | 24 | location of circuits | Buenos Aires |  |  |
| 541 | FULL_ONLY | circuits | Db | 24 | country of circuits | Argentina |  |  |
| 542 | FULL_ONLY | circuits | Db | 24 | lat of circuits | number_z=-2.9844 |  |  |
| 543 | FULL_ONLY | circuits | Db | 24 | lng of circuits | number_z=-0.91016 |  |  |
| 544 | FULL_ONLY | circuits | Db | 24 | alt of circuits | number_z=-0.65625 |  |  |
| 545 | DRIVER_NBR_INDIRECT | driver-dnf | Train | 70 | date of driver-dnf | 1998-06-07 | 1998-06-07 | drivers:Db#20 |
| 546 | COL+DRIVER_NBR_INDIRECT | driver-dnf | Train | 70 | did_not_finish of driver-dnf | 1 | 1998-06-07 | drivers:Db#20 |
| 547 | DRIVER_NBR_INDIRECT | standings | Db | 25556 | points of standings | number_z=-0.098145 | 2003-06-29 | races:Db#705; drivers:Db#20 |
| 548 | DRIVER_NBR_INDIRECT | standings | Db | 25556 | position of standings | number_z=-0.66406 | 2003-06-29 | races:Db#705; drivers:Db#20 |
| 549 | DRIVER_NBR_INDIRECT | standings | Db | 25556 | wins of standings | number_z=0.73438 | 2003-06-29 | races:Db#705; drivers:Db#20 |
| 550 | DRIVER_NBR_INDIRECT | standings | Db | 25556 | date of standings | 2003-06-29 | 2003-06-29 | races:Db#705; drivers:Db#20 |
| 551 | FULL_ONLY | races | Db | 705 | year of races | number_z=0.53906 | 2003-06-29 | circuits:Db#19 |
| 552 | FULL_ONLY | races | Db | 705 | round of races | number_z=0.099609 | 2003-06-29 | circuits:Db#19 |
| 553 | FULL_ONLY | races | Db | 705 | name of races | European Grand Prix | 2003-06-29 | circuits:Db#19 |
| 554 | FULL_ONLY | races | Db | 705 | date of races | 2003-06-29 | 2003-06-29 | circuits:Db#19 |
| 555 | FULL_ONLY | races | Db | 705 | time of races | 00:00:00 | 2003-06-29 | circuits:Db#19 |
| 556 | DRIVER_NBR_INDIRECT | standings | Db | 24533 | points of standings | number_z=0.12695 | 2000-07-30 | races:Db#656; drivers:Db#20 |
| 557 | DRIVER_NBR_INDIRECT | standings | Db | 24533 | position of standings | number_z=-0.91016 | 2000-07-30 | races:Db#656; drivers:Db#20 |
| 558 | DRIVER_NBR_INDIRECT | standings | Db | 24533 | wins of standings | number_z=-0.27148 | 2000-07-30 | races:Db#656; drivers:Db#20 |
| 559 | DRIVER_NBR_INDIRECT | standings | Db | 24533 | date of standings | 2000-07-30 | 2000-07-30 | races:Db#656; drivers:Db#20 |
| 560 | FULL_ONLY | races | Db | 656 | year of races | number_z=0.39258 | 2000-07-30 | circuits:Db#9 |
| 561 | FULL_ONLY | races | Db | 656 | round of races | number_z=0.49414 | 2000-07-30 | circuits:Db#9 |
| 562 | FULL_ONLY | races | Db | 656 | name of races | German Grand Prix | 2000-07-30 | circuits:Db#9 |
| 563 | FULL_ONLY | races | Db | 656 | date of races | 2000-07-30 | 2000-07-30 | circuits:Db#9 |
| 564 | FULL_ONLY | races | Db | 656 | time of races | 00:00:00 | 2000-07-30 | circuits:Db#9 |
| 565 | DRIVER_NBR_INDIRECT | standings | Db | 24505 | points of standings | number_z=0.12695 | 2000-07-16 | races:Db#655; drivers:Db#20 |
| 566 | DRIVER_NBR_INDIRECT | standings | Db | 24505 | position of standings | number_z=-0.91016 | 2000-07-16 | races:Db#655; drivers:Db#20 |
| 567 | DRIVER_NBR_INDIRECT | standings | Db | 24505 | wins of standings | number_z=-0.27148 | 2000-07-16 | races:Db#655; drivers:Db#20 |
| 568 | DRIVER_NBR_INDIRECT | standings | Db | 24505 | date of standings | 2000-07-16 | 2000-07-16 | races:Db#655; drivers:Db#20 |
| 569 | FULL_ONLY | races | Db | 655 | year of races | number_z=0.39258 | 2000-07-16 | circuits:Db#69 |
| 570 | FULL_ONLY | races | Db | 655 | round of races | number_z=0.29688 | 2000-07-16 | circuits:Db#69 |
| 571 | FULL_ONLY | races | Db | 655 | name of races | Austrian Grand Prix | 2000-07-16 | circuits:Db#69 |
| 572 | FULL_ONLY | races | Db | 655 | date of races | 2000-07-16 | 2000-07-16 | circuits:Db#69 |
| 573 | FULL_ONLY | races | Db | 655 | time of races | 00:00:00 | 2000-07-16 | circuits:Db#69 |
| 574 | DRIVER_NBR_INDIRECT | results | Db | 16101 | number of results | number_z=-0.84766 | 1998-05-24 | races:Db#619; drivers:Db#20; constructors:Db#21 |
| 575 | DRIVER_NBR_INDIRECT | results | Db | 16101 | grid of results | number_z=-1.1328 | 1998-05-24 | races:Db#619; drivers:Db#20; constructors:Db#21 |
| 576 | DRIVER_NBR_INDIRECT | results | Db | 16101 | position of results | number_z=-1.2422 | 1998-05-24 | races:Db#619; drivers:Db#20; constructors:Db#21 |
| 577 | DRIVER_NBR_INDIRECT | results | Db | 16101 | positionOrder of results | number_z=-1.4062 | 1998-05-24 | races:Db#619; drivers:Db#20; constructors:Db#21 |
| 578 | DRIVER_NBR_INDIRECT | results | Db | 16101 | points of results | number_z=0.96875 | 1998-05-24 | races:Db#619; drivers:Db#20; constructors:Db#21 |
| 579 | DRIVER_NBR_INDIRECT | results | Db | 16101 | laps of results | number_z=1.0703 | 1998-05-24 | races:Db#619; drivers:Db#20; constructors:Db#21 |
| 580 | DRIVER_NBR_INDIRECT | results | Db | 16101 | milliseconds of results | number_z=0.28516 | 1998-05-24 | races:Db#619; drivers:Db#20; constructors:Db#21 |
| 581 | DRIVER_NBR_INDIRECT | results | Db | 16101 | statusId of results | number_z=-0.62891 | 1998-05-24 | races:Db#619; drivers:Db#20; constructors:Db#21 |
| 582 | DRIVER_NBR_INDIRECT | results | Db | 16101 | date of results | 1998-05-24 | 1998-05-24 | races:Db#619; drivers:Db#20; constructors:Db#21 |
| 583 | FULL_ONLY | races | Db | 619 | year of races | number_z=0.29492 | 1998-05-24 | circuits:Db#5 |
| 584 | FULL_ONLY | races | Db | 619 | round of races | number_z=-0.49023 | 1998-05-24 | circuits:Db#5 |
| 585 | FULL_ONLY | races | Db | 619 | name of races | Monaco Grand Prix | 1998-05-24 | circuits:Db#5 |
| 586 | FULL_ONLY | races | Db | 619 | date of races | 1998-05-24 | 1998-05-24 | circuits:Db#5 |
| 587 | FULL_ONLY | races | Db | 619 | time of races | 00:00:00 | 1998-05-24 | circuits:Db#5 |
| 588 | DRIVER_NBR_INDIRECT | standings | Db | 22991 | points of standings | number_z=-0.37891 | 1996-05-05 | races:Db#585; drivers:Db#20 |
| 589 | DRIVER_NBR_INDIRECT | standings | Db | 22991 | position of standings | number_z=0.12793 | 1996-05-05 | races:Db#585; drivers:Db#20 |
| 590 | DRIVER_NBR_INDIRECT | standings | Db | 22991 | wins of standings | number_z=-0.27148 | 1996-05-05 | races:Db#585; drivers:Db#20 |
| 591 | DRIVER_NBR_INDIRECT | standings | Db | 22991 | date of standings | 1996-05-05 | 1996-05-05 | races:Db#585; drivers:Db#20 |
| 592 | DRIVER_NBR_INDIRECT | driver-dnf | Train | 7280 | date of driver-dnf | 1997-03-14 | 1997-03-14 | drivers:Db#20 |
| 593 | COL+DRIVER_NBR_INDIRECT | driver-dnf | Train | 7280 | did_not_finish of driver-dnf | 1 | 1997-03-14 | drivers:Db#20 |
| 594 | DRIVER_NBR_INDIRECT | driver-dnf | Train | 10748 | date of driver-dnf | 2000-07-26 | 2000-07-26 | drivers:Db#20 |
| 595 | COL+DRIVER_NBR_INDIRECT | driver-dnf | Train | 10748 | did_not_finish of driver-dnf | 1 | 2000-07-26 | drivers:Db#20 |
| 596 | DRIVER_NBR_INDIRECT | results | Db | 16533 | number of results | number_z=-0.58203 | 1999-08-01 | races:Db#639; drivers:Db#20; constructors:Db#21 |
| 597 | DRIVER_NBR_INDIRECT | results | Db | 16533 | grid of results | number_z=-0.16113 | 1999-08-01 | races:Db#639; drivers:Db#20; constructors:Db#21 |
| 598 | DRIVER_NBR_INDIRECT | results | Db | 16533 | positionOrder of results | number_z=0.79688 | 1999-08-01 | races:Db#639; drivers:Db#20; constructors:Db#21 |
| 599 | DRIVER_NBR_INDIRECT | results | Db | 16533 | points of results | number_z=-0.45117 | 1999-08-01 | races:Db#639; drivers:Db#20; constructors:Db#21 |
| 600 | DRIVER_NBR_INDIRECT | results | Db | 16533 | laps of results | number_z=-1.3125 | 1999-08-01 | races:Db#639; drivers:Db#20; constructors:Db#21 |
| 601 | DRIVER_NBR_INDIRECT | results | Db | 16533 | statusId of results | number_z=0.17285 | 1999-08-01 | races:Db#639; drivers:Db#20; constructors:Db#21 |
| 602 | DRIVER_NBR_INDIRECT | results | Db | 16533 | date of results | 1999-08-01 | 1999-08-01 | races:Db#639; drivers:Db#20; constructors:Db#21 |
| 603 | FULL_ONLY | races | Db | 639 | year of races | number_z=0.34375 | 1999-08-01 | circuits:Db#9 |
| 604 | FULL_ONLY | races | Db | 639 | round of races | number_z=0.29688 | 1999-08-01 | circuits:Db#9 |
| 605 | FULL_ONLY | races | Db | 639 | name of races | German Grand Prix | 1999-08-01 | circuits:Db#9 |
| 606 | FULL_ONLY | races | Db | 639 | date of races | 1999-08-01 | 1999-08-01 | circuits:Db#9 |
| 607 | FULL_ONLY | races | Db | 639 | time of races | 00:00:00 | 1999-08-01 | circuits:Db#9 |
| 608 | DRIVER_NBR_INDIRECT | results | Db | 16666 | number of results | number_z=-0.58203 | 1999-10-31 | races:Db#645; drivers:Db#20; constructors:Db#21 |
| 609 | DRIVER_NBR_INDIRECT | results | Db | 16666 | grid of results | number_z=0.39258 | 1999-10-31 | races:Db#645; drivers:Db#20; constructors:Db#21 |
| 610 | DRIVER_NBR_INDIRECT | results | Db | 16666 | position of results | number_z=1.25 | 1999-10-31 | races:Db#645; drivers:Db#20; constructors:Db#21 |
| 611 | DRIVER_NBR_INDIRECT | results | Db | 16666 | positionOrder of results | number_z=0.14844 | 1999-10-31 | races:Db#645; drivers:Db#20; constructors:Db#21 |
| 612 | DRIVER_NBR_INDIRECT | results | Db | 16666 | points of results | number_z=-0.45117 | 1999-10-31 | races:Db#645; drivers:Db#20; constructors:Db#21 |
| 613 | DRIVER_NBR_INDIRECT | results | Db | 16666 | laps of results | number_z=0.031006 | 1999-10-31 | races:Db#645; drivers:Db#20; constructors:Db#21 |
| 614 | DRIVER_NBR_INDIRECT | results | Db | 16666 | statusId of results | number_z=-0.47656 | 1999-10-31 | races:Db#645; drivers:Db#20; constructors:Db#21 |
| 615 | DRIVER_NBR_INDIRECT | results | Db | 16666 | date of results | 1999-10-31 | 1999-10-31 | races:Db#645; drivers:Db#20; constructors:Db#21 |
| 616 | FULL_ONLY | races | Db | 645 | year of races | number_z=0.34375 | 1999-10-31 | circuits:Db#21 |
| 617 | FULL_ONLY | races | Db | 645 | round of races | number_z=1.4766 | 1999-10-31 | circuits:Db#21 |
| 618 | FULL_ONLY | races | Db | 645 | name of races | Japanese Grand Prix | 1999-10-31 | circuits:Db#21 |
| 619 | FULL_ONLY | races | Db | 645 | date of races | 1999-10-31 | 1999-10-31 | circuits:Db#21 |
| 620 | FULL_ONLY | races | Db | 645 | time of races | 00:00:00 | 1999-10-31 | circuits:Db#21 |
| 621 | FULL_ONLY | circuits | Db | 21 | circuitRef of circuits | suzuka |  |  |
| 622 | FULL_ONLY | circuits | Db | 21 | name of circuits | Suzuka Circuit |  |  |
| 623 | FULL_ONLY | circuits | Db | 21 | location of circuits | Suzuka |  |  |
| 624 | FULL_ONLY | circuits | Db | 21 | country of circuits | Japan |  |  |
| 625 | FULL_ONLY | circuits | Db | 21 | lat of circuits | number_z=0.061279 |  |  |
| 626 | FULL_ONLY | circuits | Db | 21 | lng of circuits | number_z=2.0625 |  |  |
| 627 | FULL_ONLY | circuits | Db | 21 | alt of circuits | number_z=-0.55469 |  |  |
| 628 | DRIVER_NBR_INDIRECT | driver-dnf | Train | 4327 | date of driver-dnf | 1997-10-10 | 1997-10-10 | drivers:Db#20 |
| 629 | COL+DRIVER_NBR_INDIRECT | driver-dnf | Train | 4327 | did_not_finish of driver-dnf | 1 | 1997-10-10 | drivers:Db#20 |
| 630 | DRIVER_NBR_INDIRECT | results | Db | 16593 | number of results | number_z=-0.58203 | 1999-09-12 | races:Db#642; drivers:Db#20; constructors:Db#21 |
| 631 | DRIVER_NBR_INDIRECT | results | Db | 16593 | grid of results | number_z=0.80469 | 1999-09-12 | races:Db#642; drivers:Db#20; constructors:Db#21 |
| 632 | DRIVER_NBR_INDIRECT | results | Db | 16593 | positionOrder of results | number_z=1.0547 | 1999-09-12 | races:Db#642; drivers:Db#20; constructors:Db#21 |
| 633 | DRIVER_NBR_INDIRECT | results | Db | 16593 | points of results | number_z=-0.45117 | 1999-09-12 | races:Db#642; drivers:Db#20; constructors:Db#21 |
| 634 | DRIVER_NBR_INDIRECT | results | Db | 16593 | laps of results | number_z=-1.5156 | 1999-09-12 | races:Db#642; drivers:Db#20; constructors:Db#21 |
| 635 | DRIVER_NBR_INDIRECT | results | Db | 16593 | statusId of results | number_z=0.09668 | 1999-09-12 | races:Db#642; drivers:Db#20; constructors:Db#21 |
| 636 | DRIVER_NBR_INDIRECT | results | Db | 16593 | date of results | 1999-09-12 | 1999-09-12 | races:Db#642; drivers:Db#20; constructors:Db#21 |
| 637 | FULL_ONLY | races | Db | 642 | year of races | number_z=0.34375 | 1999-09-12 | circuits:Db#13 |
| 638 | FULL_ONLY | races | Db | 642 | round of races | number_z=0.88672 | 1999-09-12 | circuits:Db#13 |
| 639 | FULL_ONLY | races | Db | 642 | name of races | Italian Grand Prix | 1999-09-12 | circuits:Db#13 |
| 640 | FULL_ONLY | races | Db | 642 | date of races | 1999-09-12 | 1999-09-12 | circuits:Db#13 |
| 641 | FULL_ONLY | races | Db | 642 | time of races | 00:00:00 | 1999-09-12 | circuits:Db#13 |
| 642 | DRIVER_NBR_INDIRECT | results | Db | 16624 | number of results | number_z=-0.58203 | 1999-09-26 | races:Db#643; drivers:Db#20; constructors:Db#21 |
| 643 | DRIVER_NBR_INDIRECT | results | Db | 16624 | grid of results | number_z=-0.71484 | 1999-09-26 | races:Db#643; drivers:Db#20; constructors:Db#21 |
| 644 | DRIVER_NBR_INDIRECT | results | Db | 16624 | positionOrder of results | number_z=0.018921 | 1999-09-26 | races:Db#643; drivers:Db#20; constructors:Db#21 |
| 645 | DRIVER_NBR_INDIRECT | results | Db | 16624 | points of results | number_z=-0.45117 | 1999-09-26 | races:Db#643; drivers:Db#20; constructors:Db#21 |
| 646 | DRIVER_NBR_INDIRECT | results | Db | 16624 | laps of results | number_z=0.064941 | 1999-09-26 | races:Db#643; drivers:Db#20; constructors:Db#21 |
| 647 | DRIVER_NBR_INDIRECT | results | Db | 16624 | statusId of results | number_z=0.09668 | 1999-09-26 | races:Db#643; drivers:Db#20; constructors:Db#21 |
| 648 | DRIVER_NBR_INDIRECT | results | Db | 16624 | date of results | 1999-09-26 | 1999-09-26 | races:Db#643; drivers:Db#20; constructors:Db#21 |
| 649 | DRIVER_NBR_INDIRECT | standings | Db | 24701 | points of standings | number_z=-0.37891 | 2001-03-18 | races:Db#664; drivers:Db#20 |
| 650 | DRIVER_NBR_INDIRECT | standings | Db | 24701 | position of standings | number_z=-0.11572 | 2001-03-18 | races:Db#664; drivers:Db#20 |
| 651 | DRIVER_NBR_INDIRECT | standings | Db | 24701 | wins of standings | number_z=-0.27148 | 2001-03-18 | races:Db#664; drivers:Db#20 |
| 652 | DRIVER_NBR_INDIRECT | standings | Db | 24701 | date of standings | 2001-03-18 | 2001-03-18 | races:Db#664; drivers:Db#20 |
| 653 | FULL_ONLY | races | Db | 664 | year of races | number_z=0.44336 | 2001-03-18 | circuits:Db#1 |
| 654 | FULL_ONLY | races | Db | 664 | round of races | number_z=-1.2812 | 2001-03-18 | circuits:Db#1 |
| 655 | FULL_ONLY | races | Db | 664 | name of races | Malaysian Grand Prix | 2001-03-18 | circuits:Db#1 |
| 656 | FULL_ONLY | races | Db | 664 | date of races | 2001-03-18 | 2001-03-18 | circuits:Db#1 |
| 657 | FULL_ONLY | races | Db | 664 | time of races | 00:00:00 | 2001-03-18 | circuits:Db#1 |
| 658 | DRIVER_NBR_INDIRECT | results | Db | 17282 | number of results | number_z=-0.71484 | 2001-07-15 | races:Db#673; drivers:Db#20; constructors:Db#21 |
| 659 | DRIVER_NBR_INDIRECT | results | Db | 17282 | grid of results | number_z=1.0859 | 2001-07-15 | races:Db#673; drivers:Db#20; constructors:Db#21 |
| 660 | DRIVER_NBR_INDIRECT | results | Db | 17282 | position of results | number_z=1.0469 | 2001-07-15 | races:Db#673; drivers:Db#20; constructors:Db#21 |
| 661 | DRIVER_NBR_INDIRECT | results | Db | 17282 | positionOrder of results | number_z=0.018921 | 2001-07-15 | races:Db#673; drivers:Db#20; constructors:Db#21 |
| 662 | DRIVER_NBR_INDIRECT | results | Db | 17282 | points of results | number_z=-0.45117 | 2001-07-15 | races:Db#673; drivers:Db#20; constructors:Db#21 |
| 663 | DRIVER_NBR_INDIRECT | results | Db | 17282 | laps of results | number_z=0.40039 | 2001-07-15 | races:Db#673; drivers:Db#20; constructors:Db#21 |
| 664 | DRIVER_NBR_INDIRECT | results | Db | 17282 | statusId of results | number_z=-0.20996 | 2001-07-15 | races:Db#673; drivers:Db#20; constructors:Db#21 |
| 665 | DRIVER_NBR_INDIRECT | results | Db | 17282 | date of results | 2001-07-15 | 2001-07-15 | races:Db#673; drivers:Db#20; constructors:Db#21 |
| 666 | FULL_ONLY | races | Db | 673 | year of races | number_z=0.44336 | 2001-07-15 | circuits:Db#8 |
| 667 | FULL_ONLY | races | Db | 673 | round of races | number_z=0.49414 | 2001-07-15 | circuits:Db#8 |
| 668 | FULL_ONLY | races | Db | 673 | name of races | British Grand Prix | 2001-07-15 | circuits:Db#8 |
| 669 | FULL_ONLY | races | Db | 673 | date of races | 2001-07-15 | 2001-07-15 | circuits:Db#8 |
| 670 | FULL_ONLY | races | Db | 673 | time of races | 00:00:00 | 2001-07-15 | circuits:Db#8 |
| 671 | DRIVER_NBR_INDIRECT | standings | Db | 25929 | points of standings | number_z=-0.013794 | 2004-07-25 | races:Db#724; drivers:Db#20 |
| 672 | DRIVER_NBR_INDIRECT | standings | Db | 25929 | position of standings | number_z=-0.60547 | 2004-07-25 | races:Db#724; drivers:Db#20 |
| 673 | DRIVER_NBR_INDIRECT | standings | Db | 25929 | wins of standings | number_z=-0.27148 | 2004-07-25 | races:Db#724; drivers:Db#20 |
| 674 | DRIVER_NBR_INDIRECT | standings | Db | 25929 | date of standings | 2004-07-25 | 2004-07-25 | races:Db#724; drivers:Db#20 |
| 675 | FULL_ONLY | races | Db | 724 | year of races | number_z=0.58984 | 2004-07-25 | circuits:Db#9 |
| 676 | FULL_ONLY | races | Db | 724 | round of races | number_z=0.69141 | 2004-07-25 | circuits:Db#9 |
| 677 | FULL_ONLY | races | Db | 724 | name of races | German Grand Prix | 2004-07-25 | circuits:Db#9 |
| 678 | FULL_ONLY | races | Db | 724 | date of races | 2004-07-25 | 2004-07-25 | circuits:Db#9 |
| 679 | FULL_ONLY | races | Db | 724 | time of races | 00:00:00 | 2004-07-25 | circuits:Db#9 |
| 680 | DRIVER_NBR_INDIRECT | standings | Db | 24156 | points of standings | number_z=-0.013794 | 1999-08-01 | races:Db#639; drivers:Db#20 |
| 681 | DRIVER_NBR_INDIRECT | standings | Db | 24156 | position of standings | number_z=-0.78516 | 1999-08-01 | races:Db#639; drivers:Db#20 |
| 682 | DRIVER_NBR_INDIRECT | standings | Db | 24156 | wins of standings | number_z=-0.27148 | 1999-08-01 | races:Db#639; drivers:Db#20 |
| 683 | DRIVER_NBR_INDIRECT | standings | Db | 24156 | date of standings | 1999-08-01 | 1999-08-01 | races:Db#639; drivers:Db#20 |
| 684 | DRIVER_NBR_INDIRECT | standings | Db | 25009 | points of standings | number_z=-0.1543 | 2001-09-30 | races:Db#678; drivers:Db#20 |
| 685 | DRIVER_NBR_INDIRECT | standings | Db | 25009 | position of standings | number_z=-0.54297 | 2001-09-30 | races:Db#678; drivers:Db#20 |
| 686 | DRIVER_NBR_INDIRECT | standings | Db | 25009 | wins of standings | number_z=-0.27148 | 2001-09-30 | races:Db#678; drivers:Db#20 |
| 687 | DRIVER_NBR_INDIRECT | standings | Db | 25009 | date of standings | 2001-09-30 | 2001-09-30 | races:Db#678; drivers:Db#20 |
| 688 | DRIVER_NBR_INDIRECT | standings | Db | 23229 | points of standings | number_z=-0.37891 | 1996-09-22 | races:Db#595; drivers:Db#20 |
| 689 | DRIVER_NBR_INDIRECT | standings | Db | 23229 | position of standings | number_z=-0.054688 | 1996-09-22 | races:Db#595; drivers:Db#20 |
| 690 | DRIVER_NBR_INDIRECT | standings | Db | 23229 | wins of standings | number_z=-0.27148 | 1996-09-22 | races:Db#595; drivers:Db#20 |
| 691 | DRIVER_NBR_INDIRECT | standings | Db | 23229 | date of standings | 1996-09-22 | 1996-09-22 | races:Db#595; drivers:Db#20 |
| 692 | FULL_ONLY | races | Db | 595 | year of races | number_z=0.19629 | 1996-09-22 | circuits:Db#26 |
| 693 | FULL_ONLY | races | Db | 595 | round of races | number_z=1.2812 | 1996-09-22 | circuits:Db#26 |
| 694 | FULL_ONLY | races | Db | 595 | name of races | Portuguese Grand Prix | 1996-09-22 | circuits:Db#26 |
| 695 | FULL_ONLY | races | Db | 595 | date of races | 1996-09-22 | 1996-09-22 | circuits:Db#26 |
| 696 | FULL_ONLY | races | Db | 595 | time of races | 00:00:00 | 1996-09-22 | circuits:Db#26 |
| 697 | FULL_ONLY | circuits | Db | 26 | circuitRef of circuits | estoril |  |  |
| 698 | FULL_ONLY | circuits | Db | 26 | name of circuits | Autódromo do Estoril |  |  |
| 699 | FULL_ONLY | circuits | Db | 26 | location of circuits | Estoril |  |  |
| 700 | FULL_ONLY | circuits | Db | 26 | country of circuits | Portugal |  |  |
| 701 | FULL_ONLY | circuits | Db | 26 | lat of circuits | number_z=0.23242 |  |  |
| 702 | FULL_ONLY | circuits | Db | 26 | lng of circuits | number_z=-0.16016 |  |  |
| 703 | FULL_ONLY | circuits | Db | 26 | alt of circuits | number_z=-0.32422 |  |  |
| 704 | DRIVER_NBR_INDIRECT | driver-dnf | Train | 7202 | date of driver-dnf | 2003-02-11 | 2003-02-11 | drivers:Db#20 |
| 705 | COL+DRIVER_NBR_INDIRECT | driver-dnf | Train | 7202 | did_not_finish of driver-dnf | 1 | 2003-02-11 | drivers:Db#20 |
| 706 | DRIVER_NBR_INDIRECT | standings | Db | 24901 | points of standings | number_z=-0.35156 | 2001-07-15 | races:Db#673; drivers:Db#20 |
| 707 | DRIVER_NBR_INDIRECT | standings | Db | 24901 | position of standings | number_z=-0.17676 | 2001-07-15 | races:Db#673; drivers:Db#20 |
| 708 | DRIVER_NBR_INDIRECT | standings | Db | 24901 | wins of standings | number_z=-0.27148 | 2001-07-15 | races:Db#673; drivers:Db#20 |
| 709 | DRIVER_NBR_INDIRECT | standings | Db | 24901 | date of standings | 2001-07-15 | 2001-07-15 | races:Db#673; drivers:Db#20 |
| 710 | DRIVER_NBR_INDIRECT | driver-dnf | Train | 7221 | date of driver-dnf | 2001-03-23 | 2001-03-23 | drivers:Db#20 |
| 711 | COL+DRIVER_NBR_INDIRECT | driver-dnf | Train | 7221 | did_not_finish of driver-dnf | 1 | 2001-03-23 | drivers:Db#20 |
| 712 | DRIVER_NBR_INDIRECT | results | Db | 15727 | number of results | number_z=-0.38672 | 1997-05-25 | races:Db#602; drivers:Db#20; constructors:Db#16 |
| 713 | DRIVER_NBR_INDIRECT | results | Db | 15727 | grid of results | number_z=-0.4375 | 1997-05-25 | races:Db#602; drivers:Db#20; constructors:Db#16 |
| 714 | DRIVER_NBR_INDIRECT | results | Db | 15727 | position of results | number_z=0.21484 | 1997-05-25 | races:Db#602; drivers:Db#20; constructors:Db#16 |
| 715 | DRIVER_NBR_INDIRECT | results | Db | 15727 | positionOrder of results | number_z=-0.5 | 1997-05-25 | races:Db#602; drivers:Db#20; constructors:Db#16 |
| 716 | DRIVER_NBR_INDIRECT | results | Db | 15727 | points of results | number_z=-0.45117 | 1997-05-25 | races:Db#602; drivers:Db#20; constructors:Db#16 |
| 717 | DRIVER_NBR_INDIRECT | results | Db | 15727 | laps of results | number_z=0.60156 | 1997-05-25 | races:Db#602; drivers:Db#20; constructors:Db#16 |
| 718 | DRIVER_NBR_INDIRECT | results | Db | 15727 | milliseconds of results | number_z=-0.42969 | 1997-05-25 | races:Db#602; drivers:Db#20; constructors:Db#16 |
| 719 | DRIVER_NBR_INDIRECT | results | Db | 15727 | statusId of results | number_z=-0.62891 | 1997-05-25 | races:Db#602; drivers:Db#20; constructors:Db#16 |
| 720 | DRIVER_NBR_INDIRECT | results | Db | 15727 | date of results | 1997-05-25 | 1997-05-25 | races:Db#602; drivers:Db#20; constructors:Db#16 |
| 721 | FULL_ONLY | races | Db | 602 | year of races | number_z=0.24512 | 1997-05-25 | circuits:Db#3 |
| 722 | FULL_ONLY | races | Db | 602 | round of races | number_z=-0.49023 | 1997-05-25 | circuits:Db#3 |
| 723 | FULL_ONLY | races | Db | 602 | name of races | Spanish Grand Prix | 1997-05-25 | circuits:Db#3 |
| 724 | FULL_ONLY | races | Db | 602 | date of races | 1997-05-25 | 1997-05-25 | circuits:Db#3 |
| 725 | FULL_ONLY | races | Db | 602 | time of races | 00:00:00 | 1997-05-25 | circuits:Db#3 |
| 726 | DRIVER_NBR_INDIRECT | standings | Db | 25035 | points of standings | number_z=-0.1543 | 2001-10-14 | races:Db#679; drivers:Db#20 |
| 727 | DRIVER_NBR_INDIRECT | standings | Db | 25035 | position of standings | number_z=-0.54297 | 2001-10-14 | races:Db#679; drivers:Db#20 |
| 728 | DRIVER_NBR_INDIRECT | standings | Db | 25035 | wins of standings | number_z=-0.27148 | 2001-10-14 | races:Db#679; drivers:Db#20 |
| 729 | DRIVER_NBR_INDIRECT | standings | Db | 25035 | date of standings | 2001-10-14 | 2001-10-14 | races:Db#679; drivers:Db#20 |
| 730 | FULL_ONLY | races | Db | 679 | year of races | number_z=0.44336 | 2001-10-14 | circuits:Db#21 |
| 731 | FULL_ONLY | races | Db | 679 | round of races | number_z=1.6719 | 2001-10-14 | circuits:Db#21 |
| 732 | FULL_ONLY | races | Db | 679 | name of races | Japanese Grand Prix | 2001-10-14 | circuits:Db#21 |
| 733 | FULL_ONLY | races | Db | 679 | date of races | 2001-10-14 | 2001-10-14 | circuits:Db#21 |
| 734 | FULL_ONLY | races | Db | 679 | time of races | 00:00:00 | 2001-10-14 | circuits:Db#21 |
| 735 | DRIVER_NBR_INDIRECT | results | Db | 17769 | number of results | number_z=-0.58203 | 2002-10-13 | races:Db#696; drivers:Db#20; constructors:Db#16 |
| 736 | DRIVER_NBR_INDIRECT | results | Db | 17769 | grid of results | number_z=-0.4375 | 2002-10-13 | races:Db#696; drivers:Db#20; constructors:Db#16 |
| 737 | DRIVER_NBR_INDIRECT | results | Db | 17769 | positionOrder of results | number_z=0.018921 | 2002-10-13 | races:Db#696; drivers:Db#20; constructors:Db#16 |
| 738 | DRIVER_NBR_INDIRECT | results | Db | 17769 | points of results | number_z=-0.45117 | 2002-10-13 | races:Db#696; drivers:Db#20; constructors:Db#16 |
| 739 | DRIVER_NBR_INDIRECT | results | Db | 17769 | laps of results | number_z=-0.30469 | 2002-10-13 | races:Db#696; drivers:Db#20; constructors:Db#16 |
| 740 | DRIVER_NBR_INDIRECT | results | Db | 17769 | statusId of results | number_z=-0.47656 | 2002-10-13 | races:Db#696; drivers:Db#20; constructors:Db#16 |
| 741 | DRIVER_NBR_INDIRECT | results | Db | 17769 | date of results | 2002-10-13 | 2002-10-13 | races:Db#696; drivers:Db#20; constructors:Db#16 |
| 742 | FULL_ONLY | races | Db | 696 | year of races | number_z=0.49219 | 2002-10-13 | circuits:Db#21 |
| 743 | FULL_ONLY | races | Db | 696 | round of races | number_z=1.6719 | 2002-10-13 | circuits:Db#21 |
| 744 | FULL_ONLY | races | Db | 696 | name of races | Japanese Grand Prix | 2002-10-13 | circuits:Db#21 |
| 745 | FULL_ONLY | races | Db | 696 | date of races | 2002-10-13 | 2002-10-13 | circuits:Db#21 |
| 746 | FULL_ONLY | races | Db | 696 | time of races | 00:00:00 | 2002-10-13 | circuits:Db#21 |
| 747 | DRIVER_NBR_INDIRECT | standings | Db | 24736 | points of standings | number_z=-0.35156 | 2001-04-15 | races:Db#666; drivers:Db#20 |
| 748 | DRIVER_NBR_INDIRECT | standings | Db | 24736 | position of standings | number_z=-0.60547 | 2001-04-15 | races:Db#666; drivers:Db#20 |
| 749 | DRIVER_NBR_INDIRECT | standings | Db | 24736 | wins of standings | number_z=-0.27148 | 2001-04-15 | races:Db#666; drivers:Db#20 |
| 750 | DRIVER_NBR_INDIRECT | standings | Db | 24736 | date of standings | 2001-04-15 | 2001-04-15 | races:Db#666; drivers:Db#20 |
| 751 | FULL_ONLY | races | Db | 666 | year of races | number_z=0.44336 | 2001-04-15 | circuits:Db#20 |
| 752 | FULL_ONLY | races | Db | 666 | round of races | number_z=-0.88281 | 2001-04-15 | circuits:Db#20 |
| 753 | FULL_ONLY | races | Db | 666 | name of races | San Marino Grand Prix | 2001-04-15 | circuits:Db#20 |
| 754 | FULL_ONLY | races | Db | 666 | date of races | 2001-04-15 | 2001-04-15 | circuits:Db#20 |
| 755 | FULL_ONLY | races | Db | 666 | time of races | 00:00:00 | 2001-04-15 | circuits:Db#20 |
| 756 | DRIVER_NBR_INDIRECT | results | Db | 15860 | number of results | number_z=-0.38672 | 1997-08-24 | races:Db#608; drivers:Db#20; constructors:Db#16 |
| 757 | DRIVER_NBR_INDIRECT | results | Db | 15860 | grid of results | number_z=-0.99219 | 1997-08-24 | races:Db#608; drivers:Db#20; constructors:Db#16 |
| 758 | DRIVER_NBR_INDIRECT | results | Db | 15860 | position of results | number_z=-1.2422 | 1997-08-24 | races:Db#608; drivers:Db#20; constructors:Db#16 |
| 759 | DRIVER_NBR_INDIRECT | results | Db | 15860 | positionOrder of results | number_z=-1.4062 | 1997-08-24 | races:Db#608; drivers:Db#20; constructors:Db#16 |
| 760 | DRIVER_NBR_INDIRECT | results | Db | 15860 | points of results | number_z=0.96875 | 1997-08-24 | races:Db#608; drivers:Db#20; constructors:Db#16 |
| 761 | DRIVER_NBR_INDIRECT | results | Db | 15860 | laps of results | number_z=-0.069824 | 1997-08-24 | races:Db#608; drivers:Db#20; constructors:Db#16 |
| 762 | DRIVER_NBR_INDIRECT | results | Db | 15860 | milliseconds of results | number_z=-0.33984 | 1997-08-24 | races:Db#608; drivers:Db#20; constructors:Db#16 |
| 763 | DRIVER_NBR_INDIRECT | results | Db | 15860 | statusId of results | number_z=-0.62891 | 1997-08-24 | races:Db#608; drivers:Db#20; constructors:Db#16 |
| 764 | DRIVER_NBR_INDIRECT | results | Db | 15860 | date of results | 1997-08-24 | 1997-08-24 | races:Db#608; drivers:Db#20; constructors:Db#16 |
| 765 | FULL_ONLY | races | Db | 608 | year of races | number_z=0.24512 | 1997-08-24 | circuits:Db#12 |
| 766 | FULL_ONLY | races | Db | 608 | round of races | number_z=0.69141 | 1997-08-24 | circuits:Db#12 |
| 767 | FULL_ONLY | races | Db | 608 | name of races | Belgian Grand Prix | 1997-08-24 | circuits:Db#12 |
| 768 | FULL_ONLY | races | Db | 608 | date of races | 1997-08-24 | 1997-08-24 | circuits:Db#12 |
| 769 | FULL_ONLY | races | Db | 608 | time of races | 00:00:00 | 1997-08-24 | circuits:Db#12 |
| 770 | DRIVER_NBR_INDIRECT | standings | Db | 25894 | points of standings | number_z=-0.098145 | 2004-07-04 | races:Db#722; drivers:Db#20 |
| 771 | DRIVER_NBR_INDIRECT | standings | Db | 25894 | position of standings | number_z=-0.60547 | 2004-07-04 | races:Db#722; drivers:Db#20 |
| 772 | DRIVER_NBR_INDIRECT | standings | Db | 25894 | wins of standings | number_z=-0.27148 | 2004-07-04 | races:Db#722; drivers:Db#20 |
| 773 | DRIVER_NBR_INDIRECT | standings | Db | 25894 | date of standings | 2004-07-04 | 2004-07-04 | races:Db#722; drivers:Db#20 |
| 774 | FULL_ONLY | races | Db | 722 | year of races | number_z=0.58984 | 2004-07-04 | circuits:Db#7 |
| 775 | FULL_ONLY | races | Db | 722 | round of races | number_z=0.29688 | 2004-07-04 | circuits:Db#7 |
| 776 | FULL_ONLY | races | Db | 722 | name of races | French Grand Prix | 2004-07-04 | circuits:Db#7 |
| 777 | FULL_ONLY | races | Db | 722 | date of races | 2004-07-04 | 2004-07-04 | circuits:Db#7 |
| 778 | FULL_ONLY | races | Db | 722 | time of races | 00:00:00 | 2004-07-04 | circuits:Db#7 |
| 779 | DRIVER_NBR_INDIRECT | standings | Db | 23788 | points of standings | number_z=-0.013794 | 1998-06-28 | races:Db#621; drivers:Db#20 |
| 780 | DRIVER_NBR_INDIRECT | standings | Db | 23788 | position of standings | number_z=-0.84766 | 1998-06-28 | races:Db#621; drivers:Db#20 |
| 781 | DRIVER_NBR_INDIRECT | standings | Db | 23788 | wins of standings | number_z=-0.27148 | 1998-06-28 | races:Db#621; drivers:Db#20 |
| 782 | DRIVER_NBR_INDIRECT | standings | Db | 23788 | date of standings | 1998-06-28 | 1998-06-28 | races:Db#621; drivers:Db#20 |
| 783 | FULL_ONLY | races | Db | 621 | year of races | number_z=0.29492 | 1998-06-28 | circuits:Db#7 |
| 784 | FULL_ONLY | races | Db | 621 | round of races | number_z=-0.097168 | 1998-06-28 | circuits:Db#7 |
| 785 | FULL_ONLY | races | Db | 621 | name of races | French Grand Prix | 1998-06-28 | circuits:Db#7 |
| 786 | FULL_ONLY | races | Db | 621 | date of races | 1998-06-28 | 1998-06-28 | circuits:Db#7 |
| 787 | FULL_ONLY | races | Db | 621 | time of races | 00:00:00 | 1998-06-28 | circuits:Db#7 |
| 788 | DRIVER_NBR_INDIRECT | results | Db | 15651 | number of results | number_z=-0.38672 | 1997-04-13 | races:Db#599; drivers:Db#20; constructors:Db#16 |
| 789 | DRIVER_NBR_INDIRECT | results | Db | 15651 | grid of results | number_z=-0.29883 | 1997-04-13 | races:Db#599; drivers:Db#20; constructors:Db#16 |
| 790 | DRIVER_NBR_INDIRECT | results | Db | 15651 | positionOrder of results | number_z=0.53906 | 1997-04-13 | races:Db#599; drivers:Db#20; constructors:Db#16 |
| 791 | DRIVER_NBR_INDIRECT | results | Db | 15651 | points of results | number_z=-0.45117 | 1997-04-13 | races:Db#599; drivers:Db#20; constructors:Db#16 |
| 792 | DRIVER_NBR_INDIRECT | results | Db | 15651 | laps of results | number_z=-0.74219 | 1997-04-13 | races:Db#599; drivers:Db#20; constructors:Db#16 |
| 793 | DRIVER_NBR_INDIRECT | results | Db | 15651 | statusId of results | number_z=-0.51562 | 1997-04-13 | races:Db#599; drivers:Db#20; constructors:Db#16 |
| 794 | DRIVER_NBR_INDIRECT | results | Db | 15651 | date of results | 1997-04-13 | 1997-04-13 | races:Db#599; drivers:Db#20; constructors:Db#16 |
| 795 | FULL_ONLY | races | Db | 599 | year of races | number_z=0.24512 | 1997-04-13 | circuits:Db#24 |
| 796 | FULL_ONLY | races | Db | 599 | round of races | number_z=-1.0781 | 1997-04-13 | circuits:Db#24 |
| 797 | FULL_ONLY | races | Db | 599 | name of races | Argentine Grand Prix | 1997-04-13 | circuits:Db#24 |
| 798 | FULL_ONLY | races | Db | 599 | date of races | 1997-04-13 | 1997-04-13 | circuits:Db#24 |
| 799 | FULL_ONLY | races | Db | 599 | time of races | 00:00:00 | 1997-04-13 | circuits:Db#24 |
| 800 | DRIVER_NBR_INDIRECT | qualifying | Db | 1685 | number of qualifying | number_z=-0.39844 | 2003-05-31 | races:Db#703; drivers:Db#20; constructors:Db#16 |
| 801 | DRIVER_NBR_INDIRECT | qualifying | Db | 1685 | position of qualifying | number_z=0.12012 | 2003-05-31 | races:Db#703; drivers:Db#20; constructors:Db#16 |
| 802 | DRIVER_NBR_INDIRECT | qualifying | Db | 1685 | date of qualifying | 2003-05-31 | 2003-05-31 | races:Db#703; drivers:Db#20; constructors:Db#16 |
| 803 | FULL_ONLY | races | Db | 703 | year of races | number_z=0.53906 | 2003-06-01 | circuits:Db#5 |
| 804 | FULL_ONLY | races | Db | 703 | round of races | number_z=-0.29492 | 2003-06-01 | circuits:Db#5 |
| 805 | FULL_ONLY | races | Db | 703 | name of races | Monaco Grand Prix | 2003-06-01 | circuits:Db#5 |
| 806 | FULL_ONLY | races | Db | 703 | date of races | 2003-06-01 | 2003-06-01 | circuits:Db#5 |
| 807 | FULL_ONLY | races | Db | 703 | time of races | 00:00:00 | 2003-06-01 | circuits:Db#5 |
| 808 | DRIVER_NBR_INDIRECT | standings | Db | 25153 | points of standings | number_z=-0.32227 | 2002-05-12 | races:Db#685; drivers:Db#20 |
| 809 | DRIVER_NBR_INDIRECT | standings | Db | 25153 | position of standings | number_z=-0.48242 | 2002-05-12 | races:Db#685; drivers:Db#20 |
| 810 | DRIVER_NBR_INDIRECT | standings | Db | 25153 | wins of standings | number_z=-0.27148 | 2002-05-12 | races:Db#685; drivers:Db#20 |
| 811 | DRIVER_NBR_INDIRECT | standings | Db | 25153 | date of standings | 2002-05-12 | 2002-05-12 | races:Db#685; drivers:Db#20 |
| 812 | FULL_ONLY | races | Db | 685 | year of races | number_z=0.49219 | 2002-05-12 | circuits:Db#69 |
| 813 | FULL_ONLY | races | Db | 685 | round of races | number_z=-0.49023 | 2002-05-12 | circuits:Db#69 |
| 814 | FULL_ONLY | races | Db | 685 | name of races | Austrian Grand Prix | 2002-05-12 | circuits:Db#69 |
| 815 | FULL_ONLY | races | Db | 685 | date of races | 2002-05-12 | 2002-05-12 | circuits:Db#69 |
| 816 | FULL_ONLY | races | Db | 685 | time of races | 00:00:00 | 2002-05-12 | circuits:Db#69 |
| 817 | DRIVER_NBR_INDIRECT | driver-dnf | Train | 6505 | date of driver-dnf | 2000-02-27 | 2000-02-27 | drivers:Db#20 |
| 818 | COL+DRIVER_NBR_INDIRECT | driver-dnf | Train | 6505 | did_not_finish of driver-dnf | 0 | 2000-02-27 | drivers:Db#20 |
| 819 | DRIVER_NBR_INDIRECT | driver-dnf | Train | 9265 | date of driver-dnf | 2004-06-05 | 2004-06-05 | drivers:Db#20 |
| 820 | COL+DRIVER_NBR_INDIRECT | driver-dnf | Train | 9265 | did_not_finish of driver-dnf | 1 | 2004-06-05 | drivers:Db#20 |
| 821 | DRIVER_NBR_INDIRECT | qualifying | Db | 1145 | number of qualifying | number_z=-0.3418 | 1997-07-12 | races:Db#605; drivers:Db#20; constructors:Db#16 |
| 822 | DRIVER_NBR_INDIRECT | qualifying | Db | 1145 | position of qualifying | number_z=-0.19824 | 1997-07-12 | races:Db#605; drivers:Db#20; constructors:Db#16 |
| 823 | DRIVER_NBR_INDIRECT | qualifying | Db | 1145 | date of qualifying | 1997-07-12 | 1997-07-12 | races:Db#605; drivers:Db#20; constructors:Db#16 |
| 824 | FULL_ONLY | races | Db | 605 | year of races | number_z=0.24512 | 1997-07-13 | circuits:Db#8 |
| 825 | FULL_ONLY | races | Db | 605 | round of races | number_z=0.099609 | 1997-07-13 | circuits:Db#8 |
| 826 | FULL_ONLY | races | Db | 605 | name of races | British Grand Prix | 1997-07-13 | circuits:Db#8 |
| 827 | FULL_ONLY | races | Db | 605 | date of races | 1997-07-13 | 1997-07-13 | circuits:Db#8 |
| 828 | FULL_ONLY | races | Db | 605 | time of races | 00:00:00 | 1997-07-13 | circuits:Db#8 |
| 829 | DRIVER_NBR_INDIRECT | driver-dnf | Train | 10038 | date of driver-dnf | 1997-08-11 | 1997-08-11 | drivers:Db#20 |
| 830 | COL+DRIVER_NBR_INDIRECT | driver-dnf | Train | 10038 | did_not_finish of driver-dnf | 0 | 1997-08-11 | drivers:Db#20 |
| 831 | DRIVER_NBR_INDIRECT | results | Db | 15752 | number of results | number_z=-0.38672 | 1997-06-15 | races:Db#603; drivers:Db#20; constructors:Db#16 |
| 832 | DRIVER_NBR_INDIRECT | results | Db | 15752 | grid of results | number_z=-0.71484 | 1997-06-15 | races:Db#603; drivers:Db#20; constructors:Db#16 |
| 833 | DRIVER_NBR_INDIRECT | results | Db | 15752 | position of results | number_z=-1.0312 | 1997-06-15 | races:Db#603; drivers:Db#20; constructors:Db#16 |
| 834 | DRIVER_NBR_INDIRECT | results | Db | 15752 | positionOrder of results | number_z=-1.2812 | 1997-06-15 | races:Db#603; drivers:Db#20; constructors:Db#16 |
| 835 | DRIVER_NBR_INDIRECT | results | Db | 15752 | points of results | number_z=0.49609 | 1997-06-15 | races:Db#603; drivers:Db#20; constructors:Db#16 |
| 836 | DRIVER_NBR_INDIRECT | results | Db | 15752 | laps of results | number_z=0.26562 | 1997-06-15 | races:Db#603; drivers:Db#20; constructors:Db#16 |
| 837 | DRIVER_NBR_INDIRECT | results | Db | 15752 | milliseconds of results | number_z=-0.93359 | 1997-06-15 | races:Db#603; drivers:Db#20; constructors:Db#16 |
| 838 | DRIVER_NBR_INDIRECT | results | Db | 15752 | statusId of results | number_z=-0.62891 | 1997-06-15 | races:Db#603; drivers:Db#20; constructors:Db#16 |
| 839 | DRIVER_NBR_INDIRECT | results | Db | 15752 | date of results | 1997-06-15 | 1997-06-15 | races:Db#603; drivers:Db#20; constructors:Db#16 |
| 840 | FULL_ONLY | races | Db | 603 | year of races | number_z=0.24512 | 1997-06-15 | circuits:Db#6 |
| 841 | FULL_ONLY | races | Db | 603 | round of races | number_z=-0.29492 | 1997-06-15 | circuits:Db#6 |
| 842 | FULL_ONLY | races | Db | 603 | name of races | Canadian Grand Prix | 1997-06-15 | circuits:Db#6 |
| 843 | FULL_ONLY | races | Db | 603 | date of races | 1997-06-15 | 1997-06-15 | circuits:Db#6 |
| 844 | FULL_ONLY | races | Db | 603 | time of races | 00:00:00 | 1997-06-15 | circuits:Db#6 |
| 845 | FULL_ONLY | circuits | Db | 6 | circuitRef of circuits | villeneuve |  |  |
| 846 | FULL_ONLY | circuits | Db | 6 | name of circuits | Circuit Gilles Villeneuve |  |  |
| 847 | FULL_ONLY | circuits | Db | 6 | location of circuits | Montreal |  |  |
| 848 | FULL_ONLY | circuits | Db | 6 | country of circuits | Canada |  |  |
| 849 | FULL_ONLY | circuits | Db | 6 | lat of circuits | number_z=0.52734 |  |  |
| 850 | FULL_ONLY | circuits | Db | 6 | lng of circuits | number_z=-1.1406 |  |  |
| 851 | FULL_ONLY | circuits | Db | 6 | alt of circuits | number_z=-0.64453 |  |  |
| 852 | DRIVER_NBR_INDIRECT | standings | Db | 23077 | points of standings | number_z=-0.37891 | 1996-06-30 | races:Db#589; drivers:Db#20 |
| 853 | DRIVER_NBR_INDIRECT | standings | Db | 23077 | position of standings | number_z=-0.17676 | 1996-06-30 | races:Db#589; drivers:Db#20 |
| 854 | DRIVER_NBR_INDIRECT | standings | Db | 23077 | wins of standings | number_z=-0.27148 | 1996-06-30 | races:Db#589; drivers:Db#20 |
| 855 | DRIVER_NBR_INDIRECT | standings | Db | 23077 | date of standings | 1996-06-30 | 1996-06-30 | races:Db#589; drivers:Db#20 |
| 856 | FULL_ONLY | races | Db | 589 | year of races | number_z=0.19629 | 1996-06-30 | circuits:Db#7 |
| 857 | FULL_ONLY | races | Db | 589 | round of races | number_z=0.099609 | 1996-06-30 | circuits:Db#7 |
| 858 | FULL_ONLY | races | Db | 589 | name of races | French Grand Prix | 1996-06-30 | circuits:Db#7 |
| 859 | FULL_ONLY | races | Db | 589 | date of races | 1996-06-30 | 1996-06-30 | circuits:Db#7 |
| 860 | FULL_ONLY | races | Db | 589 | time of races | 00:00:00 | 1996-06-30 | circuits:Db#7 |
| 861 | DRIVER_NBR_INDIRECT | qualifying | Db | 1407 | number of qualifying | number_z=-0.39844 | 2000-03-11 | races:Db#646; drivers:Db#20; constructors:Db#21 |
| 862 | DRIVER_NBR_INDIRECT | qualifying | Db | 1407 | position of qualifying | number_z=-0.35742 | 2000-03-11 | races:Db#646; drivers:Db#20; constructors:Db#21 |
| 863 | DRIVER_NBR_INDIRECT | qualifying | Db | 1407 | date of qualifying | 2000-03-11 | 2000-03-11 | races:Db#646; drivers:Db#20; constructors:Db#21 |
| 864 | FULL_ONLY | races | Db | 646 | year of races | number_z=0.39258 | 2000-03-12 | circuits:Db#0 |
| 865 | FULL_ONLY | races | Db | 646 | round of races | number_z=-1.4766 | 2000-03-12 | circuits:Db#0 |
| 866 | FULL_ONLY | races | Db | 646 | name of races | Australian Grand Prix | 2000-03-12 | circuits:Db#0 |
| 867 | FULL_ONLY | races | Db | 646 | date of races | 2000-03-12 | 2000-03-12 | circuits:Db#0 |
| 868 | FULL_ONLY | races | Db | 646 | time of races | 00:00:00 | 2000-03-12 | circuits:Db#0 |
| 869 | DRIVER_NBR_INDIRECT | standings | Db | 24716 | points of standings | number_z=-0.35156 | 2001-04-01 | races:Db#665; drivers:Db#20 |
| 870 | DRIVER_NBR_INDIRECT | standings | Db | 24716 | position of standings | number_z=-0.66406 | 2001-04-01 | races:Db#665; drivers:Db#20 |
| 871 | DRIVER_NBR_INDIRECT | standings | Db | 24716 | wins of standings | number_z=-0.27148 | 2001-04-01 | races:Db#665; drivers:Db#20 |
| 872 | DRIVER_NBR_INDIRECT | standings | Db | 24716 | date of standings | 2001-04-01 | 2001-04-01 | races:Db#665; drivers:Db#20 |
| 873 | FULL_ONLY | races | Db | 665 | year of races | number_z=0.44336 | 2001-04-01 | circuits:Db#17 |
| 874 | FULL_ONLY | races | Db | 665 | round of races | number_z=-1.0781 | 2001-04-01 | circuits:Db#17 |
| 875 | FULL_ONLY | races | Db | 665 | name of races | Brazilian Grand Prix | 2001-04-01 | circuits:Db#17 |
| 876 | FULL_ONLY | races | Db | 665 | date of races | 2001-04-01 | 2001-04-01 | circuits:Db#17 |
| 877 | FULL_ONLY | races | Db | 665 | time of races | 00:00:00 | 2001-04-01 | circuits:Db#17 |
| 878 | DRIVER_NBR_INDIRECT | standings | Db | 23341 | points of standings | number_z=-0.26562 | 1997-05-11 | races:Db#601; drivers:Db#20 |
| 879 | DRIVER_NBR_INDIRECT | standings | Db | 23341 | position of standings | number_z=-0.54297 | 1997-05-11 | races:Db#601; drivers:Db#20 |
| 880 | DRIVER_NBR_INDIRECT | standings | Db | 23341 | wins of standings | number_z=-0.27148 | 1997-05-11 | races:Db#601; drivers:Db#20 |
| 881 | DRIVER_NBR_INDIRECT | standings | Db | 23341 | date of standings | 1997-05-11 | 1997-05-11 | races:Db#601; drivers:Db#20 |
| 882 | FULL_ONLY | races | Db | 601 | year of races | number_z=0.24512 | 1997-05-11 | circuits:Db#5 |
| 883 | FULL_ONLY | races | Db | 601 | round of races | number_z=-0.6875 | 1997-05-11 | circuits:Db#5 |
| 884 | FULL_ONLY | races | Db | 601 | name of races | Monaco Grand Prix | 1997-05-11 | circuits:Db#5 |
| 885 | FULL_ONLY | races | Db | 601 | date of races | 1997-05-11 | 1997-05-11 | circuits:Db#5 |
| 886 | FULL_ONLY | races | Db | 601 | time of races | 00:00:00 | 1997-05-11 | circuits:Db#5 |
| 887 | DRIVER_NBR_INDIRECT | qualifying | Db | 921 | number of qualifying | number_z=0.16113 | 1996-05-18 | races:Db#586; drivers:Db#20; constructors:Db#17 |
| 888 | DRIVER_NBR_INDIRECT | qualifying | Db | 921 | position of qualifying | number_z=1.0703 | 1996-05-18 | races:Db#586; drivers:Db#20; constructors:Db#17 |
| 889 | DRIVER_NBR_INDIRECT | qualifying | Db | 921 | date of qualifying | 1996-05-18 | 1996-05-18 | races:Db#586; drivers:Db#20; constructors:Db#17 |
| 890 | FULL_ONLY | races | Db | 586 | year of races | number_z=0.19629 | 1996-05-19 | circuits:Db#5 |
| 891 | FULL_ONLY | races | Db | 586 | round of races | number_z=-0.49023 | 1996-05-19 | circuits:Db#5 |
| 892 | FULL_ONLY | races | Db | 586 | name of races | Monaco Grand Prix | 1996-05-19 | circuits:Db#5 |
| 893 | FULL_ONLY | races | Db | 586 | date of races | 1996-05-19 | 1996-05-19 | circuits:Db#5 |
| 894 | FULL_ONLY | races | Db | 586 | time of races | 00:00:00 | 1996-05-19 | circuits:Db#5 |
| 895 | DRIVER_NBR_INDIRECT | qualifying | Db | 1343 | number of qualifying | number_z=-0.51172 | 1999-03-06 | races:Db#630; drivers:Db#20; constructors:Db#21 |
| 896 | DRIVER_NBR_INDIRECT | qualifying | Db | 1343 | position of qualifying | number_z=-0.67578 | 1999-03-06 | races:Db#630; drivers:Db#20; constructors:Db#21 |
| 897 | DRIVER_NBR_INDIRECT | qualifying | Db | 1343 | date of qualifying | 1999-03-06 | 1999-03-06 | races:Db#630; drivers:Db#20; constructors:Db#21 |
| 898 | DRIVER_NBR_INDIRECT | results | Db | 17145 | number of results | number_z=-0.71484 | 2001-04-29 | races:Db#667; drivers:Db#20; constructors:Db#21 |
| 899 | DRIVER_NBR_INDIRECT | results | Db | 17145 | grid of results | number_z=1.0859 | 2001-04-29 | races:Db#667; drivers:Db#20; constructors:Db#21 |
| 900 | DRIVER_NBR_INDIRECT | results | Db | 17145 | position of results | number_z=1.25 | 2001-04-29 | races:Db#667; drivers:Db#20; constructors:Db#21 |
| 901 | DRIVER_NBR_INDIRECT | results | Db | 17145 | positionOrder of results | number_z=0.14844 | 2001-04-29 | races:Db#667; drivers:Db#20; constructors:Db#21 |
| 902 | DRIVER_NBR_INDIRECT | results | Db | 17145 | points of results | number_z=-0.45117 | 2001-04-29 | races:Db#667; drivers:Db#20; constructors:Db#21 |
| 903 | DRIVER_NBR_INDIRECT | results | Db | 17145 | laps of results | number_z=0.57031 | 2001-04-29 | races:Db#667; drivers:Db#20; constructors:Db#21 |
| 904 | DRIVER_NBR_INDIRECT | results | Db | 17145 | statusId of results | number_z=-0.20996 | 2001-04-29 | races:Db#667; drivers:Db#20; constructors:Db#21 |
| 905 | DRIVER_NBR_INDIRECT | results | Db | 17145 | date of results | 2001-04-29 | 2001-04-29 | races:Db#667; drivers:Db#20; constructors:Db#21 |
| 906 | FULL_ONLY | races | Db | 667 | year of races | number_z=0.44336 | 2001-04-29 | circuits:Db#3 |
| 907 | FULL_ONLY | races | Db | 667 | round of races | number_z=-0.6875 | 2001-04-29 | circuits:Db#3 |
| 908 | FULL_ONLY | races | Db | 667 | name of races | Spanish Grand Prix | 2001-04-29 | circuits:Db#3 |
| 909 | FULL_ONLY | races | Db | 667 | date of races | 2001-04-29 | 2001-04-29 | circuits:Db#3 |
| 910 | FULL_ONLY | races | Db | 667 | time of races | 00:00:00 | 2001-04-29 | circuits:Db#3 |
| 911 | DRIVER_NBR_INDIRECT | standings | Db | 24136 | points of standings | number_z=-0.013794 | 1999-07-25 | races:Db#638; drivers:Db#20 |
| 912 | DRIVER_NBR_INDIRECT | standings | Db | 24136 | position of standings | number_z=-0.78516 | 1999-07-25 | races:Db#638; drivers:Db#20 |
| 913 | DRIVER_NBR_INDIRECT | standings | Db | 24136 | wins of standings | number_z=-0.27148 | 1999-07-25 | races:Db#638; drivers:Db#20 |
| 914 | DRIVER_NBR_INDIRECT | standings | Db | 24136 | date of standings | 1999-07-25 | 1999-07-25 | races:Db#638; drivers:Db#20 |
| 915 | FULL_ONLY | races | Db | 638 | year of races | number_z=0.34375 | 1999-07-25 | circuits:Db#69 |
| 916 | FULL_ONLY | races | Db | 638 | round of races | number_z=0.099609 | 1999-07-25 | circuits:Db#69 |
| 917 | FULL_ONLY | races | Db | 638 | name of races | Austrian Grand Prix | 1999-07-25 | circuits:Db#69 |
| 918 | FULL_ONLY | races | Db | 638 | date of races | 1999-07-25 | 1999-07-25 | circuits:Db#69 |
| 919 | FULL_ONLY | races | Db | 638 | time of races | 00:00:00 | 1999-07-25 | circuits:Db#69 |
| 920 | DRIVER_NBR_INDIRECT | standings | Db | 25663 | points of standings | number_z=-0.098145 | 2003-09-14 | races:Db#710; drivers:Db#20 |
| 921 | DRIVER_NBR_INDIRECT | standings | Db | 25663 | position of standings | number_z=-0.54297 | 2003-09-14 | races:Db#710; drivers:Db#20 |
| 922 | DRIVER_NBR_INDIRECT | standings | Db | 25663 | wins of standings | number_z=0.73438 | 2003-09-14 | races:Db#710; drivers:Db#20 |
| 923 | DRIVER_NBR_INDIRECT | standings | Db | 25663 | date of standings | 2003-09-14 | 2003-09-14 | races:Db#710; drivers:Db#20 |
| 924 | FULL_ONLY | races | Db | 710 | year of races | number_z=0.53906 | 2003-09-14 | circuits:Db#13 |
| 925 | FULL_ONLY | races | Db | 710 | round of races | number_z=1.0859 | 2003-09-14 | circuits:Db#13 |
| 926 | FULL_ONLY | races | Db | 710 | name of races | Italian Grand Prix | 2003-09-14 | circuits:Db#13 |
| 927 | FULL_ONLY | races | Db | 710 | date of races | 2003-09-14 | 2003-09-14 | circuits:Db#13 |
| 928 | FULL_ONLY | races | Db | 710 | time of races | 00:00:00 | 2003-09-14 | circuits:Db#13 |
| 929 | DRIVER_NBR_INDIRECT | qualifying | Db | 1977 | number of qualifying | number_z=-0.39844 | 2004-05-22 | races:Db#718; drivers:Db#20; constructors:Db#14 |
| 930 | DRIVER_NBR_INDIRECT | qualifying | Db | 1977 | position of qualifying | number_z=-0.038818 | 2004-05-22 | races:Db#718; drivers:Db#20; constructors:Db#14 |
| 931 | DRIVER_NBR_INDIRECT | qualifying | Db | 1977 | date of qualifying | 2004-05-22 | 2004-05-22 | races:Db#718; drivers:Db#20; constructors:Db#14 |
| 932 | DRIVER_NBR_INDIRECT | standings | Db | 25574 | points of standings | number_z=-0.098145 | 2003-07-06 | races:Db#706; drivers:Db#20 |
| 933 | DRIVER_NBR_INDIRECT | standings | Db | 25574 | position of standings | number_z=-0.60547 | 2003-07-06 | races:Db#706; drivers:Db#20 |
| 934 | DRIVER_NBR_INDIRECT | standings | Db | 25574 | wins of standings | number_z=0.73438 | 2003-07-06 | races:Db#706; drivers:Db#20 |
| 935 | DRIVER_NBR_INDIRECT | standings | Db | 25574 | date of standings | 2003-07-06 | 2003-07-06 | races:Db#706; drivers:Db#20 |
| 936 | DRIVER_NBR_INDIRECT | results | Db | 16038 | number of results | number_z=-0.84766 | 1998-04-12 | races:Db#616; drivers:Db#20; constructors:Db#21 |
| 937 | DRIVER_NBR_INDIRECT | results | Db | 16038 | grid of results | number_z=-0.16113 | 1998-04-12 | races:Db#616; drivers:Db#20; constructors:Db#21 |
| 938 | DRIVER_NBR_INDIRECT | results | Db | 16038 | position of results | number_z=-0.2002 | 1998-04-12 | races:Db#616; drivers:Db#20; constructors:Db#21 |
| 939 | DRIVER_NBR_INDIRECT | results | Db | 16038 | positionOrder of results | number_z=-0.76172 | 1998-04-12 | races:Db#616; drivers:Db#20; constructors:Db#21 |
| 940 | DRIVER_NBR_INDIRECT | results | Db | 16038 | points of results | number_z=-0.45117 | 1998-04-12 | races:Db#616; drivers:Db#20; constructors:Db#21 |
| 941 | DRIVER_NBR_INDIRECT | results | Db | 16038 | laps of results | number_z=0.87109 | 1998-04-12 | races:Db#616; drivers:Db#20; constructors:Db#21 |
| 942 | DRIVER_NBR_INDIRECT | results | Db | 16038 | milliseconds of results | number_z=0.23047 | 1998-04-12 | races:Db#616; drivers:Db#20; constructors:Db#21 |
| 943 | DRIVER_NBR_INDIRECT | results | Db | 16038 | statusId of results | number_z=-0.62891 | 1998-04-12 | races:Db#616; drivers:Db#20; constructors:Db#21 |
| 944 | DRIVER_NBR_INDIRECT | results | Db | 16038 | date of results | 1998-04-12 | 1998-04-12 | races:Db#616; drivers:Db#20; constructors:Db#21 |
| 945 | DRIVER_NBR_INDIRECT | standings | Db | 24295 | points of standings | number_z=-0.013794 | 1999-10-31 | races:Db#645; drivers:Db#20 |
| 946 | DRIVER_NBR_INDIRECT | standings | Db | 24295 | position of standings | number_z=-0.66406 | 1999-10-31 | races:Db#645; drivers:Db#20 |
| 947 | DRIVER_NBR_INDIRECT | standings | Db | 24295 | wins of standings | number_z=-0.27148 | 1999-10-31 | races:Db#645; drivers:Db#20 |
| 948 | DRIVER_NBR_INDIRECT | standings | Db | 24295 | date of standings | 1999-10-31 | 1999-10-31 | races:Db#645; drivers:Db#20 |
| 949 | DRIVER_NBR_INDIRECT | results | Db | 16997 | number of results | number_z=-0.45117 | 2000-09-24 | races:Db#660; drivers:Db#20; constructors:Db#21 |
| 950 | DRIVER_NBR_INDIRECT | results | Db | 16997 | grid of results | number_z=0.53125 | 2000-09-24 | races:Db#660; drivers:Db#20; constructors:Db#21 |
| 951 | DRIVER_NBR_INDIRECT | results | Db | 16997 | positionOrder of results | number_z=0.53906 | 2000-09-24 | races:Db#660; drivers:Db#20; constructors:Db#21 |
| 952 | DRIVER_NBR_INDIRECT | results | Db | 16997 | points of results | number_z=-0.45117 | 2000-09-24 | races:Db#660; drivers:Db#20; constructors:Db#21 |
| 953 | DRIVER_NBR_INDIRECT | results | Db | 16997 | laps of results | number_z=-0.069824 | 2000-09-24 | races:Db#660; drivers:Db#20; constructors:Db#21 |
| 954 | DRIVER_NBR_INDIRECT | results | Db | 16997 | statusId of results | number_z=-0.47656 | 2000-09-24 | races:Db#660; drivers:Db#20; constructors:Db#21 |
| 955 | DRIVER_NBR_INDIRECT | results | Db | 16997 | date of results | 2000-09-24 | 2000-09-24 | races:Db#660; drivers:Db#20; constructors:Db#21 |
| 956 | DRIVER_NBR_INDIRECT | standings | Db | 24334 | points of standings | number_z=-0.1543 | 2000-03-26 | races:Db#647; drivers:Db#20 |
| 957 | DRIVER_NBR_INDIRECT | standings | Db | 24334 | position of standings | number_z=-1.0938 | 2000-03-26 | races:Db#647; drivers:Db#20 |
| 958 | DRIVER_NBR_INDIRECT | standings | Db | 24334 | wins of standings | number_z=-0.27148 | 2000-03-26 | races:Db#647; drivers:Db#20 |
| 959 | DRIVER_NBR_INDIRECT | standings | Db | 24334 | date of standings | 2000-03-26 | 2000-03-26 | races:Db#647; drivers:Db#20 |
| 960 | FULL_ONLY | races | Db | 647 | year of races | number_z=0.39258 | 2000-03-26 | circuits:Db#17 |
| 961 | FULL_ONLY | races | Db | 647 | round of races | number_z=-1.2812 | 2000-03-26 | circuits:Db#17 |
| 962 | FULL_ONLY | races | Db | 647 | name of races | Brazilian Grand Prix | 2000-03-26 | circuits:Db#17 |
| 963 | FULL_ONLY | races | Db | 647 | date of races | 2000-03-26 | 2000-03-26 | circuits:Db#17 |
| 964 | FULL_ONLY | races | Db | 647 | time of races | 00:00:00 | 2000-03-26 | circuits:Db#17 |
| 965 | DRIVER_NBR_INDIRECT | results | Db | 15813 | number of results | number_z=-0.38672 | 1997-07-27 | races:Db#606; drivers:Db#20; constructors:Db#16 |
| 966 | DRIVER_NBR_INDIRECT | results | Db | 15813 | grid of results | number_z=-1.2656 | 1997-07-27 | races:Db#606; drivers:Db#20; constructors:Db#16 |
| 967 | DRIVER_NBR_INDIRECT | results | Db | 15813 | position of results | number_z=0.62891 | 1997-07-27 | races:Db#606; drivers:Db#20; constructors:Db#16 |
| 968 | DRIVER_NBR_INDIRECT | results | Db | 15813 | positionOrder of results | number_z=-0.24121 | 1997-07-27 | races:Db#606; drivers:Db#20; constructors:Db#16 |
| 969 | DRIVER_NBR_INDIRECT | results | Db | 15813 | points of results | number_z=-0.45117 | 1997-07-27 | races:Db#606; drivers:Db#20; constructors:Db#16 |
| 970 | DRIVER_NBR_INDIRECT | results | Db | 15813 | laps of results | number_z=-0.2041 | 1997-07-27 | races:Db#606; drivers:Db#20; constructors:Db#16 |
| 971 | DRIVER_NBR_INDIRECT | results | Db | 15813 | statusId of results | number_z=-0.094727 | 1997-07-27 | races:Db#606; drivers:Db#20; constructors:Db#16 |
| 972 | DRIVER_NBR_INDIRECT | results | Db | 15813 | date of results | 1997-07-27 | 1997-07-27 | races:Db#606; drivers:Db#20; constructors:Db#16 |
| 973 | FULL_ONLY | races | Db | 606 | year of races | number_z=0.24512 | 1997-07-27 | circuits:Db#9 |
| 974 | FULL_ONLY | races | Db | 606 | round of races | number_z=0.29688 | 1997-07-27 | circuits:Db#9 |
| 975 | FULL_ONLY | races | Db | 606 | name of races | German Grand Prix | 1997-07-27 | circuits:Db#9 |
| 976 | FULL_ONLY | races | Db | 606 | date of races | 1997-07-27 | 1997-07-27 | circuits:Db#9 |
| 977 | FULL_ONLY | races | Db | 606 | time of races | 00:00:00 | 1997-07-27 | circuits:Db#9 |
| 978 | DRIVER_NBR_INDIRECT | results | Db | 17408 | number of results | number_z=-0.71484 | 2001-10-14 | races:Db#679; drivers:Db#20; constructors:Db#21 |
| 979 | DRIVER_NBR_INDIRECT | results | Db | 17408 | grid of results | number_z=-0.71484 | 2001-10-14 | races:Db#679; drivers:Db#20; constructors:Db#21 |
| 980 | DRIVER_NBR_INDIRECT | results | Db | 17408 | position of results | number_z=1.875 | 2001-10-14 | races:Db#679; drivers:Db#20; constructors:Db#21 |
| 981 | DRIVER_NBR_INDIRECT | results | Db | 17408 | positionOrder of results | number_z=0.53906 | 2001-10-14 | races:Db#679; drivers:Db#20; constructors:Db#21 |
| 982 | DRIVER_NBR_INDIRECT | results | Db | 17408 | points of results | number_z=-0.45117 | 2001-10-14 | races:Db#679; drivers:Db#20; constructors:Db#21 |
| 983 | DRIVER_NBR_INDIRECT | results | Db | 17408 | laps of results | number_z=0.031006 | 2001-10-14 | races:Db#679; drivers:Db#20; constructors:Db#21 |
| 984 | DRIVER_NBR_INDIRECT | results | Db | 17408 | statusId of results | number_z=-0.43945 | 2001-10-14 | races:Db#679; drivers:Db#20; constructors:Db#21 |
| 985 | DRIVER_NBR_INDIRECT | results | Db | 17408 | date of results | 2001-10-14 | 2001-10-14 | races:Db#679; drivers:Db#20; constructors:Db#21 |
| 986 | DRIVER_NBR_INDIRECT | standings | Db | 24355 | points of standings | number_z=-0.1543 | 2000-04-09 | races:Db#648; drivers:Db#20 |
| 987 | DRIVER_NBR_INDIRECT | standings | Db | 24355 | position of standings | number_z=-1.0312 | 2000-04-09 | races:Db#648; drivers:Db#20 |
| 988 | DRIVER_NBR_INDIRECT | standings | Db | 24355 | wins of standings | number_z=-0.27148 | 2000-04-09 | races:Db#648; drivers:Db#20 |
| 989 | DRIVER_NBR_INDIRECT | standings | Db | 24355 | date of standings | 2000-04-09 | 2000-04-09 | races:Db#648; drivers:Db#20 |
| 990 | FULL_ONLY | races | Db | 648 | year of races | number_z=0.39258 | 2000-04-09 | circuits:Db#20 |
| 991 | FULL_ONLY | races | Db | 648 | round of races | number_z=-1.0781 | 2000-04-09 | circuits:Db#20 |
| 992 | FULL_ONLY | races | Db | 648 | name of races | San Marino Grand Prix | 2000-04-09 | circuits:Db#20 |
| 993 | FULL_ONLY | races | Db | 648 | date of races | 2000-04-09 | 2000-04-09 | circuits:Db#20 |
| 994 | FULL_ONLY | races | Db | 648 | time of races | 00:00:00 | 2000-04-09 | circuits:Db#20 |
| 995 | DRIVER_NBR_INDIRECT | standings | Db | 22967 | points of standings | number_z=-0.37891 | 1996-04-28 | races:Db#584; drivers:Db#20 |
| 996 | DRIVER_NBR_INDIRECT | standings | Db | 22967 | position of standings | number_z=0.12793 | 1996-04-28 | races:Db#584; drivers:Db#20 |
| 997 | DRIVER_NBR_INDIRECT | standings | Db | 22967 | wins of standings | number_z=-0.27148 | 1996-04-28 | races:Db#584; drivers:Db#20 |
| 998 | DRIVER_NBR_INDIRECT | standings | Db | 22967 | date of standings | 1996-04-28 | 1996-04-28 | races:Db#584; drivers:Db#20 |
| 999 | FULL_ONLY | races | Db | 584 | year of races | number_z=0.19629 | 1996-04-28 | circuits:Db#19 |
| 1000 | FULL_ONLY | races | Db | 584 | round of races | number_z=-0.88281 | 1996-04-28 | circuits:Db#19 |
| 1001 | FULL_ONLY | races | Db | 584 | name of races | European Grand Prix | 1996-04-28 | circuits:Db#19 |
| 1002 | FULL_ONLY | races | Db | 584 | date of races | 1996-04-28 | 1996-04-28 | circuits:Db#19 |
| 1003 | FULL_ONLY | races | Db | 584 | time of races | 00:00:00 | 1996-04-28 | circuits:Db#19 |
| 1004 | DRIVER_NBR_INDIRECT | results | Db | 17637 | number of results | number_z=-0.58203 | 2002-07-07 | races:Db#689; drivers:Db#20; constructors:Db#16 |
| 1005 | DRIVER_NBR_INDIRECT | results | Db | 17637 | grid of results | number_z=0.80469 | 2002-07-07 | races:Db#689; drivers:Db#20; constructors:Db#16 |
| 1006 | DRIVER_NBR_INDIRECT | results | Db | 17637 | position of results | number_z=-0.2002 | 2002-07-07 | races:Db#689; drivers:Db#20; constructors:Db#16 |
| 1007 | DRIVER_NBR_INDIRECT | results | Db | 17637 | positionOrder of results | number_z=-0.76172 | 2002-07-07 | races:Db#689; drivers:Db#20; constructors:Db#16 |
| 1008 | DRIVER_NBR_INDIRECT | results | Db | 17637 | points of results | number_z=-0.45117 | 2002-07-07 | races:Db#689; drivers:Db#20; constructors:Db#16 |
| 1009 | DRIVER_NBR_INDIRECT | results | Db | 17637 | laps of results | number_z=0.43555 | 2002-07-07 | races:Db#689; drivers:Db#20; constructors:Db#16 |
| 1010 | DRIVER_NBR_INDIRECT | results | Db | 17637 | statusId of results | number_z=-0.24805 | 2002-07-07 | races:Db#689; drivers:Db#20; constructors:Db#16 |
| 1011 | DRIVER_NBR_INDIRECT | results | Db | 17637 | date of results | 2002-07-07 | 2002-07-07 | races:Db#689; drivers:Db#20; constructors:Db#16 |
| 1012 | FULL_ONLY | races | Db | 689 | year of races | number_z=0.49219 | 2002-07-07 | circuits:Db#8 |
| 1013 | FULL_ONLY | races | Db | 689 | round of races | number_z=0.29688 | 2002-07-07 | circuits:Db#8 |
| 1014 | FULL_ONLY | races | Db | 689 | name of races | British Grand Prix | 2002-07-07 | circuits:Db#8 |
| 1015 | FULL_ONLY | races | Db | 689 | date of races | 2002-07-07 | 2002-07-07 | circuits:Db#8 |
| 1016 | FULL_ONLY | races | Db | 689 | time of races | 00:00:00 | 2002-07-07 | circuits:Db#8 |
| 1017 | DRIVER_NBR_INDIRECT | standings | Db | 25621 | points of standings | number_z=-0.098145 | 2003-08-03 | races:Db#708; drivers:Db#20 |
| 1018 | DRIVER_NBR_INDIRECT | standings | Db | 25621 | position of standings | number_z=-0.54297 | 2003-08-03 | races:Db#708; drivers:Db#20 |
| 1019 | DRIVER_NBR_INDIRECT | standings | Db | 25621 | wins of standings | number_z=0.73438 | 2003-08-03 | races:Db#708; drivers:Db#20 |
| 1020 | DRIVER_NBR_INDIRECT | standings | Db | 25621 | date of standings | 2003-08-03 | 2003-08-03 | races:Db#708; drivers:Db#20 |
| 1021 | FULL_ONLY | races | Db | 708 | year of races | number_z=0.53906 | 2003-08-03 | circuits:Db#9 |
| 1022 | FULL_ONLY | races | Db | 708 | round of races | number_z=0.69141 | 2003-08-03 | circuits:Db#9 |
| 1023 | FULL_ONLY | races | Db | 708 | name of races | German Grand Prix | 2003-08-03 | circuits:Db#9 |
