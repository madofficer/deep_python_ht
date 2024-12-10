import json
import custom_json
from faker import Faker
import timeit

def generate_large_json(num_objects=1000, max_depth=3):
    faker = Faker()
    data = {}

    def generate_object(depth=0):
        if depth >= max_depth:
            return faker.name()
        return {
            faker.word(): generate_object(depth + 1)
            for _ in range(5)
        }

    for _ in range(num_objects):
        data[faker.uuid4()] = generate_object()

    return data


def measure_time(func, *args, iterations=10):
    times = timeit.repeat(lambda: func(*args), number=1, repeat=iterations)
    avg_time = sum(times) / len(times)
    return avg_time




def main():
    json_str = '{"hello": 10, "world": "value"}'

    json_doc = json.loads(json_str)
    cust_json_doc = custom_json.loads(json_str)
    print(json_doc)
    print(json.dumps(json_doc))
    print(cust_json_doc)
    print(custom_json.dumps(custom_json.loads(json_str)))
    print(json_str)

    assert json_doc == cust_json_doc
    assert json_str == custom_json.dumps(custom_json.loads(json_str))

    print("Generating test data...")
    large_json = generate_large_json(num_objects=1000, max_depth=3)
    json_string = json.dumps(large_json)

    print("\nPerformance Test: custom_json.loads")
    custom_loads_time = measure_time(custom_json.loads, json_string)
    print(f"custom_json.loads average time: {custom_loads_time:.4f} seconds")

    print("\nPerformance Test: json.loads")
    json_loads_time = measure_time(json.loads, json_string)
    print(f"json.loads average time: {json_loads_time:.4f} seconds")

    print("\nPerformance Test: custom_json.dumps")
    custom_dumps_time = measure_time(custom_json.dumps, large_json)
    print(f"custom_json.dumps average time: {custom_dumps_time:.4f} seconds")

    print("\nPerformance Test: json.dumps")
    json_dumps_time = measure_time(json.dumps, large_json)
    print(f"json.dumps average time: {json_dumps_time:.4f} seconds")

    print("\nComparison:")
    print(f"custom_json.loads is {custom_loads_time / json_loads_time:.2f}x slower than json.loads")
    print(f"custom_json.dumps is {custom_dumps_time / json_dumps_time:.2f}x slower than json.dumps")


if __name__ == "__main__":
    main()
