def partition_text(transcript, stop_word_num=180):
    # divide the transcript into words
    words = transcript.split()

    # Create an empty list to store partitioned text, string to store the words before the stop word and a counter
    partitioned_text = []
    before_stop_word = ""
    counter = 0
    # Iterate over the words in the string
    for word in words:
        # Check if you've reached the word you want to stop at
        if counter == stop_word_num:
            if word[-1] != '.':
                # After the values is reached append until you reach an end of sentence ('.')
                before_stop_word += word + " "
            else:
                before_stop_word += word + " "
                # and finally, add the whole sentence as an element of the partitioned text list
                partitioned_text.append(before_stop_word)
                # Reset before_stop_word to an empty string and counter set to 0
                before_stop_word = ""
                counter = 0
        else:
            # Append the current word to the new string
            before_stop_word += word + " "
            counter = counter + 1
    else:
        if before_stop_word != '':
            # catch the last remaining part of text into another element of the list
            partitioned_text.append(before_stop_word)

    # print(partitioned_text)
    return partitioned_text
