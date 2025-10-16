MetaPhlAn: Taxonomic Profiling of Microbiomes



# 1. 软件介绍

MetaPhlAn 是一个用于分析微生物群落（包括**细菌、古菌和真核生物**）组成的计算工具，它基于宏基因组测序数据（即**不是16S rRNA基因测序**）进行物种水平的分析。**StrainPhlAn** 允许进行**准确的菌株水平微生物**分析。MetaPhlAn 4 依赖于从约100万个微生物基因组（约23.66万个参考基因组和77.15万个宏基因组组装基因组）中识别出的约510万个独特类群特异性标记基因，涵盖26,970个物种水平基因组箱（SGBs），其中4,992个在物种水平上未被分类（最新的标记信息文件可以在这里找到），这使得 MetaPhlAn 能够：

- **进行明确的分类学分配**
- **准确估计有机体的相对丰度**
- **达到细菌、古菌和真核生物的SGB水平分辨率**
- **识别和追踪菌株**
- **与现有方法相比，速度提高了数个数量级**

# 2. 软件安装与数据库下载

**创建Conda环境**：创建一个名为`mpa`的新Conda环境，并指定Python版本为3.7。这一步是为了避免不同软件包之间的依赖冲突。

```
conda create --name mpa -c bioconda python=3.7
```

**激活环境**：激活刚才创建的`mpa`环境，确保后续操作都在这个环境中执行。

```
conda activate mpa
```

**安装MetaPhlAn 4**：使用Conda安装MetaPhlAn 4。Bioconda是一个专门提供生物信息学软件包的Conda频道。

```
conda install -c bioconda metaphlan

```

### **配置数据库**

**安装数据库**：使用MetaPhlAn的`-install`命令来自动安装数据库。这将下载并安装最新的数据库文件。

```
metaphlan --install

```

**手动下载数据库**（如果自动安装失败）：访问MetaPhlAn数据库的官方下载页面（Github中有），手动下载数据库文件，并放置到指定的文件夹中。

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/56d9757a-5444-4ed9-827c-5573f717615b/bfc043ac-7ee1-4a0d-a327-7f5155f9611d/Untitled.png)

在这一步注意要下载同一版本的所有文件（包括bowtie2_indexes），并且放置在对应软件的文件夹中，例如/data/home/wangzuoqi/mambaforge/envs/mpa/lib/python3.7/site-packages/metaphlan/metaphlan_databases

# 3. 运行MetaPhlAn4

1. **准备输入文件**：确保你的输入文件是FASTQ或FASTA格式，这是MetaPhlAn支持的输入格式。
2. **运行分析**：使用MetaPhlAn分析宏基因组数据。这里以双端测序数据为例。

```
 metaphlan *.fastq1,*.fastq2 \
 --input_type fastq \
 -o output.txt \
 --nproc 10 \
 --stat_q 0.1 \
 --bowtie2out bowtie2out_*.bz2
```

- `.fastq1,*.fastq2`：指定输入文件的通配符，匹配所有以`.fastq1`和`.fastq2`结尾的文件。
- `-input_type fastq`：指定输入文件类型为FASTQ格式。
- `o output.txt`：指定输出文件的前缀，所有结果文件将以`output.txt`为前缀。
- `-nproc 10`：指定使用10个处理器核心来加速分析。
- `-stat_q 0.1`：指定统计置信度阈值，较低的值会提高敏感性但可能增加假阳性。
- `-bowtie2out bowtie2out_*.bz2`：指定bowtie2输出文件的前缀，输出文件将被压缩。

### **结果解释**

1. **查看输出文件**：输出文件通常包括一个文本文件（如`output.txt`）和一个二进制文件（如`bowtie2out_*.bz2`）。文本文件包含分类结果和相对丰度值。
2. **合并样本结果**：如果分析了多个样本，可以使用以下命令合并结果。

```bash
 merge_metaphlan_tables.py *.txt > merged_abundance_table.txt
```

1. **提取特定分类水平的信息**：使用Linux命令提取特定分类水平下的物种注释信息，例如种水平。

```
 grep -E '(s__)|(clade_name)' merged_abundance_table.txt \
 | grep -v 't__' \
 | sed 's/^.*s__//g' \
 | awk '{$2=null;print}' \
 | sed 's/\ \ /\ /g' \
 | sed 's/\ /\t/g' > merged_abundance_species.txt

```

