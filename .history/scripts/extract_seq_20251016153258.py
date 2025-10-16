import argparse
from Bio import SeqIO

def extract_long_sequences(fasta_file, output_file, min_length):
    with open(fasta_file, "r") as input_handle, open(output_file, "w") as output_handle:
        for record in SeqIO.parse(input_handle, "fasta"):
            # 获取序列长度
            length = int(record.description.split('len=')[-1])
            if length > min_length:
                # 将符合条件的序列写入输出文件
                SeqIO.write(record, output_handle, "fasta")

def main():
    # 创建解析器
    parser = argparse.ArgumentParser(description="提取FASTA文件中长度大于指定值的序列")

    # 添加输入文件、输出文件和最小长度参数
    parser.add_argument("input_fasta", help="输入的FASTA文件路径")
    parser.add_argument("output_fasta", help="输出的FASTA文件路径")
    parser.add_argument("--min_length", type=int, default=1000, help="最小序列长度 (默认为1000)")

    # 解析参数
    args = parser.parse_args()

    # 调用提取函数
    extract_long_sequences(args.input_fasta, args.output_fasta, args.min_length)

if __name__ == "__main__":
    main()
