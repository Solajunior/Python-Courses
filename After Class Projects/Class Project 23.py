schoolsnacks = ["apple", "banana", "carrot sticks", "granola bar", "yogurt", "cheese stick", "trail mix", "popcorn", "fruit cup", "crackers"]
school2snacks = ["crackers", "fruit cup", "chips", "energy drink", "water"]
schoolsnacks.append("pretzels")
print(schoolsnacks)
for snack in schoolsnacks:
    if snack in school2snacks:
        print(f"{snack} is in both lists.")
        print("Time to make a array of snacks that are in both lists.")
        both_snacks = [snack for snack in schoolsnacks if snack in school2snacks]
        print("This is our array:", both_snacks)
        both_snacks.append("fruit snacks")
        both_snacks.count("fruit cup")
        both_snacks.reverse()
        print("This is our array reversed:", both_snacks)