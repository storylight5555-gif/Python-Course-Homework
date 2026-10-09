class India:
    def capital(self):
        print("Capital of India is New Delhi")
    def language(self):
        print("Most popular language of India is Hindi")
    def currency(self):
        print("Currency of India is Indian Rupee")
class UAE:
    def capital(self):
        print("Capital of UAE is Abu Dhabi")
    def language(self):
        print("Most popular language of UAE is Arabic")
    def currency(self):
        print("Currency of UAE is Dirham")

obj1 = India()
obj2 = UAE()
for country in (obj1, obj2):
    country.capital()
    country.language()
    country.currency()