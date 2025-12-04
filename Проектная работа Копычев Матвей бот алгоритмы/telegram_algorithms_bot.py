import os
import asyncio
import random
from typing import Dict, List, Optional
from dataclasses import dataclass
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder


# ==================== КЛАССЫ МОДЕЛЕЙ ====================

@dataclass
class Algorithm:
    """Класс для представления алгоритма"""
    key: str
    name: str
    category: str
    summary: str
    rules: str
    explanation: str
    pseudocode: str
    example: str
    result: str
    media: str = ""


@dataclass
class InteractiveAlgorithm:
    """Класс для интерактивных алгоритмов"""
    key: str
    name: str
    category: str
    prompt: str
    handler_method: str


# ==================== КЛАСС ДЛЯ УТИЛИТ ====================

class TextUtils:
    """Утилиты для работы с текстом"""

    @staticmethod
    def parse_numbers(text: str) -> Optional[List[int]]:
        """Парсит строку чисел, разделенных пробелами"""
        try:
            return list(map(int, text.split()))
        except:
            return None

    @staticmethod
    def format_algorithm_text(alg: Algorithm) -> str:
        """Форматирует алгоритм для отображения"""
        parts = [
            f"{alg.name}",
            "",
            f"💡 Суть:\n{alg.summary}",
            "",
            f"📌 Правила:\n{alg.rules}",
            "",
            f"📝 Пояснение:\n{alg.explanation}",
            "",
            f"💻 Псевдокод:\n{alg.pseudocode}",
            "",
            f"🔎 Пример:\n{alg.example}",
            "",
            f"✅ Результат:\n{alg.result}",
        ]
        return "\n".join(parts)

    @staticmethod
    def split_long_text(text: str, max_length: int = 3800) -> List[str]:
        """Разделяет длинный текст на части"""
        if len(text) <= max_length:
            return [text]

        chunks = []
        cur = ""
        for line in text.splitlines(keepends=True):
            if len(cur) + len(line) > max_length:
                chunks.append(cur)
                cur = line
            else:
                cur += line
        if cur:
            chunks.append(cur)
        return chunks


# ==================== КЛАСС ДЛЯ РАБОТЫ С АЛГОРИТМАМИ ====================