- `grep -E '(s__)|(clade_name)'`：搜索包含`s__`（物种前缀）或`clade_name`的行。
- `grep -v 't__'`：排除包含`t__`（类型前缀）的行。
- `sed 's/^.*s__//g'`：删除行首到`s__`的部分。
- `awk '{$2=null;print}'`：使用awk打印除第二列外的所有列。
- `sed 's/\ \ /\ /g'`和`sed 's/\ /\t/g'`：格式化输出，将空格替换为制表符。

### 输出结果示例：

```bash
#mpa_vJun23_CHOCOPhlAnSGB_202403
#/data/home/wangzuoqi/mambaforge/envs/mpa/bin/metaphlan SRR7287194.man_1_clean.fastq.gz,SRR7287194.man_2_clean.fastq.gz --input_type fastq -o output_SRR7287194.txt --nproc 64 --stat_q 0.2 --bowtie2out bowtie2out_*.bz2
#51299120 reads processed
#SampleID	Metaphlan_Analysis
#clade_name	NCBI_tax_id	relative_abundance	additional_species
k__Bacteria	2	100.0
k__Bacteria|p__Firmicutes	2|1239	53.43906
k__Bacteria|p__Actinobacteria	2|201174	35.49352
k__Bacteria|p__Proteobacteria	2|1224	11.06741
k__Bacteria|p__Firmicutes|c__Bacilli	2|1239|91061	53.43906
k__Bacteria|p__Actinobacteria|c__Actinomycetia	2|201174|1760	35.49352
k__Bacteria|p__Proteobacteria|c__Gammaproteobacteria	2|1224|1236	6.4949
k__Bacteria|p__Proteobacteria|c__Alphaproteobacteria	2|1224|28211	3.23362
k__Bacteria|p__Proteobacteria|c__Betaproteobacteria	2|1224|28216	1.33889
k__Bacteria|p__Firmicutes|c__Bacilli|o__Lactobacillales	2|1239|91061|186826	53.43906
k__Bacteria|p__Actinobacteria|c__Actinomycetia|o__Bifidobacteriales	2|201174|1760|85004	35.44482
k__Bacteria|p__Proteobacteria|c__Gammaproteobacteria|o__Orbales	2|1224|1236|1240482	6.48948
k__Bacteria|p__Proteobacteria|c__Alphaproteobacteria|o__Rhodospirillales	2|1224|28211|204441	3.07755
k__Bacteria|p__Proteobacteria|c__Betaproteobacteria|o__Neisseriales	2|1224|28216|206351	1.33889
k__Bacteria|p__Proteobacteria|c__Alphaproteobacteria|o__Sphingomonadales	2|1224|28211|204457	0.1505
k__Bacteria|p__Actinobacteria|c__Actinomycetia|o__Propionibacteriales	2|201174|1760|85009	0.0487
```

# 4 krona可视化物种分类结果

将MetaPhlAn4输出结果转化为krona可以接受的格式

值得注意的是原软件github中的metaphlan2krona.py存在一定问题无法直接使用，所以做了以下修改：

```python
#!/usr/bin/env python

# ==============================================================================
# Conversion script: from MetaPhlAn output to Krona text input file
# Author: Daniel Brami (daniel.brami@gmail.com)
# Updated by: Your Name
# ==============================================================================

import sys
import optparse
import re

def main():
    # Parse Command Line
    parser = optparse.OptionParser()
    parser.add_option('-p', '--profile', dest='profile', default='', action='store', help='The input file is the MetaPhlAn standard result file')
    parser.add_option('-k', '--krona', dest='krona', default='krona.out', action='store', help='the Krona output file name')
    (options, spillover) = parser.parse_args()

    if not options.profile or not options.krona:
        parser.print_help()
        sys.exit()

    re_candidates = re.compile(r"s__")
    re_replace = re.compile(r"\w__")
    re_bar = re.compile(r"\|")

    with open(options.profile, 'r') as f:
        metaPhLan = f.readlines()

    with open(options.krona, 'w') as metaPhLan_FH:
        for aline in metaPhLan:
            if re.search(re_candidates, aline):
                aline = aline.strip()
                x = re.sub(re_replace, '\t', aline)
                x = re.sub(re_bar, '', x)
                x_cells = x.split('\t')

                # Check last column and remove until a float is found
                while x_cells:
                    try:
                        abundance = float(x_cells[-1])
                        lineage = '\t'.join(x_cells[:-2])
                        metaPhLan_FH.write(f'{abundance}\t{lineage}\n')
                        break
                    except ValueError:
                        x_cells.pop()  # Remove the last element if it's not a float
                    except IndexError:
                        print(f"Skipping line, no more elements to check: {aline}")
                        break

if __name__ == '__main__':
    main()
```

