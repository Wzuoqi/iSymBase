# Amplicon Data Processing Workflow

## Overview

This workflow describes the analysis of amplicon sequencing data (e.g., 16S rRNA gene, ITS) from insect microbiome samples. The pipeline consists of five sequential steps:

1. **Quality Control and Merging** — Fastp preprocessing of raw paired-end reads.
2. **Primer Sequence Trimming** — Seqtk-based uniform trimming of primer sequences.
3. **OTU Clustering and Taxonomic Annotation** — Vsearch-based OTU generation, chimera removal, and preliminary classification.
4. **Taxonomic Refinement** — Qiime 2 classification using a pre-trained Greengenes classifier.
5. **Functional Annotation** — FAPROTAX-based functional prediction from taxonomic profiles.

This pipeline is complementary to the metagenomics workflow; amplicon data provides taxonomic and functional profiles, while metagenomics provides genome-resolved functional insights.

---

## Required Software

| Tool | Purpose |
|---|---|
| **Fastp** | FASTQ quality control, adapter removal, and paired-end merging. |
| **Seqtk** | FASTA/Q sequence manipulation and trimming. |
| **Vsearch** | Sequence clustering, dereplication, chimera detection, and SINTAX classification. |
| **Qiime 2** | Microbiome analysis platform with pre-trained taxonomic classifiers. |
| **FAPROTAX** | Literature-based functional inference from prokaryotic taxonomic profiles. |

### Reference Databases

- **Greengenes v13.5** — 16S rRNA reference database for Vsearch SINTAX annotation.
- **Pre-trained Greengenes classifier** (`gg_2022_10_backbone_full_length.nb.qza`) — Qiime 2-compatible Naive Bayes classifier.

---

## Detailed Procedure

### 1. Quality Control and Merging (Fastp)

**a. Quality Control**

```bash
fastp -i input_file1 -I input_file2 \
    --q 15 -u 40 -l 15 \
    -o output_file1 -O output_file2 \
    --detect_adapter_for_pe
```

| Parameter | Description |
|---|---|
| `-i, -I` | Paired-end input files. |
| `--q 15` | Trim bases with quality score below 15. |
| `-u 40` | Maximum percentage of bases allowed to be trimmed per read (40%). |
| `-l 15` | Discard reads shorter than 15 bp after trimming. |
| `-o, -O` | Output files. |
| `--detect_adapter_for_pe` | Auto-detect and remove adapters for paired-end data. |

**b. Paired-End Merging**

```bash
fastp -i output_file1 -I output_file2 \
    -m --merged_out merged_file
```

- `-m, --merge`: Enable paired-end merging mode.
- `--merged_out`: Output file for successfully merged reads.

---

### 2. Primer Sequence Trimming (Seqtk)

Uniformly trim primer sequences from both ends of merged reads to eliminate primer bias in downstream clustering.

```bash
seqtk trimfq -b 20 -e 20 input_file > output_file
```

- `-b 20`: Trim 20 bases from the 5' end (forward primer).
- `-e 20`: Trim 20 bases from the 3' end (reverse primer).

---

### 3. OTU Table Generation and Annotation (Vsearch)

**a. Dereplication** — Merge identical sequences and remove singletons.

```bash
vsearch --fastx_uniques "$input_file" \
    --minuniquesize 3 --threads 8 \
    --sizeout \
    --fastaout "${output_folder}/${base_name}.na.fasta"
```

**b. OTU Clustering** — Cluster at 97% sequence similarity.

```bash
vsearch --cluster_fast "${output_folder}/${base_name}.na.fasta" \
    --id 0.97 \
    --centroid "${output_folder}/${base_name}.otu.fa" \
    --relabel "${base_name}_" \
    --sizeout --threads 8
```

**c. Chimera Removal** — De novo detection and removal of PCR chimeras.

```bash
vsearch --uchime3_denovo "${output_folder}/${base_name}.otu.fa" \
    --threads 8 \
    --nonchimeras "${output_folder}/${base_name}.otuna.fa"
```

**d. OTU Table Generation** — Map reads back to OTU representatives.

```bash
vsearch --usearch_global "$input_file" \
    --db "${output_folder}/${base_name}.otuna.fa" \
    --id 0.97 --threads 8 \
    --otutabout "${output_folder}/${base_name}.otutab.txt"
```

**e. Taxonomic Classification (SINTAX)** — Assign taxonomy using the Greengenes database.

```bash
vsearch --sintax "${output_folder}/${base_name}.otuna.fa" \
    --db "$sintax_db" \
    --sintax_cutoff 0.1 --threads 8 \
    --tabbedout "${output_folder}/${base_name}.sintax"
```

---

### 4. Taxonomic Refinement (Qiime 2)

**a. Import OTU Sequences**

```bash
qiime tools import \
    --type 'FeatureData[Sequence]' \
    --input-path "${base_name}.otuna.fa" \
    --output-path "${base_name}.repotu.qza"
```

**b. Classify with Pre-trained Greengenes Classifier**

```bash
qiime feature-classifier classify-sklearn \
    --i-classifier "gg_2022_10_backbone_full_length.nb.qza" \
    --i-reads "${base_name}.repotu.qza" \
    --o-classification "${base_name}.taxonomy.qza"
```

**c. Export Results**

```bash
qiime tools export \
    --input-path "${base_name}.taxonomy.qza" \
    --output-path "taxonomy_folder"
```

The exported `taxonomy.tsv` file is located in the specified output directory.

---

### 5. Functional Annotation (FAPROTAX)

Predict potential microbial community functions based on Qiime 2 taxonomic assignments.

```bash
python collapse_table.py \
    -i "taxonomy_folder/taxonomy.tsv" \
    -o "${base_name}.faprotax" \
    -g "FAPROTAX.txt" \
    -r "${base_name}.report.txt" \
    -v -d 'Taxon'
```

**Requirements:** The `collapse_table.py` script and `FAPROTAX.txt` database are distributed with the FAPROTAX package (http://www.loucalab.com/archive/FAPROTAX/).
