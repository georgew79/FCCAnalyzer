
import functions
import helpers
import ROOT
import argparse
import logging

logger = logging.getLogger("fcclogger")

parser = functions.make_def_argparser()
parser.add_argument("--flavor", type=str, choices=["ee", "mumu", "qq", "gaga"], help="Flavor (gaga, ee, mumu, qq)", default="mumu")
parser.add_argument("--jetAlgo", type=str, choices=["kt", "valencia", "genkt"], default="genkt", help="Jet clustering algorithm")
args = parser.parse_args()
functions.set_threads(args)

functions.add_include_file("analyses/ewk_z/functions.h")
functions.add_include_file("include/helper_jetclustering.h")

# define histograms
bins_p_mu = (2000, 0, 200) # 100 MeV bins
bins_m_ll = (2000, 0, 200) # 100 MeV bins
bins_p_ll = (2000, 0, 200) # 100 MeV bins
bins_pt_ll = (2000, 0, 200)
bins_no_ll = (2000, 0, 200)
bins_rp_ll = (2000, 0, 200)

bins_theta = (500, -5, 5)
bins_phi = (500, -5, 5)

bins_count = (100, 0, 100)
bins_pdgid = (60, -30, 30)
bins_charge = (10, -5, 5)


bins_resolution = (10000, 0.95, 1.05)

bins_resolution_1 = (20000, 0, 2)

jet_energy = (1000, 0, 100) # 100 MeV bins
dijet_m = (2000, 0, 200) # 100 MeV bins
visMass = (2000, 0, 200) # 100 MeV bins
missEnergy  = (2000, 0, 200) # 100 MeV bins

dijet_m_final = (500, 50, 100) # 100 MeV bins

bins_cos = (100, -1, 1)

bins_thrustval = (2000, 0, 2)
bins_thrustcomp = (2000, -100, 100)

#jetcluster_helper = helpers.JetClusteringHelper(1.5, 0, 0, 0, 0, -1)

