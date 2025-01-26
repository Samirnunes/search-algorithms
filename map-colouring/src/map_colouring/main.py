from pso import QuaternaryPSO

if __name__ == "__main__":
    pso = QuaternaryPSO(
        n_particles=20,
        w_max=2,
        w_min=0.8,
        c1=2,
        c2=1.8,
        max_iter=10000
    )
    result = pso.run()
    print(result)