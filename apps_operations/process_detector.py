import psutil


def get_running_processes():

    processes = []

    for process in psutil.process_iter(
        ["pid", "name", "exe"]
    ):

        try:

            info = process.info

            processes.append({
                "pid": info["pid"],
                "name": info["name"],
                "exe": info["exe"]
            })

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess
        ):
            continue

    return processes


def find_application_processes(app):

    target = app.get(
        "target",
        ""
    ).strip().lower()

    if not target:
        return []

    running_processes = get_running_processes()

    matches = []

    for process in running_processes:

        process_exe = process.get("exe")

        if not process_exe:
            continue

        if process_exe.strip().lower() == target:

            matches.append(process)

    return matches

if __name__ == "__main__":

    from apps_operations.app_database import ApplicationDatabase

    database = ApplicationDatabase()

    app = database.find("Visual Studio Code")

    if not app:

        print("Application not found")

    else:

        processes = find_application_processes(app)

        if not processes:

            print(
                f"{app['name']} is not running."
            )

        else:

            print(
                f"{app['name']} is running."
            )

            print(
                f"Processes found: {len(processes)}"
            )

            for process in processes:

                print(
                    f"PID: {process['pid']} | "
                    f"Name: {process['name']}"
                )