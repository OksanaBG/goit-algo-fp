
import sys
import argparse

class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self, iterable=None):
        self.head = None
        if iterable is not None:
            for x in iterable:
                self.insert_at_end(x)

    def insert_at_beginning(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def insert_at_end(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            cur = self.head
            while cur.next:
                cur = cur.next
            cur.next = new_node

    def insert_after(self, prev_node: Node, data):
        if prev_node is None:
            print("Попереднього вузла не існує.")
            return
        new_node = Node(data)
        new_node.next = prev_node.next
        prev_node.next = new_node

    def delete_node(self, key: int):
        cur = self.head
        if cur and cur.data == key:
            self.head = cur.next
            cur = None
            return
        prev = None
        while cur and cur.data != key:
            prev = cur
            cur = cur.next
        if cur is None:
            return
        prev.next = cur.next
        cur = None

    def search_element(self, data: int):
        cur = self.head
        while cur:
            if cur.data == data:
                return cur
            cur = cur.next
        return None

    def to_list(self):
        out = []
        current = self.head
        while current:
            out.append(current.data)
            current = current.next
        return out

    def print_list(self):
        current = self.head
        out = []
        while current:
            out.append(str(current.data))
            current = current.next
        print(" -> ".join(out) + " -> None")

    def reverse(self):
        """
        Реверсування однозв'язного списку in-place
        (зміна посилань між вузлами).
        Складність O(n) за часом, O(1) за пам'яттю.
        """
        prev = None
        current = self.head
        while current:
            nxt = current.next
            current.next = prev
            prev = current
            current = nxt
        self.head = prev

    def merge_sort(self, head):
        """
        Сортування злиттям для однозв'язного списку.
        Повертає відсортовану голову списку.
        Складність O(n log n), додаткова пам'ять O(log n) через рекурсію.
        """
        if head is None or head.next is None:
            return head

        middle = self.get_middle(head)
        next_to_mid = middle.next
        middle.next = None  # розділяємо список на дві половини

        left = self.merge_sort(head)
        right = self.merge_sort(next_to_mid)

        return self.sorted_merge(left, right)

    def get_middle(self, head):
        """
        Пошук середини списку методом повільного/швидкого вказівника.
        Якщо парна кількість елементів — повертає перший з двох "середніх".
        """
        if head is None:
            return head
        slow = head
        fast = head
        while fast.next and fast.next.next:
            slow = slow.next
            fast = fast.next.next
        return slow

    def sorted_merge(self, a, b):
        """
        Зливає два відсортовані ланцюги (за зростанням) у один.
        Повертає голову злитого списку.
        """
        if a is None:
            return b
        if b is None:
            return a

        if a.data <= b.data:
            result = a
            result.next = self.sorted_merge(a.next, b)
        else:
            result = b
            result.next = self.sorted_merge(a, b.next)
        return result

    def merge_sorted_lists(self, list1, list2):
        """
        Об'єднує два ВІДсортовані LinkedList в один відсортований LinkedList.
        Повертає новий список (щоб не змінювати вміст вхідних посилань явно).
        Заувага: через перевикористання вузлів початкові списки логічно "споживаються".
        """
        merged = LinkedList()
        merged.head = self.sorted_merge(list1.head, list2.head)
        return merged


def parse_numbers(text: str):
    """
    Приймає рядок з числами, розділеними пробілами або комами.
    Повертає список int. Ігнорує порожні елементи.
    """
    if text is None:
        return []
    # Замінюємо коми на пробіли, сплітимо, конвертуємо до int
    parts = text.replace(',', ' ').split()
    nums = []
    for p in parts:
        if p.strip():
            try:
                nums.append(int(p.strip()))
            except ValueError:
                raise ValueError(f"Не вдалося перетворити '{p}' на ціле число.")
    return nums


def read_interactive():
    """
    Інтерактивний режим: питаємо у користувача 1-й і (опційно) 2-й список.
    """
    try:
        s1 = input("Введіть елементи ПЕРШОГО списку (через пробіл або кому): ").strip()
        s2 = input("Введіть елементи ДРУГОГО списку (необов'язково; Enter, щоб пропустити): ").strip()
    except EOFError:
        # Якщо немає TTY/ввід недоступний
        return [], []
    list1 = parse_numbers(s1) if s1 else []
    list2 = parse_numbers(s2) if s2 else []
    return list1, list2


def main():
    parser = argparse.ArgumentParser(
        description="Однозв'язний список: реверс, сортування злиттям, злиття двох відсортованих списків."
    )
    parser.add_argument("--list1", type=str, help="Перший список (наприклад: '3,1,2' або '3 1 2').")
    parser.add_argument("--list2", type=str, help="Другий список (опціонально; для злиття).")
    parser.add_argument("--interactive", action="store_true", help="Інтерактивний режим введення.")
    

    args = parser.parse_args()

    if args.interactive or (args.list1 is None and args.list2 is None):
        input_l1, input_l2 = read_interactive()
    else:
        input_l1 = parse_numbers(args.list1) if args.list1 else []
        input_l2 = parse_numbers(args.list2) if args.list2 else []

    if not input_l1:
        # Якщо користувач нічого не ввів навіть у інтерактиві — покажемо підказку і завершимо
        print("Порожній перший список. Приклад: --list1 '15,10,5,20,25' --list2 '59,20,35,1,18'")
        return

    # Створюємо перший список і показуємо
    first_list = LinkedList(input_l1)
    print("Початковий список 1:")
    first_list.print_list()

    # Реверс
    first_list.reverse()
    print("Після реверсування список 1:")
    first_list.print_list()

    # Сортування
    first_list.head = first_list.merge_sort(first_list.head)
    print("Відсортований список 1:")
    first_list.print_list()

    # Якщо задано другий — також відсортуємо і зіллємо
    if input_l2:
        second_list = LinkedList(input_l2)
        print("Початковий список 2:")
        second_list.print_list()

        second_list.head = second_list.merge_sort(second_list.head)
        print("Відсортований список 2:")
        second_list.print_list()

        helper = LinkedList()
        merged = helper.merge_sorted_lists(first_list, second_list)
        print("Результат злиття відсортованих списків 1 та 2:")
        merged.print_list()


if __name__ == '__main__':
    main()
