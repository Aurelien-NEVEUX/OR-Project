def bellman_ford(capacity, cost, source):
    n = len(capacity)
    dist = [float('inf')] * n
    dist[source] = 0

    print(f"Step 0 : {['∞' if d == float('inf') else d for d in dist]}")
    
    # Iterations Bellman-Ford
    for k in range(n - 1):
        updated = False
        new_dist = dist.copy()
        for u in range(n):
            for v in range(n):
                if capacity[u][v] > 0 and dist[u] + cost[u][v] < new_dist[v]:
                    new_dist[v] = dist[u] + cost[u][v]
                    updated = True
        dist = new_dist
        affichage = ['∞' if d == float('inf') else d for d in dist]
        print(f"Step {k+1} : {affichage}")
        if not updated:
            break

    # Detection nagatif cycle
    for u in range(n):
        for v in range(n):
            if capacity[u][v] > 0 and dist[u] + cost[u][v] < dist[v]:
                print("⚠️ Negatif cycle detected.")
                return None

    return dist

min_cost_flow(capacity_matrix, cost_matrix, s, t, flow_val)

def min_cost_flow(n: int,
                  C: List[List[int]],
                  D: List[List[int]],
                  s: int,
                  t: int,
                  F: int) -> Tuple[int, int]:
    R = [r[:] for r in C]
    cost_res = [[0]*n for _ in range(n)]
    for u in range(n):
        for v in range(n):
            if C[u][v] > 0:
                cost_res[u][v] = D[u][v]
                cost_res[v][u] = -D[u][v]

    flow = 0
    cost = 0
    remain = F
    iteration = 1
    while flow < F:
        print(f"⋆ Min-cost iteration {iteration}: remaining flow = {remain}")
        pred = bellman_ford_trace(n, cost_res, R, s)
        if pred is None:
            print("No augmenting path found; desired flow not reachable.")
            break

        # reconstruct path
        path = [t]
        while path[-1] != s:
            path.append(pred[path[-1]])
        path.reverse()

        delta = min(R[u][v] for u, v in zip(path, path[1:]))
        delta = min(delta, remain)
        inc_cost = sum(D[u][v] for u, v in zip(path, path[1:])) * delta

        print(f"Augmenting along path {''.join(label(v) for v in path)} with flow {delta}\n")
        for u, v in zip(path, path[1:]):
            R[u][v] -= delta
            R[v][u] += delta

        print("Modifications to the residual graph :blush:
        display_labeled_matrix(R)
        print()

        flow += delta
        cost += inc_cost
        remain -= delta
        iteration += 1

    return flow, cost
