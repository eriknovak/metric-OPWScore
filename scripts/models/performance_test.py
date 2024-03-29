import sys
import yaml

from src.models.model import OPWScore

from src.data.preprocess import calculate_scores


# =====================================
# Import Inputs
# =====================================

languages = sys.argv[1].split(",") if len(sys.argv) >= 2 else None
datasets = sys.argv[2].split(",") if len(sys.argv) >= 3 else None

# =====================================
# Import Model Parameters
# =====================================

params = yaml.safe_load(open("params.yaml"))

distance = params["model"]["distance"]
weight_dist = params["model"]["weight_dist"]
temporal_type = params["model"]["temporal_type"]
reg1 = params["model"]["reg1"]
reg2 = params["model"]["reg2"]
nit = params["model"]["nit"]

# =====================================
# Calculate the Scores on the Datasets
# =====================================

for language in languages:
    # prepare the model
    model = OPWScore(
        distance=distance,
        weight_dist=weight_dist,
        temporal_type=temporal_type,
        lang=language,
        reg1=reg1,
        reg2=reg2,
        nit=nit,
    )

    if datasets == None or "wmt18" in datasets:
        print("WMT18 dataset: Start evaluation")
        calculate_scores(model, "wmt18")

    if datasets == None or "wmt20" in datasets:
        print("WMT20 dataset: Start evaluation")
        calculate_scores(model, "wmt20")
