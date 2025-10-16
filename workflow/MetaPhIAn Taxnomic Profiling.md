# MetaPhlAn: Taxonomic Profiling of Microbiomes

## 1. Software Introduction

MetaPhlAn is a computational tool for analyzing microbial community compositions (including **bacteria, archaea, and eukaryotes**) based on metagenomic sequencing data (**not 16S rRNA gene sequencing**) at the species level. **StrainPhlAn** enables **accurate strain-level microbial** analysis. MetaPhlAn 4 relies on approximately 5.1 million unique clade-specific marker genes identified from about 1 million microbial genomes (approximately 236,600 reference genomes and 771,500 metagenome-assembled genomes), covering 26,970 species-level genome bins (SGBs), of which 4,992 are unclassified at the species level (the latest marker information files can be found on the official website). This enables MetaPhlAn to:

- **Make clear taxonomic assignments**
- **Accurately estimate organism relative abundances**
- **Achieve SGB-level resolution for bacteria, archaea, and eukaryotes**
- **Identify and track strains**
- **Perform analyses orders of magnitude faster than existing methods**

[biobakery/MetaPhlAn: MetaPhlAn is a computational tool for profiling the composition of microbial communities from metagenomic shotgun sequencing data](https://github.com/biobakery/MetaPhlAn)

## 2. Software Installation and Database Download

**Create Conda Environment**: Create a new Conda environment named `mpa` with Python 3.7. This step helps avoid dependency conflicts between different software packages.

```
conda create --name mpa -c bioconda python=3.7
```

**Activate Environment**: Activate the newly created `mpa` environment to ensure all subsequent operations are performed within this environment.

```
conda activate mpa
```

**Install MetaPhlAn 4**: Use Conda to install MetaPhlAn 4. Bioconda is a specialized Conda channel that provides bioinformatics software packages.

```
conda install -c bioconda metaphlan
```

### **Configure Database**

**Install Database**: Use MetaPhlAn's `--install` command to automatically install the database. This will download and install the latest database files.

```
metaphlan --install
```

**Manual Database Download** (if automatic installation fails): Visit the official MetaPhlAn database download page (available on GitHub), manually download the database files, and place them in the specified folder.



Note that at this step, you need to download all files of the same version (including bowtie2_indexes) and place them in the corresponding software folder, for example: /data/home/wangzuoqi/mambaforge/envs/mpa/lib/python3.7/site-packages/metaphlan/metaphlan_databases

## 3. Running MetaPhlAn 4

1. **Prepare Input Files**: Ensure your input files are in FASTQ or FASTA format, which are the formats supported by MetaPhlAn.
2. **Run Analysis**: Use MetaPhlAn to analyze metagenomic data. Here's an example using paired-end sequencing data:

```
metaphlan *.fastq1,*.fastq2 \
--input_type fastq \
-o output.txt \
--nproc 10 \
--stat_q 0.1 \
--bowtie2out bowtie2out_*.bz2
```

- `*.fastq1,*.fastq2`: Specifies input file wildcards, matching all files ending with `.fastq1` and `.fastq2`.
- `--input_type fastq`: Specifies that the input files are in FASTQ format.
- `-o output.txt`: Specifies the prefix for output files; all result files will have the prefix `output.txt`.
- `--nproc 10`: Specifies using 10 processor cores to accelerate analysis.
- `--stat_q 0.1`: Specifies the statistical confidence threshold; lower values increase sensitivity but may increase false positives.
- `--bowtie2out bowtie2out_*.bz2`: Specifies the prefix for bowtie2 output files; output files will be compressed.

### **Result Interpretation**

1. **View Output Files**: Output files typically include a text file (e.g., `output.txt`) and a binary file (e.g., `bowtie2out_*.bz2`). The text file contains classification results and relative abundance values.
2. **Merge Sample Results**: If you've analyzed multiple samples, you can merge the results using the following command:

```bash
merge_metaphlan_tables.py *.txt > merged_abundance_table.txt
```

3. **Extract Information at Specific Taxonomic Levels**: Use Linux commands to extract species annotation information at specific taxonomic levels, such as the species level:

```
grep -E '(s__)|(clade_name)' merged_abundance_table.txt \
| grep -v 't__' \
| sed 's/^.*s__//g' \
| awk '{$2=null;print}' \
| sed 's/\ \ /\ /g' \
| sed 's/\ /\t/g' > merged_abundance_species.txt
```

- `grep -E '(s__)|(clade_name)'`: Searches for lines containing `s__` (species prefix) or `clade_name`.
- `grep -v 't__'`: Excludes lines containing `t__` (type prefix).
- `sed 's/^.*s__//g'`: Deletes everything from the beginning of the line to `s__`.
- `awk '{$2=null;print}'`: Uses awk to print all columns except the second one.
- `sed 's/\ \ /\ /g'` and `sed 's/\ /\t/g'`: Format the output, replacing spaces with tabs.

### Output Example:

```bash
#mpa_vJun23_CHOCOPhlAnSGB_202403
#/data/home/wangzuoqi/mambaforge/envs/mpa/bin/metaphlan SRR7287194.man_1_clean.fastq.gz,SRR7287194.man_2_clean.fastq.gz --input_type fastq -o output_SRR7287194.txt --nproc 64 --stat_q 0.2 --bowtie2out bowtie2out_*.bz2
#51299120 reads processed
#SampleID	Metaphlan_Analysis
#clade_name	NCBI_tax_id	relative_abundance	additional_species
k__Bacteria	2	100.0
k__Bacteria|p__Firmicutes	2|1239	53.43906
k__Bacteria|p__Actinobacteria	2|201174	35.49352
k__Bacteria|p__Proteobacteria	2|1224	11.06741
k__Bacteria|p__Firmicutes|c__Bacilli	2|1239|91061	53.43906
k__Bacteria|p__Actinobacteria|c__Actinomycetia	2|201174|1760	35.49352
k__Bacteria|p__Proteobacteria|c__Gammaproteobacteria	2|1224|1236	6.4949
k__Bacteria|p__Proteobacteria|c__Alphaproteobacteria	2|1224|28211	3.23362
k__Bacteria|p__Proteobacteria|c__Betaproteobacteria	2|1224|28216	1.33889
k__Bacteria|p__Firmicutes|c__Bacilli|o__Lactobacillales	2|1239|91061|186826	53.43906
k__Bacteria|p__Actinobacteria|c__Actinomycetia|o__Bifidobacteriales	2|201174|1760|85004	35.44482
k__Bacteria|p__Proteobacteria|c__Gammaproteobacteria|o__Orbales	2|1224|1236|1240482	6.48948
k__Bacteria|p__Proteobacteria|c__Alphaproteobacteria|o__Rhodospirillales	2|1224|28211|204441	3.07755
k__Bacteria|p__Proteobacteria|c__Betaproteobacteria|o__Neisseriales	2|1224|28216|206351	1.33889
k__Bacteria|p__Proteobacteria|c__Alphaproteobacteria|o__Sphingomonadales	2|1224|28211|204457	0.1505
k__Bacteria|p__Actinobacteria|c__Actinomycetia|o__Propionibacteriales	2|201174|1760|85009	0.0487
```

## 4. Krona Visualization of Taxonomic Classification Results

Converting MetaPhlAn 4 output to a format acceptable by Krona

Note that the original metaphlan2krona.py script in the GitHub repository has some issues and cannot be used directly, so the following modifications were made:

```python
#!/usr/bin/env python

# ==============================================================================
# Conversion script: from MetaPhlAn output to Krona text input file
# Author: Daniel Brami (daniel.brami@gmail.com)
# Updated by: Your Name
# ==============================================================================

import sys
import optparse
import re

def main():
    # Parse Command Line
    parser = optparse.OptionParser()
    parser.add_option('-p', '--profile', dest='profile', default='', action='store', help='The input file is the MetaPhlAn standard result file')
    parser.add_option('-k', '--krona', dest='krona', default='krona.out', action='store', help='the Krona output file name')
    (options, spillover) = parser.parse_args()

    if not options.profile or not options.krona:
        parser.print_help()
        sys.exit()

    re_candidates = re.compile(r"s__")
    re_replace = re.compile(r"\w__")
    re_bar = re.compile(r"\|")

    with open(options.profile, 'r') as f:
        metaPhLan = f.readlines()

    with open(options.krona, 'w') as metaPhLan_FH:
        for aline in metaPhLan:
            if re.search(re_candidates, aline):
                aline = aline.strip()
                x = re.sub(re_replace, '\t', aline)
                x = re.sub(re_bar, '', x)
                x_cells = x.split('\t')

                # Check last column and remove until a float is found
                while x_cells:
                    try:
                        abundance = float(x_cells[-1])
                        lineage = '\t'.join(x_cells[:-2])
                        metaPhLan_FH.write(f'{abundance}\t{lineage}\n')
                        break
                    except ValueError:
                        x_cells.pop()  # Remove the last element if it's not a float
                    except IndexError:
                        print(f"Skipping line, no more elements to check: {aline}")
                        break

if __name__ == '__main__':
    main()
```

Convert the format accordingly:

```bash
python3 metaphlan2krona.py -p output_SRR7287194.txt -k new_krona.txt
```

The output in Krona format looks like this:

```bash
19.50819                Bacteria        Actinobacteria  Actinomycetia   Bifidobacteriales       Bifidobacteriaceae      Bifidobacterium Bifidobacterium_choladohabitans
17.91075                Bacteria        Firmicutes      Bacilli Lactobacillales Lactobacillaceae        Lactobacillus   Lactobacillus_apis
11.47015                Bacteria        Firmicutes      Bacilli Lactobacillales Lactobacillaceae        Lactobacillus   Lactobacillus_kullabergensis
10.16333                Bacteria        Actinobacteria  Actinomycetia   Bifidobacteriales       Bifidobacteriaceae      Bifidobacterium Bifidobacterium_apousia
7.71075         Bacteria        Firmicutes      Bacilli Lactobacillales Lactobacillaceae        Lactobacillus   Lactobacillus_kimbladii
7.33696         Bacteria        Firmicutes      Bacilli Lactobacillales Lactobacillaceae        Lactobacillus   Lactobacillus_helsingborgensis
6.25894         Bacteria        Firmicutes      Bacilli Lactobacillales Lactobacillaceae        Bombilactobacillus      Bombilactobacillus_mellis
3.5019          Bacteria        Actinobacteria  Actinomycetia   Bifidobacteriales       Bifidobacteriaceae      Bifidobacterium Bifidobacterium_asteroides
3.14499         Bacteria        Proteobacteria  Gammaproteobacteria     Orbales Orbaceae        Frischella      Frischella_perrara
3.07755         Bacteria        Proteobacteria  Alphaproteobacteria     Rhodospirillales        Acetobacteraceae        Commensalibacter        Commensalibacter_sp_AMU001
2.26299         Bacteria        Actinobacteria  Actinomycetia   Bifidobacteriales       Bifidobacteriaceae      Bifidobacterium Bifidobacterium_polysaccharolyticum
1.95461         Bacteria        Proteobacteria  Gammaproteobacteria     Orbales Orbaceae        Gilliamella     Gilliamella_apicola
1.42838         Bacteria        Firmicutes      Bacilli Lactobacillales Lactobacillaceae        Lactobacillus   Lactobacillus_melliventris
1.38987         Bacteria        Proteobacteria  Gammaproteobacteria     Orbales Orbaceae        Gilliamella     Gilliamella_apis
1.33889         Bacteria        Proteobacteria  Betaproteobacteria      Neisseriales    Neisseriaceae   Snodgrassella   Snodgrassella_alvi
1.21438         Bacteria        Firmicutes      Bacilli Lactobacillales Lactobacillaceae        Bombilactobacillus      Bombilactobacillus_mellifer
0.14929         Bacteria        Proteobacteria  Alphaproteobacteria     Sphingomonadales        Sphingomonadaceae       Sphingomonas    Sphingomonas_paucimobilis
0.10877         Bacteria        Firmicutes      Bacilli Lactobacillales Lactobacillaceae        Lactobacillus   Lactobacillus_sp_W8173
0.0487          Bacteria        Actinobacteria  Actinomycetia   Propionibacteriales     Propionibacteriaceae    Cutibacterium   Cutibacterium_acnes
0.00841         Bacteria        Actinobacteria  Actinomycetia   Bifidobacteriales       Bifidobacteriaceae      Bifidobacterium Bifidobacterium_coryneforme
```

Provide the above content to Krona for visualization, which will output a taxonomic classification chart in HTML format:

```bash
ktImportText krona.txt
```