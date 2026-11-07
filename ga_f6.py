"""AG para maximizar a F6 apresentada em IC_2_1.pdf (páginas 80–88).

Execute: python ga_f6.py --seed 2026
Depende apenas da biblioteca padrão.
"""
import argparse
import json
import math
import random
from pathlib import Path

BITS = 22
LENGTH = 44
MASK = (1 << BITS) - 1
MAX_CHROMOSOME = (1 << LENGTH) - 1

def decode(chromosome):
    """44 bits -> dois inteiros de 22 bits -> reais em [-100, 100]."""
    if not 0 <= chromosome <= MAX_CHROMOSOME:
        raise ValueError("Cromossomo fora do intervalo de 44 bits")
    scale = 200 / MASK
    return -100 + (chromosome >> BITS) * scale, -100 + (chromosome & MASK) * scale

def f6(x, y):
    """Função de maximização: F6(0, 0) = 1."""
    radius_squared = x*x + y*y
    return 0.5 - (math.sin(math.sqrt(radius_squared))**2 - 0.5) / (1 + 0.001*radius_squared)**2

def evaluate(chromosome):
    return f6(*decode(chromosome))

def roulette(population, scores, rng):
    """Seleciona com probabilidade proporcional à avaliação."""
    threshold = rng.random() * sum(scores)
    cumulative = 0.0
    for chromosome, score in zip(population, scores):
        cumulative += score
        if cumulative >= threshold:
            return chromosome
    return population[-1]

def crossover(a, b, rng):
    """Cruzamento de um ponto; ponto entre 1 e 43."""
    point = rng.randrange(1, LENGTH)
    tail = (1 << point) - 1
    return (a & ~tail) | (b & tail), (b & ~tail) | (a & tail)

def mutate(chromosome, rate, rng):
    """Testa e eventualmente inverte cada bit."""
    for bit in range(LENGTH):
        if rng.random() < rate:
            chromosome ^= 1 << bit
    return chromosome

def run(population_size=100, generations=40, crossover_rate=0.65,
        mutation_rate=0.008, seed=2026):
    if population_size < 2 or generations < 1:
        raise ValueError("População >= 2 e gerações >= 1 são obrigatórias")
    if not 0 <= crossover_rate <= 1 or not 0 <= mutation_rate <= 1:
        raise ValueError("As taxas devem estar entre 0 e 1")
    rng = random.Random(seed)
    population = [rng.getrandbits(LENGTH) for _ in range(population_size)]
    history = []
    best_chromosome = None
    best_score = -math.inf
    for generation in range(generations):
        scores = [evaluate(chromosome) for chromosome in population]
        best_index = max(range(population_size), key=scores.__getitem__)
        if scores[best_index] > best_score:
            best_chromosome = population[best_index]
            best_score = scores[best_index]
        history.append({"generation": generation,
                        "best": scores[best_index],
                        "mean": sum(scores)/population_size,
                        "best_ever": best_score})
        if generation == generations - 1:
            break
        # Guarda um exemplar do melhor; os demais vêm de seleção e reprodução.
        children = [population[best_index]]
        while len(children) < population_size:
            a = roulette(population, scores, rng)
            b = roulette(population, scores, rng)
            if rng.random() < crossover_rate:
                a, b = crossover(a, b, rng)
            children.append(mutate(a, mutation_rate, rng))
            if len(children) < population_size:
                children.append(mutate(b, mutation_rate, rng))
        population = children
    x, y = decode(best_chromosome)
    return {
        "source": "IC_2_1.pdf, páginas 80–88",
        "parameters": {"population_size": population_size, "generations": generations,
                       "crossover_rate": crossover_rate, "mutation_rate": mutation_rate,
                       "seed": seed},
        "evaluations": population_size * generations,
        "best": {"chromosome": f"{best_chromosome:044b}", "x": x, "y": y,
                 "f6": best_score, "gap_to_optimum": 1-best_score},
        "history": history
    }

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=2026)
    parser.add_argument("--population-size", type=int, default=100)
    parser.add_argument("--generations", type=int, default=40)
    parser.add_argument("--crossover-rate", type=float, default=0.65)
    parser.add_argument("--mutation-rate", type=float, default=0.008)
    parser.add_argument("--output", type=Path, default=Path("resultado_execucao.json"))
    args = parser.parse_args()
    result = run(args.population_size, args.generations, args.crossover_rate,
                 args.mutation_rate, args.seed)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")
    best = result["best"]
    print(f"Semente: {args.seed}; avaliações: {result['evaluations']}")
    print(f"x={best['x']:.8f}; y={best['y']:.8f}; F6={best['f6']:.8f}")
    print(f"Distância em aptidão até 1: {best['gap_to_optimum']:.8f}")
    print(f"Histórico: {args.output}")

if __name__ == "__main__":
    main()

