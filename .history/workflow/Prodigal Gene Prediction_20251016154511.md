# Contig-based Annotation: Prodigal Gene Prediction

# 1. Prodigal Metagenomic Gene Prediction

Prodigal is a specialized gene prediction software for prokaryotic genomes and metagenomes, widely recognized for its efficiency and accuracy. Here is a **basic introduction** to Prodigal:

1. **Features**:
    - It can quickly and accurately predict protein-coding genes, providing output in GFF3, Genbank, or Sequin table formats.
    - Suitable for complete genomes, draft genomes, and metagenomic analysis.
    - No training data required; Prodigal is an unsupervised machine learning algorithm that automatically learns genome properties from the sequence itself, including genetic code, RBS motif usage, start codon usage, and coding statistics.
    - Can handle gaps, scaffolds, and partial genes; users can specify how Prodigal should handle gaps, with many options to allow or prohibit genes from entering or crossing gaps.
    - Can identify translation start sites and output information about each potential start site in the genome, including confidence scores, RBS motifs, etc.
    - Provides detailed summary statistics for each genome, including contig length, gene length, GC content, GC skew, RBS motifs used, and start and stop codon usage.
2. **Limitations**:
    - The current version does not predict RNA genes.
    - Does not process genes with introns, as this is extremely rare in prokaryotes.
    - Does not provide functional annotation and does not include logic for handling frameshifts.
    - Not yet optimized for viral gene prediction; may not be suitable for viral genome analysis.
3. **Installation and Usage**: Prodigal installation is relatively simple; you can download the source code from its GitHub page for compilation or directly download pre-compiled binary files. It offers various parameter options that allow users to adjust the prediction process according to their needs.
4. **Python Module**: There is a Python module called `pyrodigal`, which is a Python binding for Prodigal, providing the same functionality while optimizing performance and memory usage.

**Prodigal is widely used in microbial gene prediction due to its efficiency and ease of use.**

### Detailed Parameters

```bash
Usage:  prodigal [-a trans_file] [-c] [-d nuc_file] [-f output_type]
                 [-g tr_table] [-h] [-i input_file] [-m] [-n] [-o output_file]
                 [-p mode] [-q] [-s start_file] [-t training_file] [-v]

         -a:  Write protein translations to the selected file.
         -c:  Closed ends.  Do not allow genes to run off edges.
         -d:  Write nucleotide sequences of genes to the selected file.
         -f:  Select output format (gbk, gff, or sco).  Default is gbk.
         -g:  Specify a translation table to use (default 11).
         -h:  Print help menu and exit.
         -i:  Specify FASTA/Genbank input file (default reads from stdin).
         -m:  Treat runs of N as masked sequence; don't build genes across them.
         -n:  Bypass Shine-Dalgarno trainer and force a full motif scan.
         -o:  Specify output file (default writes to stdout).
         -p:  Select procedure (single or meta).  Default is single.
         -q:  Run quietly (suppress normal stderr output).
         -s:  Write all potential genes (with scores) to the selected file.
         -t:  Write a training file (if none exists); otherwise, read and use
              the specified training file.
         -v:  Print version number and exit.
```

### Usage Example

```bash
prodigal -i ./megahit/DRR505509.contigs.fa -o ./megahit/DRR505509.gff -d ./megahit/DRR505509.gene.fa -a ./megahit/DRR505509.anno.pep.fa -f gff -p meta
```

## 2. CD-HIT Redundancy Removal

```bash
cd-hit-est -i DRR505509.gene.fa -o DRR505509.cdhit.gene.fa -c 0.9 -G 0 -M 0 -T 64 -aS 0.9
```

- **`i`**: Input filename, **`dna_all.fa`** is a FASTA format DNA sequence file.
- **`o`**: Output filename, **`out.fa`** is the output FASTA format DNA sequence file after redundancy removal.
- **`c`**: Similarity threshold (Chebyshev distance), set to 0.95 in this example, meaning sequences with 95% similarity are considered members of the same gene family.
- **`G`**, **`g`**: Legal N/long sequence limit. Both are set to 0 in this example, meaning no length limit.
- **`aS`**: Global sequence alignment parameter. Set to 0.9 in this example, meaning global sequence alignment is used for clustering, and sequences need to reach over 90% similarity to be grouped into the same cluster.
- **`M`**: Memory limit. Set to 0 in this example, meaning memory size is automatically set.
- **`T`**: Number of parallel threads. Set to 20 in this example, meaning 20 CPU threads are used simultaneously to process tasks, improving processing speed.

### Common Issues

**Insufficient Memory**: If you encounter memory shortage problems, you can adjust the `-M` parameter to increase memory usage.

3. Gene Functional Annotation Using DIAMOND BLASTX
After gene prediction and redundancy removal, the next step in metagenomic analysis is functional annotation — determining the possible functions of predicted genes by comparing them to known protein sequences in reference databases.
In this workflow, DIAMOND BLASTX is used to align nucleotide sequences (genes) against a protein database (Symbionts) to infer their biological roles.

3.1 About DIAMOND
DIAMOND is a high-speed sequence aligner designed as a drop-in replacement for BLASTX, capable of achieving speeds up to 20,000 times faster than traditional BLAST while maintaining high sensitivity. It is widely used for large-scale metagenomic datasets.

Key advantages:

Ultra-fast protein alignments suitable for large metagenomic datasets.

Supports multiple output formats compatible with BLAST.

Offers flexible control over sensitivity, e-value thresholds, and output filtering.

Optimized for multi-threading and parallel computation.

3.2 About the “Symbionts” Database
The Symbionts database used here is a custom subset of the NCBI NR (non-redundant protein) database, constructed to include only sequences from:

Bacteria (taxid: 2)

Archaea (taxid: 2157)

Fungi (taxid: 4751)

This design focuses the annotation on symbiotic microorganisms, reducing computational load while improving annotation relevance for host-associated or environmental microbiomes.

Database construction (for context):

bash
复制
编辑
# Example of how Symbionts database may have been built
diamond makedb --in nr_subset_symbionts.faa -d /data/software/nr_db/Symbionts
3.3 DIAMOND BLASTX Command and Explanation
bash
复制
编辑
diamond blastx \
  --db /data/software/nr_db/Symbionts \
  --query ./DRR505509/megahit/DRR505509.cdhit.gene.fa \
  --out ./DRR505509/DRR505509.diamond.tab \
  --outfmt 6 \
  --max-target-seqs 1 \
  --evalue 1e-5 \
  -p 64
Parameter details:

Parameter	Description
--db /data/software/nr_db/Symbionts	Path to the Symbionts protein database.
--query ./DRR505509/megahit/DRR505509.cdhit.gene.fa	Input file containing non-redundant gene sequences (from CD-HIT).
--out ./DRR505509/DRR505509.diamond.tab	Output file storing BLASTX results in tabular format.
--outfmt 6	Output in BLAST tabular format (12-column TSV file).
--max-target-seqs 1	Report only the top hit per query gene (most similar protein).
--evalue 1e-5	E-value threshold for statistical significance.
-p 64	Number of threads to use for parallel computation (adjust as per CPU availability).

