from root_pandas import read_root
import numpy
#filename="/tmp/khurana/EXO-ggToXdXdHToBB_sinp_0p35_tanb_1p0_mXd_10_MH3_1200_MH4_150_MH2_1200_MHC_1200_CP3Tune_13TeV_0000_0.root"
filename="/tmp/khurana/Merged_TTSemileptonic.root"
df = read_root(filename, "monoHbb_SR_boosted", columns=["run","lumi","event","MET","nJets"])

df.to_csv(filename.replace(".root",".csv"))
