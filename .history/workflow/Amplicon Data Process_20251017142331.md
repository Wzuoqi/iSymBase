## 流程概述

本流程主要包括以下几个步骤：

1. **数据质控与合并**：使用 Fastp 对原始双端测序数据进行质量控制和双端合并。

2. **引物序列裁剪**：使用 seqtk 统一裁剪序列两端的引物序列。

3. **OTU 聚类与物种注释 (Vsearch)**：使用 Vsearch 进行 OTU（操作分类单元）聚类、去除嵌合体并进行初步的物种注释。

4. **物种注释 (Qiime2)**：使用 Qiime2 对 OTU 代表序列进行更精确的物种注释。

5. **功能注释 (FAPROTAX)**：使用 FAPROTAX 对物种注释结果进行功能预测。


---

## 依赖软件与环境准备

在开始之前，请确保您已经安装了以下软件，并将它们添加到了您的系统环境变量中：

- **Fastp**: 一个用于FASTQ文件预处理的工具，功能包括质量控制、去除接头等。

- **Seqtk**: 一个用于处理FASTA/Q格式序列的工具包。

- **Vsearch**: 一个功能多样的微生物组学分析工具，常用于序列聚类、去重复等。

- **Qiime2**: 一个强大的微生物组分析平台，提供从数据处理到统计分析的多种功能。

- **FAPROTAX**: 一个基于文献的工具，用于根据原核生物的分类学信息推断其功能。

- **Greengenes v13.5 reference database**: 用于 Vsearch 进行物种注释的参考数据库。

- **预训练的Greengenes分类器**: 用于 Qiime2 进行物种注释。


## 详细操作步骤

### 1. 数据质控与合并 (Fastp)

此步骤旨在过滤掉低质量的 reads，并对双端测序数据进行合并，以提高后续分析的准确性。

**a. 质量控制**

对原始的双端SRA数据（input_file1 和 input_file2）进行质控。

```shell
# -i, -I: 输入文件1和文件2
# --q: 质量值过滤阈值，低于15的碱基将被修剪
# -u: 对每个read修剪的百分比阈值
# -l: 长度过滤阈值，修剪后长度小于15的read将被丢弃
# -o, -O: 输出文件1和文件2
# --detect_adapter_for_pe: 自动检测双端测序的接头并去除

fastp -i input_file1 -I input_file2 --q 15 -u 40 -l 15 -o output_file1 -O output_file2 --detect_adapter_for_pe
```

**b. 双端合并**

将质控合格的双端序列（output_file1 和 output_file2）进行合并。


```shell
# -m, --merge: 开启合并模式
# --merged_out: 合并后的输出文件名

fastp -i output_file1 -I output_file2 -m --merged_out merged_file
```

### 2. 引物序列统一裁剪 (seqtk)

为了消除引物对后续聚类和分类的影响，需要统一裁剪掉序列两端的引物序列。

```shell
# trimfq: seqtk的子命令，用于修剪序列
seqtk trimfq -b 20 -e 20 input_file > output_file
```

### 3. OTU 表格生成与注释 (Vsearch)

在这一步中，我们将使用 Vsearch 对序列进行聚类，生成OTU，并基于 Greengenes 数据库进行物种注释。

**a. 去除低频序列 (Dereplication)**

将完全相同的序列合并，并去除出现频率过低的序列（minuniquesize 3 表示至少出现3次）。


```shell
vsearch --fastx_uniques "$input_file" --minuniquesize 3 --threads 8 --sizeout --fastaout "$output_folder/${base_name}.na.fasta"
```

**b. 序列聚类 (Clustering)**

将去重复后的序列按照 97% 的相似度进行聚类，生成OTU代表序列。


``` shell
vsearch --cluster_fast "$output_folder/${base_name}.na.fasta" --id 0.97 --centroid "$output_folder/${base_name}.otu.fa" --relabel "${base_name}_" --sizeout --threads 8
```

**c. 去除嵌合体 (Chimera removal)**

鉴定并去除在PCR扩增过程中可能产生的嵌合体序列。


```shell
vsearch --uchime3_denovo "$output_folder/${base_name}.otu.fa" --threads 8 --nonchimeras "$output_folder/${base_name}.otuna.fa"
```

**d. 生成 OTU 表 (OTU table generation)**

将原始的、经过处理的序列比对回OTU代表序列，生成OTU丰度表。


```shell
vsearch --usearch_global "$input_file" --db "$output_folder/${base_name}.otuna.fa" --id 0.97 --threads 8 --otutabout "$output_folder/${base_name}.otutab.txt"
```

**e. 物种分类 (Taxonomic classification with SINTAX)**

使用 SINTAX 算法和 Greengenes 数据库对 OTU 代表序列进行物种注释。


```shell
vsearch --sintax "$output_folder/${base_name}.otuna.fa" --db "$sintax_db" --sintax_cutoff 0.1 --threads 8 --tabbedout "$output_folder/${base_name}.sintax"
```

### 4. 使用 Qiime2 进行物种注释

为了获得更可靠的物种注释结果，我们使用 Qiime2 平台及其预训练的分类器对 Vsearch 生成的 OTU 代表序列进行分类。
**a. 导入 OTU 代表序列**

将 FASTA 格式的 OTU 序列文件导入为 Qiime2 的标准格式（.qza）。

codeBash

```shell
qiime tools import \
  --type 'FeatureData[Sequence]' \
  --input-path "${base_name}.otuna.fa" \
  --output-path "${base_name}.repotu.qza"
```

**b. 物种注释**

使用预训练的 Greengenes 分类器对导入的序列进行物种分类。
```shell
# --i-classifier: 指定预训练的分类器文件
# --i-reads: 输入的OTU代表序列文件
# --o-classification: 输出的物种注释结果

qiime feature-classifier classify-sklearn \
  --i-classifier "gg_2022_10_backbone_full_length.nb.qza" \
  --i-reads "${base_name}.repotu.qza" \
  --o-classification "${base_name}.taxonomy.qza"
```

**c. 导出物种注释结果**

将 Qiime2 格式的注释结果导出为制表符分隔的文本文件（.tsv），方便后续分析。

```shell
qiime tools export \
  --input-path "${base_name}.taxonomy.qza" \
  --output-path "taxonomy_folder"
```

注意：导出的 taxonomy.tsv 文件在指定的 taxonomy_folder 文件夹中。

### 5. 功能注释 (FAPROTAX)

最后，我们使用 FAPROTAX 工具，基于 Qiime2 提供的物种注释信息，来预测微生物群落的潜在功能。

codeBash

```shell
python collapse_table.py -i "taxonomy_folder/taxonomy.tsv" -o "${base_name}.faprotax" -g "FAPROTAX.txt" -r "${base_name}.report.txt" -v -d 'Taxon'
```
