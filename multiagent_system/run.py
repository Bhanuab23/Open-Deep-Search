from graph import build_graph

def main():
    print("=== Multi-Agent Research System ===\n")

    topic = input("Enter research topic: ")

    graph = build_graph()

    initial_state = {
        "topic": topic
    }

    result = graph.invoke(initial_state)

    print("\n=== Final Research Summary ===\n")
    print(result["final_summary"])


if __name__ == "__main__":
    main()
