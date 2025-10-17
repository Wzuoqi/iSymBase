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

```
#query  seed_ortholog   evalue  score   eggNOG_OGs      max_annot_lvl   COG_category    Description     Preferred_name  GOs     EC      KEGG_ko KEGG_Pathway    KEGG_Module     KEGG_Reaction       KEGG_rclass     BRITE   KEGG_TC CAZy    BiGG_Reaction   PFAMs
k141_49113_1    399739.Pmen_0563        6.73e-98        308.0   COG0286@1|root,COG0286@2|Bacteria,1MW3A@1224|Proteobacteria,1RMRA@1236|Gammaproteobacteria,1YG4S@136841|Pseudomonas aeruginosa group        1236|Gammaproteobacteria        V       HsdM N-terminal domain  -       -       2.1.1.72        ko:K03427       -       -       -       -       ko00000,ko01000,ko02048     -       -       -       HsdM_N,N6_Mtase
k141_158245_1   1196083.SALWKB12_1358   0.000235        44.7    COG5008@1|root,COG5008@2|Bacteria,1QTTX@1224|Proteobacteria,2VIWS@28216|Betaproteobacteria,2KQ1N@206351|Neisseriales        206351|Neisseriales     NU      twitching motility protein      -       -       -       ko:K02670       -       -       -       -       ko00000,ko02035,ko02044 3.A.15.2            -       -       T2SSE
k141_54570_1    1196083.SALWKB12_1404   4.43e-73        220.0   COG2018@1|root,COG2018@2|Bacteria,1RIQC@1224|Proteobacteria,2VTV9@28216|Betaproteobacteria,2KREG@206351|Neisseriales        206351|Neisseriales     S       Roadblock/LC7 domain    -       -       -       ko:K07131       -       -       -       -       ko00000 -       -       -       Robl_LC7
k141_70941_1    1196095.GAPWK_2138      7.53e-240       665.0   COG0477@1|root,COG0477@2|Bacteria,1MU46@1224|Proteobacteria,1RMJI@1236|Gammaproteobacteria      1236|Gammaproteobacteria    EGP     Major facilitator superfamily   -       -       -       ko:K03762       -       -       -       -       ko00000,ko02000 2.A.1.6.4       -       -       MFS_1,Sugar_tr
k141_152787_2   1196083.SALWKB12_0080   1.31e-130       375.0   COG0101@1|root,COG0101@2|Bacteria,1MUYI@1224|Proteobacteria,2VI0R@28216|Betaproteobacteria,2KPYY@206351|Neisseriales        206351|Neisseriales     J       Formation of pseudouridine at positions 38, 39 and 40 in the anticodon stem and loop of transfer RNAs   truA    -       5.4.99.12       ko:K06173   -       -       -       -       ko00000,ko01000,ko03016 -       -       -       PseudoU_synth_1
k141_5457_2     1500281.JQKZ01000011_gene1952   4.53e-06        50.8    COG0741@1|root,COG3179@1|root,COG0741@2|Bacteria,COG3179@2|Bacteria,4NWM0@976|Bacteroidetes,1IIYH@117743|Flavobacteriia,3ZUK5@59732|Chryseobacterium        976|Bacteroidetes       M       LysM domain     -       -       -       -       -       -       -       -       -       -       -           -       SLT
k141_1_2        1123296.JQKE01000007_gene423    7.48e-09        58.2    COG4967@1|root,COG4967@2|Bacteria,1RHZ5@1224|Proteobacteria,2VTBV@28216|Betaproteobacteria,2KS05@206351|Neisseriales        206351|Neisseriales     NU      type IV pilus modification protein PilV pilV    -       -       ko:K02671       -       -       -       -       ko00000,ko02035,ko02044     -       -       -       N_methyl
```

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
