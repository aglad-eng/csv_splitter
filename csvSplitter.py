import os
import click
import pandas as pd

def read_header(input_path, num_lines):
    with open(input_path, 'r') as file:
        header_lines = [next(file).strip() for _ in range(num_lines)]
    return header_lines

@click.command()
@click.option('--input', '-i', help='Path to the input CSV file', required=True)
@click.option('--output', '-o', help='Path to the output directory', required=True)
@click.option('--lines-per-file', '-l', default=2**16 - 1, type=int, help='Number of lines per output file')
@click.option('--header-lines', '-hl', default=0, type=int, help='Number of header lines to include in each output file')
def split_csv(input, output, lines_per_file, header_lines):
    # Read the header lines
    header_lines_content = read_header(input, num_lines=header_lines)

    # Read the CSV file
    df = pd.read_csv(input, skiprows=header_lines)  # Skip the specified number of header lines

    print(f"Number of lines in DataFrame: {len(df)}")
    print(f"Number of lines in Perfile: {lines_per_file}")

    # Calculate the number of parts needed
    num_parts = (len(df) - 1) // lines_per_file + 1

    print(f"Number of files to be created: {num_parts}")

    # Create the output folder if it doesn't exist
    os.makedirs(output, exist_ok=True)

    # Create a subdirectory with the same name as the original file
    subdirectory = os.path.join(output, os.path.splitext(os.path.basename(input))[0])
    os.makedirs(subdirectory, exist_ok=True)

    # Split the dataframe into parts and save each part to a new CSV file
    for part_num in range(num_parts):
        start_idx = part_num * lines_per_file
        end_idx = min((part_num + 1) * lines_per_file, len(df))
        part_df = df.iloc[start_idx:end_idx]

        # Generate the output filename within the subdirectory
        output_filename = f"{os.path.splitext(os.path.basename(input))[0]}_part{part_num + 1}.csv"
        output_path = os.path.join(subdirectory, output_filename)

        # Save the header lines and the part to a new CSV file
        with open(output_path, 'w', newline='') as file:
            for line in header_lines_content:
                file.write(line + '\n')
            part_df.to_csv(file, index=False, line_terminator='\n')

    print("CSV file successfully split.")

if __name__ == "__main__":
    split_csv()
