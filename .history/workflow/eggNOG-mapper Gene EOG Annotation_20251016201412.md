# 🧬 Gene Functional Annotation Workflow Using EggNOG-mapper

## 1. Overview

After metagenomic assembly and gene prediction (e.g., using **MEGAHIT** and **Prodigal**), the next step is to assign biological functions to the predicted genes.
In this workflow, **EggNOG-mapper v2** (Cantalapiedra *et al.*, 2021) was used to perform large-scale **functional annotation** of the non-redundant gene set.

EggNOG-mapper infers the function of each predicted coding sequence (CDS) by identifying **orthologous groups (OGs)** from the **EggNOG 5.0** database, providing annotations such as Gene Ontology (GO), KEGG Orthology (KO), COG categories, Enzyme Commission (EC) numbers, and Pfam domains.

---

## 2. Principle

EggNOG-mapper uses a **hierarchical orthology-based approach** rather than simple sequence similarity to annotate genes.
Its core workflow includes the following steps:

1. **Homology Search**: Each predicted CDS is aligned against the EggNOG protein database using **DIAMOND** (or MMseqs2) for high-speed sequence similarity search.
2. **Orthology Assignment**: The best hit (“seed ortholog”) is used to assign the query to a precomputed **orthologous group (OG)**.
3. **Functional Transfer**: Functional annotations (e.g., GO terms, KEGG pathways, enzyme activities) are transferred from the orthologous group to the query gene.
4. **Hierarchical Filtering**: The most appropriate phylogenetic level (e.g., bacteria, archaea, fungi) is automatically selected for annotation transfer.

---

## 3. Command and Parameters

The annotation was performed using the following command:

```bash
/data/home/wangzuoqi/mambaforge/envs/eggnog/bin/emapper.py \
    -i ./SRR7986811/SRR7986811.select.gene.fa \
    --output ./SRR7986811/SRR7986811 \
    --data_dir /data/software/eggnog5/ \
    -m diamond \
    --cpu 64 \
    --itype CDS
````

### Parameter Description

| Parameter     | Description                                                                   |
| ------------- | ----------------------------------------------------------------------------- |
| `-i`          | Input file containing coding DNA sequences (CDS) from Prodigal prediction.    |
| `--output`    | Output prefix for all EggNOG-mapper result files.                             |
| `--data_dir`  | Path to the local EggNOG 5.0 database directory.                              |
| `-m diamond`  | Use DIAMOND for rapid sequence alignment.                                     |
| `--cpu 64`    | Number of threads for parallel computation.                                   |
| `--itype CDS` | Input type is nucleotide coding sequences (will be translated automatically). |

---

## 4. Database Information

The **EggNOG 5.0** database integrates orthologous groups and functional annotations derived from major repositories such as **NCBI RefSeq**, **UniProt**, and **Ensembl**.
It includes millions of protein sequences across **bacteria, archaea, fungi, protists, and eukaryotes**, providing a comprehensive reference for metagenomic annotation.


---

## 5. Output Description

The main output file is a tab-delimited text file named like:

```
SRR7986811.emapper.annotations
```

Each row represents one annotated gene and contains fields such as:

| Column             | Description                                                                      |
| ------------------ | -------------------------------------------------------------------------------- |
| `query`            | Query sequence ID                                                                |
| `seed_ortholog`    | Closest reference ortholog in the database                                       |
| `evalue` / `score` | Alignment significance and bit score                                             |
| `eggNOG_OGs`       | Orthologous group assignments                                                    |
| `max_annot_lvl`    | Highest annotation taxonomic level                                               |
| `COG_category`     | Functional COG classification (e.g., E = Amino acid metabolism, J = Translation) |
| `Description`      | Functional description of the protein                                            |
| `Preferred_name`   | Standardized protein/gene name                                                   |
| `GOs`              | Gene Ontology terms (BP, MF, CC)                                                 |
| `EC`               | Enzyme Commission number                                                         |
| `KEGG_ko`          | KEGG Orthology identifier                                                        |
| `KEGG_Pathway`     | KEGG pathway IDs                                                                 |
| `PFAMs`            | Pfam domain annotations                                                          |

---

## 6. Example Results

Below is an example snippet of the annotation output:

| Query           | Description                            | EC        | KEGG\_ko | KEGG\_Pathway               | PFAMs              |
| --------------- | -------------------------------------- | --------- | -------- | --------------------------- | ------------------ |
| k141\_49113\_1  | HsdM N-terminal domain                 | 2.1.1.72  | K03427   | ko02048 (ABC transporters)  | HsdM\_N, N6\_Mtase |
| k141\_70941\_1  | Major facilitator superfamily          | -         | K03762   | ko02000 (Transporters)      | MFS\_1, Sugar\_tr  |
| k141\_152787\_2 | Pseudouridine synthase TruA            | 5.4.99.12 | K06173   | ko03016 (tRNA modification) | PseudoU\_synth\_1  |
| k141\_130965\_1 | Serine/Threonine protein kinase (SSK2) | 2.7.11.25 | K11230   | ko04011 (MAPK signaling)    | Pkinase            |

---

## 7. Full Workflow Overview

```bash
# Step 1: Assembly
megahit -1 sample_R1.fq -2 sample_R2.fq -o megahit_out

# Step 2: Gene Prediction
prodigal -i megahit_out/final.contigs.fa \
         -o genes.gff -d genes.fa -a genes.pep -p meta

# Step 3: Redundancy Removal
cd-hit-est -i genes.fa -o genes.cdhit.fa -c 0.9 -aS 0.9 -T 64 -M 0

# Step 4: Functional Annotation (EggNOG-mapper)
emapper.py -i genes.cdhit.fa \
           --output genes.eggnog \
           --data_dir /data/software/eggnog5/ \
           -m diamond \
           --cpu 64 \
           --itype CDS
```

---

## 8. Downstream Applications

The EggNOG-mapper annotation enables:

* **Functional category profiling** (COG/KEGG classification)
* **Pathway enrichment analysis** using KEGG KO terms
* **Metabolic network reconstruction** from EC numbers
* **Comparative functional analysis** across metagenomic samples

---

## 9. References

> Cantalapiedra, C. P., Hernández-Plaza, A., Letunic, I., Bork, P., & Huerta-Cepas, J. (2021).
> *eggNOG-mapper v2: Functional annotation, orthology assignments, and domain prediction at the metagenomic scale.*
> **Molecular Biology and Evolution**, 38(12), 5825–5829.
> [https://github.com/eggnogdb/eggnog-mapper](https://github.com/eggnogdb/eggnog-mapper)

---

✨ **Summary:**
EggNOG-mapper provides a fast, accurate, and hierarchical approach to gene functional annotation, integrating GO, KEGG, EC, COG, and Pfam information for comprehensive interpretation of metagenomic data.

```

---

Would you like me to add a **diagram (Markdown + Mermaid)** that visualizes the workflow (e.g., from assembly → annotation → downstream analysis) for your GitHub README? It can make the workflow more intuitive.
```