class AlgorithmsDatabase:
    """База данных алгоритмов"""

    def __init__(self):
        self.algorithms: Dict[str, Algorithm] = {}
        self.interactive_algorithms: Dict[str, InteractiveAlgorithm] = {}
        self.category_display = {
            "Сортировки": "Сортировки",
            "Поиск": "Поиск",
            "Графы": "Графы",
            "Динамическое программирование": "Динамическое программирование",
            "work_examples": "Примеры работы алгоритмов",
            "interactive_demo": "Интерактивные демонстрации"
        }
        self._load_algorithms()
        self._load_interactive_algorithms()

    def _load_algorithms(self):
        """Загрузка всех алгоритмов"""
        # СОРТИРОВКИ
        self.algorithms["bubble_sort"] = Algorithm(
            key="bubble_sort",
            name="🔹 Сортировка пузырьком",
            category="Сортировки",
            summary="Многократные проходы по массиву; на каждом проходе сравниваем пары соседних элементов и при необходимости меняем их местами.",
            rules="1) Делать проходы по массиву; 2) сравнивать соседние элементы; 3) менять местами при необходимости; 4) повторять до отсутствия обменов.",
            explanation="На каждом проходе наибольший элемент 'всплывает' в конец. Очень проста в реализации, но имеет квадратичную сложность в среднем и худшем случаях — O(n²). Подходит для обучения и небольших наборов данных.",
            pseudocode="for i from 0 to n-2:\n    for j from 0 to n-2-i:\n        if A[j] > A[j+1]: swap(A[j], A[j+1])",
            example="Вход: [5,3,8,4] → Результат: [3,4,5,8]",
            result="[3,4,5,8]",
            media="https://upload.wikimedia.org/wikipedia/commons/c/c8/Bubble-sort-example-300px.gif"
        )

        self.algorithms["selection_sort"] = Algorithm(
            key="selection_sort",
            name="🔹 Сортировка выбором",
            category="Сортировки",
            summary="На каждом шаге находим минимальный элемент в неотсортированном участке и ставим его на позицию начала этого участка.",
            rules="1) Для i от 0 до n-1: найти индекс минимального элемента в [i..n-1]; 2) поменять A[i] и A[minIndex].",
            explanation="Всегда делает O(n²) сравнений, но минимальное число записей (swap). Используется, когда запись дороже чтения.",
            pseudocode="for i from 0 to n-1:\n    minIndex = i\n    for j from i+1 to n-1:\n        if A[j] < A[minIndex]: minIndex = j\n    swap(A[i], A[minIndex])",
            example="Вход: [64,25,12,22,11] → Результат: [11,12,22,25,64]",
            result="[11,12,22,25,64]",
            media="https://upload.wikimedia.org/wikipedia/commons/9/94/Selection_sort_animation.gif"
        )

        self.algorithms["insertion_sort"] = Algorithm(
            key="insertion_sort",
            name="🔹 Сортировка вставками",
            category="Сортировки",
            summary="Вставляем текущий элемент на подходящую позицию внутри уже отсортированной левой части массива.",
            rules="1) i от 1 до n-1: key = A[i]; 2) сдвигать элементы > key вправо; 3) вставить key.",
            explanation="Эффективна для почти отсортированных массивов (лучший O(n)). Часто используется внутри гибридных алгоритмов для маленьких подмассивов.",
            pseudocode="for i from 1 to n-1:\n    key = A[i]\n    j = i-1\n    while j >= 0 and A[j] > key:\n        A[j+1] = A[j]\n        j -= 1\n    A[j+1] = key",
            example="Вход: [12,11,13,5,6] → Результат: [5,6,11,12,13]",
            result="[5,6,11,12,13]",
            media="https://upload.wikimedia.org/wikipedia/commons/0/0f/Insertion-sort-example-300px.gif"
        )

        self.algorithms["merge_sort"] = Algorithm(
            key="merge_sort",
            name="🔹 Сортировка слиянием",
            category="Сортировки",
            summary="Разделяем массив на две половины, рекурсивно сортируем каждую, затем сливаем их в один отсортированный массив.",
            rules="1) Если длина ≤ 1 — вернуть; 2) mid = n//2; 3) sort(left); sort(right); 4) merge(left,right).",
            explanation="Стабильная сортировка с гарантированным временем O(n log n) и памятью O(n) для слияния. Хороша для внешней сортировки больших данных.",
            pseudocode="MergeSort(A):\n    if len(A) <= 1: return A\n    mid = len(A)//2\n    left = MergeSort(A[:mid])\n    right = MergeSort(A[mid:])\n    return merge(left,right)",
            example="Вход: [38,27,43,3,9,82,10] → Результат: [3,9,10,27,38,43,82]",
            result="[3,9,10,27,38,43,82]",
            media="https://upload.wikimedia.org/wikipedia/commons/c/cc/Merge-sort-example-300px.gif"
        )

        self.algorithms["quick_sort"] = Algorithm(
            key="quick_sort",
            name="🔹 Быстрая сортировка (QuickSort)",
            category="Сортировки",
            summary="Выбираем опорный элемент (pivot), разделяем массив на элементы меньше и больше pivot, рекурсивно сортируем части.",
            rules="1) Если длина ≤ 1 — вернуть; 2) выбрать pivot; 3) left = < pivot; mid = == pivot; right = > pivot; 4) рекурсивно сортировать.",
            explanation="В среднем O(n log n), но при неудачном pivot — O(n²). Часто применяют рандомизацию pivot или медиану трёх для устойчивости.",
            pseudocode="QuickSort(A):\n    if len(A) <= 1: return A\n    pivot = choose(A)\n    left = [x for x in A if x < pivot]\n    mid = [x for x in A if x == pivot]\n    right = [x for x in A if x > pivot]\n    return QuickSort(left) + mid + QuickSort(right)",
            example="Вход: [10,7,8,9,1,5] → Результат: [1,5,7,8,9,10]",
            result="[1,5,7,8,9,10]",
            media="https://upload.wikimedia.org/wikipedia/commons/6/6a/Sorting_quicksort_anim.gif"
        )

        self.algorithms["heap_sort"] = Algorithm(
            key="heap_sort",
            name="🔹 Сортировка кучей (HeapSort)",
            category="Сортировки",
            summary="Построить max-heap, затем последовательно извлекать максимум и уменьшать размер кучи, получая отсортированный массив.",
            rules="1) buildMaxHeap; 2) for i from n-1 downto 1: swap A[0],A[i]; heapify(A,0,i).",
            explanation="In-place алгоритм с худшей сложностью O(n log n). Не является стабильным, но надёжен по времени.",
            pseudocode="HeapSort(A):\n    buildMaxHeap(A)\n    for i from n-1 downto 1:\n        swap(A[0], A[i])\n        heapify(A,0,i)",
            example="Вход: [4,10,3,5,1] → Результат: [1,3,4,5,10]",
            result="[1,3,4,5,10]",
            media="https://upload.wikimedia.org/wikipedia/commons/1/1f/HeapSortAnimation.gif"
        )

        self.algorithms["counting_sort"] = Algorithm(
            key="counting_sort",
            name="🔹 Сортировка подсчетом",
            category="Сортировки",
            summary="Подходит для целочисленных значений в небольшом диапазоне: считаем количество каждого значения и восстанавливаем отсортированный массив.",
            rules="1) count[value]++ для каждого элемента; 2) накопительный сумм; 3) построить выходной массив по counts.",
            explanation="Время O(n + k), где k — диапазон значений. Очень эффективна при малом k, но требует дополнительной памяти O(k).",
            pseudocode="CountingSort(A):\n    k = max(A)\n    count = [0]*(k+1)\n    for x in A: count[x] += 1\n    for i in 1..k: count[i] += count[i-1]\n    ...",
            example="Вход: [4,2,2,8,3,3,1] → Результат: [1,2,2,3,3,4,8]",
            result="[1,2,2,3,3,4,8]",
            media="https://upload.wikimedia.org/wikipedia/commons/7/72/Counting_sort.png"
        )

        # ПОИСК
        self.algorithms["binary_search"] = Algorithm(
            key="binary_search",
            name="🔍 Бинарный поиск",
            category="Поиск",
            summary="Ищет элемент в отсортированном массиве, деля диапазон поиска пополам на каждом шаге.",
            rules="1) left=0,right=n-1; 2) while left<=right: mid=(left+right)//2; 3) сравнить и сдвинуть границы.",
            explanation="Очень эффективный поиск с логарифмической сложностью O(log n). Требует предварительной сортировки массива.",
            pseudocode="BinarySearch(A, target):\n    left, right = 0, len(A)-1\n    while left <= right:\n        mid = (left+right)//2\n        if A[mid] == target: return mid\n        if A[mid] < target: left = mid + 1\n        else: right = mid - 1\n    return -1",
            example="Ищем 8 в [1,3,5,8,10] → индекс 3",
            result="3",
            media="https://upload.wikimedia.org/wikipedia/commons/8/84/Binary_search_tree_example.svg"
        )

        self.algorithms["exponential_search"] = Algorithm(
            key="exponential_search",
            name="🔍 Экспоненциальный поиск (Exponential)",
            category="Поиск",
            summary="Для поиска в большом отсортированном массиве сначала ищем диапазон, где может быть элемент, удваивая шаг, затем применяем бинарный поиск внутри этого диапазона.",
            rules="1) Если A[0]==target — вернуть 0; 2) i=1; пока i<n и A[i] <= target: i*=2; 3) бинарный поиск в [i/2 .. min(i,n-1)].",
            explanation="Хорош для бесконечных или очень больших массивов, где нельзя сразу узнать длину. Комбинирует линейный экспоненциальный рост диапазона и бинарный поиск.",
            pseudocode="ExponentialSearch(A, target):\n    if A[0] == target: return 0\n    i = 1\n    while i < n and A[i] <= target: i *= 2\n    return BinarySearch(A, target, i//2, min(i, n-1))",
            example="Поиск 23 в большом отсортированном массиве: сначала диапазон [..], затем бинарный поиск.",
            result="индекс или -1",
            media="https://upload.wikimedia.org/wikipedia/commons/2/25/Exponential_search.png"
        )

        self.algorithms["interpolation_search"] = Algorithm(
            key="interpolation_search",
            name="🔍 Интерполяционный поиск",
            category="Поиск",
            summary="Как бинарный поиск, но вычисляет mid по формуле пропорции (предполагается равномерное распределение ключей).",
            rules="mid = low + ((target - A[low]) * (high - low)) // (A[high] - A[low]); сужаем диапазон как в бинарном поиске.",
            explanation="При равномерно распределённых данных средняя сложность близка к O(log log n); в худшем — O(n). Полезен для больших равномерных массивов.",
            pseudocode="InterpolationSearch(A, target):\n    low = 0; high = n-1\n    while low <= high and target >= A[low] and target <= A[high]:\n        pos = low + ((target-A[low])*(high-low))//(A[high]-A[low])\n        if A[pos] == target: return pos\n        if A[pos] < target: low = pos + 1\n        else: high = pos - 1\n    return -1",
            example="Поиск по равномерно распределённым числам — быстрее, чем бинарный в среднем.",
            result="индекс или -1",
            media="https://upload.wikimedia.org/wikipedia/commons/7/7b/Interpolation_search_animation.gif"
        )

        # ГРАФЫ
        self.algorithms["dfs"] = Algorithm(
            key="dfs",
            name="🌳 Поиск в глубину (DFS)",
            category="Графы",
            summary="Рекурсивно (или со стеком) идём в глубь по ветвям графа до тех пор, пока есть непосещённые вершины.",
            rules="1) Пометить старт как visited; 2) для каждого соседа, если не visited — DFS(сосед).",
            explanation="Используется для поиска компонент связности, выявления циклов и топологической сортировки. Сложность O(V+E).",
            pseudocode="DFS(v):\n    visited[v] = true\n    for u in neighbors(v):\n        if not visited[u]: DFS(u)",
            example="Пример обхода: A,B,D,C",
            result="последовательность обхода",
            media="https://upload.wikimedia.org/wikipedia/commons/7/77/Depth-first-tree.svg"
        )

        self.algorithms["bfs"] = Algorithm(
            key="bfs",
            name="🌳 Поиск в ширину (BFS)",
            category="Графы",
            summary="Уровневый обход графа: сначала вершины на расстоянии 1, затем на расстоянии 2 и т.д.",
            rules="1) Очередь: enqueue(start), visited[start]=true; 2) пока очередь: v=dequeue(); для каждого соседа: если не visited — enqueue и пометить.",
            explanation="На невзвешенных графах даёт кратчайшие пути по числу рёбер. Сложность O(V+E).",
            pseudocode="BFS(start):\n    queue = [start]\n    visited[start] = true\n    while queue:\n        v = queue.pop(0)\n        for u in neighbors(v):\n            if not visited[u]: visited[u]=true; queue.append(u)",
            example="BFS(A) -> A,B,C,D (по уровням)",
            result="последовательность уровней",
            media="https://upload.wikimedia.org/wikipedia/commons/4/46/Breadth-First-Search-Example.png"
        )

        self.algorithms["dijkstra"] = Algorithm(
            key="dijkstra",
            name="🛣 Алгоритм Дейкстры",
            category="Графы",
            summary="Находит кратчайшие пути от стартовой вершины до всех остальных в графе с неотрицательными весами.",
            rules="1) dist[]=inf; dist[start]=0; 2) использовать priority queue; 3) relax рёбер при извлечении u.",
            explanation="С использованием подходящей структуры (куча) сложность O((V+E) log V). Широко применяется в навигации и сетевой маршрутизации.",
            pseudocode="Dijkstra(graph, start):\n    for v in V: dist[v]=inf\n    dist[start]=0\n    Q = priority_queue(dist)\n    while Q:\n        u = extract_min(Q)\n        for v in neighbors(u):\n            if dist[u] + w(u,v) < dist[v]: dist[v] = dist[u] + w(u,v)",
            example="Таблица dist после выполнения — минимальные расстояния от стартовой вершины",
            result="таблица минимальных расстояний",
            media="https://upload.wikimedia.org/wikipedia/commons/5/57/Dijkstra_Animation.gif"
        )

        self.algorithms["floyd_warshall"] = Algorithm(
            key="floyd_warshall",
            name="🛣 Алгоритм Флойда-Уоршелла",
            category="Графы",
            summary="DP-алгоритм для поиска кратчайших путей между всеми парами вершин в графе.",
            rules="Инициализировать dist матрицу; для каждого k,i,j: dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j]).",
            explanation="Подходит для небольших графов (O(n^3)). Удобен для анализа всех пар вершин.",
            pseudocode="FloydWarshall(dist):\n    for k in V:\n        for i in V:\n            for j in V:\n                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])",
            example="После завершения dist содержит кратчайшие расстояния для всех пар вершин.",
            result="матрица dist",
            media="https://upload.wikimedia.org/wikipedia/commons/1/10/Floyd-Warshall_Animation.gif"
        )

        # ДИНАМИЧЕСКОЕ ПРОГРАММИРОВАНИЕ
        self.algorithms["knapsack"] = Algorithm(
            key="knapsack",
            name="🎒 Задача о рюкзаке (0/1)",
            category="Динамическое программирование",
            summary="Выбор предметов для максимизации суммарной ценности при ограничении по весу (целые предметы — 0/1).",
            rules="DP-таблица dp[i][w] — максимальная ценность для первых i предметов и вместимости w; вычисление через выбор брать/не брать.",
            explanation="Классический DP: сложность O(nW). При большом W нужны другие подходы (approximation или meet-in-the-middle).",
            pseudocode="Knapsack(values, weights, W):\n    dp = zeros((n+1),(W+1))\n    for i in 1..n:\n        for w in 0..W:\n            if weights[i] <= w:\n                dp[i][w] = max(dp[i-1][w], dp[i-1][w-weights[i]] + values[i])\n            else:\n                dp[i][w] = dp[i-1][w]\n    return dp[n][W]",
            example="values=[60,100,120], weights=[10,20,30], W=50 → 220",
            result="220",
            media="https://upload.wikimedia.org/wikipedia/commons/6/6f/Knapsack.svg"
        )

        self.algorithms["lcs"] = Algorithm(
            key="lcs",
            name="🔁 Длина наибольшей общей подпоследовательности (LCS)",
            category="Динамическое программирование",
            summary="Найти длину самой длинной последовательности символов, которая является подпоследовательностью двух строк.",
            rules="DP: dp[i][j] — LCS для префиксов s1[:i], s2[:j]; если s1[i-1]==s2[j-1]: dp[i][j]=dp[i-1][j-1]+1, иначе max(dp[i-1][j], dp[i][j-1]).",
            explanation="Классическое DP-решение с временем O(n*m) и памятью O(n*m) (можно оптимизировать по памяти). Используется в биоинформатике, сравнении текста и др.",
            pseudocode="LCS(s1,s2):\n    n=len(s1); m=len(s2)\n    dp = zeros((n+1),(m+1))\n    for i in 1..n:\n        for j in 1..m:\n            if s1[i-1] == s2[j-1]: dp[i][j] = dp[i-1][j-1] + 1\n            else: dp[i][j] = max(dp[i-1][j], dp[i][j-1])\n    return dp[n][m]",
            example="s1='ABCBDAB', s2='BDCABA' → LCS length = 4 (e.g. 'BCBA')",
            result="длина LCS (4)",
            media="https://upload.wikimedia.org/wikipedia/commons/4/4a/LCS_example.svg"
        )

        self.algorithms["levenshtein"] = Algorithm(
            key="levenshtein",
            name="✏️ Редакционное расстояние (Levenshtein Distance)",
            category="Динамическое программирование",
            summary="Минимальное число операций (вставка/удаление/замена) для превращения одной строки в другую.",
            rules="DP: dp[i][j] — минимальные операции для s1[:i] → s2[:j]. Переходы: удалить, вставить, заменить (с учётом равенства символов).",
            explanation="Используется в проверке орфографии, сравнении строк и биоинформатике. Сложность O(n*m).",
            pseudocode="Levenshtein(s1,s2):\n    n=len(s1); m=len(s2)\n    dp = zeros((n+1),(m+1))\n    for i in 0..n: dp[i][0]=i\n    for j in 0..m: dp[0][j]=j\n    for i in 1..n:\n        for j in 1..m:\n            cost = 0 if s1[i-1]==s2[j-1] else 1\n            dp[i][j] = min(dp[i-1][j] + 1, dp[i][j-1] + 1, dp[i-1][j-1] + cost)\n    return dp[n][m]",
            example="s1='kitten', s2='sitting' → distance = 3 (replace k→s, replace e→i, insert g)",
            result="число операций (3)",
            media="https://upload.wikimedia.org/wikipedia/commons/8/84/Levenshtein_edit_distance.png"
        )

        # ПРИМЕРЫ РАБОТЫ АЛГОРИТМОВ
        self.algorithms["example_binary_search"] = Algorithm(
            key="example_binary_search",
            name="🧪 Пример: Бинарный поиск",
            category="work_examples",
            summary="Интерактивная демонстрация бинарного поиска. Введите массив и число.",
            rules="Введите массив через пробел, затем отправьте число для поиска.",
            explanation="Бот покажет, как уменьшается диапазон поиска.",
            pseudocode="Вы вводите данные — бот делает шаги бинарного поиска.",
            example="Вход: 1 3 5 8 10 → 8",
            result="Индексы mid, left, right по шагам.",
            media=""
        )

        self.algorithms["example_quicksort"] = Algorithm(
            key="example_quicksort",
            name="🧪 Пример: Быстрая сортировка",
            category="work_examples",
            summary="Вы вводите массив → бот показывает разбиения (partition).",
            rules="Введите массив через пробел.",
            explanation="На каждом шаге бот отображает left/mid/right.",
            pseudocode="QuickSort со стенографией шагов.",
            example="Вход: 5 3 8 4",
            result="[3,4,5,8]",
            media=""
        )

        self.algorithms["example_bfs"] = Algorithm(
            key="example_bfs",
            name="🧪 Пример: BFS на графе",
            category="work_examples",
            summary="Введите рёбра графа + стартовую вершину — бот выполнит обход.",
            rules="Формат: A-B,B-C,C-D; старт: A",
            explanation="Покажет очередь на каждом шаге.",
            pseudocode="Классический BFS.",
            example="A-B,B-C,C-D; старт=A",
            result="A,B,C,D",
            media=""
        )

        self.algorithms["example_lcs"] = Algorithm(
            key="example_lcs",
            name="🧪 Пример: LCS двух строк",
            category="work_examples",
            summary="Введите две строкы → бот покажет DP-таблицу и длину LCS.",
            rules="Отправьте строку 1 → затем строку 2.",
            explanation="Пошаговое заполнение таблицы.",
            pseudocode="DP по двум строкам.",
            example="ABCBDAB / BDCABA",
            result="4",
            media=""
        )

        self.algorithms["example_levenshtein"] = Algorithm(
            key="example_levenshtein",
            name="🧪 Пример: Расстояние Левенштейна",
            category="work_examples",
            summary="Введите две строки → бот покажет DP-таблицу расстояния.",
            rules="Отправьте строку 1 → затем строку 2.",
            explanation="Демонстрация вставка/удаление/замена.",
            pseudocode="Классическое DP.",
            example="kitten / sitting",
            result="3",
            media=""
        )

    def _load_interactive_algorithms(self):
        """Загрузка интерактивных алгоритмов"""
        self.interactive_algorithms["interactive_binary_search"] = InteractiveAlgorithm(
            key="interactive_binary_search",
            name="🔧 Бинарный поиск",
            category="interactive_demo",
            prompt="Введите отсортированный массив через пробел и число для поиска.\nПример: 1 2 3 4 5 4",
            handler_method="binary_search"
        )

        self.interactive_algorithms["interactive_bubble_sort"] = InteractiveAlgorithm(
            key="interactive_bubble_sort",
            name="🔧 Пузырьковая сортировка",
            category="interactive_demo",
            prompt="Введите массив чисел через пробел.\nПример: 5 2 8 1 3",
            handler_method="bubble_sort"
        )

        self.interactive_algorithms["interactive_selection_sort"] = InteractiveAlgorithm(
            key="interactive_selection_sort",
            name="🔧 Сортировка выбором",
            category="interactive_demo",
            prompt="Введите массив чисел через пробел.\nПример: 64 25 12 22 11",
            handler_method="selection_sort"
        )

        self.interactive_algorithms["interactive_insertion_sort"] = InteractiveAlgorithm(
            key="interactive_insertion_sort",
            name="🔧 Сортировка вставками",
            category="interactive_demo",
            prompt="Введите массив чисел через пробел.\nПример: 12 11 13 5 6",
            handler_method="insertion_sort"
        )

        self.interactive_algorithms["interactive_linear_search"] = InteractiveAlgorithm(
            key="interactive_linear_search",
            name="🔧 Линейный поиск",
            category="interactive_demo",
            prompt="Введите массив через пробел и число для поиска.\nПример: 5 2 8 1 3 8",
            handler_method="linear_search"
        )

    def get_sorted_categories(self) -> List[str]:
        """Получить отсортированные категории (без интерактивных)"""
        categories = {v.category for v in self.algorithms.values()}
        if "interactive_demo" in categories:
            categories.remove("interactive_demo")
        return sorted(categories)

    def get_algorithms_in_category(self, category: str) -> List[str]:
        """Получить алгоритмы в категории"""
        items = [(k, v.name) for k, v in self.algorithms.items() if v.category == category]
        return [k for k, _ in sorted(items, key=lambda t: t[1].lower())]

    def get_algorithm(self, key: str) -> Optional[Algorithm]:
        """Получить алгоритм по ключу"""
        return self.algorithms.get(key)

    def get_interactive_algorithm(self, key: str) -> Optional[InteractiveAlgorithm]:
        """Получить интерактивный алгоритм по ключу"""
        return self.interactive_algorithms.get(key)