将格式进行对应转化

```bash
python3 metaphlan2krona.py -p output_SRR7287194.txt -k new_krona.txt
```

输出的krona格式如下：

```bash
19.50819                Bacteria        Actinobacteria  Actinomycetia   Bifidobacteriales       Bifidobacteriaceae      Bifidobacterium Bifidobacterium_choladohabitans
17.91075                Bacteria        Firmicutes      Bacilli Lactobacillales Lactobacillaceae        Lactobacillus   Lactobacillus_apis
11.47015                Bacteria        Firmicutes      Bacilli Lactobacillales Lactobacillaceae        Lactobacillus   Lactobacillus_kullabergensis
10.16333                Bacteria        Actinobacteria  Actinomycetia   Bifidobacteriales       Bifidobacteriaceae      Bifidobacterium Bifidobacterium_apousia
7.71075         Bacteria        Firmicutes      Bacilli Lactobacillales Lactobacillaceae        Lactobacillus   Lactobacillus_kimbladii
7.33696         Bacteria        Firmicutes      Bacilli Lactobacillales Lactobacillaceae        Lactobacillus   Lactobacillus_helsingborgensis
6.25894         Bacteria        Firmicutes      Bacilli Lactobacillales Lactobacillaceae        Bombilactobacillus      Bombilactobacillus_mellis
3.5019          Bacteria        Actinobacteria  Actinomycetia   Bifidobacteriales       Bifidobacteriaceae      Bifidobacterium Bifidobacterium_asteroides
3.14499         Bacteria        Proteobacteria  Gammaproteobacteria     Orbales Orbaceae        Frischella      Frischella_perrara
3.07755         Bacteria        Proteobacteria  Alphaproteobacteria     Rhodospirillales        Acetobacteraceae        Commensalibacter        Commensalibacter_sp_AMU001
2.26299         Bacteria        Actinobacteria  Actinomycetia   Bifidobacteriales       Bifidobacteriaceae      Bifidobacterium Bifidobacterium_polysaccharolyticum
1.95461         Bacteria        Proteobacteria  Gammaproteobacteria     Orbales Orbaceae        Gilliamella     Gilliamella_apicola
1.42838         Bacteria        Firmicutes      Bacilli Lactobacillales Lactobacillaceae        Lactobacillus   Lactobacillus_melliventris
1.38987         Bacteria        Proteobacteria  Gammaproteobacteria     Orbales Orbaceae        Gilliamella     Gilliamella_apis
1.33889         Bacteria        Proteobacteria  Betaproteobacteria      Neisseriales    Neisseriaceae   Snodgrassella   Snodgrassella_alvi
1.21438         Bacteria        Firmicutes      Bacilli Lactobacillales Lactobacillaceae        Bombilactobacillus      Bombilactobacillus_mellifer
0.14929         Bacteria        Proteobacteria  Alphaproteobacteria     Sphingomonadales        Sphingomonadaceae       Sphingomonas    Sphingomonas_paucimobilis
0.10877         Bacteria        Firmicutes      Bacilli Lactobacillales Lactobacillaceae        Lactobacillus   Lactobacillus_sp_W8173
0.0487          Bacteria        Actinobacteria  Actinomycetia   Propionibacteriales     Propionibacteriaceae    Cutibacterium   Cutibacterium_acnes
0.00841         Bacteria        Actinobacteria  Actinomycetia   Bifidobacteriales       Bifidobacteriaceae      Bifidobacterium Bifidobacterium_coryneforme
```

将以上内容提供给krona进行可视化，最终输出为html的物种分类图

```bash
ktImportText krona.txt
```