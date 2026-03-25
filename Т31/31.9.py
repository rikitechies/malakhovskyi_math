import threading
import time
import random
import math

class Spectator:
    def __init__(self, spec_id, arrival_time):
        self.id = spec_id
        self.arrival_time = arrival_time
        self.entry_time = 0

class Stadium:
    def __init__(self, n, m, t_open_hours, t1_seconds):
        self.n = n
        self.m = m
        self.t_open = t_open_hours * 3600
        self.t1 = t1_seconds
        self.spectators = []
        self.results = []
        self.lock = threading.Lock()
        
    def _generate_spectators(self):
        for i in range(self.n):
            arrival = random.uniform(-self.t_open, 0)
            self.spectators.append(Spectator(i, arrival))
        self.spectators.sort(key=lambda x: x.arrival_time)

    def turnstile(self, turnstile_id):
        while True:
            with self.lock:
                if not self.spectators:
                    break
                spectator = self.spectators.pop(0)

            wait_until = spectator.arrival_time + self.t_open
            current_sim_time = (time.time() - self.real_start) * 1000 
            
            if wait_until > current_sim_time:
                time.sleep((wait_until - current_sim_time) / 1000)
            
            process_time = random.uniform(1, self.t1)
            time.sleep(process_time / 1000)
            
            self.results.append((time.time() - self.real_start) * 1000 - self.t_open)

    def run_simulation(self):
        self._generate_spectators()
        self.real_start = time.time()
        
        threads = []
        for i in range(self.m):
            t = threading.Thread(target=self.turnstile, args=(i,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        delays = sorted(self.results)
        idx = math.ceil(0.9 * len(delays)) - 1
        return abs(delays[idx])

if __name__ == "__main__":
    print("Введіть параметри моделювання:")
    
    n_val = int(input("Кількість глядачів (N): "))
    m_val = int(input("Кількість турнікетів (m): "))
    t_val = float(input("За скільки годин відкривають турнікети (год): "))
    t1_val = float(input("Макс. час проходу однієї людини (сек): "))

    print("\nВиконується розрахунок...")
    
    model = Stadium(n_val, m_val, t_val, t1_val)
    total_seconds = model.run_simulation()

    total_minutes = math.ceil(total_seconds / 60)
    hours = total_minutes // 60
    minutes = total_minutes % 60

    print("-" * 50)
    print("РЕЗУЛЬТАТ:")
    print(f"Щоб пройти на стадіон з імовірністю 0.9,")
    print(f"треба прийти за: {hours} год. {minutes} хв. до початку матчу.")
    print("-" * 50)
    
    input("Натисніть ENTER для виходу.")