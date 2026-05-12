# Fastp: Sequencing Data Quality Control & Preprocessing

## Software Information

- **Tool**: Fastp — an ultra-fast all-in-one FASTQ preprocessor
- **Repository**: https://github.com/OpenGene/fastp

---

## Single-End Sequencing

```bash
fastp -i SRR7986792.fastq -o SRR7986792.qc.fastq --detect_adapter_for_pe --thread 16
```

For single-end (SE) data, adapters are detected automatically in most cases. If `fastp` fails to detect the adapter, specify it manually using `-a` or `--adapter_sequence`. When an adapter sequence is specified, automatic detection is disabled.

## Paired-End Sequencing

```bash
fastp -i SRR7986792_1.fastq -I SRR7986792_2.fastq \
  -o SRR7986792_1.qc.fastq -O SRR7986792_2.qc.fastq \
  --detect_adapter_for_pe --thread 16
```

For paired-end (PE) data, adapters are trimmed automatically through per-read overlap analysis. This method is robust and fast, so manual adapter specification is usually unnecessary. If `fastp` fails to find an overlap for some read pairs (e.g., due to low-quality bases), you can specify adapter sequences using `--adapter_sequence` (read1) and `--adapter_sequence_r2` (read2).

## Batch Processing

### Paired-End Data

```bash
#!/bin/bash
for i in $(cat fastq.id); do
    fastp -i ./${i}/${i}_1.fastq -I ./${i}/${i}_2.fastq \
      -o ./${i}/${i}_1.qc.fastq -O ./${i}/${i}_2.qc.fastq \
      --detect_adapter_for_pe --thread 16 \
      &> ${i}.log
done
```

### Single-End Data

```bash
#!/bin/bash
for i in $(cat fastq.id); do
    fastp -i ./${i}/${i}.fastq -o ./${i}/${i}.qc.fastq \
      --detect_adapter_for_pe --thread 16 \
      &> ${i}.log
done
```

**Note**: The `fastq.id` file should contain one sample identifier per line, matching the subdirectory and file naming convention.
