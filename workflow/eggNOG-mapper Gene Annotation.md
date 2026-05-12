# Gene Functional Annotation Workflow Using eggNOG-mapper

## 1. Overview

After metagenomic assembly and gene prediction (e.g., using **MEGAHIT** and **Prodigal**), the next step is to assign biological functions to the predicted genes. This workflow uses **eggNOG-mapper v2** (Cantalapiedra *et al.*, 2021) for large-scale functional annotation of the non-redundant gene set.

eggNOG-mapper infers the function of each predicted coding sequence (CDS) by identifying **orthologous groups (OGs)** from the **eggNOG 5.0** database, providing annotations such as Gene Ontology (GO), KEGG Orthology (KO), COG categories, Enzyme Commission (EC) numbers, and Pfam domains.

---

## 2. Principle

eggNOG-mapper uses a **hierarchical orthology-based approach** rather than simple sequence similarity:

1. **Homology Search**: Each predicted CDS is aligned against the eggNOG protein database using **DIAMOND** (or MMseqs2) for high-speed sequence similarity search.
2. **Orthology Assignment**: The best hit ("seed ortholog") assigns the query to a precomputed orthologous group (OG).
3. **Functional Transfer**: Functional annotations (GO terms, KEGG pathways, enzyme activities) are transferred from the orthologous group to the query gene.
4. **Hierarchical Filtering**: The most appropriate phylogenetic level (e.g., bacteria, archaea, fungi) is automatically selected for annotation transfer.

---

## 3. Command and Parameters

```bash
emapper.py \
    -i ./SRR7986811/SRR7986811.select.gene.fa \
    --output ./SRR7986811/SRR7986811 \
    --data_dir /data/software/eggnog5/ \
    -m diamond \
    --cpu 64 \
    --itype CDS
```

### Parameter Description

| Parameter | Description |
|---|---|
| `-i` | Input file containing coding DNA sequences (CDS) from Prodigal prediction. |
| `--output` | Output prefix for all eggNOG-mapper result files. |
| `--data_dir` | Path to the local eggNOG 5.0 database directory. |
| `-m diamond` | Use DIAMOND for rapid sequence alignment. |
| `--cpu 64` | Number of threads for parallel computation. |
| `--itype CDS` | Input type is nucleotide coding sequences (translated automatically). |

---

## 4. Database Information

The **eggNOG 5.0** database integrates orthologous groups and functional annotations derived from major repositories including **NCBI RefSeq**, **UniProt**, and **Ensembl**. It covers millions of protein sequences across bacteria, archaea, fungi, protists, and eukaryotes, providing a comprehensive reference for metagenomic annotation.

Reference: http://eggnog5.embl.de/

---

## 5. Output Description

The main output file is a tab-delimited text file:

```
SRR7986811.emapper.annotations
```

Each row represents one annotated gene:

```
#query  seed_ortholog   evalue  score   eggNOG_OGs  max_annot_lvl   COG_category  ...
k141_49113_1    399739.Pmen_0563   6.73e-98   308.0   COG0286@1|root,...   1236|Gammaproteobacteria   V   HsdM N-terminal domain   ...
k141_158245_1   1196083.SALWKB12_1358   0.000235   44.7   COG5008@1|root,...   206351|Neisseriales   NU   twitching motility protein   ...
```

**Key output columns:**

| Column | Description |
|---|---|
| `#query` | Query gene ID (from Prodigal/CD-HIT output). |
| `seed_ortholog` | Best-matching ortholog in eggNOG database. |
| `evalue` | E-value of the sequence match. |
| `score` | Alignment bit score. |
| `eggNOG_OGs` | Assigned orthologous groups at multiple taxonomic levels. |
| `COG_category` | COG functional category letter(s). |
| `Description` | Functional description of the orthologous group. |
| `GOs` | Gene Ontology term identifiers. |
| `EC` | Enzyme Commission number(s). |
| `KEGG_ko` | KEGG Orthology identifier. |
| `KEGG_Pathway` | Associated KEGG pathway map IDs. |
| `PFAMs` | Pfam domain identifiers. |

---

## 6. References

> Cantalapiedra, C. P., Hernández-Plaza, A., Letunic, I., Bork, P., & Huerta-Cepas, J. (2021). *eggNOG-mapper v2: Functional annotation, orthology assignments, and domain prediction at the metagenomic scale.* **Molecular Biology and Evolution**, 38(12), 5825–5829.

- eggNOG-mapper: https://github.com/eggnogdb/eggnog-mapper
- eggNOG 5.0: http://eggnog5.embl.de/
