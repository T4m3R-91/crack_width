def crack_width_2waycrack_calc_title():
    print('CRACK WIDTH CALCULATIONS ACCORDING TO ACI: 224R-018')
    print('')
    print('Crack control in two way slabs and plates')
    print('')
def crack_width_2waycrack_inputs():
    n_c_row = int(input('Compression side rebar number of rows:'))
    comp_rebar_dia = float(input('Compression side rebar diameter(mm):'))
    comp_rebar_spacing = float(input('Compression side rebar spacing(mm):'))
    n_t_row = int(input('Tension side rebar number of rows:'))
    ten_rebar_dia = float(input('Tension side rebar diameter(mm):'))
    ten_rebar_spacing = float(input('Tension side rebar spacing(mm):'))
    rebar_fy = float(input('Rebar Yield strength(N/mm2):'))
    conc_fc = float(input('Concrete Compressive strength(N/mm2):'))
    sec_breadth = float(input('Section breadth(mm):'))
    sec_height = float(input('Section height(mm):'))
    cov_comp_rebar = float(input('Cover to compression side rebar(mm):'))
    nom_cover_tension_rebar = float(input('Nominal Cover to tension side rebar(mm):'))
    return (n_c_row, comp_rebar_dia, comp_rebar_spacing, n_t_row, ten_rebar_dia, ten_rebar_spacing, rebar_fy, conc_fc, sec_breadth, sec_height, cov_comp_rebar, nom_cover_tension_rebar)
def rebar_area_tot_breadth(dia,spacing,breadth,n_row):
    # calculates total rebar_area_tot_breadth of rebar in the input breadth
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
def neutral_axis(es_ten,d_main_rebar,mod_rat,sec_breadth,tot_ten_rebar_area,tot_comp_rebar_area,es_comp,cov_comp_rebar):
    num_to_zero = 0.001
    z_loc = 0.0
    if n_force >= 0:
        while True:
            equit = (z_loc**3)-((3*z_loc**2)*(es_ten+d_main_rebar))-(6*z_loc*mod_rat/sec_breadth*((tot_ten_rebar_area*es_ten)+(tot_comp_rebar_area*es_comp)))+(6*mod_rat/sec_breadth*((tot_ten_rebar_area*es_ten*d_main_rebar)+(tot_comp_rebar_area*es_comp*cov_comp_rebar)))
            z_loc = z_loc + 0.001
            if equit <= num_to_zero:
                break
    else:
            while True:
                equit = (z_loc**3)+((3*z_loc**2)*(es_ten+d_main_rebar))+(6*z_loc*mod_rat/sec_breadth*((tot_ten_rebar_area*es_ten)+(tot_comp_rebar_area*es_comp)))-(6*mod_rat/sec_breadth*((tot_ten_rebar_area*es_ten*d_main_rebar)+(tot_comp_rebar_area*es_comp*cov_comp_rebar)))
                z_loc = z_loc + 0.001
                if equit >= num_to_zero:
                    break
    return z_loc
n_c_row, comp_rebar_dia, comp_rebar_spacing, n_t_row, ten_rebar_dia, ten_rebar_spacing, rebar_fy, conc_fc, sec_breadth, sec_height, cov_comp_rebar, nom_cover_tension_rebar = crack_width_2waycrack_inputs()
# total tension rebars in the input breadth
tot_ten_rebar = sec_breadth*n_t_row/ten_rebar_spacing
#print('Total number of tension bars = ',tot_ten_rebar)
cov_center_rebar = nom_cover_tension_rebar+((n_t_row/2)*ten_rebar_dia)+(((n_t_row-1)/2)*ten_rebar_dia)
d_main_rebar = sec_height-cov_center_rebar
tot_comp_rebar_area = rebar_area_tot_breadth(comp_rebar_dia, comp_rebar_spacing, sec_breadth, n_c_row)
tot_ten_rebar_area = rebar_area_tot_breadth(ten_rebar_dia, ten_rebar_spacing, sec_breadth, n_t_row)
#print('Compression rebar area =',tot_comp_rebar_area, 'mm2')
#print('Tension rebar area =',tot_ten_rebar_area, 'mm2')
mod_elastic_rebar = float(input('Modulus of elasticity of Steel(kN/mm2):'))
mod_elastic_conc = float(input('Modulus of elasticity of Concrete(kN/mm2):'))
mod_rat = mod_elastic_rebar/mod_elastic_conc
#print('Modular ratio', mod_rat)
#print('')
#rint('')
b_moment = float(input('Moment(kN/m):'))
n_force = float(input('Norml force(kN) (+ve Tension, -ve Compression):'))
#print('')
# calculations section
# calculating eccentricities at rebar locations due to applied forces
if n_force < 0:
    es_ten = ((b_moment/-1*n_force)*1000)+(sec_height/2)-cov_center_rebar
    es_comp = ((b_moment/-1*n_force)*1000)+(sec_height/2)-cov_comp_rebar
