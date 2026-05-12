# MetaBAT 2: Metagenome Binning Workflow

This workflow is performed after metagenome assembly with MEGAHIT.

## Software Information

MetaBAT 2 (Metagenome Binning with Abundance and Tetra-nucleotide frequencies) is a robust binning tool that uses both sequence composition and coverage information to bin contigs into MAGs (Metagenome-Assembled Genomes).

**Repository**: https://bitbucket.org/berkeleylab/metabat/

---

## Introduction

MetaBAT 2 is an improved version of MetaBAT that requires virtually no parameter optimization. The default parameters are reliable for most cases, as MetaBAT 2 adapts to the given data to find the best parameters automatically.

**Key features:**
- Adaptive parameter selection based on input data characteristics
- Improved binning accuracy compared to MetaBAT 1
- Efficient handling of various metagenome complexities

---

## Workflow Steps

### 1. Filter Short Contigs

Remove contigs shorter than 1,000 bp to improve binning quality:

```bash
python scripts/extract_seq.py ./megahit/SRR12112864.man.contigs.fa \
    ./megahit/SRR12112864.man.1000.contigs.fa --min_length 1000
```

### 2. Build Contig Indices

```bash
bowtie2-build -f ./megahit/SRR12112864.man.1000.contigs.fa \
    ./metabat/SRR12112864.man.bowtie2 --threads 16
```

### 3. Align Sequencing Reads to Contigs

**Paired-end:**

```bash
bowtie2 -1 SRR12112864.man_1.qc.fastq -2 SRR12112864.man_2.qc.fastq \
    -p 32 -x ./metabat/SRR12112864.man.bowtie2 \
    -S ./metabat/SRR12112864.man.sam
```

**Single-end:**

```bash
bowtie2 -p 32 -x ./metabat/SRR12112864.man.bowtie2 \
    -U ./SRR12112864/SRR12112864.qc.fastq \
    -S ./metabat/SRR12112864.man.sam
```

### 4. Convert and Sort BAM

```bash
samtools view -@ 32 -b -S SRR12112864.man.sam -o SRR12112864.man.bam
samtools sort -@ 32 -l 9 -O BAM SRR12112864.man.bam -o SRR12112864.man.sorted.bam
```

### 5. Calculate Contig Depth

```bash
jgi_summarize_bam_contig_depths SRR12112864.man.sorted.bam \
    --outputDepth SRR12112864.man.depth.txt
```

### 6. Run MetaBAT 2 Binning

```bash
metabat2 -t 32 \
    -i ../megahit/SRR12112864.man.1000.contigs.fa \
    -a SRR12112864.man.depth.txt \
    -o SRR12112864.man.bin \
    -v
```

### 7. Bin Quality Assessment with CheckM

```bash
checkm lineage_wf -t 32 -x fa --nt --tab_table \
    -f ./checkm/bins_qa.txt ./ ./checkm
```

---

## Important Parameters

| Parameter | Description | Default |
|---|---|---|
| `-m, --minContig` | Minimum contig size for binning | 2500 (≥1500 recommended) |
| `--maxP` | Percentage of "good" contigs considered | 95 |
| `--minS` | Minimum edge score for binning | 60 (range: 1–99) |
| `--maxEdges` | Maximum edges per node | 200 |
| `-s, --minClsSize` | Minimum bin size to output | 200000 |
| `-t, --numThreads` | Number of threads | 0 (all cores) |
| `--unbinned` | Generate file for unbinned contigs | — |

### Parameter Tuning Guide

- Decrease `-m` when assembly quality is good (more contigs for binning).
- Decrease `--maxP` and `--maxEdges` when assembly quality is poor.
- Increase `--maxEdges` (typically to 500) when completeness is low.
- Increase `--minS` when assembly quality is poor.

---

## jgi_summarize_bam_contig_depths

This tool calculates coverage depth for each contig with two key adjustments:

1. Edge bases are ignored (the lesser of 1 average read length or 75 bases) to reduce edge effects.
2. Reads with mapping identity below 97% are excluded to avoid strain variation artifacts.

```bash
jgi_summarize_bam_contig_depths <options> sortedBam1 [sortedBam2 ...]
```

**Key options:**

| Option | Description | Default |
|---|---|---|
| `--outputDepth` | Output depth matrix file | — |
| `--percentIdentity` | Minimum end-to-end % identity of qualifying reads | 97 |
| `--minContigLength` | Minimum contig length to include | — |

---

## Batch Processing

### Paired-End Data

```bash
#!/bin/bash
for i in $(cat fastq.id); do
    echo "$i is processing"
    mkdir ./$i/metabat

    python scripts/extract_seq.py ./$i/megahit/$i.contigs.fa \
        ./$i/megahit/$i.1000.contigs.fa

    bowtie2-build -f ./$i/megahit/$i.1000.contigs.fa \
        ./$i/metabat/$i.bowtie2 --threads 32

    bowtie2 -p 48 -x ./$i/metabat/$i.bowtie2 \
        -1 ./$i/${i}_1.qc.fastq -2 ./$i/${i}_2.qc.fastq \
        -S ./$i/metabat/$i.sam

    samtools view -@ 32 -b -S ./$i/metabat/$i.sam -o ./$i/metabat/$i.bam
    samtools sort -@ 32 -l 9 -O BAM ./$i/metabat/$i.bam -o ./$i/metabat/$i.sorted.bam

    jgi_summarize_bam_contig_depths ./$i/metabat/$i.sorted.bam \
        --outputDepth ./$i/metabat/$i.depth.txt

    metabat2 -t 32 -i ./$i/megahit/$i.1000.contigs.fa \
        -a ./$i/metabat/$i.depth.txt -o ./$i/metabat/$i.bin -v

    checkm lineage_wf -t 64 -x fa --nt --tab_table \
        -f ./$i/bins_qa.txt ./$i/metabat ./$i/metabat/checkm_output
done
```

### Single-End Data

Replace the Bowtie2 alignment step with:

```bash
bowtie2 -p 32 -x ./$i/metabat/$i.bowtie2 \
    -U ./$i/$i.qc.fastq \
    -S ./$i/metabat/$i.sam
```

---

## Best Practices

1. Always ensure BAM files are sorted before running MetaBAT 2.
2. Default parameters work well for most datasets.
3. Use CheckM to evaluate bin quality (completeness and contamination).
4. Filter contigs by length (≥1,500 bp, ideally ≥2,500 bp) before binning.
5. For many-sample studies, consider increasing `--maxEdges` to 500.
