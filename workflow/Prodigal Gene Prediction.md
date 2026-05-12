# Prodigal: Gene Prediction and Functional Annotation

## 1. Prodigal Gene Prediction

Prodigal (PROkaryotic DYnamic programming Gene-finding ALgorithm) is a widely-used gene prediction tool for prokaryotic genomes and metagenomes.

### Overview

Prodigal is an unsupervised machine learning algorithm that automatically learns genome properties from the sequence itself—including genetic code, RBS motif usage, start codon usage, and coding statistics—without requiring external training data.

**Key features:**

- Fast, accurate prediction of protein-coding genes.
- Output in GFF3, GenBank, or Sequin table formats.
- Suitable for complete genomes, draft genomes, and metagenomes.
- Handles gaps, scaffolds, and partial genes.
- Identifies translation start sites with confidence scores.
- Provides summary statistics (GC content, GC skew, RBS motifs, codon usage).

**Limitations:**

- Does not predict RNA genes.
- Does not handle genes with introns (extremely rare in prokaryotes).
- Does not provide functional annotation.
- Not optimized for viral gene prediction.

A Python binding, **Pyrodigal**, provides the same functionality with performance optimizations.

### Installation

```bash
conda install -c bioconda prodigal
```

### Detailed Parameters

```
Usage: prodigal [-a trans_file] [-c] [-d nuc_file] [-f output_type]
                [-g tr_table] [-h] [-i input_file] [-m] [-n] [-o output_file]
                [-p mode] [-q] [-s start_file] [-t training_file] [-v]

    -a   Write protein translations to the selected file.
    -c   Closed ends. Do not allow genes to run off edges.
    -d   Write nucleotide sequences of genes to the selected file.
    -f   Select output format (gbk, gff, or sco). Default is gbk.
    -g   Specify a translation table to use (default 11).
    -h   Print help menu and exit.
    -i   Specify FASTA/GenBank input file (default reads from stdin).
    -m   Treat runs of N as masked sequence; don't build genes across them.
    -n   Bypass Shine-Dalgarno trainer and force a full motif scan.
    -o   Specify output file (default writes to stdout).
    -p   Select procedure (single or meta). Default is single.
    -q   Run quietly (suppress normal stderr output).
    -s   Write all potential genes (with scores) to the selected file.
    -t   Write a training file; or read and use the specified training file.
    -v   Print version number and exit.
```

### Usage Example

```bash
prodigal -i ./megahit/DRR505509.contigs.fa \
    -o ./megahit/DRR505509.gff \
    -d ./megahit/DRR505509.gene.fa \
    -a ./megahit/DRR505509.anno.pep.fa \
    -f gff \
    -p meta
```

**Output files:**

| File | Content |
|---|---|
| `DRR505509.gff` | Gene coordinates in GFF3 format. |
| `DRR505509.gene.fa` | Predicted gene nucleotide sequences. |
| `DRR505509.anno.pep.fa` | Translated protein sequences. |

---

## 2. CD-HIT Redundancy Removal

Remove redundant gene sequences before downstream annotation to reduce computational load.

```bash
cd-hit-est -i DRR505509.gene.fa \
    -o DRR505509.cdhit.gene.fa \
    -c 0.9 -G 0 -M 0 -T 64 -aS 0.9
```

| Parameter | Description |
|---|---|
| `-i` | Input gene sequences (FASTA). |
| `-o` | Output non-redundant gene set. |
| `-c 0.9` | Sequence identity threshold (90%). |
| `-G 0` | No length limit on sequences. |
| `-aS 0.9` | Global alignment similarity threshold (90%). |
| `-M 0` | Auto-set memory limit. |
| `-T 64` | Number of threads. |

---

## 3. Functional Annotation with DIAMOND BLASTX

After gene prediction and redundancy removal, functional annotation infers the possible functions of predicted genes by comparing them against a custom protein reference database.

### 3.1 About DIAMOND

DIAMOND is a high-speed sequence aligner designed as a drop-in replacement for BLASTX, achieving up to 20,000× speed improvement while maintaining high sensitivity. It is widely used for large-scale metagenomic datasets.

**Repository**: https://github.com/bbuchfink/diamond

### 3.2 About the Symbionts Database

The **Symbionts database** is a custom subset of the NCBI NR (non-redundant protein) database, filtered to include only sequences from:

- **Bacteria** (taxid: 2)
- **Archaea** (taxid: 2157)
- **Fungi** (taxid: 4751)

This focused design reduces computational load while improving annotation relevance for host-associated microbiomes. See `database/build_symbionts_db.py` for the construction script.

### 3.3 DIAMOND BLASTX Command

```bash
diamond blastx \
    --db /data/software/nr_db/Symbionts \
    --query ./DRR505509/megahit/DRR505509.cdhit.gene.fa \
    --out ./DRR505509/DRR505509.diamond.tab \
    --outfmt 6 \
    --max-target-seqs 1 \
    --evalue 1e-5 \
    -p 64
```

| Parameter | Description |
|---|---|
| `--db` | Path to the Symbionts protein database. |
| `--query` | Non-redundant gene sequences from CD-HIT. |
| `--out` | Output file in tabular format. |
| `--outfmt 6` | BLAST tabular format (12-column TSV). |
| `--max-target-seqs 1` | Report only the top hit per query. |
| `--evalue 1e-5` | E-value threshold for significance. |
| `-p 64` | Number of CPU threads. |

### 3.4 Output Format (outfmt 6)

| Column | Name | Description |
|---|---|---|
| 1 | qseqid | Query gene ID. |
| 2 | sseqid | Subject protein accession. |
| 3 | pident | Percentage identity. |
| 4 | length | Alignment length. |
| 5 | mismatch | Mismatch count. |
| 6 | gapopen | Gap openings. |
| 7 | qstart | Query start position. |
| 8 | qend | Query end position. |
| 9 | sstart | Subject start position. |
| 10 | send | Subject end position. |
| 11 | evalue | E-value. |
| 12 | bitscore | Bit score. |

### Example Output

```
k141_70941_1    WP_267357184.1   96.6   354   12   0   1   1062   1   354    1.66e-243   677
k141_152787_2   WP_096766202.1   98.5   204    3   0   1    612   80  283    1.41e-142   409
k141_5457_1     WP_144093549.1   95.8   120    5   0   1    360   1   120    3.29e-79    242
k141_1_2        ORF04991.1       100    107    0   0   1    321   1   107    1.24e-62    197
```

### 3.5 Downstream Analysis

Map matched protein accessions to functional annotations (KEGG, COG, GO) using annotation mapping tables:

```bash
# Extract unique matched protein accessions
awk '{print $2}' DRR505509.diamond.tab | sort | uniq > matched_proteins.list
```

For comprehensive functional annotation (GO, KEGG, COG, EC, Pfam), use **eggNOG-mapper** on the non-redundant gene set. See [eggNOG-mapper Gene Annotation](eggNOG-mapper%20Gene%20Annotation.md).
