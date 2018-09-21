#
set terminal pngcairo font "arial,18" size 800, 600 enhanced rounded truecolor

#set lmargin at screen 0.0
#set rmargin at screen 0.0
#set bmargin at screen 0.0
#set tmargin at screen 0.0

# color definitions
set style line 11 lc rgb '#8b1a0e' pt 1 ps 1 lt 1 lw 5 # --- red
set style line 12 lc rgb '#FF0000' pt 1 ps 1 lt 1 lw 5 # --- bright red
set style line 13 lc rgb '#FF4500' pt 6 ps 1 lt 1 lw 5 # --- orangered
set style line 14 lc rgb '#B22222' pt 6 ps 1 lt 1 lw 5 # --- firebrick
set style line 15 lc rgb '#DC143C' pt 6 ps 1 lt 1 lw 5 # --- crimson
set style line 16 lc rgb '#FF7000' pt 6 ps 1 lt 1 lw 5 # --- dark orange

set style line 21 lc rgb '#5e9c36' pt 6 ps 1 lt 1 lw 5 # --- green
set style line 22 lc rgb '#006400' pt 6 ps 1 lt 1 lw 5 # --- darkgreen
set style line 23 lc rgb '#228B22' pt 6 ps 1 lt 1 lw 5 # --- forestgreen
set style line 24 lc rgb '#808000' pt 6 ps 1 lt 1 lw 5 # --- olive
set style line 25 lc rgb '#00FF10' pt 6 ps 1 lt 1 lw 5 # --- lime
set style line 26 lc rgb '#20B2AA' pt 6 ps 1 lt 1 lw 5 # --- light sea green

set style line 31 lc rgb '#8A2BE2' pt 6 ps 1 lt 1 lw 5 # --- blueviolet
set style line 32 lc rgb '#000E8B' pt 6 ps 1 lt 1 lw 5 # --- royalblue
set style line 33 lc rgb '#00008B' pt 6 ps 1 lt 1 lw 5 # --- darkblue
set style line 34 lc rgb '#800080' pt 6 ps 1 lt 1 lw 5 # --- purple

set style line 41 lc rgb '#2F4F4F' pt 6 ps 1 lt 1 lw 5 # --- darkslategray
set style line 42 lc rgb '#C0C0C0' pt 6 ps 1 lt 1 lw 5 # --- silver
set style line 43 lc rgb '#D2691E' pt 6 ps 1 lt 1 lw 5 # --- chocolate

set linetype 1 dashtype (2,2,4,4,6,6) lc rgb '#00FF10'
set linetype 2 dashtype (7,7,4,4,6,6) lc rgb '#000E8B' 



set xlabel "Time (fs)" offset 0.0, 0.5
set ylabel "Reaction Probability" offset 1.7, 0.0
set border 31 lw 2

#======== Model I ========#
set output "Model_I_React_Prob.png"
set label " Model I " at 1, 0.26
set key top left
set xrange [0:30]
set yrange [0:0.4]
plot  "_output_100.txt" u ($1/41.3410):5 w l lt 2  lw 8   t "C p=3",\
      "_output_101.txt" u ($1/41.3410):5 w l lt 1  lw 8   t "C p=4",\
      "_output_110.txt" u ($1/41.3410):5 w l ls 32 lw 8   t "ETHD p=3",\
      "_output_111.txt" u ($1/41.3410):5 w l ls 25 lw 8   t "ETHD p=4",\


#======== Model II ========#
set output "Model_II_React_Prob.png"
set label " Model II " at 1, 0.26
set key top left
set xrange [0:30]
set yrange [0:0.4]
plot  "_output_200.txt" u ($1/41.3410):5 w l lt 2  lw 8   t "C p=3",\
      "_output_201.txt" u ($1/41.3410):5 w l lt 1  lw 8   t "C p=4",\
      "_output_210.txt" u ($1/41.3410):5 w l ls 32 lw 8   t "ETHD p=3",\
      "_output_211.txt" u ($1/41.3410):5 w l ls 25 lw 8   t "ETHD p=3",\
 
 
 
 

