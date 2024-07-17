import os
import re
import pandas as pd
import matplotlib.pyplot as plt




# Pick folder
SF = '12'
BW = '125'










def plotter(dispositivo, final_df):
    pd.set_option('display.max_rows', None)  # Show all rows
    pd.set_option('display.max_columns', None)  # Show all columns
    pd.set_option('display.width', None)  # Auto-detect the display width
    pd.set_option('display.max_colwidth', None)  # Show full width of showing columns

    # Display the final DataFrame
    print(final_df)
    # make a scatter plot of id vs rsssi and id vs snr
    plt.scatter(final_df['Msg ID'], final_df['RSSI'])
    plt.xlabel('Msg ID')
    plt.ylabel('RSSI (dBm)')
    plt.title('Msg ID vs RSSI ' + dispositivo)
    plt.show()

    plt.scatter(final_df['Msg ID'], final_df['SNR'])
    plt.xlabel('Msg ID')
    plt.ylabel('SNR (dB)')
    plt.title('Msg ID vs SNR ' + dispositivo)
    plt.show()
    return


def parser(pattern,subdir,file):
    all_packets_data = []
    file_path = os.path.join(subdir, file)
    print(f"Opening file: {file_path}")  # Debug print
    with open(file_path, 'r', encoding='ISO-8859-1') as f:
        content = f.read()
        # Find all matches in the file content
        matches = pattern.findall(content)
        # Create a DataFrame for the current file if matches are found
        if matches:
            df = pd.DataFrame(matches, columns=['Msg ID', 'RSSI', 'SNR'])
            # Convert data types
            df['Msg ID'] = df['Msg ID'].astype(int)
            df['RSSI'] = df['RSSI'].astype(int)
            df['SNR'] = df['SNR'].astype(float)
            # Append the DataFrame to the list
    all_packets_data.append(df)
    return pd.concat(all_packets_data, ignore_index=True)




# Define the base directory where the log files are located
base_dir = 'E:\Proyectos\CAMARONES\Pruebas LoRa\sf'+ SF + ' bw' + BW

# Define the pattern to extract Msg ID, RSSI, and SNR from the log content
# Adjust the pattern as necessary based on the actual content structure
pattern_central = re.compile(r"Sender ID: 0x0\n.*?Msg ID: (\d+).*?RSSI: ([-\d]+) dBm\n.*?SNR: ([-\d.]+) dB", re.DOTALL)
pattern_nodo = re.compile(r"Sender ID: 0xe\n.*?Msg ID: (\d+).*?RSSI: ([-\d]+) dBm\n.*?SNR: ([-\d.]+) dB", re.DOTALL)

# Initialize an empty list to hold all packets data


# Walk through the directory to find log files
for subdir, dirs, files in os.walk(base_dir):
    for file in files:
        # Process files that start with 'central' or 'nodo'
        if file.startswith('central'):
            final_df_central = parser(pattern_central, subdir, file)
            plotter('Central' + ' SF' + SF + ' BW' + BW, final_df_central)

        if file.startswith('nodo'):
            final_df_nodo = parser(pattern_nodo, subdir, file)
            plotter('Nodo' + ' SF' + SF + ' BW' + BW, final_df_nodo)


