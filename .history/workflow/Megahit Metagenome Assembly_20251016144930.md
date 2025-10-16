# MEGAHIT: Metagenome Assembly

## Input File Preparation

MEGAHIT accepts input files in **FASTQ** format, which can be either single-end or paired-end sequencing data. Files can be compressed in gz or bz2 format. FASTQ files contain quality information for each DNA sequence fragment and the corresponding base sequence.

## Basic Command Usage

Below is a basic MEGAHIT command with line-by-line parameter explanations:

```
megahit --presets meta-large -t 30 --12 B1W10_1.fq,B1W101_2.fq -o ./megahit
```

- `--presets meta-large`: Preset parameters designed for metagenomic analysis, which performs multiple assemblies and selects the best result.
- `-t 30`: Sets the number of threads to 30, which can be adjusted according to your computer's performance.
- `--12 B1W10_1.fq,B1W101_2.fq`: Specifies the two paired-end sequencing data files, separated by a comma.
- `-o ./megahit`: Specifies the output directory as the `megahit` folder in the current directory.

## Input File Format

The FASTQ file format is the standard format for storing raw sequencing data. **Each read in the file includes a sequence identifier, base sequence, separator `+`, and quality score**.

## Output File Analysis

The most important output files from MEGAHIT include:

- `final.contigs.fa`: **Assembled contigs stored in FASTA format.**
- `log`: Program execution log, recording progress and possible error messages.
- `options.json`: Parameters used during execution, stored in JSON format.

## Common Issues and Solutions

- **std::bad_alloc/Exit code -6**: Memory insufficient error. You can increase the memory usage rate specified by the `-m` parameter or try using a larger kmer value to reduce assembly complexity.
- **Continuing from an interruption point**: If assembly is interrupted due to insufficient memory or other reasons, you can use the `--continue` parameter to continue running from the previous output directory.

## Preset Parameters

MEGAHIT provides two sets of preset parameters:

- `meta-sensitive`: More sensitive, takes longer.
- `meta-large`: Suitable for large and complex metagenomic data, such as soil samples.

## Memory Requirements

MEGAHIT's memory requirement is at least 1.04 to 1.5 times the original data size. Memory consumption is mainly in the kmer counting and de Bruijn Graph construction steps.

# Command Examples

```bash
# Paired-end sequence assembly:
megahit -1 pe_1.fq -2 pe_2.fq -o out
#-1: pair-end 1 sequence, -2: pair-end 2 sequence, -o: output directory

# Single-end sequence:
megahit -r single_end.fq -o out

# Interleaved paired-end sequence:
megahit --12 interleaved.fq -o out
```

## Continuing from an Interruption Point

When assembling large datasets, the process may be interrupted due to insufficient memory or other reasons. In such cases, you can use:

```
megahit --continue -o former_megahit_out -m 0.9
```

Parameter explanation:
- `--continue`: Continue running from the interruption point
- `-o former_megahit_out`: Output directory, must be a previously generated directory containing relevant intermediate files
- `-m 0.9`: Memory usage percentage, other parameters can also be added