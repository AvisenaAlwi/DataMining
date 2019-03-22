from AprioriAlgorithm.Apriori import Apriori

print("=== -> Apriori Algorithm <- ===")
minimum_support = 3
try:
    str_input = input("Minimum support : ")
    minimum_support = int(str_input)
except ValueError as ex:
    print("Input harus berupa angka")
    quit()

apriori = Apriori(minimum_support)
# apriori.add_transaction([1,2,3,4,6])
# apriori.add_transaction([2,3,5,4,6])
# apriori.add_transaction([1,2,3,5,6])
# apriori.add_transaction([2,5,6])
# apriori.add_transaction([5,1,6])
# apriori.add_transaction([5,3,4,6,1])
apriori.add_transaction(['Kelengkeng',	'Leci',	'Mangga',	'Pisang',	'Rambutan'])
apriori.add_transaction(['Apel',	'Ceri',	'Durian',	'Jeruk',	'Kelengkeng'])
apriori.add_transaction(['Ceri', 'Durian', 'Jeruk', 'Kelengkeng', 'Leci'])
apriori.add_transaction(['Durian', 'Jeruk', 'Kelengkeng', 'Leci', 'Mangga'])
apriori.add_transaction(['Jeruk', 'Kelengkeng', 'Leci', 'Mangga', 'Pisang'])
apriori.add_transaction(['Leci', 'Semangka', 'Rambutan', 'Kelengkeng'])
apriori.add_transaction(['Mangga', 'Pisang', 'Rambutan', 'Semangka', 'Apel'])
apriori.add_transaction(['Pisang', 'Apel', 'Mangga'])
apriori.add_transaction(['Mangga', 'Pisang', 'Kelengkeng', 'Rambutan'])
apriori.add_transaction(['Jeruk', 'Durian'])
apriori.print_transaction()
apriori.scan()

