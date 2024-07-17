import os
import re
import pandas as pd
import matplotlib.pyplot as plt



# Define the pattern to extract Msg ID, RSSI, and SNR from the log content
# Adjust the pattern as necessary based on the actual content structure
pattern_central = re.compile(r"Sender ID: 0x0\n.*?Msg ID: (\d+).*?RSSI: ([-\d]+) dBm\n.*?SNR: ([-\d.]+) dB", re.DOTALL)
#pattern_nodo = re.compile(r"Sender ID: 0xe\n.*?Msg ID: (\d+).*?RSSI: ([-\d]+) dBm\n.*?SNR: ([-\d.]+) dB", re.DOTALL)
pattern_nodo = re.compile(r"Data acknowledged. Msg: (\d+). Ack: \d+.*?Sender ID: 0xe\n.*?Msg ID: \d+.*?RSSI: ([-\d]+) dBm\n.*?SNR: ([-\d.]+) dB", re.DOTALL)




# Pick folder
SF = '12'
BW = '125'

# Define the base directory where the log files are located
base_dir = 'E:\Proyectos\CAMARONES\Pruebas LoRa\sf'+ SF + ' bw' + BW

base_dir2 = 'E:\Proyectos\CAMARONES\Pruebas LoRa'






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


def calc_pdr(temp):
    daf = temp
    daf = daf.sort_values(['Msg ID'])
    daf = daf.drop_duplicates(subset=['Msg ID'])
    daf = daf.reset_index(drop=True)
    first_msg_id = daf['Msg ID'].iloc[0]  # primero
    last_msg_id = daf['Msg ID'].iloc[-1]  # ultimo
    count = daf['Msg ID'].count()         # no. elementos
    diff = last_msg_id - first_msg_id    # restarlos
    pdr = 100 * count / (diff+1)             # dividir entre no. elementos
    return round(pdr,2)


# Walk through the directory to find log files
for subdir, dirs, files in os.walk(base_dir2):
        for file in files:
            # Process files that start with 'central' or 'nodo'
            if file.startswith('central sf7 bw125'):
                central_sf7_bw125 = parser(pattern_central, subdir, file)
                # plotter('Central' + ' SF' + SF + ' BW' + BW, central_sf7_bw125)
            if file.startswith('nodo sf7 bw125'):
                nodo_sf7_bw125 = parser(pattern_nodo, subdir, file)
                # plotter('Nodo' + ' SF' + SF + ' BW' + BW, nodo_sf7_bw125)

            if file.startswith('central sf12 bw125'):
                central_sf12_bw125 = parser(pattern_central, subdir, file)
            if file.startswith('nodo sf12 bw125'):
                nodo_sf12_bw125 = parser(pattern_nodo, subdir, file)
            
            if file.startswith('central sf7 bw250'):
                central_sf7_bw250 = parser(pattern_central, subdir, file)
            if file.startswith('nodo sf7 bw250'):
                nodo_sf7_bw250 = parser(pattern_nodo, subdir, file)
            
            if file.startswith('central sf12 bw250'):
                central_sf12_bw250 = parser(pattern_central, subdir, file)
            if file.startswith('nodo sf12 bw250'):
                nodo_sf12_bw250 = parser(pattern_nodo, subdir, file)

            if file.startswith('central sf7 bw500'):
                central_sf7_bw500 = parser(pattern_central, subdir, file)
            if file.startswith('nodo sf7 bw500'):
                nodo_sf7_bw500 = parser(pattern_nodo, subdir, file)

            if file.startswith('central sf12 bw500'):
                central_sf12_bw500 = parser(pattern_central, subdir, file)
            if file.startswith('nodo sf12 bw500'):
                nodo_sf12_bw500 = parser(pattern_nodo, subdir, file)
        


daf = nodo_sf7_bw250
daf = daf.sort_values(['Msg ID'])
daf = daf.drop_duplicates(subset=['Msg ID'])
daf = daf.reset_index(drop=True)
daf.to_csv('a.csv')


print('central,sf7,bw125',   calc_pdr(central_sf7_bw125),"%",   round(central_sf7_bw125['RSSI'].mean(),2),   round(central_sf7_bw125['SNR'].mean(),2),     sep=",")
print('nodo,sf7,bw125',      calc_pdr(nodo_sf7_bw125),"%",      round(nodo_sf7_bw125['RSSI'].mean(),2),      round(nodo_sf7_bw125['SNR'].mean(),2),     sep=",")
print('central,sf12,bw125',  calc_pdr(central_sf12_bw125),"%",  round(central_sf12_bw125['RSSI'].mean(),2),  round(central_sf12_bw125['SNR'].mean(),2),     sep=",")
print('nodo,sf12,bw125',     calc_pdr(nodo_sf12_bw125),"%",     round(nodo_sf12_bw125['RSSI'].mean(),2),     round(nodo_sf12_bw125['SNR'].mean(),2),     sep=",")
print('central,sf7,bw250',   calc_pdr(central_sf7_bw250),"%",   round(central_sf7_bw250['RSSI'].mean(),2),   round(central_sf7_bw250['SNR'].mean(),2),     sep=",")
print('nodo,sf7,bw250',      calc_pdr(nodo_sf7_bw250),"%",      round(nodo_sf7_bw250['RSSI'].mean(),2),      round(nodo_sf7_bw250['SNR'].mean(),2),     sep=",")
print('central,sf12,bw250',  calc_pdr(central_sf12_bw250),"%",  round(central_sf12_bw250['RSSI'].mean(),2),  round(central_sf12_bw250['SNR'].mean(),2),     sep=",")
print('nodo,sf12,bw250',     calc_pdr(nodo_sf12_bw250),"%",     round(nodo_sf12_bw250['RSSI'].mean(),2),     round(nodo_sf12_bw250['SNR'].mean(),2),     sep=",")
print('central,sf7,bw500',   calc_pdr(central_sf7_bw500),"%",   round(central_sf7_bw500['RSSI'].mean(),2),   round(central_sf7_bw500['SNR'].mean(),2),     sep=",")
print('nodo,sf7,bw500',      calc_pdr(nodo_sf7_bw500),"%",      round(nodo_sf7_bw500['RSSI'].mean(),2),      round(nodo_sf7_bw500['SNR'].mean(),2),     sep=",")
print('central,sf12,bw500',  calc_pdr(central_sf12_bw500),"%",  round(central_sf12_bw500['RSSI'].mean(),2),  round(central_sf12_bw500['SNR'].mean(),2),     sep=",")
print('nodo,sf12,bw500',     calc_pdr(nodo_sf12_bw500),"%",     round(nodo_sf12_bw500['RSSI'].mean(),2),     round(nodo_sf12_bw500['SNR'].mean(),2),     sep=",")