def build_graph_ll(df, dataset):

    logger.info(f"Build graph {dataset.name}")
    results = []

    df = df.Define("weight", "1.0")
    weightsum = df.Sum("weight")


    df = df.Alias("Particle0", "Particle#0.index")
    df = df.Alias("Particle1", "Particle#1.index")
    df = df.Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
    df = df.Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")
    if args.flavor == "mumu":
        df = df.Alias("Lepton0", "Muon#0.index")
        #df = df.Alias("Lepton1", "Muon#1.index")
    else:
        df = df.Alias("Lepton0", "Electron#0.index")
        #df = df.Alias("Lepton1", "Electron#0.index")

    # all leptons
    df = df.Define("leps_all", "FCCAnalyses::ReconstructedParticle::get(Lepton0, ReconstructedParticles)")
    df = df.Define("leps_all_p", "FCCAnalyses::ReconstructedParticle::get_p(leps_all)")
    df = df.Define("leps_all_pt", "FCCAnalyses::ReconstructedParticle::get_pt(leps_all)")
    df = df.Define("leps_all_theta", "FCCAnalyses::ReconstructedParticle::get_theta(leps_all)")
    df = df.Define("leps_all_phi", "FCCAnalyses::ReconstructedParticle::get_phi(leps_all)")
    df = df.Define("leps_all_q", "FCCAnalyses::ReconstructedParticle::get_charge(leps_all)")
    df = df.Define("leps_all_no", "FCCAnalyses::ReconstructedParticle::get_n(leps_all)")

    # cuts on leptons
    df = df.Define("leps_sel_p", "FCCAnalyses::ReconstructedParticle::sel_p(1)(leps_all)")
    df = df.Alias("leps", "leps_sel_p") 

    df = df.Define("leps_p", "FCCAnalyses::ReconstructedParticle::get_p(leps)")
    df = df.Define("leps_theta", "FCCAnalyses::ReconstructedParticle::get_theta(leps)")
    df = df.Define("leps_phi", "FCCAnalyses::ReconstructedParticle::get_phi(leps)")
    df = df.Define("leps_q", "FCCAnalyses::ReconstructedParticle::get_charge(leps)")
    df = df.Define("leps_no", "FCCAnalyses::ReconstructedParticle::get_n(leps)")

    # momentum resolution: reco/gen
    df = df.Define("leps_all_reso_p", "FCCAnalyses::leptonResolution_p(leps_all, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle)")
    df = df.Define("leps_reso_p", "FCCAnalyses::leptonResolution_p(leps, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle)")

    # lepton kinematic histograms
    
    ## TODO: Dump histogram of muon 1, dump histogram of muon 2, etc. 
    # Do histogram after SELECTIOn of ONLY 2 MUONS
    
    ## NOTE: Reconstructed leptons -- prior to cuts (cut0)
    results.append(df.Histo1D(("leps_all_p_cut0", "", *bins_p_mu), "leps_all_p"))
    results.append(df.Histo1D(("leps_all_theta_cut0", "", *bins_theta), "leps_all_theta"))
    results.append(df.Histo1D(("leps_all_phi_cut0", "", *bins_phi), "leps_all_phi"))
    results.append(df.Histo1D(("leps_all_q_cut0", "", *bins_charge), "leps_all_q"))
    results.append(df.Histo1D(("leps_all_no_cut0", "", *bins_count), "leps_all_no"))
    results.append(df.Histo1D(("leps_all_reso_p_cut0", "", *bins_resolution), "leps_all_reso_p"))


    results.append(df.Histo1D(("leps_p_cut0", "", *bins_p_mu), "leps_p"))
    results.append(df.Histo1D(("leps_theta_cut0", "", *bins_theta), "leps_theta"))
    results.append(df.Histo1D(("leps_phi_cut0", "", *bins_phi), "leps_phi"))
    results.append(df.Histo1D(("leps_q_cut0", "", *bins_charge), "leps_q"))
    results.append(df.Histo1D(("leps_no_cut0", "", *bins_count), "leps_no"))
    results.append(df.Histo1D(("leps_reso_p_cut0", "", *bins_resolution), "leps_reso_p"))

    #########
    ### CUT 0: all events
    #########
    df = df.Define("cut0", "0")
    
    df = df.Define("visibleEnergy", "FCCAnalyses::visibleEnergy(ReconstructedParticles)")
    
    results.append(df.Histo1D(("cutFlow_cut0", "", *bins_count), "cut0"))

    
    

    #########
    ### CUT 1: at least a lepton with at least 1 isolated one
    #########
    df = df.Filter("leps_no >= 1").Define("cut1", "1")
    results.append(df.Histo1D(("cutFlow_cut1", "", *bins_count), "cut1"))


    #########
    ### CUT 2 :at least 2 leptons, and build the resonance
    #########
    df = df.Filter("leps_no >= 2").Define("cut2", "2")
    results.append(df.Histo1D(("cutFlow_cut2", "", *bins_count), "cut2"))
    
    # write a C++ function that you pass the leptons (leps_all... 'root vector' of all leptons in just A event)...
    # select one with higher pt, and lower pt
    # maybe plot highest pt distributions, lowest pt distributions, etc.

    df = df.Define("theta_plus", "(leps_all_q[0] > 0) ? leps_all_theta[0] : leps_all_theta[1]")
    df = df.Define("theta_minus", "(leps_all_q[0] < 0) ? leps_all_theta[0] : leps_all_theta[1]")
    df = df.Define("leading_pT", "(leps_all_pt[0] > leps_all_pt[1]) ? leps_all_pt[0] : leps_all_pt[1]")
    df = df.Define("subleading_pT", "(leps_all_pt[0] > leps_all_pt[1]) ? leps_all_pt[1] : leps_all_pt[0]")
    
    results.append(df.Histo1D(("theta_plus", "", *bins_theta), "theta_plus"))
    results.append(df.Histo1D(("theta_minus", "", *bins_theta), "theta_minus"))
    results.append(df.Histo1D(("leading_pT", "", *bins_p_mu), "leading_pT"))
    results.append(df.Histo1D(("subleading_pT", "", *bins_p_mu), "subleading_pT"))
    
    
    ## NOTE: Same class format for zll as reconstructed particles.
    ## NOTE: Can dumpy zll theta, and go from there. 
    # build the Z resonance from the reconstructed particles
    df = df.Define("zll", "FCCAnalyses::resonanceBuilder(91)(leps)")
    df = df.Define("zll_m", "FCCAnalyses::ReconstructedParticle::get_mass(zll)")
    df = df.Define("zll_no", "FCCAnalyses::ReconstructedParticle::get_n(zll)")
    df = df.Define("zll_p", "FCCAnalyses::ReconstructedParticle::get_p(zll)")
    df = df.Define("zll_pt", "FCCAnalyses::ReconstructedParticle::get_pt(zll)")
    df = df.Define("zll_eta", "FCCAnalyses::ReconstructedParticle::get_eta(zll)")

    ## NOTE: Code for available FCCAnalyses::ReconstructedParticle from Jan
    
    #########
    ### CUT 3 :at least 1 resonance (i.e. one opposite sign pair muon)
    #########
    df = df.Filter("zll_no >= 1").Define("cut3", "3")
    results.append(df.Histo1D(("cutFlow_cut3", "", *bins_count), "cut3"))
    results.append(df.Histo1D(("visibleEnergy", "", *bins_m_ll), "visibleEnergy"))
    

    #########
    ### CUT 4 :cut on Z mass
    #########
    df = df.Filter("(zll_m[0] > 73 && zll_m[0] < 109) || true").Define("cut4", "4")
    results.append(df.Histo1D(("cutFlow_cut4", "", *bins_count), "cut4"))
    #results.append(df.Hist1D(("", "", *bins_...), TODONAME))

    ########################
    # Final histograms
    ########################
    ## NOTE: Error ??
    results.append(df.Histo1D(("zll_m_cut4", "", *bins_m_ll), "zll_m"))
    results.append(df.Histo1D(("zll_pt_cut4", "", *bins_pt_ll), "zll_pt"))
    results.append(df.Histo1D(("zll_p_cut4", "", *bins_p_ll), "zll_p"))
    results.append(df.Histo1D(("leps_p_cut4", "", *bins_p_mu), "leps_p"))
    results.append(df.Histo1D(("zll_no_cut4", "", *bins_no_ll), "zll_no"))
    results.append(df.Histo1D(("zll_eta_cut4", "", *bins_rp_ll), "zll_eta"))

    return results, weightsum


