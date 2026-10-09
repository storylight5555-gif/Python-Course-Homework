class Books:
    def __init__(self, title, author, genre, year, borrowed=False, return_book=False):
        self.title = title
        self.author = author
        self.genre = genre
        self.year = year
        self.borrowed = borrowed
        self.book = return_book


    def borrow(self):
        if not self.borrowed:
            self.borrowed = True
            print("The book '{}' by {} has been borrowed.".format(self.title, self.author))
        else:
            print("The book '{}' by {} is already borrowed.".format(self.title, self.author))

    def returnbook(self):
        if self.borrowed:
            self.borrowed = False
            self.book = True
            print("The book '{}' by {} has been returned.".format(self.title, self.author))
        else:
            print("The book '{}' by {} is not currently borrowed.".format(self.title, self.author))


Book1=Books("The Great Gatsby", "F. Scott Fitzgerald", "Fiction", 1925)
Book1.borrow()

Book2=Books("To Kill a Mockingbird", "Harper Lee", "Fiction", 1960)
Book2.borrow()

Book3=Books("1984", "George Orwell", "Dystopian", 1949)

Book3.borrow()
print("Book1 borrowed status:", Book1.borrowed)
print("Book2 borrowed status:", Book2.borrowed)
print("Book3 borrowed status:", Book3.borrowed)
Book1.returnbook()

Book2.returnbook()

Book3.returnbook()
print("Book1 borrowed status:", Book1.borrowed)
print("Book2 borrowed status:", Book2.borrowed)
print("Book3 borrowed status:", Book3.borrowed)