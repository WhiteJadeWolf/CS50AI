from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# common knowledge base
common = And(
    Or(AKnight, AKnave), # A is either a knight or a knave
    Or(BKnight, BKnave), # B is either a knight or a knave
    Or(CKnight, CKnave), # C is either a knight or a knave
    Not(And(AKnight, AKnave)), # it is not true that A is both a knight and a knave
    Not(And(BKnight, BKnave)), # it is not true that B is both a knight and a knave
    Not(And(CKnight, CKnave)), # it is not true that C is both a knight and a knave
)

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    common,
    Implication(AKnight, And(AKnight, AKnave)), # if A is a knight, then it is true that A is both a knight and a knave
    Implication(AKnave, Not(And(AKnight, AKnave))), # if A is a knight, then it is not true that A is both a knight and a knave
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    common,
    Implication(AKnight, And(AKnave, BKnave)), # if A is a knight, then it is true that A and B both are knaves
    Implication(AKnave, Not(And(AKnave, BKnave))), # if A is a knave, then it is not true that A and B both are knaves
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    common,
    Implication(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))), # if A is a knight, then A and B are the same kind (both knights or both knaves)
    Implication(AKnave, Not(Or(And(AKnight, BKnight), And(AKnave, BKnave)))), # if A is a knave, then A and B are not the same kind
    Implication(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight))), # if B is a knight, then A and B are of different kinds
    Implication(BKnave, Not(Or(And(AKnight, BKnave), And(AKnave, BKnight)))), # if B is a knave, then A and B are not of different kinds
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    common,
    Implication(CKnight, AKnight), # if C is a knight, then his statement is true that A is a knight
    Implication(CKnave, Not(AKnight)), # if C is a knave, then his statement is false
    Implication(BKnight, CKnave), # if B is a knight, then his statement is true that C is a knave
    Implication(BKnave, Not(CKnave)), # if C is a knave, then his statement is false
    Implication(BKnight, Implication(AKnight, AKnave)), # if B is a knight, then its true that "A SAID that A is a knave". Now, if A is a knight, then its true that A is a knave
    Implication(BKnight, Implication(AKnave, Not(AKnave))), # if B is a knight, then its true that "A SAID that A is a knave". Now, if A is a knave, then its not true that A is a knave
    Implication(BKnave, Implication(AKnight, AKnight)), # if B is a knave, then its not true that "A SAID that A is a knave". So, A must have said "I am a Knight". Now, if A is a knight, then its true that A is a knight.
    Implication(BKnave, Implication(AKnave, Not(AKnight))), # if B is a knave, then its not true that "A SAID that A is a knave". So, A must have said "I am a Knight". Now, if A is a knave, then its not true that A is a knight.
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
