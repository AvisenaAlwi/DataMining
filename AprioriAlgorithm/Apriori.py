class Apriori:

    def __init__(self, minimum_support=3):
        """
        Konstruktor class
        :param minimum_support: minimum support, default = 3
        """
        self.__minimum_support = minimum_support
        self.__transaction = dict()
        self.__items = set()

    def add_transaction(self, items):
        """
        Menambahkan transaksi baru
        :param items: berupa list nama nama barang
        :return: None
        """
        if self.__transaction:
            last_tid = max(self.__transaction)
        else:
            last_tid = 0
        self.__transaction[last_tid + 1] = items

    def print_transaction(self):
        print("TID\t\tItems")
        for tid, items in self.__transaction.items():
            str_items = ", ".join(sorted(list(items)))
            print("{}  :  {}".format(str(tid), str_items))

    def __print_dict(self, d):
        """
        Mencetak dictionary C / L dengan lebih bagus
        :param d: dictionary yang akan di cetak
        :return: None
        """
        for froset, value in d.items():
            items = ', '.join(list(froset))
            print("{%s} : \033[1m%d\033[0m" % (items, value))

    def __count_support_of_itemset(self, other):
        """
        Method untuk meghitung berapa transaksi yang mengandung itemset pada variabel other
        :param other: harus berupa set() atau frozenset()
        :return: int
        """
        count = 0
        for tid, items in self.__transaction.items():
            if set(items).issuperset(other):
                count += 1
        return count

    def __create_C2(self, L):
        list_key = list(L.keys())
        result_set = set()
        for key_first in list_key:
            key_first = list(key_first)[0]
            for key_second in list_key:
                key_second = list(key_second)[0]
                if key_second != key_first:
                    new_item_set = {key_first, key_second}
                    result_set.add(frozenset(new_item_set))
        return result_set

    def __create_candidate(self, L, k):
        """
        Method untuk membuat kandidat dari L sebelumnya
        :param L: L-1
        :param k: Index (perulangan) saat ini
        :return:
        """
        indexes = range(k - 2)
        c = set()
        for index, (itemset_i, sup) in enumerate(L.items()):
            itemset_i = list(itemset_i)

            same_items_i = []
            for i in indexes:
                same_items_i.append(itemset_i[i])

            setz = set(itemset_i)
            ada_yang_kembar = False
            for indexj, itemset_j in enumerate(L):
                itemset_j = list(itemset_j)
                same_items_j = []
                for i in indexes:
                    same_items_j.append(itemset_j[i])
                if index != indexj:
                    if same_items_i == same_items_j:
                        ada_yang_kembar = True
                        itemsetj = list(itemset_j)
                        setz.update(itemsetj)
                        break

            if not ada_yang_kembar:
                setz.clear()
            if setz:
                c.add(frozenset(setz))
        return c

    def scan(self, min_support=-1):
        """
        Method untuk memindai transaksi untuk mendapatkan C dan L pada data transaksi
        :return:
        """
        if min_support < 0:
            min_support = self.__minimum_support
        print("\nScan dengan minimum support : %d" % min_support)
        C = dict()
        L = dict()
        idx = 0
        # Perulangan selama L ada isinya atau idx = 0
        while L or idx == 0:
            idx += 1
            if idx == 1:
                # Membuat C1
                for tid, items in self.__transaction.items():
                    for item in items:
                        item = frozenset({item})
                        if item in C:
                            C[item] += 1
                        else:
                            C[item] = 1
            elif idx == 2:
                # Membuat C2 dengan nilai support_count awal = 0
                C = dict.fromkeys(self.__create_C2(L), 0)
            else:
                # Membuat C3 - n dengan nilai support_count awal = 0
                C = dict.fromkeys(self.__create_candidate(L, idx), 0)

            # Menghitung berapa transaksi yang mengandung itemset pada setiap C
            for k, val in C.items():
                C[k] = self.__count_support_of_itemset(k)

            # Mengeliminasi itemset di C yang kurang dari minimum support dan disimpan pada variable L
            L.clear()
            for key, val in C.items():
                if val >= min_support:
                    L[key] = val

            if C:
                print("\n" + "=" * 50)
                print("C%d :" % idx)
                self.__print_dict(C)
                print("L%d :" % idx)
                if L:
                    self.__print_dict(L)
                else:
                    print("Kosong karena semua kandidat tidak memenuhi minimum support")
            else:
                print("\nTidak dapat membentuk kandidat selanjutnya. Program Berhenti.")
