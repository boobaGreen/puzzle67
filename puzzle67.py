import multiprocessing
from bit import Key
import os
import json
from datetime import datetime

# Definizione dei limiti
START = int("68000000000000000", 16)
END = int("6ffffffffffffffff", 16)
COUNTER = 100
# Target address
TARGET_ADDRESS = "1BY8GQbnueYofwSuFAT3USAhGjPrkxDdW9"

# Cartella per i file di progresso
CHECKPOINT_FOLDER = "progress_files"
KEY_FOUND_FILE = "found_key.txt"  # File per salvare la chiave trovata

# Dimensione della gamma di ricerca (diviso in 200 parti)
RANGE_SIZE = (END - START) // COUNTER

# Inizializzazione dei range di ogni puntatore
RANGES = [
    (int(START + i * RANGE_SIZE), int(START + (i + 1) * RANGE_SIZE - 1))
    for i in range(COUNTER)  # 200 puntatori
]

# Assicurati che la cartella per i file di progresso esista
os.makedirs(CHECKPOINT_FOLDER, exist_ok=True)

# Funzione per caricare il progresso di un singolo puntatore
def load_progress(pointer_id):
    checkpoint_file = os.path.join(CHECKPOINT_FOLDER, f"{pointer_id}.json")
    if os.path.exists(checkpoint_file):
        with open(checkpoint_file, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                print(f"Warning: Il file di progresso {pointer_id}.json è corrotto. Ripristino impostazioni iniziali.")
                return None
    return None

# Funzione per salvare il progresso di un singolo puntatore
def save_progress(pointer_id, progress):
    checkpoint_file = os.path.join(CHECKPOINT_FOLDER, f"{pointer_id}.json")
    with open(checkpoint_file, 'w') as f:
        json.dump(progress, f)

# Funzione di scansione per ogni puntatore
def scan_range(start, end, pointer_id):
    # Carica il progresso, o inizia dall'inizio della gamma specificata
    progress = load_progress(pointer_id) or start
    attempt_count = 0  # Contatore di tentativi

    total_range = end - start + 1  # Range totale per il calcolo della percentuale

    # Adatta il ciclo per assicurarsi che non si esca dai limiti
    while progress <= end:
        # Genera la chiave privata e l'indirizzo pubblico
        key = Key.from_int(progress)
        address = key.address

        # Controlla se l'indirizzo generato corrisponde all'indirizzo target
        if address == TARGET_ADDRESS:
            found_key = hex(progress)
            print(f"Chiave privata trovata! Chiave: {found_key}")
            # Salva la chiave privata in un file
            with open(KEY_FOUND_FILE, 'w') as key_file:
                key_file.write(f"Found private key: {found_key}\n")
            break

        # Aggiorna la chiave corrente
        progress += 1
        attempt_count += 1

        # Calcola la percentuale
        percentage = (progress - start) / total_range * 100

        # Salva il progresso ogni 10000 tentativi
        if attempt_count % 10000 == 0:
            save_progress(pointer_id, progress)

            # Log del progresso con indirizzo pubblico, range e timestamp
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"Progress: {percentage:.10f}% - "
                  f"PVT: {hex(progress)} - PUB: {address} - "
                  f"Range: {hex(start)} to {hex(end)} - {pointer_id} - "
                  f"Time: {current_time}")

# Avvia la scansione con i puntatori
def main():
    processes = []
    
    for i, (start, end) in enumerate(RANGES):
        pointer_id = f"pointer_{i+1}"
        p = multiprocessing.Process(target=scan_range, args=(start, end, pointer_id))
        processes.append(p)
        p.start()

    # Attendi la fine di tutti i processi
    for p in processes:
        p.join()

if __name__ == "__main__":
    main()
