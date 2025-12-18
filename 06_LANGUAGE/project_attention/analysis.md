# Analysis

## Layer 6, Head 7

This attention head has learned to pay attention to the relationship between prepositions and their corresponding verbs (which generally precedes them).
For example, for the sentence "She looked at the map, walked toward the station, and waited for the [MASK]." , the attention scores in layer 6 head 7 are higher for the pairs [(row, column)] : (at, looked), (toward, walked), (for, waited).
Similarly, for the sentence "The child ran into the yard, climbed onto the [MASK], and jumped off the step." , the attention scores in layer 6 head 7 are higher for the pairs [(row, column)] : (into, ran), (onto, climbed), (off, jumped).

Example Sentences:

- She looked at the map, walked toward the station, and waited for the [MASK].
        - She looked at the map, walked toward the station, and waited for the train.
        - She looked at the map, walked toward the station, and waited for the signal.
        - She looked at the map, walked toward the station, and waited for the elevator.

- The child ran into the yard, climbed onto the [MASK], and jumped off the step.
        - The child ran into the yard, climbed onto the porch, and jumped off the step.
        - The child ran into the yard, climbed onto the railing, and jumped off the step.
        - The child ran into the yard, climbed onto the step, and jumped off the step.

## Layer 7, Head 10

This attention head has learned to pay attention to the relationship between noun phrases and their corresponding prepositions (which generally precedes them).
For example, for the sentence "The cat slept under the table, beside the chair, and near the [MASK]." , the attention scores in layer 7 head 10 are higher for the pairs [(row, column)] : (table, under), (chair, beside), ([MASK], near). The determiners of the nouns are also paying attention to the prepositions. For example, 'the' identifying 'table' pays attention to 'under'; 'the' identifying 'chair' pays attention to 'beside'. Hence, it is important to note that the noun phrases are paying attention to the corresponding prepositions.
Similarly, for the sentence "The keys were found inside the [MASK], beneath the papers, and beside the lamp." , the attention scores in layer 7 head 10 are higher for the pairs [(row, column)] : ([MASK], inside), (papers, beneath), (lamp, beside).

Example Sentences:

- The cat slept under the table, beside the chair, and near the [MASK].
        - The cat slept under the table, beside the chair, and near the window.
        - The cat slept under the table, beside the chair, and near the bed.
        - The cat slept under the table, beside the chair, and near the door.

- The keys were found inside the [MASK], beneath the papers, and beside the lamp.
        - The keys were found inside the envelope, beneath the papers, and beside the lamp.
        - The keys were found inside the box, beneath the papers, and beside the lamp.
        - The keys were found inside the drawer, beneath the papers, and beside the lamp.

## Layer 8, Head 11

This attention head has learned to pay attention to the relationship between determiners and the nouns to which they are referring (which generally comes after them).
For example, for the sentence "The teacher returned his book and her [MASK] to the student." , the attention scores in layer 8 head 11 are higher for the pairs [(row, column)] : (the, teacher), (his, book), (her, [MASK]), (the, student).
Similarly, for the sentence "A child left his bag on the chair and her [MASK] near the door." , the attention scores in layer 8 head 11 are higher for the pairs [(row, column)] : (a, child), (his, bag), (the, chair), (her, [MASK]), (the, door).

Example Sentences:

- The teacher returned his book and her [MASK] to the student.
        - The teacher returned his book and her notes to the student.
        - The teacher returned his book and her book to the student.
        - The teacher returned his book and her notebook to the student.

- A child left his bag on the chair and her [MASK] near the door.
        - A child left his bag on the chair and her purse near the door.
        - A child left his bag on the chair and her bag near the door.
        - A child left his bag on the chair and her suitcase near the door.