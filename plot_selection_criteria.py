#!/usr/bin/env python3

# Place import files below
import copy

import matplotlib.pyplot as plt
import numpy as np

from common_functions import save_figures
from process_data import UDGData
from universal_settings import (ax_limit_edge_adjustment, mu_e, mu_e2, reff,
                                reff2, sim_ids, sim_styles)


def main():
    # Plot settings
    try:
        plt.style.use('./paper.mplstyle')
    except OSError:
        pass

    # File locations
    r_eff_mu_plot_by_sim = 'fig1_selection_criteria.pdf'

    # Load simulation data for Fig. 1
    udg_data = UDGData()
    data_list = [
        'simulation_id', 'select_udgs_reff1_mu1', 'select_udgs_reff1_mu2',
        'select_udgs_reff2_mu1', 'select_udgs_reff2_mu2', 'rband_mu_mag_arsec',
        're_rband'
    ]
    (simulation_id, select_udgs_reff1_mu1, select_udgs_reff1_mu2,
     select_udgs_reff2_mu1, select_udgs_reff2_mu2, rband_mu_mag_arsec,
     re_rband) = udg_data.retrieve_data(data_list)

    # Plot limits (Re and mu_e)
    re_ylims = np.asarray([0.5, 5.8]) * ax_limit_edge_adjustment
    mu_mag_ylims = np.asarray([23.5, 29.]) * ax_limit_edge_adjustment

    ####################################################################
    # Individual R_e vs surface brightness (by sim)
    ####################################################################
    fig_rlum = plt.figure(figsize=(8, 8))
    ax_rlum = fig_rlum.add_subplot(111)

    print()
    print("N_UDG,tot")
    print("##############")
    for sim_id in sim_ids:
        select_all_udgs_reff1_mu1 = ((simulation_id == sim_id) *
                                     select_udgs_reff1_mu1)
        select_all_udgs_reff1_mu2 = ((simulation_id == sim_id) *
                                     select_udgs_reff1_mu2)
        select_all_udgs_reff2_mu1 = ((simulation_id == sim_id) *
                                     select_udgs_reff2_mu1)
        select_all_udgs_reff2_mu2 = ((simulation_id == sim_id) *
                                     select_udgs_reff2_mu2)

        ################################################################
        # Print out relevant information
        ################################################################
        print(sim_id)
        print("Reff1, Mu1: {}".format(select_all_udgs_reff1_mu1.sum()))
        print("Reff1, Mu2: {}".format(select_all_udgs_reff1_mu2.sum()))
        print("Reff2, Mu1: {}".format(select_all_udgs_reff2_mu1.sum()))
        print("Reff2, Mu2: {}".format((select_all_udgs_reff2_mu2).sum()))
        print("##############")

        sim_style_dict = copy.deepcopy(sim_styles[sim_id])
        sim_style_dict_sub_select = copy.deepcopy(sim_styles[sim_id])
        sim_style_dict_sub_select.update({'alpha': 0.5})

        middle_selection = ((simulation_id == sim_id) * select_udgs_reff1_mu1 *
                            (~select_udgs_reff2_mu2))

        # Plot main selection
        main_marker = ax_rlum.scatter(
            rband_mu_mag_arsec[select_all_udgs_reff2_mu2],
            re_rband[select_all_udgs_reff2_mu2],
            label=sim_id.replace('_', '\_'),
            **sim_style_dict)

        sim_style_dict_sub_select.update(
            {'color': main_marker.get_facecolor()})

        # Plot selection in less stringent selection criteria
        ax_rlum.scatter(rband_mu_mag_arsec[middle_selection],
                        re_rband[middle_selection],
                        **sim_style_dict_sub_select)

        if 's' in sim_style_dict:
            s = sim_style_dict['s']
        else:
            s = 30

        # Plot all remaining field galaxies
        ax_rlum.scatter(rband_mu_mag_arsec[(simulation_id == sim_id) *
                                           (~select_udgs_reff1_mu1)],
                        re_rband[(simulation_id == sim_id) *
                                 (~select_udgs_reff1_mu1)],
                        edgecolors='silver',
                        facecolors='none',
                        linewidth=1.5,
                        s=s,
                        marker=sim_style_dict['marker'])

    # Plot less stringent criteria Re and mu_e limits
    ax_rlum.axvline(mu_e, linestyle=':', color='grey')
    ax_rlum.axhline(reff, linestyle=':', color='grey')
    # Plot fiducial criteria Re and mu_e limits
    ax_rlum.axvline(mu_e2, linestyle='--', color='k')
    ax_rlum.axhline(reff2, linestyle='--', color='k')

    # Axis settings
    ax_rlum.set(xlabel=r'$\mu_{\rm e}\, \left({\rm mag\, arcsec^{-2}}\right)$',
                ylabel=r'$R_{\rm e}\, \left({\rm kpc}\right)$',
                xlim=mu_mag_ylims,
                ylim=re_ylims)
    ax_rlum.legend(loc='upper right',
                   frameon=True,
                   fancybox=True,
                   framealpha=0.75)
    ax_rlum.minorticks_on()
    ax_rlum.tick_params(axis='x', which='major', pad=7)

    save_figures(fig_rlum, r_eff_mu_plot_by_sim)
    return None


if __name__ == "__main__":
    main()
