import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency() # ensures every value in a variable's domain satisfy unary constraints
        self.ac3() # ensures binary constraints are satisfied
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for var in self.domains:
            to_be_removed = []
            for value in self.domains[var]:
                if len(value) != var.length:
                    to_be_removed.append(value)
            for value in to_be_removed:
                self.domains[var].remove(value)
        

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        overlap = self.crossword.overlaps[x, y]
        if not overlap:
            return False # there is no overlap, so arc consistency is maintained and no revision required
        xindex, yindex = overlap
        revised = False
        for valx in self.domains[x].copy():
            if all(valx[xindex] != valy[yindex] for valy in self.domains[y]): # if there is no valy in y's domain satisfying constraint valx[xindex] == valy[yindex]
                self.domains[x].remove(valx)
                revised = True
        return revised
                
                

    def ac3(self, arcs = None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        arcs_queue = []
        if not arcs:
            arcs_queue = [(x, y) for x in self.crossword.variables for y in self.crossword.neighbors(x)]
        else:
            arcs_queue = arcs
        while arcs_queue:
            x, y = arcs_queue.pop(0)
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                for z in self.crossword.neighbors(x):
                    arcs_queue.append((z, x))
        return True
                    

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for var in self.crossword.variables:
            if var not in assignment or assignment[var] is None:
                return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        
        # checking if all values are distinct
        values = [val for val in assignment.values() if val is not None]
        if len(values) != len(set(values)):
            return False
        
        for var, value in assignment.items():
            if value is None:
                continue
            
            # checking for correct value length
            if len(value) != var.length:
                return False
            
            # checking for conflicts between neighboring variables
            neighbors = self.crossword.neighbors(var)
            for neighbor in neighbors:
                if neighbor in assignment and assignment[neighbor] is not None:
                    v_ind, n_ind = self.crossword.overlaps[var, neighbor]
                    if value[v_ind] != assignment[neighbor][n_ind]: # conflict identified
                        return False

        return True


    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        domain = self.domains[var]
        neighbors = self.crossword.neighbors(var)
        nuvs = [neighbor for neighbor in neighbors if neighbor not in assignment] # collection of neighboring unassigned variables of var
        n_dict = {val: 0 for val in domain} # dictionary with each domain value of var as keys and its constraining capacity w.r.t neighboring variables' domains as value
        for value in domain:
            for nuv in nuvs:
                v_ind, n_ind = self.crossword.overlaps[var, nuv]
                for nval in self.domains[nuv]:
                    if value[v_ind] != nval[n_ind]:
                        n_dict[value] += 1
        # sorting the dictionary n_dict
        sorted_ndict_items = sorted(n_dict.items(), key = lambda item: item[1])
        sorted_domain = [item[0] for item in sorted_ndict_items]
        return sorted_domain
            

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        x = []
        uvs = [uv for uv in self.crossword.variables if uv not in assignment] # list of unassigned variables
        mrv = len(self.domains[uvs[0]]) # minimum no. of remaining values
        for uv in uvs:
            len_domain_uv = len(self.domains[uv])
            if len_domain_uv < mrv:
                mrv = len_domain_uv
                x = [uv]
            elif len_domain_uv == mrv:
                x.append(uv)
            else:
                continue
        if len(x) == 1:
            return x[0]
        elif len(x) > 1:
            return self.degree_heuristic(x)
        return
        
    def degree_heuristic(self, l):
        """
        Given that l contains a list of variables (>1) tied according to the minimum remaining value heuristic, this helper function returns the variable among them which has the highest degree.
        If there's a tie in that too, return an arbitrarily chosen variable.
        """
        x = []
        max_degree = 0
        for var in l:
            neighbors_no_var = len(self.crossword.neighbors(var))
            if neighbors_no_var > max_degree:
                x = [var]
                max_degree = neighbors_no_var
            elif neighbors_no_var == max_degree:
                x.append(var)
            else:
                continue
        if not x:
            return l[0]
        return x[0]
        

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        self.enforce_node_consistency()
        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            new_assignment = assignment.copy()
            new_assignment[var] = value
            if self.consistent(new_assignment):
                inference = self.ac3()
                if inference:
                    result = self.backtrack(new_assignment)
                    if result is not None:
                        return result
        return None
            


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