pd.set_option('display.max_rows', None)  # Show all rows
pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.width', None)  # Auto-detect the display width
pd.set_option('display.max_colwidth', None)  # Show full width of showing columns

# make scatter plots of id vs rsssi and id vs snr

# CENTRAL
plt.scatter(central_sf7_bw125['Msg ID'], central_sf7_bw125['RSSI'], label='BW125 SF7')
plt.scatter(central_sf12_bw125['Msg ID'], central_sf12_bw125['RSSI'], label='BW125 SF12')
plt.scatter(central_sf7_bw250['Msg ID'], central_sf7_bw250['RSSI'], label='BW250 SF7')
plt.scatter(central_sf12_bw250['Msg ID'], central_sf12_bw250['RSSI'], label='BW250 SF12')
plt.scatter(central_sf7_bw500['Msg ID'], central_sf7_bw500['RSSI'], label='BW500 SF7')
plt.scatter(central_sf12_bw500['Msg ID'], central_sf12_bw500['RSSI'], label='BW500 SF12')
plt.xlabel('Msg ID')
plt.ylabel('RSSI (dBm)')
plt.title('Msg ID vs RSSI ' + 'central')
handles, labels = plt.gca().get_legend_handles_labels()
plt.legend(handles, labels, loc='lower right')
plt.show()

plt.scatter(central_sf7_bw125['Msg ID'], central_sf7_bw125['SNR'], label='BW125 SF7')
plt.scatter(central_sf12_bw125['Msg ID'], central_sf12_bw125['SNR'], label='BW125 SF12')
plt.scatter(central_sf7_bw250['Msg ID'], central_sf7_bw250['SNR'], label='BW250 SF7')
plt.scatter(central_sf12_bw250['Msg ID'], central_sf12_bw250['SNR'], label='BW250 SF12')
plt.scatter(central_sf7_bw500['Msg ID'], central_sf7_bw500['SNR'], label='BW500 SF7')
plt.scatter(central_sf12_bw500['Msg ID'], central_sf12_bw500['SNR'], label='BW500 SF12')
plt.xlabel('Msg ID')
plt.ylabel('SNR (dB)')
plt.title('Msg ID vs SNR ' + 'central')
handles, labels = plt.gca().get_legend_handles_labels()
plt.legend(handles, labels, loc='upper right')
plt.show()
        



# NODOS
plt.scatter(nodo_sf7_bw125['Msg ID'], nodo_sf7_bw125['RSSI'], label='BW125 SF7')
plt.scatter(nodo_sf12_bw125['Msg ID'], nodo_sf12_bw125['RSSI'], label='BW125 SF12')
plt.scatter(nodo_sf7_bw250['Msg ID'], nodo_sf7_bw250['RSSI'], label='BW250 SF7')
plt.scatter(nodo_sf12_bw250['Msg ID'], nodo_sf12_bw250['RSSI'], label='BW250 SF12')
plt.scatter(nodo_sf7_bw500['Msg ID'], nodo_sf7_bw500['RSSI'], label='BW500 SF7')
plt.scatter(nodo_sf12_bw500['Msg ID'], nodo_sf12_bw500['RSSI'], label='BW500 SF12')
plt.xlabel('Msg ID')
plt.ylabel('RSSI (dBm)')
plt.title('Msg ID vs RSSI ' + 'nodo')
handles, labels = plt.gca().get_legend_handles_labels()
plt.legend(handles, labels, loc='upper right')
plt.show()

plt.scatter(nodo_sf7_bw125['Msg ID'], nodo_sf7_bw125['SNR'], label='BW125 SF7')
plt.scatter(nodo_sf12_bw125['Msg ID'], nodo_sf12_bw125['SNR'], label='BW125 SF12')
plt.scatter(nodo_sf7_bw250['Msg ID'], nodo_sf7_bw250['SNR'], label='BW250 SF7')
plt.scatter(nodo_sf12_bw250['Msg ID'], nodo_sf12_bw250['SNR'], label='BW250 SF12')
plt.scatter(nodo_sf7_bw500['Msg ID'], nodo_sf7_bw500['SNR'], label='BW500 SF7')
plt.scatter(nodo_sf12_bw500['Msg ID'], nodo_sf12_bw500['SNR'], label='BW500 SF12')
plt.xlabel('Msg ID')
plt.ylabel('SNR (dB)')
plt.title('Msg ID vs SNR ' + 'nodo')
handles, labels = plt.gca().get_legend_handles_labels()
plt.legend(handles, labels, loc='lower right')
plt.show()
