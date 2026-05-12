# Kraken 2: Taxonomic Sequence Classification

## Software Introduction

Kraken 2 is a taxonomic annotation tool for metagenomic research that identifies the species origin of DNA sequences through fast, accurate k-mer matching. It assigns taxonomic labels to metagenomic reads by comparing each k-mer against a reference database.

**Key features:**

- **High efficiency**: Multi-threaded k-mer matching enables large-scale classification in a short time.
- **High accuracy**: K-mer-based classification outperforms traditional alignment methods like BLAST for taxonomic assignment.
- **Extensive databases**: Supports NCBI, Greengenes, RDP, and SILVA reference databases.
- **Flexibility**: Users can build custom reference databases for specific research needs.
- **Clear output**: Results in table format for straightforward downstream analysis and visualization.
- **Integration**: Can be paired with **Bracken** to improve abundance estimation from Kraken 2 reports.

**Repository**: https://github.com/DerrickWood/kraken2

---

## Annotation Workflow

### 1. Database Preparation

#### Download Taxonomy Information

```bash
DBNAME=~/db/kraken2
mkdir -p $DBNAME

# Download NCBI taxonomy
kraken2-build --download-taxonomy --threads 24 --db $DBNAME
```

#### Download Sequence Libraries

```bash
# Download a single library (e.g., bacteria)
kraken2-build --download-library bacteria --threads 24 --db $DBNAME

# Batch download all standard libraries
for lib in archaea bacteria plasmid viral human fungi plant protozoa \
           nr nt env_nr env_nt UniVec; do
    kraken2-build --download-library $lib --threads 24 --db $DBNAME
done
```

#### Build Database Index

```bash
kraken2-build --build --db $DBNAME --threads 48
```

---

### 2. Run Classification

```bash
kraken2 --db $DBNAME \
    --threads 48 \
    --report DRR505509.kraken.txt \
    DRR505509.qc.fastq
```

**Parameter explanation:**

| Parameter | Description |
|---|---|
| `--db` | Path to the Kraken 2 database. |
| `--threads` | Number of CPU threads. |
| `--report` | Output report file with taxonomic abundances. |
| `<input_file>` | Quality-controlled FASTQ file. |

---

### 3. Abundance Estimation with Bracken

Bracken (Bayesian Reestimation of Abundance after Kraken) refines Kraken 2 reports to produce more accurate species- or genus-level abundance estimates.

```bash
bracken -d $DBNAME \
    -i DRR505509.kraken.txt \
    -o DRR505509.bracken.S \
    -w DRR505509.S.kreport \
    -l S \
    -t 48
```

- `-l S`: Estimate at species (S) level. Use `G` for genus, `F` for family.
- `-w`: Output a Kraken-style report with Bracken-adjusted abundances.

---

### 4. Krona Visualization

```bash
ktImportTaxonomy -q 2 -t 3 DRR505509.S.kreport -o DRR505509.kraken.krona.html
```

---

## Output File Formats

### Standard Output (tab-delimited)

| Column | Content |
|---|---|
| 1 | Classification status (`C` = classified, `U` = unclassified) |
| 2 | Sequence identifier |
| 3 | Taxonomic assignment (NCBI taxid or `A` for ambiguous) |
| 4 | Length of alignment region |
| 5 | LCA alignment results |

### Report Format

| Column | Content |
|---|---|
| 1 | Percentage of reads covered |
| 2 | Cumulative read count |
| 3 | Direct read count at this taxon |
| 4 | Taxonomic level (`S`, `G`, `F`, etc.) |
| 5 | NCBI taxonomy ID |
| 6 | Scientific name |
