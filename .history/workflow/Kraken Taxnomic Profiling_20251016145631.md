## **Introduction to Kraken 2**

Kraken2 is a taxonomic annotation tool for metagenomic research that **identifies the species origin of DNA sequences through fast and accurate k-mer matching technology**. Here are some key points about Kraken2:

1. **Basic Principle**: Kraken2 uses precise k-mer-based matching and minimizes the Lowest Common Ancestor (LCA) voting results to annotate metagenomic DNA sequences.
2. **Software Development**: Kraken2's predecessor, Kraken1, was limited by high memory requirements. Kraken2 has been optimized to reduce memory usage and produce more user-friendly output formats for downstream analysis.
3. **Software Installation**: Installation via conda is recommended, which can be completed with a single command. Alternatively, you can download the source code via git or wget and install according to the official documentation.
4. **Database Construction**: Kraken2 supports multiple databases, including NCBI, Greengenes, RDP, and SILVA. Users can select appropriate databases based on their specific needs.
5. **Features**:
    - Highly Efficient: Kraken2 uses an efficient k-mer matching algorithm with multi-threading support, enabling large-scale taxonomic annotation in a short time.
    - High Accuracy: Compared to traditional alignment algorithms like BLAST, Kraken2 provides higher accuracy.
    - Extensive Databases: Kraken2's reference databases include complete genome sequences and representative sequences of various organisms, covering different taxonomic levels.
    - High Flexibility: Users can customize reference databases to suit specific research areas.
    - Clear Output: Kraken2's output is presented in table or chart format, facilitating data analysis and visualization.
6. **Use Cases**: Kraken2 can be used for taxonomic annotation of various biological samples, including but not limited to marine microbial communities, soil microbiota, and human microbiome research.
7. **Command-line Operations**: Kraken2 offers rich command-line options, allowing users to customize settings such as thread count, fast operations, and sequence filtering.
8. **Integration with Other Tools**: Kraken2 can be integrated with other analysis software like Bracken to improve the accuracy of taxonomic annotation results and provide more detailed relative abundance values.

# Annotation Workflow

Kraken 2 is a fast, accurate, and scalable system for metagenomic analysis that identifies and annotates microbial sequences through k-mer classification. Below is a detailed tutorial on using Kraken 2 for metagenomic taxonomic annotation, including line-by-line code annotations, suitable for beginners.

### **1. Preparing the Kraken 2 Database**

First, you need to download or build the Kraken 2 database. The Kraken 2 database is built based on known bacterial, archaeal, viral, and eukaryotic sequences.

```
# Visit the Kraken2 official website to download the database
# URL: https://ccb.jhu.edu/software/kraken2/index.shtml

# Use the kraken2-build command to download the database
# For example, download the bacterial database for Kraken2
kraken2-build --download-library bacteria --db /path/to/database
```

### **2. Downloading Taxonomic Information and Sequence Libraries**

Kraken 2 requires taxonomic information and sequence libraries for species annotation.

```
# Set the database storage location
DBNAME=~/db/kraken2
mkdir -p $DBNAME
cd $DBNAME

# Download taxonomic information
kraken2-build --download-taxonomy --threads 24 --db $DBNAME

# Download the fungi library from non-default databases
kraken2-build --download-library fungi --threads 24 --db $DBNAME

# Batch download non-standard databases
for i in archaea bacteria plasmid viral human fungi plant protozoa nr nt env_nr env_nt UniVec; do
  kraken2-build --download-library $i --threads 24 --db $DBNAME
done
```

### **3. Building the Database**

After downloading the database, you need to build an index to enable Kraken 2 to query quickly.

```
# Build the database
kraken2-build --build --db $DBNAME --threads [NUMBER_OF_THREADS]
```

### **4. Sequence Classification**

Use Kraken 2 to classify sequences.

```
# Classify sequence files
kraken2 --db $DBNAME --threads <number_of_threads> --report <output_file> <input_file>
```

### **5. Code Annotations**

- `--db`: Specify the database path.
- `--threads`: Specify the number of threads to improve processing speed.
- `--download-taxonomy`: Download taxonomic information.
- `--download-library`: Download specific sequence libraries.
- `--build`: Build the database index.

### **6. Output File Format**

Kraken 2's output has standard output format and report output format.

- The standard output format includes five columns: classification status, sequence ID, species annotation, alignment region, and LCA alignment results.
- The report output format includes six columns: percentage, count, optimal count, taxonomic level, NCBI species ID, and scientific species name.

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/56d9757a-5444-4ed9-827c-5573f717615b/ef727e27-d9c3-4dd8-9f75-2e8afbbc5689/image.png)

## Usage Examples

```bash
kraken2 --db /data/software/kraken_database/ --threads 48 --report DRR505509.kraken.txt DRR505509.qc.fastq

bracken -d /data/software/kraken_database/ -i DRR505509.kraken.txt -o DRR505509.bracken.S -w DRR505509.S.kreport -l S -t 48

ktImportTaxonomy -q 2 -t 3 DRR505509.S.kreport -o DRR505509.kraken.krona.html
```