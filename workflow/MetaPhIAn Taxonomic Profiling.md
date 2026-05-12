# MetaPhlAn 4: Taxonomic Profiling of Microbiomes

## 1. Software Introduction

MetaPhlAn is a computational tool for analyzing microbial community composition (**bacteria, archaea, and eukaryotes**) from metagenomic shotgun sequencing data at species-level resolution. **StrainPhlAn** enables accurate strain-level microbial analysis.

MetaPhlAn 4 relies on approximately 5.1 million unique clade-specific marker genes identified from about 1 million microbial genomes (~236,600 reference genomes and ~771,500 metagenome-assembled genomes), covering 26,970 species-level genome bins (SGBs), of which 4,992 are unclassified at the species level.

**Key capabilities:**
- Species-level taxonomic assignments
- Accurate relative abundance estimation
- SGB-level resolution for bacteria, archaea, and eukaryotes
- Strain identification and tracking
- Orders of magnitude faster than traditional alignment-based methods

**Repository**: https://github.com/biobakery/MetaPhlAn

---

## 2. Installation and Database Setup

### Create Conda Environment

```bash
conda create --name mpa -c bioconda python=3.7
conda activate mpa
```

### Install MetaPhlAn 4

```bash
conda install -c bioconda metaphlan
```

### Configure Database

**Automatic installation** (recommended):

```bash
metaphlan --install
```

**Manual installation** (if automatic download fails):

Visit the official MetaPhlAn database download page, manually download all files of the same version (including `bowtie2_indexes`), and place them in the MetaPhlAn database directory. The exact path can be located with:

```bash
python -c "import metaphlan; print(metaphlan.__path__[0])"
```

Typical location: `<conda_env>/lib/python3.7/site-packages/metaphlan/metaphlan_databases/`

---

## 3. Running MetaPhlAn 4

### Basic Usage

```bash
metaphlan *.fastq1,*.fastq2 \
    --input_type fastq \
    -o output.txt \
    --nproc 10 \
    --stat_q 0.1 \
    --bowtie2out bowtie2out_*.bz2
```

**Parameter explanation:**

| Parameter | Description |
|---|---|
| `*.fastq1,*.fastq2` | Input file wildcards matching paired-end FASTQ files. |
| `--input_type fastq` | Input file format. |
| `-o output.txt` | Output file prefix. |
| `--nproc 10` | Number of processor cores. |
| `--stat_q 0.1` | Statistical confidence threshold; lower values increase sensitivity but may increase false positives. |
| `--bowtie2out bowtie2out_*.bz2` | Prefix for compressed Bowtie2 alignment output. |

### Input Requirements

Input files must be in **FASTQ** or **FASTA** format, the standard formats for sequencing data. These are the quality-controlled outputs from Fastp preprocessing.

---

## 4. Result Processing

### Merge Multiple Samples

```bash
merge_metaphlan_tables.py *.txt > merged_abundance_table.txt
```

### Extract Species-Level Information

```bash
grep -E '(s__)|(clade_name)' merged_abundance_table.txt \
    | grep -v 't__' \
    | sed 's/^.*s__//g' \
    | awk '{$2=null;print}' \
    | sed 's/\ \ /\ /g' \
    | sed 's/\ /\t/g' > merged_abundance_species.txt
```

**Explanation of the pipeline:**
- `grep -E '(s__)|(clade_name)'` — keep species-level lines and header.
- `grep -v 't__'` — exclude strain-level entries.
- `sed 's/^.*s__//g'` — strip the lineage prefix before the species identifier.
- `awk '{$2=null;print}'` — drop the second column.
- `sed` commands — format spacing as tab-delimited output.

### Example Output

```
#mpa_vJun23_CHOCOPhlAnSGB_202403
#SampleID    Metaphlan_Analysis
#clade_name  NCBI_tax_id  relative_abundance  additional_species
k__Bacteria  2   100.0
k__Bacteria|p__Firmicutes  2|1239  53.43906
k__Bacteria|p__Actinobacteria  2|201174  35.49352
k__Bacteria|p__Proteobacteria  2|1224  11.06741
k__Bacteria|p__Firmicutes|c__Bacilli  2|1239|91061  53.43906
k__Bacteria|p__Actinobacteria|c__Actinomycetia  2|201174|1760  35.49352
k__Bacteria|p__Proteobacteria|c__Gammaproteobacteria  2|1224|1236  6.4949
...
```

---

## 5. Krona Visualization

Convert MetaPhlAn output to Krona-compatible format for interactive HTML visualization.

### Conversion Script

The `scripts/metaphlan2krona.py` script in this repository handles the conversion:

```bash
python scripts/metaphlan2krona.py -p output.txt -k new_krona.txt
```

### Generate Krona Chart

```bash
ktImportText new_krona.txt -o taxonomy_chart.html
```

### Example Krona Output

```
19.50819   Bacteria   Actinobacteria   Actinomycetia   Bifidobacteriales   ...
17.91075   Bacteria   Firmicutes       Bacilli         Lactobacillales      ...
11.47015   Bacteria   Firmicutes       Bacilli         Lactobacillales      ...
10.16333   Bacteria   Actinobacteria   Actinomycetia   Bifidobacteriales   ...
...
```
