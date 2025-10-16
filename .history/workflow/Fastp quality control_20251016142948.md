# Fastp Quality Control: Sequencing Data Preprocessing Workflow

## Software Information

GitHub Repository: https://github.com/OpenGene/fastp

## Single-End Sequencing

```bash
fastp -i SRR7986792.fastq -o SRR7986792.qc.fastq --detect_adapter_for_pe --thread 16
```

For single-end (SE) data, the adapter can be detected automatically in most cases. However, if `fastp` fails to find the adapter sequence, you can specify it using the `-a` or `--adapter_sequence` option. When an adapter sequence is specified, the automatic detection is disabled.

## Paired-End Sequencing

```bash
fastp -i SRR7986792_1.fastq -I SRR7986792_2.fastq -o SRR7986792_1.qc.fastq -O SRR7986792_2.qc.fastq --detect_adapter_for_pe --thread 16
```

For paired-end (PE) data, adapters can be trimmed automatically through per-read overlap analysis, which identifies the overlap between each pair of reads. This method is robust and fast, so you typically don't need to input the adapter sequence manually. However, you can still specify adapter sequences for read1 using `--adapter_sequence` and for read2 using `--adapter_sequence_r2`. If `fastp` fails to find an overlap for some pairs (e.g., due to low quality bases), it will use these specified sequences to trim adapters for read1 and read2 respectively.

## Batch Processing Scripts

### For Paired-End Data:

```bash
#!/bin/bash
for i in `cat fastq.id`
do
    touch $i.log
    fastp -i ./$i/${i}_1.fastq -I ./$i/${i}_2.fastq -o ./$i/${i}_1.qc.fastq -O ./$i/${i}_2.qc.fastq --detect_adapter_for_pe --thread 16
done
```

### For Single-End Data:

```bash
#!/bin/bash
for i in `cat fastq.id`
do
    fastp -i ./$i/$i.fastq -o ./$i/$i.qc.fastq --detect_adapter_for_pe --thread 16
done
```