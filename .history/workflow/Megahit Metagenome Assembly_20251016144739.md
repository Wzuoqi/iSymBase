# Megahit宏基因组组装

### **4. 输入文件准备**

MEGAHIT 接受的输入文件格式为**fastq**，可以是单端或双端测序数据，文件可以是gz或bz2压缩格式。Fastq文件包含了每个DNA序列片段的质量信息和相应的碱基序列。

### **5. 基本命令使用**

以下是一些基本的MEGAHIT命令及其参数的逐行注释：

```
megahit --presets meta-large -t 30 --12 B1W10_1.fq,B1W101_2.fq -o ./megahit
```

- `-presets meta-large`：这是为宏基因组分析设计的预设参数，会进行多次组装并选择最佳结果。
- `t 30`：设置线程数为30，可以根据你的计算机性能调整。
- `-12 B1W10_1.fq,B1W101_2.fq`：指定双端测序数据的两个文件，用逗号分隔。
- `o ./megahit`：指定输出目录为当前目录下的`megahit`文件夹。

### **6. 输入文件格式**

FASTQ文件格式是存储原始测序数据的标准格式。文件的**每一行代表一个read，包括序列标识符、碱基序列、分隔符`+`和质量得分**。

### **7. 输出文件解析**

MEGAHIT的输出文件中，最重要的包括：

- `final.contigs.fa`：**组装后的contigs，以fasta格式存储。**
- `log`：程序运行日志，记录了执行进度和可能的错误信息。
- `options.json`：执行时使用的参数，以JSON格式存储。

[](https://mmbiz.qpic.cn/mmbiz_png/ZgRhHg3laFrkFYFMSMpRh47CRHb9ofyGdfH4PBW9ssmcsia6ibG1fQ2QxYdrMXrnnw93nOZH3wvCmH7VDCnmqqEQ/640?wx_fmt=png&from=appmsg&tp=wxpic&wxfrom=5&wx_lazy=1&wx_co=1)

### **8. 常见问题与解决**

- **std::bad_alloc/Exit code -6**：内存不足错误。可以通过增加`m`参数指定的内存使用率或尝试使用更大的kmer值来降低组装复杂度。
- **从中断点继续运行**：如果组装因内存不足或其他原因中断，可以使用`-continue`参数从之前的输出目录继续运行。

### **9. 预设参数**

MEGAHIT提供了两组预设参数：

- `meta-sensitive`：更灵敏，耗时较长。
- `meta-large`：适合大型且复杂的宏基因组数据，如土壤样本。

### **10. 内存需求**

MEGAHIT的内存需求至少是原始数据的1.04倍到1.5倍。内存消耗主要在kmer计数和构建de Bruijn Graph步骤。

# 命令示例

```bash
# 双端序列组装：
	megahit -1 pe_1.fq -2 pe_2.fq -o out
	#-1：pair-end 1序列，-2 pair-end 2序列，-o输出目录
# 单端序列：
	megahit -r single_end.fq -o out
# 交错的双端序列：
	megahit --12 interleaved.fq -o out
```

## 从中断点继续运行

当组装大数据的时候可能由于内存不够或其他原因中断，此使可以使用

```
megahit --continue -o former_megahit_out  -m 0.9
```

参数说明：
–continue：从中断处继续运行
-o former_megahit_out: 输出目录，必须是之前已经生成的目录，包含相关中间文件
-m 0.9：使用内存百分比，也可加其他参数