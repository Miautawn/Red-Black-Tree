#RED-BLACK Tree, Martynas Jašinskas VU ISI 1k.
from os import system

class Node():
    def __init__(self, key):
        self.colour = "RED"
        self.key = key
        self.left = None
        self.right = None
        self.parent = None

class RBTree():
    def __init__(self):
        self.NILL = Node("NILL")
        self.NILL.colour = "BLACK"
        self.root = self.NILL
    
    def __transmutate(self, deletable_node, changeable_node):
        if deletable_node.parent == None:
            self.root = changeable_node
        elif deletable_node == deletable_node.parent.left:
            deletable_node.parent.left = changeable_node
        else:
            deletable_node.parent.right = changeable_node
        changeable_node.parent = deletable_node.parent

    def delete(self, item):
        """
        ištrina elementą iš medžio
        """
        x = self.root
        z = self.NILL

        #find the lowest possible node with this number
        while x != self.NILL:
            if x.key == item:
                z = x
            
            if x.key <= item:
                x = x.right
            else:
                x = x.left
        
        #if there is no such node
        if z == self.NILL:
            print("Tokio elemento nėra")
            return

        y = z
        y_orginal = y.colour

        #Simple BST delete
        ##################
        # Šie atvejai jei tas node turi tik viena vaiką
        # arba išvis neturi
        if(z.right == self.NILL):
            x = z.left
            self.__transmutate(z, z.left)
        elif(z.left == self.NILL):
            x = z.right
            self.__transmutate(z, z.right)
        #Jeigu turi abu vaikus
        else:
            #reikia surasti pakaitalą
            y = self.get_minimum(z.right)
            y_orginal = y.colour
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self.__transmutate(y, y.right)
                y.right = z.right
                y.right.parent = y
            self.__transmutate(z, y)
            y.left = z.left
            y.left.parent = y
            y.colour = z.colour
        # Jeigu istrintas yra juodas
        if y_orginal == "BLACK":
            self.fix_delete(x)

    def fix_delete(self, x):
        while x != self.root and x.colour == "BLACK":
            if x == x.parent.left:
                sibling = x.parent.right
                #Case 1 - Sibling is red
                if(sibling.colour == "RED"):
                    sibling.colour = "BLACK"
                    x.parent.colour = "RED"
                    self.left_rotate(x.parent)
                    sibling = x.parent.right
                #Case 2 - both of siblings children are black
                if(sibling.left.colour == "BLACK" and sibling.right.colour == "BLACK"):
                    sibling.colour = "RED"
                    x = x.parent
                #Case 3 - left sibling child is red, right is black
                else:
                    if(sibling.right.colour == "BLACK"):
                        sibling.left.colour = "BLACK"
                        sibling.colour = "RED"
                        self.right_rotate(sibling)
                        sibling = x.parent.right
                    #Case 4 - left sibling child is black, right is red
                    sibling.colour = x.parent.colour
                    sibling.right.colour = "BLACK"
                    x.parent.colour = "BLACK"
                    self.left_rotate(x.parent)
                    x = self.root

            else:
                sibling = x.parent.left
                #Case 1 - Sibling is red (inverted)
                if(sibling.colour == "RED"):
                    sibling.colour = "BLACK"
                    x.parent.colour = "RED"
                    sefl.right_rotate(x.parent)
                    sibling = x.parent.left
                #Case 2 - both of siblings children are black
                if(sibling.left.colour == "BLACK" and sibling.right.colour == "BLACK"):
                    sibling.colour = "RED"
                    x = x.parent
                else:
                    #Case 3 - left sibling child is red, right is black (inverted)
                    if(sibling.left.colour == "BLACK"):
                        sibling.right.colour = "BLACK"
                        sibling.colour = "RED"
                        self.left_rotate(sibling)
                        sibling = x.parent.left
                    #Case 4 - left sibling child is black, right is red (inverted)
                    sibling.colour = x.parent.colour
                    x.parent.colour = "BLACK"
                    sibling.left.colour = "BLACK"
                    self.right_rotate(x.parent)
                    x = self.root
        x.colour = "BLACK"

    def insert(self, item):
        """
        įdeda elementą į medį
        """
        new_node = Node(item)
        new_node.left, new_node.right = self.NILL, self.NILL

        #get the parent of the to be inserted node
        y = None
        x = self.root

        while x != self.NILL:
            y = x
            if(item > x.key):
                x = x.right
            else:
                x = x.left
        
        new_node.parent = y
        #if parent is non egzisatnt, aka new_node is the root
        if y == None:
            self.root = new_node
            self.root.colour = "BLACK"
            return
        if(item > y.key):
            y.right = new_node
        else:
            y.left = new_node

        #if the inserted node is in the second level
        if new_node.parent.parent == None:
            return

        #if nothing else, let's do the fixing
        self.fix_insert(new_node)

    def fix_insert(self, new_node):
        while new_node.parent.colour == "RED":

            #if the parent is the left child of GrandParent
            uncle = None
            if(new_node.parent == new_node.parent.parent.left):
                uncle = new_node.parent.parent.right
            else:
                uncle = new_node.parent.parent.left

            # Case 1 - tėvas Raudonas, o Dėdė Raudonas
            if uncle.colour == "RED":
                new_node.parent.colour = "BLACK"
                uncle.colour = "BLACK"
                new_node.parent.parent.colour = "RED"
                new_node = new_node.parent.parent
                
            else:
                if(new_node.parent == new_node.parent.parent.left):
                    # Case 2 - tėvas Raudonas, o Dėdė Juodas, O x dešinys
                    if new_node == new_node.parent.right:
                        new_node = new_node.parent
                        self.left_rotate(new_node)
                    # Case 3 - tėvas Raudonas, o Dėdė Juodas, o X kairys
                    new_node.parent.colour = "BLACK"
                    new_node.parent.parent.colour = "RED"
                    self.right_rotate(new_node.parent.parent)
                else:
                    #Case 2 - tėvas Raudonas, o Dėdė Juodas, o x dešinys (apkeista vietom)
                    if new_node == new_node.parent.left:
                        new_node = new_node.parent
                        self.right_rotate(new_node)
                    # Case 3 - tėvas Raudonas, o Dėdė Juodas, o X kairys (apkeista vietom)
                    new_node.parent.colour = "BLACK"
                    new_node.parent.parent.colour = "RED"
                    self.left_rotate(new_node.parent.parent)  
            #if after changes the pointing node is a root - exit
            if new_node == self.root:
                break
        self.root.colour = "BLACK"

    def get_minimum(self, node):
        """
        gauti tam tikro pomedžio mažiausią elementą
        """
        while node.left != self.NILL:
            node = node.left
        return node

    def print_tree(self):
        """
        atspausdinti medį aukščio metodu
        """
        def print_level(root, level):
            if root == None:
                return
            elif level == 1:
                if root != self.NILL:
                    print('(', root.key,root.colour,')', end=" ")
                else:
                    print('(', root.key, ')', end=" ")
            elif level > 1:
                print_level(root.left, level - 1)
                print_level(root.right, level - 1)
        
        h = self.get_height(self.root)
        for i in range(1, h+1):
            print_level(self.root, i)
            print("\n")

    def get_height(self, node):
        """
        Grąžina medžio ilgį
        """
        if(node == self.NILL):
            return 0
        else:
            return max(self.get_height(node.left), self.get_height(node.right)) + 1

    def find(self, value):
        """
        suranda ir gražina medžio ieškomą elementą
        """
        x = self.root
        y = self.NILL
        level = 0
        while x != self.NILL:
            level += 1
            if x.key == value:
                y = x
                break
            if(value >= x.key):
                x = x.right
            else:
                x = x.left
            
        if(y == self.NILL):
            print("Tokio elemento nėra!")
        else:
            print("Rastas toks elementas: {}, {} lygyje".format(y.key, level))
    

    def left_rotate(self, x):
        """
        padaryti pasukimą kairėn
        """
        y = x.right
        x.right = y.left
        if y.left != self.NILL:
            y.left.parent = x
        
        y.parent = x.parent
        if(x.parent == None):
            self.root = y
        elif(x == x.parent.left):
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y
    
    def right_rotate(self, x):
        """
        padaryti pasukimą dešinėn
        """
        y = x.left
        x.left = y.right
        if y.right != self.NILL:
            y.right.parent = x
        
        y.parent = x.parent
        if(x.parent == None):
            self.root = y
        elif(x == x.parent.right):
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

tree = RBTree()
while True:
    print("Įvesti - 1, Ištrinti - 2, Spausdinti - 3, Surasti - 4")
    selection = int(input("Jūsų pasirinkimas: "))
    if(selection == 1):
        number = int(input("Kokį skaičių įvesti: "))
        tree.insert(number)
        _ = system('clear')
    elif(selection == 2):
        number = int(input("Kokį elementą ištrinti: "))
        tree.delete(number)
        _ = system('clear')
    elif(selection == 3):
        _ = system('clear')
        print("***********************")
        tree.print_tree()
        print("***********************")
    else:
        _ = system('clear')
        number = int(input("Kokios reikšmės ieškote: "))
        tree.find(number)