# ==================== КЛАСС ДЛЯ КЛАВИАТУР ====================

class KeyboardManager:
    """Менеджер для создания клавиатур"""

    def __init__(self, database: AlgorithmsDatabase):
        self.db = database

    def make_main_menu(self, columns: int = 2) -> types.InlineKeyboardMarkup:
        """Создает главное меню"""
        builder = InlineKeyboardBuilder()

        for cat in self.db.get_sorted_categories():
            builder.button(
                text=f"📂 {self.db.category_display.get(cat, cat)}",
                callback_data=f"cat_{cat}"
            )

        # Отдельная кнопка для интерактивных демонстраций
        builder.button(
            text="🧪 Интерактивные демонстрации",
            callback_data="interactive_menu"
        )

        builder.adjust(columns)
        return builder.as_markup()

    def make_category_menu(self, category: str, columns: int = 3) -> types.InlineKeyboardMarkup:
        """Создает меню категории"""
        builder = InlineKeyboardBuilder()

        for key in self.db.get_algorithms_in_category(category):
            alg = self.db.get_algorithm(key)
            if alg:
                builder.button(text=alg.name, callback_data=f"alg_{key}")

        # Служебные кнопки
        builder.button(text="🏠 Главное меню", callback_data="main_menu")
        builder.button(text="🎲 Случайный алгоритм", callback_data=f"random_{category}")

        builder.adjust(columns)
        return builder.as_markup()

    def make_back_menu(self) -> types.InlineKeyboardMarkup:
        """Создает меню с кнопкой Назад"""
        builder = InlineKeyboardBuilder()
        builder.button(text="🔙 Назад в категорию", callback_data="back_to_category")
        builder.button(text="🏠 Главное меню", callback_data="main_menu")
        builder.adjust(2)
        return builder.as_markup()

    def make_interactive_menu(self) -> types.InlineKeyboardMarkup:
        """Создает меню интерактивных демонстраций"""
        builder = InlineKeyboardBuilder()

        for key, data in self.db.interactive_algorithms.items():
            builder.button(text=data.name, callback_data=f"inter_{key}")

        builder.button(text="🏠 Главное меню", callback_data="main_menu")
        builder.adjust(1)
        return builder.as_markup()


