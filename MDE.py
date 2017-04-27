import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# set basic parameters
n_spp = 92
grad_hgt = 3000
n_sim = 1000

lmn_rng = np.log(grad_hgt/10)
lsg_rng = np.log(grad_hgt/750)

# set range size frequency distribution
spp_rng = np.random.lognormal(lmn_rng, sigma=lsg_rng, size=n_spp)
while sum(spp_rng > grad_hgt) > 0:
    tooLarge = [i for i, spp_rng in enumerate(spp_rng) if spp_rng > grad_hgt]
    spp_rng[tooLarge] = np.random.lognormal(lmn_rng, sigma=lsg_rng, size=len(tooLarge))

# initialize output dataframe
mde_col = list(range(0, n_sim))
mde_index = list(range(0, grad_hgt+100, 100))
mde_out = pd.DataFrame(index=mde_index, columns=mde_col)

# run simulations
for s in range(0, n_sim):
    # assign midpoints
    spp_mp = np.random.uniform(low=0, high=grad_hgt, size=n_spp)
    loEl = spp_mp - spp_rng/2
    hiEl = spp_mp + spp_rng/2
    spp_el = pd.DataFrame(list(zip(loEl, hiEl)), columns=['Lo', "Hi"])

    # contain ranges within boundaries
    spp_el['outBounds'] = pd.Series((spp_el['Lo'] < 0) | (spp_el['Hi'] > grad_hgt))
    while sum(spp_el['outBounds']) > 0:
        spp_out = list(np.where(spp_el['outBounds'] == 1)[0])
        spp_mp[spp_out] = np.random.uniform(low=0, high=grad_hgt, size=len(spp_out))
        spp_el['Lo'] = spp_mp - spp_rng/2
        spp_el['Hi'] = spp_mp + spp_rng/2
        spp_el['outBounds'] = (spp_el['Lo'] < 0) | (spp_el['Hi'] > grad_hgt)

    # calculate richness
    el_band = pd.Series(range(0, grad_hgt+100, 100))
    el_rich = np.repeat(0, len(el_band))
    S_df = pd.DataFrame(list(zip(el_band, el_rich)), columns=['El', 'S'])
    for i in range(0, len(S_df)):
        i_e = S_df['El'][i]
        el_rich[i] = sum((spp_el['Lo'] < i_e+100) & (spp_el['Hi'] > i_e))
    S_df['S'] = el_rich

    # store output
    mde_out[s] = list(S_df['S'])

    # add output to plot
    plt.plot(S_df['El'], S_df['S'], c='black', alpha=0.05)

plt.plot(S_df['El'], mde_out.mean(1), c='blue')
plt.plot(S_df['El'], mde_out.quantile(.025, 1), c='blue', alpha=0.5)
plt.plot(S_df['El'], mde_out.quantile(.975, 1), c='blue', alpha=0.5)
plt.xlabel('Elevation')
plt.ylabel('Species richness')
plt.show()

