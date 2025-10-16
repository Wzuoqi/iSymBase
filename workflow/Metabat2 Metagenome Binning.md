# MetaBAT2: Metagenome Binning Workflow

This workflow is performed after metagenome assembly with MEGAHIT.

## Software Information

MetaBAT2 (Metagenome Binning with Abundance and Tetra-nucleotide frequencies) is a robust binning tool that uses both sequence composition and coverage information to bin contigs into MAGs (Metagenome-Assembled Genomes).

Official repository: [berkeleylab/metabat — Bitbucket](https://bitbucket.org/berkeleylab/metabat/src/master/)

## Introduction to MetaBAT2

MetaBAT2 is an improved version of MetaBAT that requires virtually no parameter optimization. The default parameters are reliable for most cases as MetaBAT2 adapts to the given data to find the best parameters. This makes it easier for users to obtain high-quality bins without extensive parameter tuning.

Key features:
- Adaptive parameter selection based on input data
- Improved binning accuracy compared to MetaBAT1
- Efficient handling of various metagenome complexities

## Workflow Steps

### 1. Building Contig Indices

```bash
bowtie2-build -f ./megahit/SRR12112864.man.contigs.fa ./metabat/SRR12112864.man.bowtie2 --threads 16
```

### 2. Aligning Sequencing Data to Contigs

For paired-end sequencing:

```bash
bowtie2 -1 SRR12112864.man_1.qc.fastq -2 SRR12112864.man_2.qc.fastq -p 32 -x ./metabat/SRR12112864.man.bowtie2 -S ./metabat/SRR12112864.man.sam
```

### 3. BAM Format Conversion and Sorting

```bash
samtools view -@ 32 -b -S SRR12112864.man.sam -o SRR12112864.man.bam
samtools sort -@ 32 -l 9 -O BAM SRR12112864.man.bam -o SRR12112864.man.sorted.bam
```

### 4. Calculating Contig Depth

```bash
jgi_summarize_bam_contig_depths SRR12112864.man.sorted.bam --outputDepth SRR12112864.man.depth.txt
```

### 5. Binning

```bash
metabat2 -t 32 -i ../megahit/SRR12112864.man.contigs.fa -a SRR12112864.man.depth.txt -o SRR12112864.man.bin -v
```

### 6. Bin Quality Assessment

```bash
checkm lineage_wf -t 32 -x fa --nt --tab_table -f ./checkm/bins_qa.txt ./ ./checkm
```

## Important Parameters for MetaBAT2

MetaBAT2 offers several parameters that can be adjusted for specific scenarios:

- `-m, --minContig`: Minimum size of a contig for binning (default: 2500, should be ≥1500)
- `--maxP`: Percentage of 'good' contigs considered for binning (default: 95)
- `--minS`: Minimum score of an edge for binning (default: 60, range: 1-99)
- `--maxEdges`: Maximum number of edges per node (default: 200)
- `-s, --minClsSize`: Minimum size of a bin to be output (default: 200000)
- `-t, --numThreads`: Number of threads to use (default: 0, uses all cores)
- `--unbinned`: Generate a file for unbinned contigs

For advanced users:
- You can decrease `-m` when assembly quality is good
- You can decrease `--maxP` and `--maxEdges` when assembly quality is poor
- You can increase `--maxEdges` (typically to 500) when completeness level is low
- You can increase `--minS` when assembly quality is poor

## jgi_summarize_bam_contig_depths Tool

This tool calculates coverage depth for each sequence in the assembly with several adjustments to improve binning accuracy:

1. Edge bases are ignored by default (the lesser of 1 average read length or 75 bases)
2. Reads with mapping identity below 97% are excluded to avoid strain variation issues

Usage:
```bash
jgi_summarize_bam_contig_depths <options> sortedBam1 [sortedBam2 ...]
```

Key options:
- `--outputDepth`: Output file for the depth matrix
- `--percentIdentity`: Minimum end-to-end % identity of qualifying reads (default: 97)
- `--minContigLength`: Minimum length of contig to include

## Batch Processing Scripts

### For Single-End Data

```bash
#!/bin/bash
for i in `cat fastq.id`
do
        touch $i.metabat.log
        echo "$i is processing"
        mkdir ./$i/metabat
        python extract_seq.py ./$i/megahit/$i.contigs.fa ./$i/megahit/$i.1000.contigs.fa
        bowtie2-build -f ./$i/megahit/$i.1000.contigs.fa ./$i/metabat/$i.bowtie2 --threads 32
        bowtie2 -p 32 -x ./$i/metabat/$i.bowtie2 -U ./$i/$i.qc.fastq -S ./$i/metabat/$i.sam
        samtools view -@ 32 -b -S ./$i/metabat/$i.sam -o ./$i/metabat/$i.bam
        samtools sort -@ 32 -l 9 -O BAM ./$i/metabat/$i.bam -o ./$i/metabat/$i.sorted.bam
        jgi_summarize_bam_contig_depths ./$i/metabat/$i.sorted.bam --outputDepth ./$i/metabat/$i.depth.txt
        metabat2 -t 32 -i ./$i/megahit/$i.1000.contigs.fa -a ./$i/metabat/$i.depth.txt -o ./$i/metabat/$i.bin -v
        checkm lineage_wf -t 64 -x fa --nt --tab_table -f ./$i/bins_qa.txt ./$i/metabat ./$i/metabat/checkm_output
done
```

### For Paired-End Data

```bash
#!/bin/bash
for i in `cat fastq.id`
do
        touch $i.bowtie2.log
        echo "$i is processing"
        mkdir ./$i/metabat
        python extract_seq.py ./$i/megahit/$i.contigs.fa ./$i/megahit/$i.1000.contigs.fa
        bowtie2-build -f ./$i/megahit/$i.1000.contigs.fa ./$i/metabat/$i.bowtie2 --threads 32
        bowtie2 -p 48 -x ./$i/metabat/$i.bowtie2 -1 ./$i/${i}_1.qc.fastq -2 ./$i/${i}_2.qc.fastq -S ./$i/metabat/$i.sam
        samtools view -@ 32 -b -S ./$i/metabat/$i.sam -o ./$i/metabat/$i.bam
        samtools sort -@ 32 -l 9 -O BAM ./$i/metabat/$i.bam -o ./$i/metabat/$i.sorted.bam
        jgi_summarize_bam_contig_depths ./$i/metabat/$i.sorted.bam --outputDepth ./$i/metabat/$i.depth.txt
        metabat2 -t 32 -i ./$i/megahit/$i.1000.contigs.fa -a ./$i/metabat/$i.depth.txt -o ./$i/metabat/$i.bin -v
        checkm lineage_wf -t 64 -x fa --nt --tab_table -f ./$i/bins_qa.txt ./$i/metabat ./$i/metabat/checkm_output
done
```

## Best Practices

1. Always ensure BAM files are sorted before running MetaBAT2
2. For most datasets, the default parameters work well
3. Use CheckM to evaluate bin quality (completeness and contamination)
4. Consider filtering contigs by length (≥1500 bp, ideally ≥2500 bp) before binning
5. When working with many samples, consider increasing the `--maxEdges` parameter to 500