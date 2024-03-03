import numpy as np
from tabulate import tabulate



muabo = np.genfromtxt("muabo.txt", delimiter=",")
muabd = np.genfromtxt("muabd.txt", delimiter=",")

red_wavelength = 600 # Replace with wavelength in nanometres
green_wavelength = 515 # Replace with wavelength in nanometres
blue_wavelength = 460 # Replace with wavelength in nanometres

wavelength = np.array([red_wavelength, green_wavelength, blue_wavelength])

def mua_blood_oxy(x): return np.interp(x, muabo[:, 0], muabo[:, 1])
def mua_blood_deoxy(x): return np.interp(x, muabd[:, 0], muabd[:, 1])

bvf = 0.01 # Blood volume fraction, average blood amount in tissue
oxy = 0.8 # Blood oxygenation

# Absorption coefficient ($\mu_a$ in lab text)

mua_other = 25 # Background absorption due to collagen, et cetera
mua_blood = (mua_blood_oxy(wavelength)*oxy # Absorption due to
            + mua_blood_deoxy(wavelength)*(1-oxy)) # pure blood
def mua(bloodVolumeFraction = bvf): 
    return mua_blood*bloodVolumeFraction + mua_other

# reduced scattering coefficient ($\mu_s^\prime$ in lab text)
# the numerical constants are thanks to N. Bashkatov, E. A. Genina and
# V. V. Tuchin. Optical properties of skin, subcutaneous and muscle
# tissues: A review. In: J. Innov. Opt. Health Sci., 4(1):9-38, 2011.
# Units: 1/m
musr = 100 * (17.6*(wavelength/500)**-4 + 18.78*(wavelength/500)**-0.22)

# mua and musr are now available as shape (3,) arrays
# Red, green and blue correspond to indexes 0, 1 and 2, respectively

print("mua: ", mua(), "\nmusr: ", musr)

#oppg1 a)

def pen_depth_func(bloodVolumeFraction = bvf):
    return np.sqrt(1/(3*mua(bloodVolumeFraction)*(musr + mua(bloodVolumeFraction))))

pen_depth = pen_depth_func()



pen_depth_lst = np.array([
    ["Red", pen_depth[0]],
    ["Green", pen_depth[1]],
    ["Blue", pen_depth[2]]
])

print("1a)\n",tabulate(pen_depth_lst, headers=['Color', 'Penetration depth [meters]'], tablefmt='grid'))

#oppg1 b)

fing_thickness = 2.2*10**(-2) #meters


def transmittans(d, bloodVolumeFraction = bvf):
    C = np.sqrt(3*mua(bloodVolumeFraction)*(musr + mua(bloodVolumeFraction)))
    return np.exp(-C*d)

transmittans_fing = transmittans(fing_thickness)

transmittans_lst = np.array([
    ["Red", transmittans_fing[0]],
    ["Green", transmittans_fing[1]],
    ["Blue", transmittans_fing[2]]
])
print("1b)\n",tabulate(transmittans_lst, headers=['Color', 'Transmittans gjennom {:.3}m finger'.format(fing_thickness)], tablefmt='grid'))


#oppg1 c)

#antar at mesteparten av refletert lys er som følge av lys som reflekteres innenfor 1 penetrasjonsdybde, altså se oppga 1a

# reflektans_fing = transmittans(2*pen_depth)
# print(reflektans_fing)

# reflektans_lst = np.array([
#     ["Red", reflektans_fing[0]],
#     ["Green", reflektans_fing[1]],
#     ["Blue", reflektans_fing[2]]
# ])

# print("1c)\n",tabulate(reflektans_lst, headers=['Color', 'Reflektans fra en {:.3}m finger'.format(fing_thickness)], tablefmt='grid'))

#oppg1 d)
bvf_vein = 1
vein_diameter = 300*10**(-6) #meter

transmittance_vein = transmittans(vein_diameter, bvf_vein) #1bvf
transmittance_tissue = transmittans(vein_diameter) #0.01bvf

print("vein: ", transmittance_vein , "\ntissue: ", transmittance_tissue)

kontrast = np.abs(transmittance_vein - transmittance_tissue)/transmittance_tissue

pulsutslag_lst = np.array([
    ["Red", transmittance_vein[0], transmittance_tissue[0], kontrast[0]],
    ["Green", transmittance_vein[1], transmittance_tissue[1], kontrast[1]],
    ["Blue", transmittance_vein[2], transmittance_tissue[2], kontrast[2]]
])

print("1d)\n",tabulate(pulsutslag_lst, headers=['Color', 'Transmittans høyt blodvolum', "transmittans lavt blodvolum", kontrast], tablefmt='grid'))
