

import text_examples
# Define the string
my_string = text_examples.qchnn_good + text_examples.qchnn_end + text_examples.qchnn_end

# Split the string into a list of words
words = my_string.split()

# Set the word number you want to stop at
stop_word_num = 300

# Create an empty string to store the words before the stop word
before_stop_word = ""

# Iterate over the words in the string
for i, word in enumerate(words):
  # Check if you've reached the word you want to stop at
  if i == stop_word_num:
    # Do something
    print("Reached word number", stop_word_num)
    break
  else:
    # Append the current word to the new string
    before_stop_word += word + " "

# Print the new string
print(before_stop_word)

