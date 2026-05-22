# roommate_finder.py

DATA_FILE = "students.txt"

AREAS = [
    "Gachibowli", "Hitech City", "Madhapur", "Kondapur", "Kukatpally",
    "Ameerpet", "Begumpet", "Banjara Hills", "Jubilee Hills", "Secunderabad",
    "Dilsukhnagar", "LB Nagar", "Kompally", "Miyapur", "Nallagandla"
]

id_counter = [1]  # using a list so it can be modified inside functions


def generate_id():
    new_id = "STU" + str(id_counter[0]).zfill(3)
    id_counter[0] += 1
    return new_id


def save_students(students):
    """Save students to a plain text file, one field per line per student."""
    file = open(DATA_FILE, "w")

    for s in students:
        file.write(s["id"] + "\n")
        file.write(s["name"] + "\n")
        file.write(s["college"] + "\n")
        file.write(s["year"] + "\n")
        file.write(s["area"] + "\n")
        file.write(str(s["budget"]) + "\n")
        file.write(s["gender"] + "\n")
        file.write(s["bio"] + "\n")
        file.write(s["contact"] + "\n")
        file.write(s["status"] + "\n")
        file.write("---\n")  # separator between students

    file.close()
    print("  Data saved to '" + DATA_FILE + "'")


def load_students():
    """Load students from plain text file. Returns list of dicts."""
    students = []

    try:
        file = open(DATA_FILE, "r")
    except FileNotFoundError:
        return students

    lines = file.read().splitlines()
    file.close()

    i = 0

    while i < len(lines):

        if lines[i] == "---":
            i += 1
            continue

        if i + 9 < len(lines):
            student = {
                "id": lines[i],
                "name": lines[i + 1],
                "college": lines[i + 2],
                "year": lines[i + 3],
                "area": lines[i + 4],
                "budget": int(lines[i + 5]),
                "gender": lines[i + 6],
                "bio": lines[i + 7],
                "contact": lines[i + 8],
                "status": lines[i + 9],
            }

            students.append(student)
            i += 11

        else:
            break

    return students


def add_student(students):

    print("\n── Register New Student ──────────────────")

    name = input("  Full Name       : ").strip()
    college = input("  College/Univ    : ").strip()

    years = ["1st Year", "2nd Year", "3rd Year", "4th Year", "PG/Masters"]

    print("  College Year:")

    for i in range(len(years)):
        print("    " + str(i + 1) + ". " + years[i])

    while True:
        choice = input("  Choose (1-5): ").strip()

        if choice in ["1", "2", "3", "4", "5"]:
            year = years[int(choice) - 1]
            break

        print("  Invalid. Try again.")

    print("  Preferred Area (Hyderabad):")

    for i in range(len(AREAS)):
        print("    " + str(i + 1) + ". " + AREAS[i])

    while True:
        a_choice = input("  Choose (1-" + str(len(AREAS)) + "): ").strip()

        if a_choice.isdigit() and 1 <= int(a_choice) <= len(AREAS):
            area = AREAS[int(a_choice) - 1]
            break

        print("  Invalid. Try again.")

    while True:

        budget_input = input("  Monthly Budget  : ").strip()

        is_valid = True

        for ch in budget_input:
            if ch not in "0123456789":
                is_valid = False
                break

        if is_valid and len(budget_input) > 0 and int(budget_input) > 0:
            budget = int(budget_input)
            break

        print("  Enter a valid positive number.")

    genders = ["Male", "Female", "Other"]

    print("  Gender: 1.Male  2.Female  3.Other")

    while True:
        g = input("  Choose (1-3): ").strip()

        if g in ["1", "2", "3"]:
            gender = genders[int(g) - 1]
            break

        print("  Invalid. Try again.")

    bio = input("  Short Bio       : ").strip()
    contact = input("  Contact Email   : ").strip()

    student = {
        "id": generate_id(),
        "name": name,
        "college": college,
        "year": year,
        "area": area,
        "budget": budget,
        "gender": gender,
        "bio": bio,
        "contact": contact,
        "status": "looking",
    }

    students.append(student)

    print("\n  " + name + " added! ID: " + student["id"])

    return students


def display_students(students):

    if len(students) == 0:
        print("\n  No students found.\n")
        return

    print("\n  " + "-" * 62)

    print("  {:<20} {:<14} {:>8}  {:<12} {}".format(
        "NAME", "AREA", "BUDGET", "YEAR", "STATUS"
    ))

    print("  " + "-" * 62)

    for s in students:

        icon = ">> Looking" if s["status"] == "looking" else "** Found"

        print("  {:<20} {:<14} Rs{:>6}  {:<12} {}".format(
            s["name"],
            s["area"],
            s["budget"],
            s["year"],
            icon
        ))

    print("  " + "-" * 62)
    print("  Total: " + str(len(students)) + " student(s)\n")


def filter_students(students, filters):

    result = []

    for s in students:

        if "budget_min" in filters and s["budget"] < filters["budget_min"]:
            continue

        if "budget_max" in filters and s["budget"] > filters["budget_max"]:
            continue

        if "area" in filters and filters["area"].lower() not in s["area"].lower():
            continue

        if "gender" in filters and s["gender"] != filters["gender"]:
            continue

        if "year" in filters and s["year"] != filters["year"]:
            continue

        if "status" in filters and s["status"] != filters["status"]:
            continue

        result.append(s)

    return result


