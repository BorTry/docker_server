import docker

CLIENT = docker.from_env()

def get_cpu_percentage(stats):
    print(stats["cpu_stats"])
    # Calculate deltas between current and previous stats
    cpu_delta = stats["cpu_stats"]["cpu_usage"]["total_usage"] - \
                stats["precpu_stats"]["cpu_usage"]["total_usage"]
    system_delta = stats["cpu_stats"]["system_cpu_usage"] - \
                   stats["precpu_stats"]["system_cpu_usage"]
    
    # Get number of CPU cores to normalize percentage (for values > 100%)
    online_cpus = stats["cpu_stats"].get("online_cpus", 
                   len(stats["cpu_stats"]["cpu_usage"].get("percpu_usage", [])))
    
    if system_delta > 0.0 and cpu_delta > 0.0:
        return (cpu_delta / system_delta) * online_cpus * 100.0
    return 0.0


container = CLIENT.containers.get("docker_server-minecraft-1")
stats = container.stats(stream=False)

print(f"CPU Usage: {get_cpu_percentage(stats):.2f}%")