# ==================== КЛАСС ДЛЯ ОТПРАВКИ МЕДИА ====================

class MediaSender:
    """Класс для отправки медиа-файлов"""

    def __init__(self, bot: Bot):
        self.bot = bot

    async def send_media(self, chat_id: int, media_url: str) -> None:
        """
        Отправляет анимацию (если gif/mp4) или фото (иначе).
        Отправляется отдельным сообщением.
        """
        if not media_url:
            return

        try:
            low = media_url.lower()
            if low.endswith((".gif", ".mp4", ".webm")):
                await self.bot.send_animation(chat_id, animation=media_url)
            else:
                await self.bot.send_photo(chat_id, photo=media_url)
        except Exception as e:
            print(f"[WARN] Не удалось отправить media: {media_url}, ошибка: {e}")


# ==================== КЛАСС ДЛЯ ИНТЕРАКТИВНЫХ АЛГОРИТМОВ ====================

class InteractiveAlgorithmsHandler:
    """Обработчик интерактивных алгоритмов"""

    def __init__(self):
        self.text_utils = TextUtils()

    async def handle_binary_search(self, text: str) -> str:
        """Обработка бинарного поиска"""
        try:
            parts = text.split()
            if len(parts) < 2:
                return "Введите массив и число для поиска через пробел.\nПример: 1 2 3 4 5 4"

            arr = list(map(int, parts[:-1]))
            target = int(parts[-1])

            # Проверяем, отсортирован ли массив
            if arr != sorted(arr):
                return "⚠️ Массив должен быть отсортирован по возрастанию!"

            steps = []
            left, right = 0, len(arr) - 1
            step_num = 1

            while left <= right:
                mid = (left + right) // 2
                steps.append(f"Шаг {step_num}: left={left}, right={right}, mid={mid}, arr[{mid}]={arr[mid]}")

                if arr[mid] == target:
                    steps.append(f"✅ Найдено! Элемент {target} на позиции {mid}")
                    break
                elif arr[mid] < target:
                    steps.append(f"   arr[{mid}]={arr[mid]} < {target}, ищем в правой части")
                    left = mid + 1
                else:
                    steps.append(f"   arr[{mid}]={arr[mid]} > {target}, ищем в левой части")
                    right = mid - 1
                step_num += 1

            if left > right:
                steps.append(f"❌ Элемент {target} не найден в массиве")

            return f"📘 Ход работы бинарного поиска:\n\n" + "\n".join(steps)

        except Exception as e:
            return f"Ошибка формата: {e}\nПопробуйте снова. Пример: 1 2 3 4 5 4"

    async def handle_bubble_sort(self, text: str) -> str:
        """Обработка пузырьковой сортировки"""
        try:
            arr = self.text_utils.parse_numbers(text)
            if arr is None:
                return "Ошибка формата. Введите числа через пробел.\nПример: 5 2 8 1 3"

            steps = []
            a = arr[:]  # копия массива для сортировки
            steps.append(f"Исходный массив: {a}")

            n = len(a)
            swapped = True
            pass_num = 1

            while swapped:
                swapped = False
                steps.append(f"\n🌀 Проход {pass_num}:")

                for j in range(0, n - 1):
                    steps.append(f"   Сравниваем {a[j]} и {a[j + 1]}")
                    if a[j] > a[j + 1]:
                        a[j], a[j + 1] = a[j + 1], a[j]
                        swapped = True
                        steps.append(f"   → Меняем местами: {a}")

                if not swapped:
                    steps.append("   Обменов не было, массив отсортирован!")

                pass_num += 1

            steps.append(f"\n✅ Итоговый отсортированный массив: {a}")
            return "📘 Ход работы пузырьковой сортировки:\n" + "\n".join(steps)

        except:
            return "Ошибка формата. Введите числа через пробел.\nПример: 5 2 8 1 3"

    async def handle_selection_sort(self, text: str) -> str:
        """Обработка сортировки выбором"""
        try:
            arr = self.text_utils.parse_numbers(text)
            if arr is None:
                return "Ошибка формата. Введите числа через пробел.\nПример: 64 25 12 22 11"

            steps = []
            a = arr[:]  # копия массива для сортировки
            steps.append(f"Исходный массив: {a}")

            n = len(a)

            for i in range(n):
                steps.append(f"\n🌀 Шаг {i + 1}: Ищем минимальный в [{i}..{n - 1}]")
                min_idx = i

                for j in range(i + 1, n):
                    steps.append(f"   Сравниваем {a[min_idx]} и {a[j]}")
                    if a[j] < a[min_idx]:
                        min_idx = j
                        steps.append(f"   → Новый минимум: {a[min_idx]} на позиции {min_idx}")

                if min_idx != i:
                    a[i], a[min_idx] = a[min_idx], a[i]
                    steps.append(f"   Меняем {a[min_idx]} и {a[i]}: {a}")
                else:
                    steps.append(f"   Минимум уже на месте")

                steps.append(f"   Текущее состояние: {a}")

            steps.append(f"\n✅ Итоговый отсортированный массив: {a}")
            return "📘 Ход работы сортировки выбором:\n" + "\n".join(steps)

        except:
            return "Ошибка формата. Введите числа через пробел.\nПример: 64 25 12 22 11"

    async def handle_insertion_sort(self, text: str) -> str:
        """Обработка сортировки вставками"""
        try:
            arr = self.text_utils.parse_numbers(text)
            if arr is None:
                return "Ошибка формата. Введите числа через пробел.\nПример: 12 11 13 5 6"

            steps = []
            a = arr[:]  # копия массива для сортировки
            steps.append(f"Исходный массив: {a}")

            n = len(a)

            for i in range(1, n):
                steps.append(f"\n🌀 Шаг {i}: Вставляем элемент {a[i]} на позицию {i}")
                key = a[i]
                j = i - 1

                steps.append(f"   Сравниваем с элементами слева...")
                while j >= 0 and a[j] > key:
                    steps.append(f"   {a[j]} > {key}, сдвигаем {a[j]} вправо")
                    a[j + 1] = a[j]
                    j -= 1

                a[j + 1] = key
                steps.append(f"   Вставляем {key} на позицию {j + 1}: {a}")

            steps.append(f"\n✅ Итоговый отсортированный массив: {a}")
            return "📘 Ход работы сортировки вставками:\n" + "\n".join(steps)

        except:
            return "Ошибка формата. Введите числа через пробел.\nПример: 12 11 13 5 6"

    async def handle_linear_search(self, text: str) -> str:
        """Обработка линейного поиска"""
        try:
            parts = text.split()
            if len(parts) < 2:
                return "Введите массив и число для поиска через пробел.\nПример: 5 2 8 1 3 8"

            arr = list(map(int, parts[:-1]))
            target = int(parts[-1])

            steps = []
            steps.append(f"Ищем элемент {target} в массиве: {arr}")
            found = False

            for i in range(len(arr)):
                steps.append(f"\nШаг {i + 1}: Проверяем элемент arr[{i}] = {arr[i]}")
                if arr[i] == target:
                    steps.append(f"✅ Найдено! Элемент {target} на позиции {i}")
                    found = True
                    break
                else:
                    steps.append(f"   {arr[i]} ≠ {target}, продолжаем поиск...")

            if not found:
                steps.append(f"\n❌ Элемент {target} не найден в массиве")

            return f"📘 Ход работы линейного поиска:\n\n" + "\n".join(steps)

        except:
            return "Ошибка формата. Введите массив и число через пробел.\nПример: 5 2 8 1 3 8"


