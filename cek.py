file_path = 'dictionary_title.txt'

with open(file_path, 'r', encoding='mac_roman') as file:
    data = file.readlines()
    for line in data[:10]:  # Menampilkan 10 baris pertama
        print(line)
grep -r "dictionary_title.txt" .
