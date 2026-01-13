# validator.py
import os

def validate_file_content(path):
    """
    Rygorystyczna walidacja struktury pliku PFSP-SDST.
    Sprawdza wymiary macierzy proc_time (n x m) oraz setup_time (n x n dla każdej maszyny).
    """
    if not os.path.isfile(path): 
        return False, "Błąd: Podana ścieżka nie jest plikiem.", 0, 0
        
    try:
        n, m = 0, 0
        lines = []
        with open(path, 'r') as f:
            lines = [line.strip() for line in f.readlines()]

        # 1. Szukanie n (jobs) i m (machines)
        for line in lines:
            if line.startswith('jobs'):
                if '=' not in line: return False, "Błąd formatu: Brak '=' w definicji 'jobs'.", 0, 0
                n = int(line.split('=')[1].strip())
            elif line.startswith('machines'):
                if '=' not in line: return False, "Błąd formatu: Brak '=' w definicji 'machines'.", 0, 0
                m = int(line.split('=')[1].strip())
        
        if n <= 0 or m <= 0:
            return False, "Błąd: Liczba zadań i maszyn musi być większa niż 0.", 0, 0

        # Zmienne pomocnicze do śledzenia sekcji
        current_section = None
        proc_time_rows = 0
        setup_matrices = {i: 0 for i in range(1, m + 1)}
        current_machine = None

        for line in lines:
            if not line or line.startswith('#') and not line.startswith('# machine'):
                continue
            
            # Detekcja startu sekcji
            if line.startswith('proc_time'):
                current_section = 'proc_time'
                continue
            elif line.startswith('setup_time'):
                current_section = 'setup_time'
                continue
            elif line.startswith('# machine'):
                try:
                    current_machine = int(line.replace('# machine', '').strip())
                    current_section = 'machine_data'
                    continue
                except:
                    return False, f"Błąd formatu: Niepoprawny numer maszyny w '{line}'.", 0, 0

            # Walidacja danych w sekcjach
            values = line.split()
            if not values: continue

            if current_section == 'proc_time':
                if len(values) != m:
                    return False, f"Błąd w proc_time: Wiersz {proc_time_rows + 1} ma {len(values)} kolumn, a powinien mieć {m}.", 0, 0
                proc_time_rows += 1
            
            elif current_section == 'machine_data':
                if current_machine not in setup_matrices:
                    return False, f"Błąd: Znaleziono dane dla maszyny {current_machine}, która nie została zadeklarowana.", 0, 0
                if len(values) != n:
                    return False, f"Błąd w macierzy maszyny {current_machine}: Wiersz {setup_matrices[current_machine] + 1} ma {len(values)} kolumn, a powinien mieć {n}.", 0, 0
                setup_matrices[current_machine] += 1

        # 2. Weryfikacja końcowa kompletności danych
        if proc_time_rows != n:
            return False, f"Błąd: Sekcja proc_time zawiera {proc_time_rows} wierszy, a powinna zawierać {n}.", 0, 0

        for m_id, rows in setup_matrices.items():
            if rows == 0:
                return False, f"Błąd: Macierz przezbrojeń dla maszyny {m_id} jest pusta.", 0, 0
            if rows != n:
                return False, f"Błąd: Macierz maszyny {m_id} zawiera {rows} wierszy, a powinna zawierać {n}.", 0, 0

        return True, "", n, m

    except Exception as e:
        return False, f"Błąd krytyczny podczas odczytu: {str(e)}", 0, 0