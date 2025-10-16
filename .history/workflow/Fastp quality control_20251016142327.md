软件地址

https://github.com/OpenGene/fastp

## 单端测序

```jsx
fastp -i SRR7986792.fastq -o SRR7986792.qc.fastq --detect_adapter_for_pe --thread 16
```

单端测序For SE data, the adapter can be detected for most cases, but if `fastp` failed to find the adapter sequence, you can specify it by `-a` or `--adapter_sequence` option. If adapter sequence is specified, the auto detection is disabled.

## 双端测序

```jsx
fastp -i SRR7986792_1.fastq -I SRR7986792_2.fastq -o SRR7986792_1.qc.fastq -O SRR7986792_2.qc.fastq --detect_adapter_for_pe --thread 16
```

For PE data, the adapters can be trimmed automatically by per-read overlap analysis, which seeks for the overlap of each pair of reads. This method is robust and fast, so normally you don't have to input the adapter sequence. But you can still specify the adapter sequences for read1 by `--adapter_sequence`, and for read2 by `--adapter_sequence_r2`. In case `fastp` fails to find an overlap for some pairs (i.e. due to low quality bases), it will use these sequences to trim adapters for read1 and read2 respectively.

## 批量运行脚本

```bash
#!/bin/bash
for i in `cat fastq.id`
do

        touch $i.log
        fastp -i ./$i/${i}_1.fastq -I ./$i/${i}_2.fastq -o ./$i/${i}_1.qc.fastq -O ./$i/${i}_2.qc.fastq --detect_adapter_for_pe --thread 16

done

```

```bash
#!/bin/bash
for i in `cat fastq.id`
do
fastp -i ./$i/$i.fastq  -o ./$i/$i.qc.fastq --detect_adapter_for_pe --thread 16
done

```