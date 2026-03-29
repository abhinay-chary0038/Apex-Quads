import random

class Module:
    def __init__(self, name, hours, dependencies):
        self.name = name
        self.hours = hours
        self.dependencies = dependencies

class LearningPlan:
    def __init__(self, modules):
        self.modules = modules


class ExecutionEngine:
    def __init__(self, plan, time_pressure, motivation_sensitivity, market_volatility):
        self.plan = plan
        self.time_pressure = time_pressure
        self.motivation_sensitivity = motivation_sensitivity
        self.market_volatility = market_volatility

    def simulate_once(self):
        completed = []
        failed = []
        available_time = 100 * (1 - self.time_pressure)
        motivation = 1.0

        for m in self.plan.modules:
            if any(dep not in completed for dep in m.dependencies):
                failed.append(m.name)
                continue

            motivation -= random.random() * self.motivation_sensitivity
            effort = m.hours * (1 + random.random() * self.market_volatility)

            if motivation <= 0 or available_time < effort:
                failed.append(m.name)
            else:
                completed.append(m.name)
                available_time -= effort

        return completed, failed


if __name__ == "__main__":
    n = int(input("Enter number of modules: "))
    modules = []

    for _ in range(n):
        name = input("Module name: ")
        hours = int(input("Hours required: "))
        deps = input("Dependencies (comma separated or none): ")

        if deps.lower() == "none" or deps.strip() == "":
            deps_list = []
        else:
            deps_list = [d.strip() for d in deps.split(",")]

        modules.append(Module(name, hours, deps_list))

    plan = LearningPlan(modules)

    time_pressure = float(input("Time pressure (0-1): "))
    motivation = float(input("Motivation sensitivity (0-1): "))
    market = float(input("Market volatility (0-1): "))

    engine = ExecutionEngine(plan, time_pressure, motivation, market)

    runs = 50
    all_failures = {}
    total_completed = 0

    print("\n--- Simulation Runs ---")
    for i in range(runs):
        completed, failed = engine.simulate_once()
        print(f"Run {i+1}: Completed={completed}, Failed={failed}")

        total_completed += len(completed)
        for f in failed:
            all_failures[f] = all_failures.get(f, 0) + 1

    print("\n--- Final Report ---")
    print("Total Runs:", runs)
    print("Average Modules Completed:", total_completed / runs)
    print("Failure Frequency:", all_failures)

    sorted_failures = sorted(all_failures.items(), key=lambda x: -x[1])
    print("Top Failure Points:", sorted_failures[:3])

    print("\nRecommendations:")
    for f, _ in sorted_failures[:3]:
        print(f"- Improve planning or reduce load for module: {f}")

    print("\nSystem Stress Summary:")
    print("Time Pressure:", time_pressure)
    print("Motivation Sensitivity:", motivation)
    print("Market Volatility:", market)