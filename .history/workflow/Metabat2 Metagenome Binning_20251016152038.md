# Metabat2宏基因组分箱binning流程

在megahit对于宏基因组组装完成后进行

软件地址
[berkeleylab / metabat — Bitbucket](https://bitbucket.org/berkeleylab/metabat/src/master/)

# 1. 构建contigs索引

```bash
bowtie2-build -f ./megahit/SRR12112864.man.contigs.fa ./metabat/SRR12112864.man.bowtie2 --threads 16

```

# 2.比对测序数据与contigs

双端测序

```bash
bowtie2 -1 SRR12112864.man_1.qc.fastq -2 SRR12112864.man_2.qc.fastq -p 32 -x ./metabat/SRR12112864.man.bowtie2 -S ./metabat/SRR12112864.man.sam
```

# 3.BAM格式转换与排序

```bash
samtools view -@ 32 -b -S SRR12112864.man.sam -o SRR12112864.man.bam
samtools sort -@ 32 -l 9 -O BAM SRR12112864.man.bam -o SRR12112864.man.sorted.bam
```

# 4.计算contig深度

```bash
jgi_summarize_bam_contig_depths SRR12112864.man.sorted.bam --outputDepth SRR12112864.man.depth.txt
```

# 5.分箱

```bash
metabat2 -t 32 -i ../megahit/SRR12112864.man.contigs.fa -a SRR12112864.man.depth.txt -o SRR12112864.man.bin -v
```

# 6.评估

```bash
checkm lineage_wf -t 32 -x fa --nt --tab_table -f ./checkm/bins_ qa.txt ./ ./checkm
```

# 批量流程（单端）

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

# 批量流程（双端）

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