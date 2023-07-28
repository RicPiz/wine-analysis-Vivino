# Open the file containing URLs and read all lines, removing trailing whitespaces
with open('red_wines_urls.txt') as f:
    lines = [line.rstrip() for line in f]

# Remove duplicate URLs by converting the list to a set, then convert it back to a list
lines = list(set(lines))

# Print the number of unique URLs
print(len(lines))

# Open a new file to write the unique URLs
fin = open('red_wines_urls_clean', 'w')

# Write each unique URL to the new file, followed by a newline character
for line in lines:
    fin.write(line)
    fin.write('\n')

# Close the file
fin.close()