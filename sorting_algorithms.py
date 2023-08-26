
from random import randint
from pprint import pprint
import timeit


class Sort:
    """
    Class containing different sorting algorithms. 
    Should be able to time all of them, and compare.
    """
    timeout: int = 10
    
    disabled_sorting_algorithms = ['bozosort']

    def __init__(self) -> None:
        pass

    def swap(self, unsorted_list: list[int], a: int, b: int) -> None:
        """
        Swaps indexes 'a' and 'b'.
        """
        unsorted_list[a], unsorted_list[b] = unsorted_list[b], unsorted_list[a]
    
    def move(self, unsorted_list: list[int], a: int, b: int) -> None:
        """
        Moves item at index 'a' to index 'b', and moves item at index 'b' one step up.
        """
        item_a = unsorted_list.pop(a)
        unsorted_list.insert(b, item_a)
    
    def time_sorting_algorithm(self, sorting_algorithm, unsorted_list: list[int]) -> tuple[int, list[int]]:
        """
        Times a given sorting algorithm
        """
        start = timeit.default_timer()
        sorted_list = sorting_algorithm(unsorted_list)
        end = timeit.default_timer()
        return end - start, sorted_list
    
    def validate_sorted_list(self, sorted_list) -> bool:
        """
        Validates that list was sorted correctly.
        """
        last_number = sorted_list[0]
        for number in sorted_list[1:]:
            if last_number > number:
                return False
            last_number = number
        return True

    def generate_random_list(self, n: int) -> list[int]:
        return [randint(0, n) for _ in range(n)]

    def compare_sorting_algorithms(self, n: int = 100) -> None:
        unsorted_list: list[int] = self.generate_random_list(n)

        sorting_algorithms: list[str] = [sorting_algorithm for sorting_algorithm in dir(self) if not sorting_algorithm.startswith('__') ]
        # Filter out non-sorting functions
        sorting_algorithms: list[str] = list(filter(lambda x: x.endswith('sort') and x not in self.disabled_sorting_algorithms, sorting_algorithms))

        results: dict[str: float] = {}
        for sorting_algorithm in sorting_algorithms:
            sorting_algorithm_to_run = getattr(self, sorting_algorithm)
            if callable(sorting_algorithm_to_run):  # validate if this is a sorting_algorithm
                sorting_time, sorted_list = self.time_sorting_algorithm(sorting_algorithm_to_run, list(unsorted_list))
                print(f"{sorting_algorithm.capitalize()} with 'n = {n}' took {sorting_time:.3f} seconds.")
                print(f"Validated: {self.validate_sorted_list(sorted_list)}")
                results[sorting_algorithm] = sorting_time
        print()
        pprint(results)

    def bozosort(self, unsorted_list: list[int]) -> list[int]:
        """
        Swaps two items at random, and checks if list is sorted.
        Source: https://en.wikipedia.org/wiki/Bogosort#:~:text=Related-,algorithms,-%5Bedit%5D
        """
        n = len(unsorted_list)
        while not self.validate_sorted_list(unsorted_list):
            a, b = randint(0, n - 1), randint(0, n - 1)
            self.swap(unsorted_list, a, b)
        return unsorted_list
    
    def insertion_sort(self, unsorted_list: list[int]) -> list[int]:
        """
        For each item, it compares with all the items that came before, 
        and inserts the item if it's smaller than any of the items that came before.
        Complexity: O(n^2)
        Source: https://en.wikipedia.org/wiki/Insertion_sort
        """
        for i, num_i in enumerate(unsorted_list[1:], start = 1):
            for j, num_j in enumerate(unsorted_list[:i]):
                if num_i < num_j:
                    self.move(unsorted_list, i, j)
                    break
        return unsorted_list


sorting_session = Sort()
sorting_session.compare_sorting_algorithms(n = 1000)