# ==================== ГЛАВНЫЙ КЛАСС БОТА ====================

class TelegramAlgorithmsBot:
    """Главный класс Telegram бота для изучения алгоритмов"""

    def __init__(self):
        # Загрузка конфигурации
        load_dotenv()
        self.BOT_TOKEN = os.getenv("BOT_TOKEN")
        if not self.BOT_TOKEN:
            raise ValueError("BOT_TOKEN не найден в переменных окружения (.env)")

        # Инициализация компонентов
        self.bot = Bot(token=self.BOT_TOKEN)
        self.dp = Dispatcher()

        # Инициализация менеджеров
        self.database = AlgorithmsDatabase()
        self.keyboard_manager = KeyboardManager(self.database)
        self.media_sender = MediaSender(self.bot)
        self.interactive_handler = InteractiveAlgorithmsHandler()

        # Текущее состояние для интерактивных алгоритмов
        self.current_interactive_algorithm = {}

        # Регистрация обработчиков
        self._register_handlers()

    def _register_handlers(self):
        """Регистрация всех обработчиков"""
        self.dp.message(Command(commands=["start"]))(self.cmd_start)
        self.dp.callback_query()(self.callbacks_handler)
        self.dp.message()(self.handle_interactive_input)

    async def cmd_start(self, message: Message):
        """Обработка команды /start"""
        text = "👋 Привет! Это бот-справочник по алгоритмам.\nВыбери категорию:"
        await message.answer(text, reply_markup=self.keyboard_manager.make_main_menu())

    async def callbacks_handler(self, callback: CallbackQuery):
        """Обработка всех callback-запросов"""
        data = callback.data or ""

        # ---------------- Категории ----------------
        if data.startswith("cat_"):
            category = data[len("cat_"):]
            await callback.message.edit_text(
                f"📂 Категория: {category}\nВыберите алгоритм:",
                reply_markup=self.keyboard_manager.make_category_menu(category)
            )
            await callback.answer()
            return

        # ---------------- Главное меню ----------------
        if data == "main_menu":
            await callback.message.edit_text(
                "👋 Главное меню. Выберите категорию:",
                reply_markup=self.keyboard_manager.make_main_menu()
            )
            await callback.answer()
            return

        # ---------------- Случайный алгоритм ----------------
        if data.startswith("random_"):
            category = data[len("random_"):]
            candidates = self.database.get_algorithms_in_category(category)
            if not candidates:
                await callback.answer("В категории пока нет алгоритмов.", show_alert=True)
                return
            key = random.choice(candidates)
            data = f"alg_{key}"

        # ---------------- Выбор алгоритма ----------------
        if data.startswith("alg_"):
            key = data[len("alg_"):]
            alg = self.database.get_algorithm(key)
            if not alg:
                await callback.answer("Алгоритм не найден.", show_alert=True)
                return

            chat_id = callback.message.chat.id

            # 1) Отправляем медиа отдельным сообщением
            if alg.media:
                await self.media_sender.send_media(chat_id, alg.media)

            # 2) Формируем текст и отправляем
            full_text = TextUtils.format_algorithm_text(alg)
            if len(full_text) <= 3800:
                await self.bot.send_message(chat_id, full_text, reply_markup=self.keyboard_manager.make_back_menu())
            else:
                # Аккуратно разбиваем на части
                chunks = TextUtils.split_long_text(full_text)
                for i, chunk in enumerate(chunks):
                    if i < len(chunks) - 1:
                        await self.bot.send_message(chat_id, chunk)
                    else:
                        await self.bot.send_message(chat_id, chunk, reply_markup=self.keyboard_manager.make_back_menu())

            await callback.answer()
            return

        # ---------------- Меню интерактивных демонстраций ----------------
        if data == "interactive_menu":
            await callback.message.edit_text(
                "🧪 *Интерактивные демонстрации алгоритмов*\n\n"
                "Выберите алгоритм, введите данные в одной строке через пробел, "
                "и бот покажет пошаговую работу алгоритма.",
                reply_markup=self.keyboard_manager.make_interactive_menu(),
                parse_mode="Markdown"
            )
            await callback.answer()
            return

        # ---------------- Выбор конкретного интерактивного алгоритма ----------------
        if data.startswith("inter_"):
            key = data[len("inter_"):]
            info = self.database.get_interactive_algorithm(key)

            if not info:
                await callback.answer("Алгоритм не найден.", show_alert=True)
                return

            # Сохраняем выбранный интерактивный алгоритм
            self.current_interactive_algorithm[callback.from_user.id] = info.handler_method

            await callback.message.answer(
                f"🔧 {info.name}\n\n{info.prompt}\n\n"
                "Отправьте данные одним сообщением в формате, указанном выше."
            )
            await callback.answer()
            return

        # ---------------- Назад в категорию / главное меню ----------------
        if data == "back_to_category":
            await callback.message.edit_text(
                "👋 Главное меню. Выберите категорию:",
                reply_markup=self.keyboard_manager.make_main_menu()
            )
            await callback.answer()
            return

        await callback.answer()

    async def handle_interactive_input(self, message: Message):
        """Обработка ввода данных для интерактивных алгоритмов"""
        user_id = message.from_user.id
        handler_method = self.current_interactive_algorithm.get(user_id)

        if not handler_method:
            return  # обычное сообщение — игнорируем

        text = message.text.strip()
        result = ""

        # Вызов соответствующего обработчика
        if handler_method == "binary_search":
            result = await self.interactive_handler.handle_binary_search(text)
        elif handler_method == "bubble_sort":
            result = await self.interactive_handler.handle_bubble_sort(text)
        elif handler_method == "selection_sort":
            result = await self.interactive_handler.handle_selection_sort(text)
        elif handler_method == "insertion_sort":
            result = await self.interactive_handler.handle_insertion_sort(text)
        elif handler_method == "linear_search":
            result = await self.interactive_handler.handle_linear_search(text)
        else:
            result = "❌ Неизвестный алгоритм"

        # Отправляем результат
        await message.answer(result)

        # Очищаем состояние пользователя после обработки
        if user_id in self.current_interactive_algorithm:
            del self.current_interactive_algorithm[user_id]

    async def run(self):
        """Запуск бота"""
        try:
            print("🤖 Бот запущен...")
            await self.dp.start_polling(self.bot)
        except (KeyboardInterrupt, SystemExit):
            print("🤖 Бот остановлен")


# ==================== ТОЧКА ВХОДА ====================

if __name__ == "__main__":
    bot = TelegramAlgorithmsBot()
    asyncio.run(bot.run())