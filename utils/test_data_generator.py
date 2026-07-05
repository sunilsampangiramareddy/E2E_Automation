import pandas as pd
import itertools
import os
from datetime import datetime  # Import datetime module for timestamp

class TestDataGenerator:
    """
    TestDataGenerator class reads an input Excel file containing rows of data. It generates all possible permutations 
    of the columns for each row, especially when multiple values are provided per cell (comma-separated). 
    The output preserves the original headers and limits the number of permutations if specified. 
    The final set is written to a new Excel file in a designated output folder.

    Attributes:
        input_folder (str): Folder where the input Excel is located.
        input_filename (str): Name of the input Excel file.
        output_folder (str): Folder where the generated permutations will be saved.
        num_permutations (int): Maximum number of permutations (if exceeded, it trims results).
        output_filename (str): Name of the output Excel file.
        input_path (str): Full path to the input Excel file.
    """

    def __init__(self):
        self.input_filename = 'test_data_generator.xlsx'
        self.num_permutations = 20000  # Hardcoded number of permutations

        self.input_folder = 'test_data_generator'        
        self.output_folder = 'generated_test_data'
        # Add timestamp to output filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.output_filename = f'generated_test_data_{timestamp}.xlsx'
        self.input_path = os.path.join(self.input_folder, self.input_filename)

    def run(self):
        """Runs the full data generation process: reading input, generating combinations, and writing output."""
        self.read_input()
        self.generate_combinations()
        self.write_output()

    def read_input(self):
        """
        Reads the input Excel file into a DataFrame, treating the first two rows as headers
        and the third row onward as test data.
        """
        # Read the Excel file without assuming a single header row
        raw_df = pd.read_excel(self.input_path, header=None)

        # Separate headers and data
        self.headers = raw_df.iloc[:2]  # First two rows as headers
        self.data = raw_df.iloc[2:]  # Data starting from the third row

        # Combine the first two rows to create multi-level column headers
        self.combined_headers = [" ".join(map(str, header)).strip() for header in zip(*self.headers.values)]

        # Create the main DataFrame using the combined headers
        self.df = pd.DataFrame(self.data.values, columns=self.combined_headers)

        print("Headers combined from first two rows:")
        print(self.combined_headers)

    def generate_combinations(self):
        """Generates all permutations for each row based on possible multiple values per cell."""
        columns = self.df.columns
        all_combinations = []

        for index, row in self.df.iterrows():
            row_values = []

            for col in columns:
                if pd.notna(row[col]):
                    # Split by comma to handle multiple values in a cell
                    values = [v.strip() for v in str(row[col]).split(',')]
                    row_values.append(values)
                    print(f"Row {index + 3}, column '{col}' split values: {values}") # type: ignore
                else:
                    row_values.append([None])  # Placeholder if missing

            # Generate combinations for this row
            row_combinations = list(itertools.product(*row_values))
            print(f"Row {index + 3} has {len(row_combinations)} combinations") # type: ignore

            for comb in row_combinations:
                combined_row = {col: comb[i] for i, col in enumerate(columns)}
                all_combinations.append(combined_row)

        # Limit to num_permutations if needed
        if len(all_combinations) > self.num_permutations:
            all_combinations = all_combinations[:self.num_permutations]

        # Create a DataFrame from the combinations
        self.output_df = pd.DataFrame(all_combinations)

    def write_output(self):
        """Writes the generated combinations to an Excel output file in the specified folder."""
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

        output_path = os.path.join(self.output_folder, self.output_filename)

        # Write the output DataFrame to Excel with the first two rows as headers
        with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
            # Write headers
            self.headers.to_excel(writer, index=False, header=False, startrow=0)
            # Write data
            self.output_df.to_excel(writer, index=False, startrow=2, header=False)

        print(f"Generated test data written to: {output_path}")

# Example usage
if __name__ == "__main__":
    generator = TestDataGenerator()
    generator.run()
