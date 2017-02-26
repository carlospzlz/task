"""
Module task that contains the solution of the task.
"""
from collections import deque


class Solution(object):
    """
    Class that encapsulates all the functionality needed to solve the given
    task.
    """

    def find_shortest_transformations_length(self, start, end, words):
        """
        Args:
            start (str): Starting word of the transformation sequence.
            end (str): Ending word of the transformation sequence.
            words (List[str]): Valid words to use to make a transformation.

        Returns:
           int. Length of the shortest transformation sequence from start to
                end.

        This is the core method that contains the main logic to solve the
        problem. We interpret words as a graph, and perform a
        Breadth-First-Search from start to end using a queue.

        In order to optimize the algorithm, we do a pre-computation grouping
        the neighbours. See '_group_neighbours'

        The runtime complexity of this algorithm is bounded by:

                    O(n * l) + O(v + e)

        n: number of words
        l: number of letters
        v: vertex of the graph (words)
        e: edges of the graph (neighbourhoods)

        Assumptions made:
            - Start and end are valid words.
            - No duplicates in the word list.
            - Return -1 if there is not a valid transformation sequence.
        """
        if start == end:
            return 0

        neighbours = self._group_neighbours(words)
        queue = deque([(start, 0)])
        visited = set([start])
        shortest_transformations_length = -1
        while shortest_transformations_length == -1 and queue:
            word, number_of_transformations = queue.popleft()
            shortest_transformations_length = self._visit_word_neighbours(
               word, end, neighbours, queue, visited,
               number_of_transformations)
        return shortest_transformations_length

    def _group_neighbours(self, words):
        """
        Args:
            words (List[str]): All the valid words.

        Returns:
            Dict{str, List[str]}. The words grouped by pattern.

        In order to avoid checking every single word to find the neighbours of
        a certain word (which would give us O(n^2)), we perfom this neighbours
        grouping.

        We build a pattern where one of the letters can be any, and we group
        all the words that satify that pattern:

        neighbours = {
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

        This way, the neighbours of a certain word would be the lists indexed
        by the patterns that that word satisfies:

        Neighbours of 'dog':

            "?og" : ["dog", "cog", "log"]
            "d?g" : ["dog"]
            "do?" : ["dot", "dog"]

        Being n the number of words and l the number of letters, this
        pre-computation has a cost of O(n * l)
        """
        neighbours = {}
        for word in words:
            for letter_index in range(len(word)):
                pattern = self._get_pattern(word, letter_index)
                neighbours[pattern] = neighbours.get(pattern, []) + [word]
        return neighbours

    def _visit_word_neighbours(
            self, word, end, neighbours, queue, visited,
            number_of_transformations):
        """
        Args:
            word (str): Word to visit the neighbours for.
            end (str): Ending word of the transformation sequence.
            neighours (Dict{str, List[str]}: Neighbours indexed by pattern.
            queue (Deque[(str, int)]): Auxiliar queue for the BFS.
            visited (Set{str}): Already visited words.
            number_of_transformations (int): Number of transformations needed
                to reach the previous word.
 
        Returns:
            int. Number of transformation needed to reach the end. -1 if not
                 reached yet.

        With the help of the neighbours dictionary we iterate over all the
        neighbours that satisfy the word's pattern and visit them.
        """
        for letter_index in range(len(word)):
            pattern = self._get_pattern(word, letter_index)
            for neighbour in neighbours[pattern]:
                shortest_transformations_length = self._visit_neighbour(
                    neighbour, end, queue, visited, number_of_transformations)
                if shortest_transformations_length != -1:
                    return shortest_transformations_length
        return -1

    def _visit_neighbour(
            self, neighbour, end, queue, visited, number_of_transformations):
        """
        Args:
            neighbour (str): Neighbour to visit.
            end (str): Ending word of the transformation sequence.
            queue (Deque[(str, int)]): Auxiliar queue for the BFS.
            visited (Set{str}): Already visited words.
            number_of_transformations (int): Number of transformations needed
                to reach the previous word.

        Returns:
            int. Number of transformation needed to reach the end. -1 if not
                 reached yet.

        We visit the neighbour and check if it is the end. If it is not we
        update the auxiliar data structures and return -1.
        """
        if neighbour not in visited:
            if neighbour == end:
                return number_of_transformations + 1
            visited.add(neighbour)
            queue.append((neighbour, number_of_transformations + 1))
        return -1

    def _get_pattern(self, word, letter_index):
        """
        Args:
            word (str): Word to build the pattern for.
            letter_index (int): Index of the letter that can be any letter.

        Returns:
            str. Pattern built by replacing the letter at index_letter of word
                 by '?'.

        Examples:
            _get_pattern("spam", 2) -> "sp?m"
            _get_pattern("spam", 0) -> "?pam"
            _get_pattern("spam", 3) -> "spa?"
        """
        return "{}?{}".format(word[:letter_index], word[letter_index+1:])
