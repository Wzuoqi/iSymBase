# iSymSeek: RAGflow Workflow for iSymBase Database

## Overview

This workflow describes the integration of a deepseek-based AI model with the iSymBase database using RAGflow to enhance query capabilities for insect symbiont information. The process involves building four specialized knowledge bases within RAGflow to provide domain-specific context and improve response accuracy without model retraining or fine-tuning.

---

## RAGflow Implementation Process

### 1. AI Model Integration with iSymBase

The iSymBase contains extensive information about insect symbionts, including host data, gene sequences, and geographical information. To simplify user access to this information, we integrated a deepseek-based AI model. Users can obtain basic symbiont information and learn how to retrieve data from iSymBase through natural language queries. Due to the highly specialized nature of insect symbiont knowledge in iSymBase, the standard deepseek model responses were insufficient. Therefore, we implemented RAGflow for preprocessing and knowledge enhancement.

### 2. RAGflow Working Principle

RAGflow represents an optimized extension of the RAG (Retrieval-Augmented Generation) framework for large language models. RAG functions as an external knowledge repository that enhances model performance through pre-stored domain knowledge.

The standard RAG process involves:
- Converting domain-specific documents into text format and segmenting them into text chunks
- Transforming these chunks into computer-readable vectors (Embedding process)
- Converting user queries into vectors and comparing them with stored vectors using similarity metrics
- Generating prompts based on the most similar vectors from the knowledge base

RAGflow enhances this basic framework with two key improvements:
1. **OCR and Table Recognition**: Simplifies text preprocessing by enabling direct processing of various file formats with different chunk methods
2. **Query Analysis**: Extracts keywords from user queries to improve vector similarity matching accuracy

In essence, RAGflow connects models to knowledge bases, enabling accurate responses without the need for training or fine-tuning through direct information retrieval.

### 3. Knowledge Base Configuration

We configured the deepseek API to connect with external knowledge bases built through RAGflow processing.

#### Knowledge Base Structure

We established four specialized knowledge bases:

1. **Literature Knowledge Base**
   - Contains 106 core publications selected by citation count
   - PDF documents processed using RAGflow's built-in OCR capability
   - Provides professional knowledge foundation and terminology explanations for insect symbionts

2. **Table Knowledge Base**
   - Includes 2,665 entries from website data records
   - Each entry contains: symbiont name, host, function, paper source, and journal
   - Covers authoritative symbiont research published since the 20th century
   - Expands the breadth of model responses

3. **Manual Knowledge Base**
   - Functions as a "help" document for database usage
   - Enables models to master basic database query methods
   - Improves response efficiency and knowledge-query matching

4. **FAQ Knowledge Base**
   - Contains 36 common questions and answers
   - Includes both database usage questions and classic symbiont domain questions
   - Optimizes response logic and ensures answer accuracy

#### Embedding Model and Chunk Methods

**Embedding Model**: BAAI/bge-base-en-v1.5

**Chunk Methods by Knowledge Base**:

- **FAQ Knowledge Base**: Q&A method (supports xlsx, csv, txt formats)
  - Uses separators to distinguish questions from answers
  - Suitable for question-answer pair knowledge bases

- **Table Knowledge Base**: Table method
  - Specifically designed for table file recognition and chunking
  - Requires first row as column headers for xls files

- **Literature & Manual Knowledge Bases**: General method
  - Basic text chunking for unstructured files (pdf, markdown, txt)
  - Uses "naïve" approach with visual detection model
  - Splits text using symbols: ".", "/n", "!", etc.
  - Merges adjacent segments until token count exceeds threshold

#### Parameter Configuration

**Paper Rank**: 0
- Higher values create importance scoring between chunks
- Set to 0 to avoid bias from similar experimental methods across different papers

**Auto-keyword & Auto-question**: 0 (both)
- Disabled to prevent generation of meaningless keywords/questions from literature content
- Manual content is concise and doesn't require automatic generation

**Chunk Token-number**: 128
- Determines chunk size threshold
- Values between 128-512 tested; 128 provided optimal results
- Smaller values prevent semantic truncation, larger values maintain text relevance

**Delimiter**: "/n!?;。；！？"
- Special symbols indicating complete semantic expression
- Used to split text into smaller fragments

### 4. Validation and Results

After completing the RAGflow processing and knowledge base construction, we validated the retrieval-augmented generation effectiveness using common queries. Testing confirmed that the model successfully:

- Provides accurate answers to basic insect symbiont questions
- Guides users in further information retrieval from iSymBase
- Demonstrates foundational knowledge in insect symbiont domain
- Offers practical assistance for iSymBase usage

The implemented system represents a specialized model capable of handling insect symbiont domain queries while supporting user navigation through the iSymBase database.