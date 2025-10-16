# 基于contig注释 Prodigal-cdhit-nt比对

# 1.Prodigal宏基因组基因预测

Prodigal是一款专门用于原核生物基因组和宏基因组的基因预测软件，以其高效和准确的预测能力而受到广泛认可。以下是对Prodigal的一些**基本介绍**：

1. **功能特点**：
    - 它能够快速、准确地预测蛋白质编码基因，提供GFF3、Genbank或Sequin表格格式的输出。
    - 适用于完成的基因组、草图基因组和宏基因组的分析。
    - 无需提供训练数据，Prodigal是一种无监督机器学习算法，能够自动从序列本身学习基因组的属性，包括遗传密码、RBS基序使用、起始密码子使用和编码统计。
    - 能够处理间隙、支架和部分基因，用户可以指定Prodigal应如何处理间隙，并有许多选项来允许或禁止基因进入或跨越间隙。
    - 能够识别翻译起始位点，并输出有关基因组中每个潜在起始位点的信息，包括置信度评分、RBS基序等。
    - 提供每个基因组的详细汇总统计数据，包括重叠群长度、基因长度、GC含量、GC偏度、使用的RBS基序以及开始和停止密码子的使用。
2. **局限性**：
    - 当前版本不预测RNA基因。
    - 不处理带有内含子的基因，因为这种情况在原核生物中非常罕见。
    - 不提供功能注释，也不包含处理frameshift的逻辑。
    - 尚未对病毒基因预测进行优化，可能不适用于病毒基因组的分析。
3. **安装和使用**：Prodigal的安装相对简单，可以从其GitHub页面下载源代码进行编译，或直接下载预编译的二进制文件。它提供了多种参数选项，允许用户根据需要调整预测过程。
4. **Python模块**：存在一个名为`pyrodigal`的Python模块，它是Prodigal的Python绑定，提供了与Prodigal相同的功能，同时优化了性能和内存使用。

**Prodigal因其高效性和易用性，在微生物基因预测领域得到了广泛应用。**

### 详细参数

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

### 使用实例

```bash
prodigal -i ./megahit/DRR505509.contigs.fa -o ./megahit/DRR505509.gff -d ./megahit/DRR505509.gene.fa -a ./megahit/DRR505509.anno.pep.fa -f gff -p meta
```

## 2. CD-HIT去冗余

```bash
cd-hit-est -i DRR505509.gene.fa -o DRR505509.cdhit.gene.fa -c 0.9 -G 0 -M 0 -T 64 -aS 0.9
```

- **`i`**：输入文件名，**`dna_all.fa`**为fasta格式的DNA序列文件。
- **`o`**：输出文件名，**`out.fa`**为输出的去冗余后的fasta格式的DNA序列文件。
- **`c`**：相似度阈值（切比雪夫距离），本例中设为0.95，即两个序列相似度达到95%时被认为是同一个基因家族的成员。
- **`G`**,**`g`**：法定N/长序列限制。本例中都为0，即没有长度限制。
- **`aS`**：全局序列比对参数。本例中设为0.9，即聚类时使用全局序列比对，且序列相似度需要达到90%以上才能归到同一簇中。
- **`M`**：内存限制。本例中为0，即自动设置内存大小。
- **`T`**：并行线程数。本例中为20，即同时使用20个CPU线程处理任务，提高处理速度。

### 常见错误

**内存不足**：如果遇到内存不足的问题，可以通过调整 `-M` 参数来增加内存使用量。