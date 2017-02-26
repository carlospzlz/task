"""
Test module for the given task.
"""
from collections import deque
import unittest

import task


class Test_Solution(unittest.TestCase):
    """
    Class that encapsulates all the test cases.
    """

    def test_find_shortest_transformations_length_example(self):
        """
        Test case for the example attached to the task.

        Graph:
                                 log
                               /
        ^hit - hot - dot - dog
                               \
                                 *cog

        """
        my_solution = task.Solution()
        start = "hit"
        end = "cog"
        words = ["hit", "dot", "dog", "cog", "hot", "log"]
        result = my_solution.find_shortest_transformations_length(
            start, end, words)
        expected = 4
        self.assertEqual(result, expected)

    def test_find_shortest_transformations_length_general_case(self):
        """
        Test case for a more complex scenario.

        Graph:
                    ------- dot -------
                   /       /           \
        ^hit - hot ---- pot -- poc ---- *doc
                   \       \   /
                     hop -- pop

        """
        my_solution = task.Solution()
        start = "hit"
        end = "doc"
        words = ["hit", "hot", "hop", "pot", "dot", "pop", "poc", "doc"]
        result = my_solution.find_shortest_transformations_length(
            start, end, words)
        expected = 3
        self.assertEqual(result, expected)

    def test_find_shortest_transformations_length_start_is_end(self):
        """
        Test case where the start is the end.

        Graph:
                                 log
                                /
        ^*hit - hot - dot - dog
                                \
                                 cog

        """
        my_solution = task.Solution()
        start = "hit"
        end = "hit"
        words = ["hit", "dot", "dog", "cog", "hot", "log"]
        result = my_solution.find_shortest_transformations_length(
            start, end, words)
        expected = 0
        self.assertEqual(result, expected)

    def test_find_shortest_transformations_length_end_is_unreachable(self):
        """
        Test case for when there is not a transformation sequence from the
        start to the end.

        Graph:
                                 log
                               /
        ^hit - hot         dog
                               \
                                 *cog

        """
        my_solution = task.Solution()
        start = "hit"
        end = "cog"
        words = ["hit", "dog", "cog", "hot", "log"]
        result = my_solution.find_shortest_transformations_length(
            start, end, words)
        expected = -1
        self.assertEqual(result, expected)

    def test__group_neighbours_example(self):
        """
        Test that the group of the neighbours work correctly for the example
        case.
        """
        my_solution = task.Solution()
        words = ["hit", "dot", "dog", "cog", "hot", "log"]
        expected = {
            "?it" : ["hit"],
            "h?t" : ["hit", "hot"],
            "hi?" : ["hit"],
            "?ot" : ["dot", "hot"],
            "d?t" : ["dot"],
            "do?" : ["dot", "dog"],
            "?og" : ["dog", "cog", "log"],
            "d?g" : ["dog"],
            "c?g" : ["cog"],
            "co?" : ["cog"],
            "ho?" : ["hot"],
            "l?g" : ["log"],
            "lo?" : ["log"]
        }
        result = my_solution._group_neighbours(words)
        self.assertEqual(result, expected)

    def test__visit_word_neighbours_end_not_found(self):
        """
        Test that the neighbours of a word are visited correclty when the end is
        not found yet.

                 cop
               /
           cup - mug
               \
                 sup
        """
        my_solution = task.Solution()
        word = "cup"
        end = "foo"
        neighbours = {
            "?up" : ["cup", "sup"],
            "c?p" : ["cup", "cop"],
            "cu?" : ["cup", "mug"]
        }
        queue = deque()
        visited = {"cup"}
        number_of_transformations = 0

        result = my_solution._visit_word_neighbours(
            word, end, neighbours, queue, visited, number_of_transformations)

        expected_result = -1
        expected_queue_list = [("cop", 1), ("mug", 1), ("sup", 1)]
        expected_visited = {"cup", "cop", "mug", "sup"}
        self.assertEqual(result, expected_result)
        self.assertEqual(sorted(list(queue)), expected_queue_list)
        self.assertEqual(visited, expected_visited)

    def test__visit_word_neighbours_end_found(self):
        """
        Test that when the end word is among the neighbours the number of
        transformations is returned correctly.

                 cop
               /
           cup - mug
               \
                 *sup
        """
        my_solution = task.Solution()
        word = "cup"
        end = "cop"
        neighbours = {
            "?up" : ["cup", "sup"],
            "c?p" : ["cup", "cop"],
            "cu?" : ["cup", "mug"]
        }
        queue = deque()
        visited = {"cup"}
        number_of_transformations = 0

        result = my_solution._visit_word_neighbours(
            word, end, neighbours, queue, visited, number_of_transformations)

        expected_result = 1
        self.assertEqual(result, expected_result)

    def test__visit_neighbour_end_not_found(self):
        """
        Test that when we visit a neighbour and it is not end the result is -1
        and the auxiliar data structures (queue, visited) are updated
        correctly.

            foo    *spam

        """
        my_solution = task.Solution()
        neighbour = "foo"
        end = "spam"
        queue = deque()
        visited = set()
        number_of_transformations = 0

        result = my_solution._visit_neighbour(
          neighbour, end, queue, visited, number_of_transformations)

        expected_result = -1
        expected_queue = deque([("foo", 1)])
        expected_visited = {"foo"}
        self.assertEqual(result, expected_result)
        self.assertEqual(queue, expected_queue)
        self.assertEqual(visited, expected_visited)

    def test__visit_neighbour_end_found(self):
        """
        Test that when we visit a neighbour and it is the end the result is the
        number of transformation to get to that neighbour.

            *spam

        """
        my_solution = task.Solution()
        neighbour = "spam"
        end = "spam"
        queue = deque()
        visited = set()
        number_of_transformations = 0

        result = my_solution._visit_neighbour(
          neighbour, end, queue, visited, number_of_transformations)

        expected_result = 1
        self.assertEqual(result, expected_result)

    def test__get_pattern_general_case(self):
        """
        Test that the pattern for a word and for a certain letter index is
        built and returned correctly.
        """
        my_solution = task.Solution()
        word = "spam"
        letter_index = 2
        result = my_solution._get_pattern(word, letter_index)
        expected = "sp?m"
        self.assertEqual(result, expected)

    def test__get_pattern_first_index(self):
        """
        Test that the pattern for a word and for the first letter index is
        built and returned correctly.
        """
        my_solution = task.Solution()
        word = "spam"
        letter_index = 0
        result = my_solution._get_pattern(word, letter_index)
        expected = "?pam"
        self.assertEqual(result, expected)

    def test__get_pattern_last_index(self):
        """
        Test that the pattern for a word and for the last letter index is built
        and returned correctly.
        """
        my_solution = task.Solution()
        word = "spam"
        letter_index = 3
        result = my_solution._get_pattern(word, letter_index)
        expected = "spa?"
        self.assertEqual(result, expected)