def get_recommendations(students, profile):

    scored = []

    for s in students:

        if s["id"] == profile["id"] or s["status"] != "looking":
            continue

        score = 0

        diff = s["budget"] - profile["budget"]

        if diff < 0:
            diff = -diff

        if diff <= 2000:
            score += 30

        if s["area"].lower() == profile["area"].lower():
            score += 25

        if s["gender"] == profile["gender"]:
            score += 20

        if s["year"] == profile["year"]:
            score += 15

        if s["college"] == profile["college"]:
            score += 10

        scored.append([score, s])

    for i in range(len(scored)):
        for j in range(i + 1, len(scored)):

            if scored[j][0] > scored[i][0]:
                scored[i], scored[j] = scored[j], scored[i]

    return scored[:5]


def update_status(students, student_id, new_status):

    for s in students:

        if s["id"] == student_id:
            s["status"] = new_status
            print("  " + s["name"] + " status updated to '" + new_status + "'")
            return students

    print("  No student found with ID '" + student_id + "'")

    return students


def browse_with_filters(students):

    print("\n── Filter Students ───────────────────────")
    print("  (Press Enter to skip any filter)")

    filters = {}

    print("  Area (Hyderabad):")

    for i in range(len(AREAS)):
        print("    " + str(i + 1) + ". " + AREAS[i])

    print("    (Press Enter to skip)")

    a = input("  Choose: ").strip()

    if a.isdigit() and 1 <= int(a) <= len(AREAS):
        filters["area"] = AREAS[int(a) - 1]

    print("  Gender: 1.Male  2.Female  3.Other  [Enter=any]")

    g = input("  Choose: ").strip()

    if g == "1":
        filters["gender"] = "Male"

    elif g == "2":
        filters["gender"] = "Female"

    elif g == "3":
        filters["gender"] = "Other"

    years = ["1st Year", "2nd Year", "3rd Year", "4th Year", "PG/Masters"]

    print("  Year:")

    for i in range(len(years)):
        print("    " + str(i + 1) + ". " + years[i])

    y = input("  Choose (or Enter): ").strip()

    if y in ["1", "2", "3", "4", "5"]:
        filters["year"] = years[int(y) - 1]

    bmin = input("  Min Budget (Rs) : ").strip()
    bmax = input("  Max Budget (Rs) : ").strip()

    if bmin != "":
        try:
            filters["budget_min"] = int(bmin)
        except:
            pass

    if bmax != "":
        try:
            filters["budget_max"] = int(bmax)
        except:
            pass

    print("  Status: 1.Looking  2.Found  [Enter=all]")

    st = input("  Choose: ").strip()

    if st == "1":
        filters["status"] = "looking"

    elif st == "2":
        filters["status"] = "found"

    results = filter_students(students, filters)

    print("\n  Results (" + str(len(results)) + " match(es)):")

    display_students(results)


def main():

    print("\n" + "=" * 50)
    print("  RoomieFind  –  Student PG Finder")
    print("=" * 50)

    students = load_students()

    print("  Loaded " + str(len(students)) + " student record(s).\n")

    while True:

        print("  MENU")
        print("  1. Browse all students")
        print("  2. Search / Filter")
        print("  3. Register (add yourself)")
        print("  4. Get recommendations")
        print("  5. Update roommate-found status")
        print("  6. Save & Exit")
        print()

        choice = input("  Your choice: ").strip()

        if choice == "1":

            display_students(students)

        elif choice == "2":

            browse_with_filters(students)

        elif choice == "3":

            students = add_student(students)
            save_students(students)

        elif choice == "4":

            if len(students) == 0:
                print("\n  No students registered yet.\n")
                continue

            print("\n  Student list:")

            for s in students:
                print("  [" + s["id"] + "] " + s["name"])

            sid = input("  Enter ID: ").strip()

            profile = None

            for s in students:

                if s["id"] == sid:
                    profile = s
                    break

            if profile is None:
                print("  ID not found.\n")
                continue

            recs = get_recommendations(students, profile)

            if len(recs) == 0:

                print("\n  No matches found for " + profile["name"] + ".\n")

            else:

                print("\n  Top matches for " + profile["name"] + ":")

                for score, s in recs:

                    bar = "#" * (score // 10) + "." * (10 - score // 10)

                    print("\n  [" + bar + "] " + str(score) + "% match")

                    print("  Name   : " + s["name"] + "  (" + s["college"] + ")")
                    print("  Area   : " + s["area"] + "  Budget: Rs." + str(s["budget"]) + "/mo")
                    print("  Year   : " + s["year"] + "  Gender: " + s["gender"])
                    print("  Contact: " + s["contact"])

                print()

        elif choice == "5":

            if len(students) == 0:
                print("\n  No students registered yet.\n")
                continue

            for s in students:

                icon = ">> looking" if s["status"] == "looking" else "** found"

                print("  [" + s["id"] + "] " + s["name"] + " -- " + icon)

            sid = input("\n  Enter student ID: ").strip()

            print("  New status: 1.Looking  2.Found")

            ns = input("  Choose: ").strip()

            if ns == "1":
                students = update_status(students, sid, "looking")

            elif ns == "2":
                students = update_status(students, sid, "found")

            else:
                print("  Invalid choice.")

            save_students(students)

        elif choice == "6":

            save_students(students)

            print("\n  Goodbye! Good luck finding your roommate!\n")

            break

        else:
            print("  Invalid option. Choose 1-6.\n")


main()
