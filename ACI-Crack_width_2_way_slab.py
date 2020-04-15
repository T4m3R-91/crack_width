# Inputs section
print('CRACK WIDTH CALCULATIONS ACCORDING TO ACI: 224R-018')
print('')
print('Crack control in two way slabs and plates')
print('')
n_c_row = int(input('Compression side rebar number of rows:'))
comp_rebar_dia = float(input('Compression side rebar diameter(mm):'))
comp_rebar_spacing = float(input('Compression side rebar spacing(mm):'))
n_t_row = int(input('Tension side rebar number of rows:'))
ten_rebar_dia = float(input('Tension side rebar diameter(mm):'))
ten_rebar_spacing = float(input('Tension side rebar spacing(mm):'))
ten_rebar_spacing
fy = float(input('Rebar Yield strength(N/mm2):'))
fc = float(input('Concrete strength(N/mm2):'))
b = float(input('Section breadth(mm):'))
# total tension rebars in the input breadth
tot_ten_rebar = b*n_t_row/ten_rebar_spacing
print('Total number of tension bars = ',tot_ten_rebar)
h = float(input('Section height(mm):'))
cc = float(input('Cover to compression side rebar(mm):'))
nct = float(input('Nominal Cover to tension side rebar(mm):'))
fct = nct+((n_t_row/2)*ten_rebar_dia)+(((n_t_row-1)/2)*ten_rebar_dia)
d_main_rebar = h-fct
def area(dia,spc,br,ro):
    # calculates total area of rebar in the input breadth
    rebar_area=((22/7)*(dia**2)/4)*(br/spc)*ro
    return rebar_area
tot_comp_rebar_area = area(comp_rebar_dia, comp_rebar_spacing, b, n_c_row)
tot_ten_rebar_area = area(ten_rebar_dia, ten_rebar_spacing, b, n_t_row)
print('Compression rebar area =',tot_comp_rebar_area, 'mm2')
print('Tension rebar area =',tot_ten_rebar_area, 'mm2')
es = float(input('Modulus of elasticity of Steel(kN/mm2):'))
ec = float(input('Modulus of elasticity of Concrete(kN/mm2):'))
mod_rat = es/ec
print('Modular ratio', mod_rat)
print('')
print('')
mom = float(input('Moment(kN/m):'))
nf = float(input('Norml force(kN) (+ve Tension, -ve Compression):'))
print('')
# calculations section
# calculating eccentricities at rebar locations due to applied forces
if nf < 0:
    es_ten = ((mom/-1*nf)*1000)+(h/2)-fct
    es_comp = ((mom/-1*nf)*1000)+(h/2)-cc
else:
    es_ten = ((mom/nf)*1000)-(h/2)-fct
    es_comp = ((mom/nf)*1000)-(h/2)-cc
# calculating corrected value of moment
mom_cor = es_ten * nf /1000
print('M resultant =', mom_cor, '(kN/m)')
# calculating section neutral axis location
num_to_zero = 0.001
z_loc = 0.0
if nf >= 0:
    while True:
        equit = (z_loc**3)-((3*z_loc**2)*(es_ten+d_main_rebar))-(6*z_loc*mod_rat/b*((tot_ten_rebar_area*es_ten)+(tot_comp_rebar_area*es_comp)))+(6*mod_rat/b*((tot_ten_rebar_area*es_ten*d_main_rebar)+(tot_comp_rebar_area*es_comp*cc)))
        z_loc = z_loc + 0.001
        if equit <= num_to_zero:
            break
else:
        while True:
            equit = (z_loc**3)+((3*z_loc**2)*(es_ten+d_main_rebar))+(6*z_loc*mod_rat/b*((tot_ten_rebar_area*es_ten)+(tot_comp_rebar_area*es_comp)))-(6*mod_rat/b*((tot_ten_rebar_area*es_ten*d_main_rebar)+(tot_comp_rebar_area*es_comp*cc)))
            z_loc = z_loc + 0.001
            if equit >= num_to_zero:
                break
print ('Neutral axis Z =', z_loc, 'mm from compression fiber')
print('')
print('')
# input tolerable crack width per Table 4.1
print('Table 4.1 - Tolerable crack widths, reinforced concrete')
print('')
print('A- Dry air or protective membrane                      0.41 mm')
print('B- Humidity, moist air, soil                           0.30 mm')
print('C- Deicing chemicals                                   0.18 mm')
print('D- Seawater and seawater spray; wetting and drying     0.15 mm')
print('E- Water retaining structures                          0.10 mm')
print('')
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
print('Tolerable crack width = ',cond, 'mm')
print('')
# calculating and checking stresses
comp_Stress_conc =(mom_cor*1000000*z_loc)/(((b*z_loc**2)/2*(d_main_rebar-(z_loc/3))+(mod_rat*tot_comp_rebar_area*(z_loc-cc)*(d_main_rebar-cc))))
print ('Compression stress on concrete =', comp_Stress_conc, 'N/mm2')
if comp_Stress_conc <= 0.45*fc:
    print ('Compressive stress on concrete is less than 0.45*Fc - Pass')
else:
    print ('Compressive stress on concrete is larger than 0.45*Fc - Compression Failure')
print('')
comp_Stress_rebar =(comp_Stress_conc/z_loc)*(z_loc-cc)*mod_rat
print ('Compression stress on compression rebar =', comp_Stress_rebar, 'N/mm2')
if comp_Stress_rebar <= 0.6*fy:
    print ('Compressive stress on compression rebar is less than 0.6*Fy - Pass')
else:
    print ('Compressive stress on compression rebar is larger than 0.6*Fy - Compression Failure')
print('')
ten_Stress_rebar =(comp_Stress_conc/z_loc)*(d_main_rebar-z_loc)*mod_rat
print ('Tensile stress on tension rebar =', ten_Stress_rebar, 'N/mm2')
if ten_Stress_rebar <= 0.6*fy:
    print ('Tensile stress on tension rebar is less than 0.6*Fy - Pass')
else:
    print ('Tensile stress on tension rebar is larger than 0.6*Fy - Tension Failure')
print('')
# calculating and checking crack width
# K fracture cooficient
k_frac_coof = 0.000021
# beta ratio of distance between neutral axis and tension fiber to distance between neutral axis and tension reinforcement rebar
b_ratio = 1.25
dc = nct+(0.5*ten_rebar_dia)
# rebar spacing in tension side in 2 orthogonal directions - usually equal
s_1 = ten_rebar_spacing
s_2 = ten_rebar_spacing
g_index = ((s_1/25.4)*(s_2/25.4)*(dc/25.4)*8)/((ten_rebar_dia/25.4)*22/7)
# crack width in mm
# 1 N/mm2 = 0.145 KSI (Kilo pound force per square inch)
crack_width = (k_frac_coof*b_ratio*(ten_Stress_rebar*0.145)*(g_index**(1/2)))*25.4
print ('Using equation (4-15), Maximum Crack width =', crack_width, 'mm')
if crack_width <= cond:
    print ('Maximum Crack width is less than tolerable crack width - Pass')
else:
    print ('Maximum Crack width is larger than tolerable crack width - Fail')
quit()