def build_graph_qq(df, dataset):

    logger.info(f"Build graph {dataset.name}")
    results = []

    df = df.Define("weight", "1.0")
    weightsum = df.Sum("weight")

    df = df.Define("RP_px", "FCCAnalyses::ReconstructedParticle::get_px(ReconstructedParticles)")
    df = df.Define("RP_py", "FCCAnalyses::ReconstructedParticle::get_py(ReconstructedParticles)")
    df = df.Define("RP_pz", "FCCAnalyses::ReconstructedParticle::get_pz(ReconstructedParticles)")
    df = df.Define("RP_e",  "FCCAnalyses::ReconstructedParticle::get_e(ReconstructedParticles)")
    df = df.Define("RP_m",  "FCCAnalyses::ReconstructedParticle::get_mass(ReconstructedParticles)")
    df = df.Define("RP_q",  "FCCAnalyses::ReconstructedParticle::get_charge(ReconstructedParticles)")
    df = df.Define("RP_no",  "FCCAnalyses::ReconstructedParticle::get_n(ReconstructedParticles)")
    df = df.Define("pseudo_jets", "FCCAnalyses::JetClusteringUtils::set_pseudoJets(RP_px, RP_py, RP_pz, RP_e)")

    # sum of reco particles energy
    df = df.Define("Evis",  "FCCAnalyses::visibleEnergy(ReconstructedParticles)")
    df = df.Define("Evis_norm", "Evis/91.188")

    results.append(df.Histo1D(("Evis", "", *bins_m_ll), "Evis"))
    results.append(df.Histo1D(("Evis_norm", "", *bins_resolution_1), "Evis_norm"))

    results.append(df.Histo1D(("RP_no", "", *bins_count), "RP_no"))


    # more info: https://indico.cern.ch/event/1173562/contributions/4929025/attachments/2470068/4237859/2022-06-FCC-jets.pdf
    # https://github.com/HEP-FCC/FCCAnalyses/blob/master/addons/FastJet/src/JetClustering.cc
    if args.jetAlgo == "kt":
        df = df.Define("clustered_jets", "JetClustering::clustering_ee_kt(2, 2, 0, 10)(pseudo_jets)")
    elif args.jetAlgo == "valencia":
        df = df.Define("clustered_jets", "JetClustering::clustering_valencia(0.5, 1, 2, 0, 0, 1., 1.)(pseudo_jets)")
    elif args.jetAlgo == "genkt":
        #df = jetcluster_helper.run_clustering(df)
        df = df.Define("clustered_jets", "FCCAnalyses::clustering_ee_genkt(1.5, 0, 0, 0, 0, -1)(pseudo_jets)")
        #df = df.Define("clustered_jets", "JetClustering::clustering_ee_genkt(1.5, 0, 0, 0, 0, -1)(pseudo_jets)")


    df = df.Define("jets", "FCCAnalyses::JetClusteringUtils::get_pseudoJets(clustered_jets)")
    df = df.Define("jetconstituents", "FCCAnalyses::JetClusteringUtils::get_constituents(clustered_jets)")
    df = df.Define("jets_e", "FCCAnalyses::JetClusteringUtils::get_e(jets)")
    df = df.Define("jets_px", "FCCAnalyses::JetClusteringUtils::get_px(jets)")
    df = df.Define("jets_py", "FCCAnalyses::JetClusteringUtils::get_py(jets)")
    df = df.Define("jets_pz", "FCCAnalyses::JetClusteringUtils::get_pz(jets)")
    df = df.Define("jets_phi", "FCCAnalyses::JetClusteringUtils::get_phi(jets)")
    df = df.Define("jets_m", "FCCAnalyses::JetClusteringUtils::get_m(jets)")

    df = df.Define("njets", "jets_e.size()")
    results.append(df.Histo1D(("njets", "", *bins_count), "njets"))
    df = df.Filter("njets >= 2")

    # reconstruct resonance (jets are pT ordered)
    df = df.Define("jet1", "ROOT::Math::PxPyPzEVector(jets_px[0], jets_py[0], jets_pz[0], jets_e[0])")
    df = df.Define("jet2", "ROOT::Math::PxPyPzEVector(jets_px[1], jets_py[1], jets_pz[1], jets_e[1])")
    df = df.Define("dijet", "jet1+jet2")
    df = df.Define("dijet_m", "dijet.M()")

    # added mass cut
    df = df.Filter("(dijet_m > 73 && dijet_m < 109) || true").Define("cut3", "3")

    #df = df.Define("dijet_m", "dijet.M()")

    results.append(df.Histo1D(("jets_e", "", *jet_energy), "jets_e"))
    results.append(df.Histo1D(("dijet_m", "", *dijet_m), "dijet_m"))
    results.append(df.Histo1D(("dijet_m_final", "", *dijet_m_final), "dijet_m"))

    results.append(df.Histo1D(("jets_phi", "", *bins_phi), "jets_phi"))    


    df = df.Define("visibleMass", "FCCAnalyses::visibleMass(ReconstructedParticles)") # scalar
    df = df.Define("missingEnergy_vec", "FCCAnalyses::missingEnergy(91.1, ReconstructedParticles)") # returns a vector
    df = df.Define("missingEnergy", "FCCAnalyses::ReconstructedParticle::get_e(missingEnergy_vec)")

    results.append(df.Histo1D(("visibleMass", "", *visMass), "visibleMass"))    
    results.append(df.Histo1D(("missingEnergy", "", *missEnergy), "missingEnergy"))    

    df = df.Define('EVT_thrust',     'FCCAnalyses::Algorithms::minimize_thrust("Minuit2","Migrad")(RP_px, RP_py, RP_pz)')
    df = df.Define('EVT_thrust_x',   "EVT_thrust.at(1)")
    df = df.Define('EVT_thrust_y',   "EVT_thrust.at(3)")
    df = df.Define('EVT_thrust_z',   "EVT_thrust.at(5)")
    df = df.Define('EVT_thrust_r',   "sqrt(EVT_thrust_x*EVT_thrust_x+EVT_thrust_y*EVT_thrust_y+EVT_thrust_z*EVT_thrust_z)")
    df = df.Define('EVT_thrust_val', "EVT_thrust.at(0)")
    df = df.Define('EVT_cos_thrustangle', 'EVT_thrust_z/EVT_thrust_r')
    df = df.Define('EVT_cos_thrustangle_abs', 'abs(EVT_cos_thrustangle)')

    results.append(df.Histo1D(("EVT_thrust_val", "", *bins_thrustval), "EVT_thrust_val"))
    results.append(df.Histo1D(("EVT_cos_thrustangle", "", *bins_cos), "EVT_cos_thrustangle"))
    results.append(df.Histo1D(("EVT_cos_thrustangle_abs", "", *bins_cos), "EVT_cos_thrustangle_abs"))
    results.append(df.Histo1D(("EVT_thrust_x", "", *bins_thrustcomp), "EVT_thrust_x"))
    results.append(df.Histo1D(("EVT_thrust_y", "", *bins_thrustcomp), "EVT_thrust_y"))
    results.append(df.Histo1D(("EVT_thrust_z", "", *bins_thrustcomp), "EVT_thrust_z"))
    results.append(df.Histo1D(("EVT_thrust_r", "", *bins_thrustcomp), "EVT_thrust_r"))

    return results, weightsum


