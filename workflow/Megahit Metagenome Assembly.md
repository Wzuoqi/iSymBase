# MEGAHIT: Metagenome Assembly

## Software Information

- **Tool**: MEGAHIT — an ultra-fast and memory-efficient metagenome assembler
- **Repository**: https://github.com/voutcn/megahit

---

## Input File Format

MEGAHIT accepts **FASTQ** format input files, supporting both single-end and paired-end sequencing data. Files may be compressed in gzip or bzip2 format. FASTQ files contain quality information for each DNA sequence fragment alongside the base calls.

## Basic Command Usage

```bash
megahit --presets meta-large -t 30 --12 B1W10_1.fq,B1W10_2.fq -o ./megahit
```

**Parameter explanation:**

| Parameter | Description |
|---|---|
| `--presets meta-large` | Preset parameters optimized for large, complex metagenomic data (e.g., soil). Performs multiple assemblies and selects the best result. |
| `-t 30` | Number of threads; adjust according to available CPU cores. |
| `--12 B1W10_1.fq,B1W10_2.fq` | Comma-separated paired-end sequencing files (interleaved format). |
| `-o ./megahit` | Output directory. |

## Alternative Input Formats

```bash
# Paired-end (separate files):
megahit -1 pe_1.fq -2 pe_2.fq -o out

# Single-end:
megahit -r single_end.fq -o out

# Interleaved paired-end:
megahit --12 interleaved.fq -o out
```

## Preset Parameters

MEGAHIT provides two preset configurations:

| Preset | Description |
|---|---|
| `meta-sensitive` | More sensitive, longer runtime. Suitable for simple communities. |
| `meta-large` | Suitable for large, complex metagenomic data. Default for most insect microbiome samples. |

## Output Files

| File | Description |
|---|---|
| `final.contigs.fa` | Assembled contigs in FASTA format — the primary output for downstream analysis. |
| `log` | Program execution log with progress and any error messages. |
| `options.json` | Parameters used during execution, stored in JSON format. |

## Memory Requirements

MEGAHIT's memory requirement is approximately **1.04–1.5× the original data size**. Memory consumption is concentrated in the k-mer counting and de Bruijn graph construction steps.

## Resuming from Interruption

When assembling large datasets, the process may be interrupted due to insufficient memory. Resume with:

```bash
megahit --continue -o former_megahit_out -m 0.9
```

- `--continue`: Resume from the interruption point.
- `-o`: Previously generated output directory containing intermediate files.
- `-m 0.9`: Memory usage fraction (90%).

## Common Issues

- **std::bad_alloc / Exit code -6**: Insufficient memory. Increase the `-m` parameter or use a larger k-mer value to reduce assembly complexity.
