def crack_width_tencrack_calc_title():
    print('CRACK WIDTH CALCULATIONS ACCORDING TO ACI: 224R-018')
    print('')
    print('Tesnsion cracking')
    print('')
def crack_width_tencrack_inputs():
    n_st_row = int(input('Secondary tension side rebar number of rows:'))
    sec_ten_rebar_dia = float(input('Secondary tension side rebar diameter(mm):'))
    sec_ten_rebar_spacing = float(input('Secondary tension side rebar spacing(mm):'))
    n_mt_row = int(input('Main tension side rebar number of rows:'))
    main_ten_rebar_dia = float(input('Main tension side rebar diameter(mm):'))
    main_ten_rebar_spacing = float(input('Main tension side rebar spacing(mm):'))
    rebar_fy = float(input('Rebar Yield strength(N/mm2):'))
    sec_breadth = float(input('Section breadth(mm):'))
    sec_height = float(input('Section height(mm):'))
    cov_sec_rebar = float(input('Cover to Secondary tension side rebar(mm):'))
    nom_cover_main_rebar = float(input('Nominal Cover to Main tension side rebar(mm):'))
    print('')
    b_moment = float(input('Moment(kN/m):'))
    while True:
        n_force = float(input('Norml force(kN) (+ve Tension only):'))
        print('')
        if n_force >= 0:
            eccen = ((b_moment/n_force)*1000)
            break
        else:
            print('input +ve value for tension force')
            continue
    print('')
    return (n_st_row, sec_ten_rebar_dia, sec_ten_rebar_spacing, n_mt_row, main_ten_rebar_dia, main_ten_rebar_spacing, rebar_fy, sec_breadth, sec_height, cov_sec_rebar, nom_cover_main_rebar, b_moment, n_force, eccen)
def rebar_area_tot_breadth(dia,spacing,breadth,n_row):
    # calculates total rebar_area of rebar in the input breadth
    rebar_area=((22/7)*(dia**2)/4)*(breadth/spacing)*n_row
    return rebar_area
def aci224r_table4_1_tolerable_crack_widths():
    # input tolerable crack width per Table 4.1
    print('Table 4.1 - Tolerable crack widths, reinforced concrete')
    print('')
    print('A- Dry air or protective membrane                      0.41 mm')
    print('B- Humidity, moist air, soil                           0.30 mm')
    print('C- Deicing chemicals                                   0.18 mm')
    print('D- Seawater and seawater spray; wetting and drying     0.15 mm')
    print('E- Water retaining structures                          0.10 mm')
    print('')
n_st_row, sec_ten_rebar_dia, sec_ten_rebar_spacing, n_mt_row, main_ten_rebar_dia, main_ten_rebar_spacing, rebar_fy, sec_breadth, sec_height, cov_sec_rebar, nom_cover_main_rebar, b_moment, n_force, eccen = crack_width_tencrack_inputs()
# total tension rebars in the input breadth
tot_main_ten_rebar = sec_breadth*n_mt_row/main_ten_rebar_spacing
#print('Total number of main tension bars = ',tot_main_ten_rebar)
fct = nom_cover_main_rebar+((n_mt_row/2)*main_ten_rebar_dia)+(((n_mt_row-1)/2)*main_ten_rebar_dia)
tot_sec_ten_rebar_area = rebar_area_tot_breadth(sec_ten_rebar_dia, sec_ten_rebar_spacing, sec_breadth, n_st_row)
tot_main_ten_rebar_area = rebar_area_tot_breadth(main_ten_rebar_dia, main_ten_rebar_spacing, sec_breadth, n_mt_row)
#print('Secondary tension rebar area =',tot_sec_ten_rebar_area, 'mm2')
#print('Main tension rebar area =',tot_main_ten_rebar_area, 'mm2')
# calculating eccentricities at rebar locations due to applied forces
aci224r_table4_1_tolerable_crack_widths()
while True:
    exp = input('Exposure condition: ')
    if exp == 'A':
        cond = 0.41
        break
    elif exp == 'B':
        cond = 0.30
        break
    elif exp == 'C':
        cond = 0.18
        break
    elif exp == 'D':
        cond = 0.15
        break
    elif exp == 'E':
        cond = 0.10
        break
    else:
        print('')
        print('input correct Exposure condition')
        continue
#print('Tolerable crack width = ',cond, 'mm')
# calculating and checking stresses
main_ten_force =(n_force*(sec_height/2+eccen-cov_sec_rebar))/(sec_height-fct-cov_sec_rebar)
main_ten_Stress_rebar =(main_ten_force*1000/tot_main_ten_rebar_area)
#print ('Tensile stress on main tension rebar =', main_ten_Stress_rebar, 'N/mm2')
if main_ten_Stress_rebar <= 0.6*rebar_fy:
    print ('Tensile stress on main tension rebar is less than 0.6*fy - Pass')
else:
    print ('Compressive stress on main compression rebar is larger than 0.6*fy - Tension Failure')
sec_ten_force =(n_force*(sec_height/2-eccen-fct))/(sec_height-fct-cov_sec_rebar)
sec_ten_Stress_rebar =(sec_ten_force*1000/tot_sec_ten_rebar_area)
#print ('Tensile stress on secondary tension rebar =', sec_ten_Stress_rebar, 'N/mm2')
if sec_ten_Stress_rebar <= 0.6*rebar_fy:
    print ('Tensile stress on secondary tension rebar is less than 0.6*fy - Pass')
else:
    print ('Tensile stress on secondary tension rebar is larger than 0.6*fy - Tension Failure')
# calculating and checking crack width
# A area of concrete symmetric with reinforcing steel divided by number of bars
a_symm =(2*sec_breadth*fct)/tot_main_ten_rebar
# crack width in mm
# 1 N/mm2 = 0.145 KSI (Kilo pound force per square inch)
# 1 in3 = 16387 mm3
crack_width = (0.1*main_ten_Stress_rebar*0.145*((fct*a_symm/16387)**(1/3))/1000)*25.4
#print ('Using equation (4-21), Maximum Crack width =', crack_width, 'mm')
if crack_width <= cond:
    print ('Maximum Crack width is less than tolerable crack width - Pass')
else:
    print ('Maximum Crack width is larger than tolerable crack width - Fail')
quit()
