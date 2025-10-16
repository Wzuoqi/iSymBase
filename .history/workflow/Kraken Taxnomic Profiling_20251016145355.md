## **Kraken 2介绍**

Kraken2 是一种用于宏基因组学研究的物种注释工具，它通过**快速且准确的k-mer比对技术来识别DNA序列的物种来源**。以下是关于Kraken2的一些关键信息：

1. **基本原理**：Kraken2 利用基于k-mer的精确比对，通过最小化最近公共祖先（LCA）投票结果来对宏基因组DNA序列进行物种注释。
2. **软件发展**：Kraken2 的前身Kraken1由于内存需求大而受到限制，Kraken2 在此基础上进行了优化，减少了内存使用，并且使得输出结果格式更加友好，便于下游分析。
3. **软件安装**：推荐使用conda进行安装，一条命令即可完成安装过程。此外，也可以通过git或wget下载源码，然后按照官方文档进行安装。
4. **数据库构建**：Kraken2 支持多种数据库，包括NCBI、Greengenes、RDP和SILVA等，用户可以根据自己的需求选择合适的数据库进行建库。
5. **特点**：
    - 高效快速：Kraken2 使用高效的k-mer比对算法，支持多线程处理，能够在短时间内完成大规模的物种注释。
    - 准确性高：与传统的BLAST等比对算法相比，Kraken2 提供了更高的准确性。
    - 数据库广泛：Kraken2 的参考数据库包括了各种生物的完整基因组序列和代表性序列，覆盖了不同的分类级别。
    - 灵活性高：用户可以自定义参考数据库，以适应特定研究领域的需求。
    - 输出结果清晰：Kraken2 的输出结果以表格或图表形式展示，方便用户进行数据分析和可视化。
6. **使用场景**：Kraken2 可以用于各种类型的生物样品的物种注释，包括但不限于海洋微生物群落、土壤微生物以及人体微生物组的研究。
7. **命令行操作**：Kraken2 提供了丰富的命令行选项，允许用户根据需要进行个性化设置，例如使用特定线程数、快速操作、序列过滤等。
8. **与其他工具的集成**：Kraken2 可以与Bracken等其他分析软件集成使用，以提高物种注释结果的准确性，并提供更精细的相对丰度值。

# 注释流程

Kraken 2是一个用于宏基因组学分析的快速、准确、可扩展的系统，它通过k-mer分类来识别和注释微生物序列。以下是Kraken 2宏基因组物种注释的详细使用教程，包括代码逐行注释，适合初学者学习。

### **1. 准备Kraken 2数据库**

首先，需要下载或构建Kraken 2的数据库。Kraken 2数据库是基于已知的细菌、古菌、病毒和真核生物序列构建的。

```
# 访问Kraken2官方网站下载数据库
# 网址：https://ccb.jhu.edu/software/kraken2/index.shtml

# 使用kraken2-build命令下载数据库
# 例如，下载Kraken2的细菌数据库
kraken2-build --download-library bacteria --db /path/to/database
```

### **2. 下载分类学信息和序列库**

Kraken 2需要分类学信息和序列库来进行物种注释。

```
# 设置数据库存放位置
DBNAME=~/db/kraken2
mkdir -p $DBNAME
cd $DBNAME

# 下载分类学信息
kraken2-build --download-taxonomy --threads 24 --db $DBNAME

# 下载非默认数据库中的真菌库
kraken2-build --download-library fungi --threads 24 --db $DBNAME

# 批量下载非标准数据库
for i in archaea bacteria plasmid viral human fungi plant protozoa nr nt env_nr env_nt UniVec; do
  kraken2-build --download-library $i --threads 24 --db $DBNAME
done

```

### **3. 构建数据库**

下载完数据库后，需要构建索引以便Kraken 2能够快速查询。

```
# 构建数据库
kraken2-build --build --db $DBNAME --threads [NUMBER_OF_THREADS]

```

### **4. 序列分类**

使用Kraken 2对序列进行分类。

```
# 对序列文件进行分类
kraken2 --db $DBNAME --threads <number_of_threads> --report <output_file> <input_file>

```

### **5. 代码注释**

- `-db`: 指定数据库路径。
- `-threads`: 指定线程数，提高处理速度。
- `-download-taxonomy`: 下载分类学信息。
- `-download-library`: 下载特定的序列库。
- `-build`: 构建数据库索引。

### **6. 输出文件格式**

Kraken 2的输出有标准输出格式和报告输出格式。

- 标准输出格式包括五列：分类状态、序列ID、物种注释、比对区域、LCA比对结果。
- 报告输出格式包括六列：百分比、计数、最优计数、分类层级、NCBI物种ID、科学物种名。

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/56d9757a-5444-4ed9-827c-5573f717615b/ef727e27-d9c3-4dd8-9f75-2e8afbbc5689/image.png)

## 使用实例

```bash
kraken2 --db /data/software/kraken_database/ --threads 48 --report DRR505509.kraken.txt DRR505509.qc.fastq

bracken -d /data/software/kraken_database/ -i DRR505509.kraken.txt -o DRR505509.bracken.S -w DRR505509.S.kreport -l S -t 48

ktImportTaxonomy -q 2 -t 3 DRR505509.S.kreport -o DRR505509.kraken.krona.html
```