else:
    es_ten = ((b_moment/n_force)*1000)-(sec_height/2)-cov_center_rebar
    es_comp = ((b_moment/n_force)*1000)-(sec_height/2)-cov_comp_rebar
# calculating corrected value of moment
mom_cor = es_ten * n_force /1000
#print('M resultant =', mom_cor, '(kN/m)')
# calculating section neutral axis location
z_loc = neutral_axis(es_ten,d_main_rebar,mod_rat,sec_breadth,tot_ten_rebar_area,tot_comp_rebar_area,es_comp,cov_comp_rebar)
#print ('Neutral axis Z =', z_loc, 'mm from compression fiber')
#print('')
print('')
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
#print('')
# calculating and checking stresses
comp_Stress_conc =(mom_cor*1000000*z_loc)/(((sec_breadth*z_loc**2)/2*(d_main_rebar-(z_loc/3))+(mod_rat*tot_comp_rebar_area*(z_loc-cov_comp_rebar)*(d_main_rebar-cov_comp_rebar))))
#print ('Compression stress on concrete =', comp_Stress_conc, 'N/mm2')
if comp_Stress_conc <= 0.45*conc_fc:
    print ('Compressive stress on concrete is less than 0.45*conc_fc - Pass')
else:
    print ('Compressive stress on concrete is larger than 0.45*conc_fc - Compression Failure')
#print('')
comp_Stress_rebar =(comp_Stress_conc/z_loc)*(z_loc-cov_comp_rebar)*mod_rat
#print ('Compression stress on compression rebar =', comp_Stress_rebar, 'N/mm2')
if comp_Stress_rebar <= 0.6*rebar_fy:
    print ('Compressive stress on compression rebar is less than 0.6*rebar_fy - Pass')
else:
    print ('Compressive stress on compression rebar is larger than 0.6*rebar_fy - Compression Failure')
#print('')
ten_Stress_rebar =(comp_Stress_conc/z_loc)*(d_main_rebar-z_loc)*mod_rat
#print ('Tensile stress on tension rebar =', ten_Stress_rebar, 'N/mm2')
if ten_Stress_rebar <= 0.6*rebar_fy:
    print ('Tensile stress on tension rebar is less than 0.6*rebar_fy - Pass')
else:
    print ('Tensile stress on tension rebar is larger than 0.6*rebar_fy - Tension Failure')
#print('')
# calculating and checking crack width
# K fracture cooficient
k_frac_coof = 0.000021
# beta ratio of distance between neutral axis and tension fiber to distance between neutral axis and tension reinforcement rebar
b_ratio = 1.25
dc = nom_cover_tension_rebar+(0.5*ten_rebar_dia)
# rebar spacing in tension side in 2 orthogonal directions - usually equal
s_1 = ten_rebar_spacing
s_2 = ten_rebar_spacing
g_index = ((s_1/25.4)*(s_2/25.4)*(dc/25.4)*8)/((ten_rebar_dia/25.4)*22/7)
# crack width in mm
# 1 N/mm2 = 0.145 KSI (Kilo pound force per square inch)
crack_width = (k_frac_coof*b_ratio*(ten_Stress_rebar*0.145)*(g_index**(1/2)))*25.4
#print ('Using equation (4-15), Maximum Crack width =', crack_width, 'mm')
if crack_width <= cond:
    print ('Maximum Crack width is less than tolerable crack width - Pass')
else:
    print ('Maximum Crack width is larger than tolerable crack width - Fail')
quit()
