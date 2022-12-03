#THIS CODE IS MODIFIED FROM PART !, WHICH WAS AI GENERATED
# Read the input file and split each line into two parts, one for each compartment
with open('Day3/input', 'r') as input_file:
    lines = input_file.readlines()
    lines = [line.strip() for line in lines]
    lineGroup = zip(*[iter(lines)]*3)
# Use a dictionary to store the values of each item per bag
item_values = {}

# Process the items in compartment 1 and 2
for lines in lineGroup:
    # Check which characters appear in both compartments
    common_chars = set(lines[0]).intersection(set(lines[1]).intersection(set(lines[2])))

    # Update the values for each common character
    for char in common_chars:
        # Assign a value to the character based on its ASCII code
        if char.islower():
            value = ord(char) - 96
        else:
            value = ord(char) - 38

    item_values[lines] = [value]

# Get the total sum of the values of the duplicate items for all bags
total_sum = sum([sum(bag_values) for bag, bag_values in item_values.items()])

# Print the total sum
print(f"Total sum: {total_sum}")