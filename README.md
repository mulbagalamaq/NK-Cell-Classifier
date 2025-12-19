# NK Cell Multimodal Single-Cell Analysis

Analysis of NK cell differentiation using CITE-seq, scRNA-seq, and ATAC-seq data
from Foltz et al. 2024 (Science Immunology).

## Data Sources

- GSE264696: CITE-seq (NK cells, 28-protein panel)


## Target Cell Types

- CD56bright NK cells
- CD56dim NK cells  
- eML-1 (enriched memory-like, from CD56bright)
- eML-2 (enriched memory-like, from CD56dim)

## Environment
```bash
conda env create -f envs/environment.yml
conda activate nk_analysis
```

## Reproducibility

- Random seed: 42
- All dependencies pinned in environment.yml


## Notebooks

### 01_preprocessing_qc.ipynb
- Loaded CITE-seq data from two donors (21,167 cells, 28-protein panel)
- Removed 31,053 mouse spike-in genes and applied QC filters (≥200 genes, <15% mito)
- Ran TOTALVI to jointly model 4,000 HVGs and 28 surface proteins
- Batch-corrected across donors, extracted 20-dimensional latent embeddings
- Annotated NK subsets via hierarchical protein gating: CD56bright (CD117+), CD56dim (CD57+CD16+), eML (NKG2A+ only)
- Final dataset: 19,443 cells with denoised protein expression

### 02_classifier_training.ipynb
- Trained classifiers on TOTALVI latent embeddings to predict NK subsets from RNA
- Compared BalancedBaggingClassifier and XGBoost on 3-class problem (excluding Unassigned)
- XGBoost achieved best performance: macro F1 = 0.789 (5-fold CV)
- eML classification challenging (F1 = 0.56) due to small sample size (4%) and phenotypic overlap
- Saved trained models for downstream inference


## References

Foltz JA, Tran J, Wong P, Fan C, Schmidt E, Fisk B, Becker-Hapak M, Russler-Germain DA, Johnson J, Marin ND, Cubitt CC, Pence P, Rueve J, Pureti S, Hwang K, Gao F, Zhou AY, Foster M, Schappe T, Marsala L, Berrien-Elliott MM, Cashen AF, Bednarski JJ, Fertig E, Griffith OL, Griffith M, Wang T, Petti AA, Fehniger TA. Cytokines drive the formation of memory-like NK cell subsets via epigenetic rewiring and transcriptional regulation. *Science Immunology*. 2024 Jun 28;9(96):eadk4893. doi: 10.1126/sciimmunol.adk4893

**Data availability:**
- CITE-seq: [GSE264696](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE264696)
