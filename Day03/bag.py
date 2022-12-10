#THIS CODE WAS 100% AI GENEREATED WITH OPEN AI CHATBOT AS A EXCERSIZE, IT IS NOT MY CODE
#I DO NOT CLAIM IT IS MY CODE
# Read the input file and split each line into two parts, one for each compartment
with open('Day03/input', 'r') as input_file:
    lines = input_file.readlines()
    comp1_items = [line.strip()[:len(line)//2] for line in lines]
    comp2_items = [line.strip()[len(line)//2:] for line in lines]

# Use a dictionary to store the values of each item per bag
item_values = {}

# Process the items in compartment 1 and 2
for comp1_items, comp2_items in zip(comp1_items, comp2_items):
    # Split the items into individual characters
    comp1_chars = list(comp1_items)
    comp2_chars = list(comp2_items)

    # Check which characters appear in both compartments
    common_chars = set(comp1_chars).intersection(set(comp2_chars))

    # Update the values for each common character
    for char in common_chars:
        # Assign a value to the character based on its ASCII code
        if char.islower():
            value = ord(char) - 96
        else:
            value = ord(char) - 38

        # Check if the current bag is already in the dictionary
        if comp1_items in item_values:
            # Add the value of the character to the current bag
            item_values[comp1_items].append(value)
        else:
            # Add the current bag to the dictionary with a value of the character
            item_values[comp1_items] = [value]

# Get the total sum of the values of the duplicate items for all bags
total_sum = sum([sum(bag_values) for bag, bag_values in item_values.items()])

# Print the total sum
print(f"Total sum: {total_sum}")