if __name__ == "__main__":

    datadict = functions.get_datadicts() # get default datasets

    if args.flavor == "mumu": 
        #datasets_to_run = ["wzp6_ee_mumu_ecm91p2", "wzp6_ee_tautau_ecm91p2", "wzp6_ee_qq_ecm91p2"]
        datasets_to_run = ["wz3p6_ee_gaga_mumu_ecm91p2", "p8_ee_gaga_mumu_ecm91p2"]
        #result = functions.build_and_run(datadict, datasets_to_run,  build_graph_ll, f"output_z_xsec_mumu.root", args, norm=True, lumi=150000000)
        result = functions.build_and_run(datadict, datasets_to_run,  build_graph_ll, f"output_z_xsec_mumu_gaga.root", args, norm=True, lumi=150000000)

    if args.flavor == "ee":
        #datasets_to_run = ["wzp6_ee_ee_Mee_5_150_ecm91p2", "wzp6_ee_tautau_ecm91p2", "wzp6_ee_qq_ecm91p2"]
        datasets_to_run = ["wz3p6_ee_gaga_mumu_ecm91p2", "p8_ee_gaga_mumu_ecm91p2"]

        result = functions.build_and_run(datadict, datasets_to_run, build_graph_ll, f"output_z_xsec_mumu_gagaELECTRON.root", args, norm=True, lumi=150000000)
 
    if args.flavor == "qq":
        #datasets_to_run = ["wzp6_ee_qq_ecm91p2"]
        datasets_to_run = ["wz3p6_ee_gaga_qq_ecm91p2", "p8_ee_gaga_qq_ecm91p2"]
        result = functions.build_and_run(datadict, datasets_to_run, build_graph_qq, f"output_z_xsec_qq_gaga.root", args, norm=True, lumi=150000000)

