import argparse
from Bio import SeqIO

def extract_long_sequences(fasta_file, output_file, min_length):
    with open(fasta_file, "r") as input_handle, open(output_file, "w") as output_handle:
        for record in SeqIO.parse(input_handle, "fasta"):
            # Get sequence length
            length = int(record.description.split('len=')[-1])
            if length > min_length:
                # Write sequences that meet the criteria to the output file
                SeqIO.write(record, output_handle, "fasta")

def main():
    # Create parser
    parser = argparse.ArgumentParser(description="Extract sequences longer than the specified length from a FASTA file")

    # Add input file, output file, and minimum length arguments
    parser.add_argument("input_fasta", help="Path to the input FASTA file")
    parser.add_argument("output_fasta", help="Path to the output FASTA file")
    parser.add_argument("--min_length", type=int, default=1000, help="Minimum sequence length (default: 1000)")

    # Parse arguments
    args = parser.parse_args()

    # Call the extraction function
    extract_long_sequences(args.input_fasta, args.output_fasta, args.min_length)

if __name__ == "__main__":
    main()
